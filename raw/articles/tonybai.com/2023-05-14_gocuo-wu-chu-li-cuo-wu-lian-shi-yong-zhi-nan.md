---
title: Go错误处理：错误链使用指南
url: https://tonybai.com/2023/05/14/a-guide-of-using-go-error-chain/
published: '2023-05-14'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go错误处理：错误链使用指南

![](../../assets/6c32581f9a5444a6.png)


[本文永久链接](https://tonybai.com/2023/05/14/a-guide-of-using-go-error-chain) – https://tonybai.com/2023/05/14/a-guide-of-using-go-error-chain

## 0. Go错误处理简要回顾

Go是一种非常强调错误处理的编程语言。在Go中，错误被表示为实现了error接口的类型的值，error接口只有一个方法：

```
type error interface {
Error() string
}
```


这个接口的引入使得Go程序可以以一致和符合惯用法的方式进行错误处理。

在所有编程语言中，错误处理的挑战之一都是能提供足够的错误上下文信息，以帮助开发人员诊断问题，同时又可以避免开发人员淹没在不必要的细节中。在Go中，这一挑战目前是通过使用**错误链(error chain)**来解决的。

注：

[Go官方用户调查结果]表明，Go社区对Go错误处理机制改进的期望还是很高的。这对Go核心团队而言，依然是一个不小的挑战。好在[Go 1.18泛型落地]，随着Go泛型的逐渐成熟，更优雅的错误处理方案有可能会在不远的将来浮出水面。

错误链是一种将一个错误包裹在另一个错误中的技术，以提供关于错误的额外的上下文。当错误通过多层代码传播时，这种技术特别有用，每层代码都会为错误信息添加自己的上下文。

不过，最初Go的错误处理机制是不支持错误链的，Go对错误链的支持和完善是在[Go 1.13版本](https://tonybai.com/2019/10/27/some-changes-in-go-1-13/)中才开始的事情。

众所周知，在Go中，错误处理通常使用if err != nil的惯用法来完成。当一个函数返回一个错误时，调用代码会检查该错误是否为nil。如果错误不是nil，通常会被打印到日志中或返回给调用者。

例如，看下面这个读取文件的函数：

```
func readFile(filename string) ([]byte, error) {
data, err := os.ReadFile(filename)
if err != nil {
return nil, err
}
return data, nil
}
```


在这段代码中，os.ReadFile()如果读取文件失败，会返回一个错误。如果发生这种情况，readFile函数会将错误返回给它的调用者。Go的这种基本的错误处理机制简单有效好理解，但它也有自己的局限性。其中一个主要的限制是错误信息可能是模糊的。当一个错误在多层代码中传播时，开发人员可能很难确定错误的真实来源和原因。 我们看一下下面这段代码：

```
func processFile(filename string) error {
data, err := readFile(filename)
if err != nil {
return fmt.Errorf("can not read file: %s", filename)
}
// process the file data...
return nil
}
```


在这个例子中，如果processFile因readFile失败而返回一个错误，错误信息将只表明该文件无法被读取，它**不会提供任何关于造成错误的原因或错误发生地点的准确信息**。

Go基本错误处理的另一个约束是在处理错误时，错误的上下文可能会丢失。尤其是当一个错误通过多层代码时，某一层可能会忽略收到的错误信息，而是构造自己的错误信息并返回给调用者，这样最初的错误上下文就会在错误的传递过程中丢失了，这不利于问题的快速诊断。

那么，我们如何解决这些限制呢？下面我们就来探讨一下错误链是如何如何帮助Go开发人员解决这些限制问题的。

## 1. 错误包装(error wrapping)与错误链

为了解决基本错误处理的局限性，[Go在1.13版本中提供了Unwrap接口和fmt.Errorf的%w的格式化动词](https://tonybai.com/2019/10/18/errors-handling-in-go-1-13/)，用于构建可以包裹(wrap)其他错误的错误以及从一个包裹了其他错误的错误中判断是否有某个指定错误，并从中提取错误信息。

fmt.Errorf是最常用的用于包裹错误的函数，它接收一个现有的错误，并将其包装在一个新的错误中，并可以附着更多的错误上下文信息。

例如，改造一下上面的示例代码：

```
func processFile(filename string) error {
data, err := readFile(filename)
if err != nil {
return fmt.Errorf("failed to read file: %w", err)
}
// process the file data...
return nil
}
```


在这段代码中，fmt.Errorf通过%w创建了一个新的错误，新错误包裹(wrap)了原来的错误，并附加了一些错误上下文信息(failed to read file)。这个新的错误可以在调用堆栈中传播并提供更多关于这个错误的上下文。

为了从错误链中检索原始错误，Go在errors包中提供了Is、As和Unwrap()函数。Is和As函数用于判定某个error是否存在于错误链中，Unwrap这个函数返回错误链中的下一个直接错误。

下面是一个完整的例子：

```
func readFile(filename string) ([]byte, error) {
data, err := os.ReadFile(filename)
if err != nil {
return nil, err
}
return data, nil
}
func processFile(filename string) error {
data, err := readFile(filename)
if err != nil {
return fmt.Errorf("failed to read file: %w", err)
}
fmt.Println(string(data))
return nil
}
func main() {
err := processFile("1.txt")
if err != nil {
fmt.Println(err)
fmt.Println(errors.Is(err, os.ErrNotExist))
err = errors.Unwrap(err)
fmt.Println(err)
err = errors.Unwrap(err)
fmt.Println(err)
return
}
}
```


运行这个程序(前提：1.txt文件并不存在)，结果如下：

```
$go run demo1.go
failed to read file: open 1.txt: no such file or directory
true
open 1.txt: no such file or directory
no such file or directory
```


该示例中错误的wrap和unwrap关系如下图：

![](../../assets/7d9520cdf0768e80.png)


像这种由错误逐个包裹而形成的链式结构(如下图)，我们称之为**错误链**。

![](../../assets/7549af6dcfe5d354.png)


接下来，我们再来详细说一下Go错误链的使用。

## 2. Go中错误链的使用

### 2.1 如何创建错误链

就像前面提到的，我们**通过包裹错误来创建错误链**。

目前Go标准库中提供的用于wrap error的API有fmt.Errorf和errors.Join。fmt.Errorf最常用，在上面的示例中我们演示过了。errors.Join用于将一组errors wrap为一个error。

fmt.Errorf也支持通过多个%w一次打包多个error，下面是一个完整的例子：

```
func main() {
err1 := errors.New("error1")
err2 := errors.New("error2")
err3 := errors.New("error3")
err := fmt.Errorf("wrap multiple error: %w, %w, %w", err1, err2, err3)
fmt.Println(err)
e, ok := err.(interface{ Unwrap() []error })
if !ok {
fmt.Println("not imple Unwrap []error")
return
}
fmt.Println(e.Unwrap())
}
```


示例运行输出如下：

```
wrap multiple error: error1, error2, error3
[error1 error2 error3]
```


我们看到，通过fmt.Errorf一次wrap的多个error在String化后，是在一行输出的。这点与errors.Join的有所不同。下面是用errors.Join一次打包多个error的示例：

```
func main() {
err1 := errors.New("error1")
err2 := errors.New("error2")
err3 := errors.New("error3")
err := errors.Join(err1, err2, err3)
fmt.Println(err)
errs, ok := err.(interface{ Unwrap() []error })
if !ok {
fmt.Println("not imple Unwrap []error")
return
}
fmt.Println(errs.Unwrap())
}
```


这个示例输出如下：

```
$go run demo2.go
error1
error2
error3
[error1 error2 error3]
```


我们看到，通过errors.Join一次wrap的多个error在String化后，每个错误单独占一行。

如果对上面的输出格式都不满意，那么你还可以自定义Error类型，只要至少实现了String() string和Unwrap() error 或Unwrap() []error即可。

### 2.2 判定某个错误是否在错误链中

前面提到过errors包提供了Is和As函数来判断某个错误是否在错误链中，对于一次wrap多个error值的情况，errors.Is和As也都按预期可用。

### 2.3 获取错误链中特定错误的上下文信息

有些时候，我们需要从错误链上获取某个特定错误的上下文信息，通过Go标准库可以至少有两种实现方式：

第一种：通过errors.Unwrap函数来逐一unwrap错误链中的错误。

由于不确定错误链上的error个数以及每个error的特征，这种方式十分适合用来获取root cause error，即错误链中最后面的一个error。下面是一个示例：

```
func rootCause(err error) error {
for {
e, ok := err.(interface{ Unwrap() error })
if !ok {
return err
}
err = e.Unwrap()
if err == nil {
return nil
}
}
}
func main() {
err1 := errors.New("error1")
err2 := fmt.Errorf("2nd err: %w", err1)
err3 := fmt.Errorf("3rd err: %w", err2)
fmt.Println(err3) // 3rd err: 2nd err: error1
fmt.Println(rootCause(err1)) // error1
fmt.Println(rootCause(err2)) // error1
fmt.Println(rootCause(err3)) // error1
}
```


第二种：通过errors.As函数将error chain中特定类型的error提取出来

error.As函数用于判断某个error是否是特定类型的error，如果是则将那个error提取出来，比如：

```
type MyError struct {
err string
}
func (e *MyError) Error() string {
return e.err
}
func main() {
err1 := &MyError{"temp error"}
err2 := fmt.Errorf("2nd err: %w", err1)
err3 := fmt.Errorf("3rd err: %w", err2)
fmt.Println(err3)
var e *MyError
ok := errors.As(err3, &e)
if ok {
fmt.Println(e)
return
}
}
```


在这个示例中，我们通过errors.As将错误链err3中的err1提取到e中，后续就可以使用err1这个特定错误的信息了。

## 3. 小结

错误链是Go中提供信息丰富的错误信息的一项重要技术。通过用额外的上下文包装错误，你可以提供关于错误的更具体的信息，并帮助开发人员更快地诊断出问题。

不过错误链在使用中有一些事项还是要注意的，比如：避免嵌套错误链。嵌套的错误链会使你的代码难以调试，也难以理解错误的根本原因。

结合错误链，通过给错误添加上下文，创建自定义错误类型，并在适当的抽象层次上处理错误，你可以写出简洁、可读和信息丰富的错误处理代码。

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023 – 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论