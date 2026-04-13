---
title: Go2 Error Inspection前瞻
url: https://tonybai.com/2019/01/27/perspective-study-on-go2-error-inspection/
published: '2019-01-27'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go2 Error Inspection前瞻

这几年关于[Go语言未来演化](https://blog.golang.org/toward-go2)的讨论成为了Gopher世界的热点，Go team官方对于[Go语言](https://tonybai.com/2018/11/12/go-opensource-9-years/)的演化(以Go2为标签)也是十分上心，但吸取了其他语言，比如：[Python3](https://www.python.org/)割裂社区的、不兼容演化的教训，Go team最终选择了一条[尽可能地兼容Go1、稳健、平滑的演化之路](https://blog.golang.org/go2-here-we-come)，并逐渐开始落地。[Go 1.11](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)的[Go modules](https://tonybai.com/2018/07/15/hello-go-module/)是Go team开启**Go2**演化进程的标志性事件。随着[“Go 2 Draft Design”](https://blog.golang.org/go2draft)的[发布](https://github.com/golang/proposal/blob/master/design/go2draft.md)，Go team正在努力着手解决Go社区反响较为强烈的[Error handling](https://github.com/golang/proposal/blob/master/design/go2draft-error-handling-overview.md)、[Error values](https://github.com/golang/proposal/blob/master/design/go2draft-error-values-overview.md)和[Generics（泛型）](https://github.com/golang/proposal/blob/master/design/go2draft-generics-overview.md)这三个问题。从目前的进展上来看，Go error value相关机制的改善近期率先在以[Proposal形式](https://github.com/golang/proposal/blob/master/design/29934-error-values.md)出现，并给出了待社区反馈的[参考实现(golang.org/x/exp/xerrors)](https://github.com/golang/exp/tree/master/xerrors)，并很可能是继Go module之后第二个落地的Go2 特性。在本文中，我们就和大家一起来前瞻性探索一下Go2 error inspection及其参考实现。

## 一. Go2要解决关于Error的哪些问题

从全局角度，Go亟需解决的关于Error的问题包含两个大的方面，一个是Error handling机制，即尝试解决代码中大量重复出现下面代码的问题：

```
if err != nil {
.... ....
}
```


第二个要解决的就是有关**测试error变量值，并根据error变量值来选择后续代码执行路线的问题（面向机器）**，同时也要解决如何将error信息更完整、更全面地呈现给人的问题（面向人）。

关于error handling，[draft引入了handle和check的新设计机制](https://github.com/golang/proposal/blob/master/design/go2draft-error-handling-overview.md)，该draft目前还在discuss之中；而第二个问题的解决正如我们前面提到的，已经率先成为Proposal并给出了参考实现，也是我们在本文中要重点探讨的内容。

Go error最初被创新地设计为一个interface：

```
type error interface {
Error() string
}
```


这种设计是符合OCP(open-close principle)的，但是由于在error value test方面相对模糊且在标准库中缺少统一机制，导致gopher们在使用error时体验并不好。这里我们先来回顾一下在这之前我们是如何测试error变量值的。

**1. 与预先定义好的知名error变量进行值相等测试 （以下称方法1）**

如下面例子中，我们通过将ReadByte调用返回的err与io包中预定义的error变量: EOF(var EOF = errors.New(“EOF”))进行值测试，并根据测试结果选择接下来的代码执行路线：

```
func main() {
reader := strings.NewReader("string reader buffer demo")
for {
s, err := reader.ReadByte()
if err == io.EOF {
fmt.Println("end")
return
} else if err != nil {
fmt.Println(err)
return
}
fmt.Printf("%c\n", s)
}
}
```


对于预先已经定义的error变量，这样的error test方法是非常自然的，多数程序员从学习C语言那个时候就已经熟知该方法了。但是这种方法的局限就在于“扩展不足”。这些预定义好的error变量要么在标准库中，要么在依赖的第三方包中，我们只能使用这么多且这些变量所携带的信息有限。如果包中没有预定义或是想让这些变量携带更多对程序员有益的错误信息，我们就还得用其他办法来做error变量的值测试和扩展定义。

**2. 使用type assertion和type switch来测试是否是某种error的实现 **

标准库中net包中OpError的一些method中就采用了这种方式：

```
// $GOROOT/src/net/net.go
func (e *OpError) Timeout() bool {
if ne, ok := e.Err.(*os.SyscallError); ok {
t, ok := ne.Err.(timeout)
return ok && t.Timeout()
}
t, ok := e.Err.(timeout)
return ok && t.Timeout()
}
```


一些包还提供了一些专用方法来测试判定特定的error实现类型，比如：os包提供的IsNotExist、IsPermission等方法。不过这些方法在实现层面也都是使用的type assertion。

**3. 通过字符串匹配 **

由于缺少标准的、统一的error变量的值测试方法，尤其是针对重新wrapped的error变量(加上自己了的context信息，隐藏了underlying的error变量类型信息)，在上述两种方法都无法使用的情况下，基于error变量Error()方法返回的string进行字符串匹配来进行error变量测试的手段成为了广大Gopher最后的“救命稻草”，但是这种方法也是最为“丑陋”的，是Go team最不希望gopher们使用的。

```
// 一个demo，现实中可能不存在这样的逻辑
func writeTxtFile(path string, content string) error {
f, err := os.OpenFile("notes.txt", os.O_RDWR, 0755)
if err != nil {
return fmt.Errorf("open txt file: %s failed, reason: %s", path, err.Error())
}
defer f.Close()
// ... write something
_, err = f.Write([]byte(content))
if err != nil {
return fmt.Errorf("write to txt file: %s failed, reason: %s", path, err.Error())
}
return nil
}
func main() {
err := writeTxtFile("./notes.txt", "write txt test")
if err != nil {
s := err.Error()
if strings.Contains(s, "open txt file") {
fmt.Println("open txt file error:", s) //但是我们仍然无法根据打开txt文件的具体原因类型(比如权限、还是文件不存在)做出相应的动作
return
}
if strings.Contains(s, "write to txt file") {
fmt.Println("write txt file error:", s)
return
}
}
}
```


归根结底，fmt.Errorf提供的error wrap功能将最原始的error信息隐藏了起来，使得我们没有办法通过方法1或2来对wrapped的error变量进行值测试。这也是go2 error新方案要解决的问题。

## 二. xerrors的使用

下面我们来结合一下参考实现golang.org/x/exp/xerrors来看看该proposal是如何解决上述问题的。

### 1. wrapping error变量的创建

从前面的问题描述，我们知道Go2亟需提供一种简单的、标准的包裹(wrap)其他error变量并生成新error变量的方法，生成的新error变量中将包含被wrapped的error变量的信息：

![img{512x368}](../../assets/a34d00ca4f22e908.png)


xerrors通过Errorf来提供这个功能。下面是参考上图函数调用和error变量包裹关系的一个Demo：

```
//github.com/bigwhite/experiments/xerrors/wrapper/wrapper1.go
func function4() error {
return xerrors.New("original_error")
}
func function3() error {
err := function4()
if err != nil {
return xerrors.Errorf("wrap3: %w", err)
}
return nil
}
func function2() error {
err := function3()
if err != nil {
return xerrors.Errorf("wrap2: %w", err)
}
return nil
}
func function1() error {
err := function2()
if err != nil {
return xerrors.Errorf("wrap1: %w", err)
}
return nil
}
func main() {
err := function1()
if err != nil {
fmt.Printf("%v\n", err)
return
}
fmt.Printf("ok\n")
}
```


通过xerror.Errorf对已知error变量进行包裹后，返回的error变量所归属的类型实现了error、xerrors.Formatter和xerrors.Wrapper接口，携带了被包裹(wrap)变量的信息，而传统的通过fmt.Errorf生成的error变量仅仅实现了error接口，没有被包裹的error变量的任何信息。这些携带的信息将在后续error变量值测试时(Is和As)以及error变量信息展示时被充分利用。

![img{512x368}](../../assets/ca5b94729991e2f4.png)


我们运行一下上面的demo(默认得到单行的错误信息输出)：

```
$go run wrapper1.go
wrap1: wrap2: wrap3: original_error
```


如果使用”+v%”输出error信息，我们将得到下面输出(多行)：

```
$go run wrapper1.go
wrap1:
main.function1
/Users/tony/go/src/github.com/bigwhite/experiments/xerrors/wrapper/wrapper1.go:32
- wrap2:
main.function2
/Users/tony/go/src/github.com/bigwhite/experiments/xerrors/wrapper/wrapper1.go:24
- wrap3:
main.function3
/Users/tony/go/src/github.com/bigwhite/experiments/xerrors/wrapper/wrapper1.go:16
- original_error:
main.function4
/Users/tony/go/src/github.com/bigwhite/experiments/xerrors/wrapper/wrapper1.go:10
```


我们看到”+v%”还输出每个错误变量生成时的**位置**信息，这是因为xerrors.Errorf生成的变量类型:wrapError中携带了“位置信息(frame Frame)”：

```
// golang.org/x/exp/xerrors/fmt.go
type wrapError struct {
msg string
err error
frame Frame
}
```


上面的demo仅是为了演示通过xerrors.Errorf wrap的error variable携带了error chain的信息，并可以输出这些信息。下面我们来看看在函数调用的外部，如何对wrapped error variable进行各种值test。

### 2. error value test

对应上面提到方法1(等值测试)和方法2(type断言的类型测试)，xerrors提供了对应的Is和As方法，这两个方法最大的不同就是可以针对wrapped error变量，**在变量的error chain上做逐个进行测试**，只要某个chain上的error变量满足要求，则返回true。我们分别来看看！

1) Is方法

xerrors的Is方法原型如下：

```
func Is(err, target error) bool
```


Is会将target与err中的error chain上的每个error 信息进行等值比较，如果相同，则返回true。我们用下面这幅图来诠释一下其原理:

![img{512x368}](../../assets/b86c1f8a9cf98714.png)


对应的测试代码见下面：

```
// github.com/bigwhite/experiments/xerrors/errortest/errortest1.go
func main() {
err1 := xerrors.New("1")
err2 := xerrors.Errorf("wrap 2: %w", err1)
err3 := xerrors.Errorf("wrap 3: %w", err2)
erra := xerrors.New("a")
b := xerrors.Is(err3, err1)
fmt.Println("err3 is err1? -> ", b)
b = xerrors.Is(err2, err1)
fmt.Println("err2 is err1? -> ", b)
b = xerrors.Is(err3, err2)
fmt.Println("err3 is err2? -> ", b)
b = xerrors.Is(erra, err1)
fmt.Println("erra is err1? -> ", b)
}
运行结果：
err3 is err1? -> true
err2 is err1? -> true
err3 is err2? -> true
erra is err1? -> false
```


2) As方法

Is方法是在error chain上做值测试。有些时候我们更方便做类型测试，即某一个err是否是某error类型。xerror提供了As方法：

```
func As(err error, target interface{}) bool
```


As会将err中的error chain上的每个error type与target的类型做匹配，如果相同，则返回true，并且将匹配的那个error var的地址赋值给target，相当于通过As的target将error chain中类型匹配的那个error变量析出。我们也用下面这幅图来诠释一下其原理:

![img{512x368}](../../assets/b023f9cd02861590.png)


对应的测试代码见下面：

```
// github.com/bigwhite/experiments/xerrors/errortest/errortest2.go
type MyError struct{}
func (MyError) Error() string {
return "MyError"
}
func main() {
err1 := MyError{}
err2 := xerrors.Errorf("wrap 2: %w", err1)
err3 := xerrors.Errorf("wrap 3: %w", err2)
var err MyError
b := xerrors.As(err3, &err)
fmt.Println("err3 as MyError? -> ", b)
fmt.Println("err is err1? -> ", xerrors.Is(err, err1))
err4 := xerrors.Opaque(err3)
b = xerrors.As(err4, &err)
fmt.Println("err4 as MyError? -> ", b)
b = xerrors.Is(err4, err3)
fmt.Println("err4 is err3? -> ", b)
}
运行结果:
err3 as MyError? -> true
err is err1? -> true
err4 as MyError? -> false
err4 is err3? -> false
```


我们看到As方法从err3的error chain中匹配到MyError类型的err1，并将err1赋值给err变量析出。在后续的Is测试也证实了这一点。代码中还调用了xerrors的Opaque方法，该方法将传入的支持unwrap操作的error变量转换为一个不支持unwrap的类型的error变量。在最后的对err4（通过Opaque调用得到)的测试我们也可以看到：err4无法匹配MyError type，与err3的等值测试也返回false。

## 三. 小结

以上就是xerrors提供的有关Go2 error inspection机制的主要功能。注意：**xerrors及其proposal仍然可能会变动(包括设计和具体的实现)，因此这里不能保证本文demo示例在后续的版本中依然可以编译运行**。本文中的示例代码可以在[这里](https://github.com/bigwhite/experiments/tree/master/xerrors)得到。

目前go官方的golang.org/x/exp repo中有两个版本的实现：golang.org/x/exp/errors和golang.org/x/exp/xerrors。差别在于前者没有提供errors.Errorf。如果我们将wrapper1.go中的xerrors换成golang.org/x/exp/errors，则会在编译的时候出现下面错误：

```
$go run wrapper1.go
go: finding golang.org/x/exp/errors latest
go: downloading golang.org/x/exp/errors v0.0.0-20190125153040-c74c464bbbf2
# command-line-arguments
./wrapper.go:15:10: undefined: errors.Errorf
./wrapper.go:16:10: undefined: errors.Errorf
./wrapper.go:27:10: undefined: errors.Errorf
./wrapper.go:28:10: undefined: errors.Errorf
```


从官方的说明情况来看，golang.org/x/exp/errors将来要么进化到golang.org/x/errors，并作为Go标准库的vendor(类似于http/2) 包；要么直接merge到Go标准库中，然后该库作废（类似于[vgo](https://github.com/golang/vgo))。无论哪种形式，errors在merge后，会由fmt.Errorf来提供xerrors.Errorf的功能。

而golang.org/x/exp/xerrors则是可以用于任何版本的。

目前Go team给出的初步计划是在Go 1.13 dev cycle中将该Go 2 error inspection机制加入到main branch，并就像当年的http/2、vgo一样期待Gopher社区对该机制的反馈、然后优化，直到成熟并被广大Gopher所接受。

我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我要发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

我的联系方式：

微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2019, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

赞赞赞，我们在实际使用中自定义error类型时，有些类似思想了。期待官方版本

您好, 我是一名初学者，一些问题请教一下您。我理解xerrors包扩展了原有errors包的一些功能, 增加了错误栈打印等等，但是还是有一些问题不是太清楚：

1. “wrapping error” 是如何避免大量 “err!=nil” 的出现呀

2. ”error chain“ 是在 go2 draft 最新引入的么, 在工程中实际使用是怎样的, 一层层的错误封装除了方便问题定位，对实际的代码架构设计有什么积极影响呀

谢谢您！

if err != nil {} 大量重复的问题由另外一个design: error handling: https://github.com/golang/proposal/blob/master/design/go2draft-error-handling-overview.md 负责解决。

谢谢您回复！

golang.org/x/exp/xerrors 已经被删除了，现在已经被 golang.org/x/xerrors 替代，见[xerrors: delete x/exp/xerrors](https://github.com/golang/exp/commit/21964bba6549f73cc16f1ddbc95bcbbb5b679985)

谢谢提醒。