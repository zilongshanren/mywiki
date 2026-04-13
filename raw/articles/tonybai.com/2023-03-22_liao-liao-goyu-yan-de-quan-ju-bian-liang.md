---
title: 聊聊Go语言的全局变量
url: https://tonybai.com/2023/03/22/global-variable-in-go/
published: '2023-03-22'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 聊聊Go语言的全局变量

![](../../assets/cdf14e0f2845f7eb.png)


[本文永久链接](https://tonybai.com/2023/03/22/global-variable-in-go) – https://tonybai.com/2023/03/22/global-variable-in-go

注：上面篇首配图的底图由百度

[文心一格]生成。

C语言是Go语言的先祖之一，Go继承了很多C语言的语法与表达方式，这其中就包含了**全局变量**，虽然Go在其[语法规范](https://go.dev/ref/spec)中并没有直接给出全局变量的定义。但是已经[入门Go的童鞋](https://tonybai.com/2023/02/23/learn-go-in-10-min)都知道，在Go中**包的导出变量(exported variable)起到的就是全局变量的作用**。Go包导出变量与C的全局变量在优缺点与使用方式也有相似之处。

我是[C程序员出身](https://tonybai.com/2022/05/16/the-short-guide-of-embracing-c-lang-for-gopher)，对[全局变量](http://en.wikipedia.org/wiki/Global_variable)并不陌生，因此学习Go语言全局变量时，也没有太多Gap。不过来自其他语言(比如Java)的童鞋在学习Go全局变量时可能会觉得别扭，在全局变量的使用方式的理解方面也久久不能到位。

在这一篇中，我们就来聊聊Go语言的全局变量，和大家一起系统地理解一下。

## 一. Go中的全局变量

全局变量是**一个可以在整个程序中被访问和修改的变量**，不管它在哪里被定义。不同的编程语言有着不同的声明和使用全局变量的方式。

在Python中，你可以在module的任何地方声明一个全局变量。就像下面示例中的globvar。但是如果你想给它重新赋值，则需要在函数中使用global关键字。

```
globvar = 0
def set_globvar_to_one():
global globvar # 要给全局变量globvar赋值
globvar = 1
def print_globvar():
print(globvar) # 读取全局变量globvar时无需global关键字
set_globvar_to_one()
print_globvar() # 打印1
```


Java中没有全局变量的概念，但你却可以使用一个类的public静态变量来模拟全局变量的作用，因为这样的public类静态变量可以被任何其他类在任何地方访问到。比如下面Java代码中globalVar：

```
public class GlobalExample {
// 全局变量
public static int globalVar = 10;
// 全局常量
public static final String GLOBAL_CONST = "Hello";
}
```


在Go中，全局变量指的是在包的最顶层声明的头母大写的导出变量，这样这个变量在整个Go程序的任何角落都可以被访问和修改，比如下面示例代码中foo包的变量Global：

```
package foo
var Global = "myvalue" // Go全局变量
package bar
import "foo"
func F1() {
println(foo.Global)
foo.Global = "another value"
}
```


foo.Global可以被任何导入foo包的其他包所读取和修改，就像上面代码F1中对它的那些操作。

即便是全局变量，按Go语法规范，上述Global变量的作用域也是package block的，而非universe block的，关于Go标识符的作用域，

[Go语言第一课专栏第11讲]有系统详细地说明。

Go导出变量在Go中既然充当着全局变量的角色，它也就有了和其他语言全局变量一样的优劣势。接下来我们就来看看全局变量的优点与不足。

## 二. 全局变量的优缺点

俗话说：既然存在就有存在的“道理”！我们不去探讨“存在即合理”在哲学层面是否正确，我们先来看看全局变量的存在究竟能带来哪些好处。

### 1. 全局变量的优点

- 首先，
**全局变量易于访问**。

全局变量的定义决定了它可以在程序的任何地方被访问。无论是在函数、方法、循环体内、深度缩进的条件语句块内部，全局变量都可以被直接访问到。这为减少函数参数个数带来一定“便利”，同时也省去了确定参数类型、实施参数传递的“烦恼”。

破壁人：全局变量容易被意外修改或被局部变量遮蔽，从而导致意想不到的问题。


- 其次，
**全局变量易于共享数据**。

由于易于访问的特性，全局变量常用于在程序的不同部分之间共享数据，比如配置项数据、命令行标志(cmd flag)等。又由于全局变量的生命周期与程序的整个生命周期等同，不会因为函数调用结束而销毁，也不会被GC掉，可以始终存在并保持其值。因此全局变量被用作共享数据时，开发人员也不会有担心全局变量所在内存“已被回收”的心智负担。

破壁人: 并发的多线程或多协程(包括goroutine)访问同一个全局变量时需要考虑“数据竞争”问题。


- 最后，
**全局变量让代码显得更为简洁**。

Go全局变量只需要在包的顶层声明一次即可，之后便可以在程序的任何地方对其进行访问和修改。对于声明全局变量的包的维护者而言，这样的代码再简洁不过了！

破壁人: 多处访问和修改全局变量的代码都与全局变量产生了直接的数据耦合，降低了可维护性和扩展性。


在上面的说明中，我针对全局变量的每条优点都写了一条“破壁人”观点，把这些破壁观点聚拢起来，就构成了全局变量的缺点集合，我们继续来看一下。

### 2. 全局变量的缺点

- 首先，
**全局变量容易被意外修改或被局部变量遮蔽**。

前面提到，全局变量易于访问，这意味着所有地方都可能会直接访问或修改全局变量。任何一个位置改变了全局变量，都可能会以意想不到的方式影响着另外一个使用它的函数。这将导致针对这些函数的测试更为困难，全局变量的存在让各个测试之间隔离性不好，测试用例执行过程中如果修改了全局变量，测试执行结束前可能都需要将全局变量恢复到之前的状态，以尽可能保证对其他测试用例的干扰最小，下面是一个示例：

```
var globalVar int
func F1() {
globalVar = 5
}
func F2() {
globalVar = 6
}
func TestF1(t *testing) {
old := globalVar
F1()
// assert the result
... ...
globalVar = old // 恢复globalVar
}
func TestF2(t *testing) {
old := globalVar
F2()
// assert the result
... ...
globalVar = old // 恢复globalVar
}
```


此外，全局变量十分容易被函数、方法、循环体的同名局部变量所遮蔽(shadow)，导致一些奇怪难debug的问题，尤其是**与Go的短变量声明语法结合使用时**。

go vet支持对代码的静态分析，不过变量遮蔽检查的功能需要额外安装：

```
$go install golang.org/x/tools/go/analysis/passes/shadow/cmd/shadow@latest
$go vet -vettool=$(which shadow)
```


- 其次，
**并发条件下，对全局变量的访问存在“数据竞争”问题**

如果你的程序存在多个goroutine对全局变量的并发读写，那么“数据竞争”问题便不可避免。你需要使用额外的同步手段对全局变量进行保护，比如互斥锁、读写锁、原子操作等。

同理，没有同步手段保护的全局变量也限制了[单元测试](https://tonybai.com/2023/03/15/an-intro-of-go-subtest/)的并行执行能力(-paralell)。

- 最后，全局变量在带来代码简洁性的同时，
**更多带来的是对扩展和复用不利的耦合性**！

全局变量让程序中所有访问和修改它的代码对其产生了数据耦合，全局变量的细微变化都将对这些代码产生影响。这样，如果要复用或扩展这些依赖全局变量的代码将变得十分困难。比如：若要对它们进行并行化执行，需要考虑其耦合的全局变量是否支持同步手段。若要复用其中的代码逻辑到其他程序中，可能还需要在新程序中创建一个新的全局变量。

我们看到，Go全局变量有优点，更有一堆不足，那么我们在实际生产编码过程中到底该如何对待全局变量呢？我们继续往下看。

## 三. Go全局变量的使用惯例与替代方案

到底Go语言是如何对待全局变量的？我翻了翻标准库来看看Go官方团队是如何对待全局变量的，我得到的结论是**尽量少用**。

Go标准库中的全局变量用了“不少”，但绝大多数都是全局的“哨兵”错误变量，比如：

```
// $GOROOT/src/io/io.go
var ErrShortWrite = errors.New("short write")
// ErrShortBuffer means that a read required a longer buffer than was provided.
var ErrShortBuffer = errors.New("short buffer")
// EOF is the error returned by Read when no more input is available.
// (Read must return EOF itself, not an error wrapping EOF,
// because callers will test for EOF using ==.)
// Functions should return EOF only to signal a graceful end of input.
// If the EOF occurs unexpectedly in a structured data stream,
// the appropriate error is either ErrUnexpectedEOF or some other error
// giving more detail.
var EOF = errors.New("EOF")
// ErrUnexpectedEOF means that EOF was encountered in the
// middle of reading a fixed-size block or data structure.
var ErrUnexpectedEOF = errors.New("unexpected EOF")
... ...
```


关于错误处理中的“哨兵”错误处理模式，可以参考我的

[Go语言第一课专栏]。更多Go错误处理模式在专栏中有系统讲解。

这些ErrXXX全局变量虽说是被定义为了“变量(Var)”，但Go开源许久以来，大家已经达成默契：这些ErrXXX变量仅是“只读”的，没人会对其进行任何修改操作。到这里有初学者可能会问：那为什么不将它们定义为常量呢？那是因为Go语言对常量的类型是有要求的：

```
Go常量有布尔常量、rune常量、整数常量、浮点常量、复数常量和字符串常量。
```


其他类型均不能被定义为常量。而errors.New返回的动态类型为errors.errorString结构体类型的指针，显然也不在常量类型范围之内。

除了ErrXXX这类全局变量外，Go标准库中其他全局变量就很少了。一个典型的全局变量是http.DefaultServeMux：

```
// $GOROOT/src/net/http/server.go
// DefaultServeMux is the default ServeMux used by Serve.
var DefaultServeMux = &defaultServeMux
var defaultServeMux ServeMux
// NewServeMux allocates and returns a new ServeMux.
func NewServeMux() *ServeMux { return new(ServeMux) }
```


http包是Go早期就携带的高频使用的包，我猜早期实现时出于某种原因定义了全局变量DefaultServeMux，后期可能由于兼容性原因保留了该全局变量，但从代码逻辑来看，去掉也不会有任何影响。

通过http包的DefaultServeMux、defaultServeMux和NewServeMux等逻辑，我们也可以看出Go语言采用的替代全局变量的方案，那就是**“封装”**。以http.ServeMux为例(我们假设删除掉DefaultServeMux这个全局变量，用包级非导出变量defaultServeMux替代它)。

http包定义了ServeMux类型以及相应方法用于处理HTTP请求的多路复用，但http包并未直接定义一个ServerMux的全局变量(我们假设删除了DefaultServeMux变量)，而是定义了一个包级非导出变量defaultServeMux作为默认的Mux。

http包仅导出两个函数Handle和HandleFunc供调用者注册http请求路径与对应的handler(下面代码中的DefaultServeMux可换成defaultServeMux)：

```
// $GOROOT/src/net/http/server.go
// Handle registers the handler for the given pattern
// in the DefaultServeMux.
// The documentation for ServeMux explains how patterns are matched.
func Handle(pattern string, handler Handler) { DefaultServeMux.Handle(pattern, handler) }
// HandleFunc registers the handler function for the given pattern
// in the DefaultServeMux.
// The documentation for ServeMux explains how patterns are matched.
func HandleFunc(pattern string, handler func(ResponseWriter, *Request)) {
DefaultServeMux.HandleFunc(pattern, handler)
}
```


这样http完全不需要暴露Mux实现的细节，调用者也无需依赖一个全局变量，这个方案将原先的对全局变量的数据耦合转换为对http包的行为耦合。

类似的作法我们在标准库log包中也能看到，log包定义了包级变量std用作默认的Logger，但对外仅暴露Printf等系列打印函数，这些函数的实现会使用包级变量std的相应方法：

```
// $GOROOT/src/log/log.go
// Print calls Output to print to the standard logger.
// Arguments are handled in the manner of fmt.Print.
func Print(v ...any) {
if std.isDiscard.Load() {
return
}
std.Output(2, fmt.Sprint(v...))
}
// Printf calls Output to print to the standard logger.
// Arguments are handled in the manner of fmt.Printf.
func Printf(format string, v ...any) {
if std.isDiscard.Load() {
return
}
std.Output(2, fmt.Sprintf(format, v...))
}
// Println calls Output to print to the standard logger.
// Arguments are handled in the manner of fmt.Println.
func Println(v ...any) {
if std.isDiscard.Load() {
return
}
std.Output(2, fmt.Sprintln(v...))
}
... ...
```


注：其他语言可能有一些其他的替代全局变量的方案，比如Java的依赖注入。


## 四. 小结

综上，全局变量虽然有易于访问、易于共享、代码简洁等优点，但相较于其带来的意外修改、并发数据竞争、更高的耦合性等弊端而言，Go开发者选择了“尽量少用全局变量”的最佳实践。

此外，在Go中最常见的替代全局变量的方案就是**封装**，这个大家可以通过阅读标准库的典型源码慢慢体会。

注：本文部分内容来自于New Bing的Chat功能(据说是基于GPT-4大语言模型)生成的答案。


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

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论