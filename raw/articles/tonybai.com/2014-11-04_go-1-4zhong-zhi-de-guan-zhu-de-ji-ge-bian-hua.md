---
title: Go 1.4中值得关注的几个变化
url: https://tonybai.com/2014/11/04/some-changes-in-go-1-4/
published: '2014-11-04'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.4中值得关注的几个变化

在Go 1.3发布半年过去后，[Go](http://tonybai.com/tag/golang)核心项目组于本月初发布了[Go 1.4 Beta1版本](http://tip.golang.org/doc/go1.4)。这个版本的几个变化点虽然不是革命性的，但对后续Go语言的发展来说，打下了基础，定下了基调。这里就几个值得关注的变化点结合Go 1.4代码进行一些简单描述，希望大家能对Go 1.4有个感性的认知和了解。

Go 1.4依旧保持了Go 1兼容性的承诺，你的已有代码几乎无需任何改动就可以通过Go 1.4的编译并运行。(以下是我的测试环境：go version go1.3 darwin/amd64 vs. go version go1.4beta1 linux/amd64）

**一、语言变化**

**1、For-range循环**

在Go 1.3及以前，for-range循环具有两种形式：

for k, v := range x {

…

}

和

for k := range x {

…

}

问题：如果我们不关心循环中的值，我们只关心循环本身，我们仍然要提供一个变量，或用_占位。

for _ = range x {

…

}

下面这样的语法在Go 1.3及以前是无法编译通过的：

for range x {

…

}

不过Go 1.4支持这种形式的语法，它使得代码更加clean，虽然它可能很少会被使用到。

例子：

//testforrange.go

package main

import "fmt"

func main() {

var a [5]int = [5]int{2, 3, 4, 5, 6}

for k, v := range a {

fmt.Println(k, v)

}

for k := range a {

fmt.Println(k)

}

for _ = range a {

fmt.Println("print without care about the key and value")

}

for range a {

fmt.Println("new syntax – print without care about the key and value")

}

}

Go 1.3编译出错：

$go run testforrange.go

# command-line-arguments

./testforrange.go:19: syntax error: unexpected range, expecting {

./testforrange.go:22: syntax error: unexpected }

Go 1.4编译成功并输出正确结果：

0 2

1 3

2 4

3 5

4 6

0

1

2

3

4

print without care about the key and value

print without care about the key and value

print without care about the key and value

print without care about the key and value

print without care about the key and value

new syntax – print without care about the key and value

new syntax – print without care about the key and value

new syntax – print without care about the key and value

new syntax – print without care about the key and value

new syntax – print without care about the key and value

**2、通过**T调用方法**

下面这个例子：

package main

import "fmt"

type T int

func (T) M() {

fmt.Println("Call M")

}

var x **T

func main() {

x.M()

}

按照Go 1.4官方release note的说法，1.3版本及以前的gc和gccgo都会正常接受这种调用方式。但Go 1规范只允许自动在x前面加一个解引用，而不是两个，因此这个是有悖于定义的。Go 1.4强制禁止这种调用。

不过根据我实际的测试，Go 1.3和Go 1.4针对上面代码都会出现同样地编译错误。

$go run testdoubledeferpointer.go

# command-line-arguments

./testdoubledeferpointer.go:14: calling method M with receiver x (type **T) requires explicit dereference

**二、支持的操作系统以及处理器体系架构的变化**

这个无法演示。不过一个主要的变化就是Go 1.4可以构建出运行于ARM处理器Android操作系统上的二进制程序了。使用[go.mobile库](http://code.google.com /p/go.mobile)中的支持包，Go 1.4也可以构建出可以被Android应用加载的.so库。

**三、兼容性变化**

人们通过unsafe包并利用Go的内部实现细节和数据的机器表示形式来绕过Go语言类型系统的约束。Go的设计者们认为这是对Go兼容性规范的 不尊重，在Go 1.4中，Go核心组正式宣布unsafe code不再保证其兼容性。这次Go 1.4并没有针对此做任何代码变动，只是一个clarification而已。

**四、实现和工具的变化**

**1、运行时(runtime)的变化**

Go 1.3及以前版本，Go语言的runtime（垃圾收集、并发支持、interface管理、maps、slices、strings等）主要由C语言和 少量汇编语言实现的。在1.4版本中，很多代码被替换成了用Go自身实现，这样垃圾回收器可以扫描程序运行时栈，获取活跃变量的精确信息。这个变 化很大，但对程序应该没有语义上的影响。

这次重写使得垃圾回收器变得更加精确，这意味着它知道所有程序中活跃指针的位置。这些相关改变将减小heap的大小，总体上大约减少 10%~30%。

这样做的结果是栈也不再需要是分段的(segmented)了，消除了“hot split”的问题。如果一个stack到达了使用上限，Go将分配一个新的更大的stack，相应goroutine中的所有活跃的栈帧将被复制到新 stack上，所有指向栈的指针将被更新。在某些场景下，其性能将会变得显著提升，并且这样修改后，其性能更具可预测性。

连续栈(contiguous stacks)的使用使得栈的初始Size可以更小，在Go 1.4中goroutine的初始栈大小从8192字节缩小为2048字节。（正式发布时也许会改为4096）。

interface值类型的实现也做了调整。在之前的发布版中，interface值内部用一个字(word)来承载，要么是一个指针，要么是一 个单字（one-word）大小的纯量值，这取决于interface值变量中具体存储的是什么对象。这个实现会给垃圾收集器带来诸多困难，因此 在Go 1.4版本中interface值内部就用指针表示。在运行的程序中，绝大多数interface值都是指针，因此这个影响很小。不过那些在 interface值类型变量中存储整型值的程序将会有更多的内存分配。

**2、gccgo的状态**

[Gcc](http://gcc.gnu.org)和Go两个项目的发布计划不是同步的，GCC 4.9版本包含了实现了1.2规范的gccgo，下一个发布版gcc 5.0将可能包含实现了1.4规范的gccgo。

**3、internal包**（内部包）

Go以package为基本逻辑单元组织代码。Go 1.3及之前版本的Go语言实际上只支持两种形式Package内符号的可见性：本地的(unexported)和全局的(exported)。有些时候 我们希望一些包并非能被所有外部包所导入，但却能被其**“临近”**的包所导入和访问。但之前的Go语言不具备这种特性。Go 1.4引入了"internal"包的概念，导入这种internal包的规则约束如下：

*如果导入代码本身不在以"internal"目录的父目录为root的目录树中，那么 不允许其导入路径(import path)中包含internal元素。*

例如：

– a/b/c/internal/d/e/f只可以被以a/b/c为根的目录树下的代码导入，不能被a/b/g下的代码导入。

– $GOROOT/src/pkg/internal/xxx只能被标准库($GOROOT/src)中的代码所导入。（注：Go 1.4 取消了$GOROOT/src/pkg，标准库都移到$GOROOT/src下了)。

– $GOROOT/src/pkg/net/http/internal只能被net/http和net/http/*的包所导入

– $GOPATH/src/mypkg/internal/foo只能被$GOPATH/src/mypkg包的代码所导入

对于Go 1.4该规则首先强制应用于$GOROOT下。Go 1.5将扩展应用到$GOPATH下。

**4、权威导入路径(import paths)**

我们经常使用托管在公共代码托管服务中的代码，诸如github.com，这意味着包导入路径包含托管服务名，比如github.com/rsc /pdf。一些场景下为了不破坏用户代码，我们用rsc.io/pdf，屏蔽底层具体哪家托管服务，比如rso.io/pdf的背后可能是 github.com也可能是bitbucket。但这样会引入一个问题，那就是不经意间我们为一个包生成了两个合法的导入路径。如果一个程序中 使用了这两个合法路径，一旦某个路径没有被识别出有更新，或者将包迁移到另外一个不同的托管公共服务下去时，使用旧导入路径包的程序就会报错。

Go 1.4引入一个包字句的注释，用于标识这个包的权威导入路径。如果使用的导入的路径不是权威路径，go命令会拒绝编译。语法很简单：

package pdf // import "rsc.io/pdf"

如果pdf包使用了权威导入路径注释，那么那些尝试使用github.com/rsc/pdf导入路径的程序将会被go编译器拒绝编译。

这个权威导入路径检查是在编译期进行的，而不是下载阶段。

我们举个例子：

我们的包foo以前是放在github.com/bigwhite/foo下面的，后来主托管站换成了tonybai.com/foo，最新的 foo包的代码：

package foo // import "tonybai.com/foo"

import "fmt"

func Echo(a string) {

fmt.Println("Foo:, a)

}

某个应用通过旧路径github.com/bigwhite/foo导入了该包：

//testcanonicalimportpath.go

package main

import "github.com/bigwhite/foo"

func main() {

foo.Echo("Hello!")

}

我们编译该go文件，得到以下结果：

code in directory /home/tonybai/Test/Go/src/github.com/bigwhite/foo expects import "tonybai.com/foo"

**5、go generate子命令**

go 1.4中go工具集合新引入一个子命令：go generate，用于在编译前自动化生成某类代码。例如在.y上运行yacc编译器生成实现该语法的.go源文件。或是使用stringer工 具自动为常量生成String方法。这个命令并非由go tools(build, get等)自动执行，而必须显式执行。

不过我简单测试了一下，似乎这个命令设计文档中的：

// +build generate

并不好用啊。即便将其作为generate directive放入go源文件，该文件依旧会被go编译器当做正常go文件编译。Go 1.4标准库中使用go generate directive的有三个地方：

strconv/quote.go://go:generate go run makeisprint.go -output isprint.go

time/zoneinfo_windows.go://go:generate go run genzabbrs.go -output zoneinfo_abbrs_windows.go

unicode/letter.go://go:generate go run maketables.go -tables=all -output tables.go

通过go generate来实现泛型(generics)似乎不那么优雅啊。虽然设计者并非将其作为Go泛型的实现^_^。

**6、源码布局变化**

在Go自身源码库($GOROOT下)中，包的源码放在src/pkg中，这样做与其他库不同，包括Go自己的子库，比如go.tools。因此在Go 1.4中，pkg这一层目录树将被去除，比如fmt包的源码曾经放在src/pkg/fmt下，现在则放在src/fmt下。

**五、性能**

绝大多数程序使用1.4编译后的运行速度会与1.3的一致或略有提升，有些可能也会变得慢些。这次修改的较多，很难准确预测。

这次许多runtime的代码由C变为Go，这将导致一些heap大小有所缩减。另外这样做后有利于Go编译器的优化，诸如内联，会带来性能上的小幅提升。

垃圾回收器一方面得到了加速，使得重度依赖垃圾收集的程序得到可衡量的提升。但另外一方面，新的write barrier又引起了性能下降。提升和下降的量的多少取决于程序的行为。

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

学习了。翻译的非常好。理解了。