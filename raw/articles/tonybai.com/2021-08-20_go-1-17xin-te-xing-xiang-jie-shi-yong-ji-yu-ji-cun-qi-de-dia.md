---
title: Go 1.17新特性详解：使用基于寄存器的调用惯例
url: https://tonybai.com/2021/08/20/using-register-based-calling-convention-in-go-1-17/
published: '2021-08-20'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.17新特性详解：使用基于寄存器的调用惯例

![](../../assets/b3a5063f41899219.png)


[本文永久链接](https://tonybai.com/2021/08/20/using-register-based-calling-convention-in-go-1-17) – https://tonybai.com/2021/08/20/using-register-based-calling-convention-in-go-1-17

除了[Go语言特性](https://mp.weixin.qq.com/s/Afj9pV79AParMkMvcNlCTw)与[go module](https://mp.weixin.qq.com/s/Fer90nattWxXDWDC1VV55w)有重要变化之外，Go编译器与Go运行时也都有着优化与改进，这两方面的变化对Go程序的构建与运行影响巨大。在这个系列的最后一篇中，我们来看看编译器与运行时中那些值得关注的变化。

### 1. 使用基于寄存器的调用惯例替代基于堆栈的调用惯例

所谓“调用惯例(calling convention)”是调用方和被调用方对于函数调用的一个明确的约定，包括：函数参数与返回值的传递方式、传递顺序。只有双方都遵守同样的约定，函数才能被正确地调用和执行。如果不遵守这个约定，函数将无法正确执行。

Go 1.17版本之前，Go采用基于栈的调用约定，即函数的参数与返回值都通过栈来传递，这种方式的优点是实现简单，不用担心底层cpu架构寄存器的差异，适合跨平台；但缺点就是牺牲了一些性能，我们都知道寄存器的访问速度要远高于内存。

大多数平台上的大多数语言实现都使用基于寄存器的调用约定，通过寄存器而不是内存传递函数参数和返回结果，并指定一些寄存器为调用保存寄存器，允许函数在不同的调用中保持状态。

于是Go在1.17版本决定向这些语言看齐，在amd64架构下率先实现了从基于堆栈的调用惯例到[基于寄存器的调用惯例](https://go.googlesource.com/proposal/+/master/design/40724-register-calling.md)的[切换](https://github.com/golang/go/issues/40724)。

在Go 1.17的版本发布说明文档中有提到：切换到[基于寄存器的调用惯例](https://go.googlesource.com/go/+/refs/heads/dev.regabi/src/cmd/compile/internal-abi.md)后，一组有代表性的Go包和程序的基准测试显示，Go程序的运行性能提高了约5%，二进制文件大小典型减少约2%。

我们来实测一下，下面采用的是之前[进阶专栏](https://www.imooc.com/read/87)中的[一个多种方法进行字符串连接的benchmark测试](https://github.com/bigwhite/publication/blob/master/column/imooc/go-50tips/sources/string_concat_benchmark_test.go)，在Go 1.16.5和Go 1.17下面分别运行Benchmark结果如下：

Go 1.16.5：

```
$go test -bench .
goos: darwin
goarch: amd64
pkg: github.com/bigwhite/demo
cpu: Intel(R) Core(TM) i5-8257U CPU @ 1.40GHz
BenchmarkConcatStringByOperator-8 12132355 91.51 ns/op
BenchmarkConcatStringBySprintf-8 2707862 445.1 ns/op
BenchmarkConcatStringByJoin-8 24101215 50.84 ns/op
BenchmarkConcatStringByStringsBuilder-8 11104750 124.4 ns/op
BenchmarkConcatStringByStringsBuilderWithInitSize-8 24542085 48.24 ns/op
BenchmarkConcatStringByBytesBuffer-8 14425054 77.73 ns/op
BenchmarkConcatStringByBytesBufferWithInitSize-8 20863174 49.07 ns/op
PASS
ok github.com/bigwhite/demo 9.166s
```


Go 1.17：

```
$go test -bench .
goos: darwin
goarch: amd64
pkg: github.com/bigwhite/demo
cpu: Intel(R) Core(TM) i5-8257U CPU @ 1.40GHz
BenchmarkConcatStringByOperator-8 13058850 89.47 ns/op
BenchmarkConcatStringBySprintf-8 2889898 410.1 ns/op
BenchmarkConcatStringByJoin-8 25469310 47.15 ns/op
BenchmarkConcatStringByStringsBuilder-8 13064298 92.33 ns/op
BenchmarkConcatStringByStringsBuilderWithInitSize-8 29780911 41.14 ns/op
BenchmarkConcatStringByBytesBuffer-8 16900072 70.28 ns/op
BenchmarkConcatStringByBytesBufferWithInitSize-8 27310650 43.96 ns/op
PASS
ok github.com/bigwhite/demo 9.198s
```


我们看到，相对于Go 1.16.5跑出的结果，Go 1.17在每一个测试项上都有小幅的性能提升，有些性能提升甚至达到10%左右。这种新版本带来的性能的“自然提升”显然是广大Gopher想看到的。

我们再来看看编译后的Go二进制文件的Size变化。以一个自有的1w行左右代码的Go程序为例，分别用Go 1.16.5和Go 1.17进行编译，得到的结果如下：

```
-rwxr-xr-x 1 tonybai staff 7264432 8 13 18:31 myapp-go1.16.5*
-rwxr-xr-x 1 tonybai staff 6934352 8 13 18:32 myapp-go1.17*
```


我们看到Go 1.17编译后的二进制文件大小相较于Go 1.16.5版本的减少了约4%。

另外Go 1.17发布说明也提到了：改为基于register的调用惯例后，绝大多数程序不会受到影响。只有那些之前就已经违反unsafe.Pointer的使用规则的代码可能会受到影响，比如不遵守unsafe规则通过unsafe.Pointer访问函数参数，或依赖一些像比较函数代码指针的未公开的行为。

除了改为基于寄存器的调用惯例之外，Go 1.17编译器还支持包含[闭包](https://mp.weixin.qq.com/s/bldzzSw-X0YdRcmN3fPhaw)的函数的内联(inline)了！这样一来，一个带有闭包的函数可能会在函数被内联的每个地方产生一个不同的闭包代码指针，因此，**Go函数的值不能直接比较**！

### 2. 引入//go:build形式的构建约束指示符，以替代原先易错的// +build形式

Go 1.17之前，我们可以通过在源码文件头部放置+build构建约束指示符来实现构建约束，但这种形式十分易错，并且它并不支持&&和||这样的直观的逻辑操作符，而是用逗号、空格替代，下面是原+build形式构建约束指示符的用法及含义：

![](../../assets/5388bf8b0f9fd231.png)


这种与程序员直觉“有悖”的形式让Gopher们十分痛苦，于是Go 1.17回归“正规”，引入了[//go:build形式的构建约束指示符](https://go.googlesource.com/proposal/+/master/design/draft-gobuild.md)，这样一方面是与源文件中的其他指示符保持形式一致，比如: //go:nosplit、//go:norace、//go:noinline、//go:generate等。另外一方面，新形式将支持&&和||逻辑操作符，对于程序员来说，这样的形式就是自解释的，我们无需再像上面那样列出一个表来解释每个指示符组合的含义了，如下代码所示：

```
//go:build linux && (386 || amd64 || arm || arm64 || mips64 || mips64le || ppc64 || ppc64le)
//go:build linux && (mips64 || mips64le)
//go:build linux && (ppc64 || ppc64le)
//go:build linux && !386 && !arm
```


考虑到兼容性，Go命令可以识别这两种形式的构建约束指示符，但推荐Go 1.17之后都用新引入的这种形式。

gofmt可以兼容处理两种形式，处理原则是：如果一个源码文件只有// +build形式的指示符，gofmt会将与其等价的//go:build行加入。否则，如果一个源文件中同时存在这两种形式的指示符行，那么//+build行的信息将被//go:build行的信息所覆盖。

go vet工具也会检测源文件中同时存在的不同形式的构建指示符语义不一致的情况，比如针对下面这段代码：

```
// github.com/bigwhite/experiments/tree/master/go1.17-examples/runtime/buildtag.go
//go:build linux && !386 && !arm
// +build linux
package main
import "fmt"
func main() {
fmt.Println("hello, world")
}
```


go vet会提示如下问题：

```
./buildtag.go:2:1: +build lines do not match //go:build condition
```


### 3. 运行时栈跟踪输出信息的格式更“可读”

之前写过一篇文章《[记一次go panic问题的解决过程](https://tonybai.com/2019/04/04/notes-about-fixing-a-go-panic-problem/)》，在那篇文章中，我们探讨了如何解读panic发生后输出的函数栈跟踪信息。

下面的代码示例用于对比运行时栈输出信息的差异：

```
// github.com/bigwhite/experiments/tree/master/go1.17-examples/runtime/stacktrace.go
package main
type myStruct struct {
m int
s string
p *float64
}
func foo(a int, b string, c []byte, f *myStruct) (int, error) {
panic("mypanic")
}
func main() {
f := 3.14
ms := myStruct{
m: 17,
s: "myStruct",
p: &f,
}
a := 11
b := "hello"
c := []byte{'a', 'b', 'c'}
foo(a, b, c, &ms)
}
```


在这个示例程序中，我们在foo函数中“故意”panic，以便go运行时在程序退出前输出栈跟踪信息（注意编译时关闭内联优化）。针对这个示例程序，Go 1.17之前的版本输出的栈跟踪信息是这样的(go 1.16.5版本):

```
$go build -gcflags '-N -l' -o stacktrace-go1.16.5 stacktrace.go
$./stacktrace-go1.16.5
panic: mypanic
goroutine 1 [running]:
main.foo(0xb, 0x1073f53, 0x5, 0xc000046715, 0x3, 0x3, 0xc000046758, 0x0, 0x0, 0x0)
/Users/tonybai/Go/src/github.com/bigwhite/experiments/go1.17-examples/runtime/stacktrace.go:10 +0x4a
main.main()
/Users/tonybai/Go/src/github.com/bigwhite/experiments/go1.17-examples/runtime/stacktrace.go:23 +0x148
```


上面输出信息中foo函数后面括号中的各个值与foo函数原型完全对不上。要想知道这些数值的含义究竟是什么，可以参考我上面提到的[那篇文章](https://tonybai.com/2019/04/04/notes-about-fixing-a-go-panic-problem/)，这里不赘述。

使用Go 1.17版本编译后会是什么样子呢？我们再来看一下：

go 1.17:

```
$go build -gcflags '-N -l' -o stacktrace-go1.17 stacktrace.go
$./stacktrace
panic: mypanic
goroutine 1 [running]:
main.foo(0xb, {0x10608d4, 0x5}, {0xc00004270d, 0x3, 0x3}, 0xc000042750)
/Users/tonybai/Go/src/github.com/bigwhite/experiments/go1.17-examples/runtime/stacktrace.go:10 +0x59
main.main()
/Users/tonybai/Go/src/github.com/bigwhite/experiments/go1.17-examples/runtime/stacktrace.go:23 +0x10f
```


对照着该示例程序中foo函数的原型：

```
func foo(a int, b string, c []byte, f *myStruct) (int, error)
```


这回一目了然了！我们看到Go 1.17改进了当发送未捕获的panic或当runtime.Stack被调动时，运行时输出的栈跟踪信息的格式。Go 1.17版本之前，函数参数被打印成基于内存布局的十六进制值的形式，就像前面那个难于解读的输出信息。Go 1.17版，源码中函数的每个参数都被单独打印，用逗号分隔。聚合类型（结构体、数组、字符串、切片、接口和complex）的参数用大括号分隔。需要注意的是，只存在于寄存器中而没有存储到内存中的参数的值可能是不准确的。函数的返回值（通常是不准确的）不再被打印了。

通过上的输出，我们还可以清晰的看到[string](https://www.imooc.com/read/87/article/2384)、[byte切片](https://www.imooc.com/read/87/article/2383)以及结构体在内存中的表示方式，string本质上是一个拥有两个字段的结构，而切片则是一个三元组表示的结构。

### 3. 小结

上面是Go 1.17编译器与运行时的主要改动，通过使用寄存器的调用惯例，我们的Go程序可以轻松获得5%左右的性能提升，可执行程序的Size也会得到减小。Go 1.17对运行时栈输出信息的“可读化”改进进一步提升了开发体验。

除此之外，Go的标准库随着新版本的发布都会有大量的改动，但每个开发人员对标准库的关注点差别很大，因此，在这个系列中不会详细做说明了，大家还是参考[Go 1.17的发布说明文档](https://tip.golang.org/doc/go1.17)各取所需吧^_^。

本文所涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/go1.17-examples/) – https://github.com/bigwhite/experiments/tree/master/go1.17-examples/

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强。在2021年上半年，部落将策划两个专题系列分享，并且是部落独享哦：

- Go技术书籍的书摘和读书体会系列
- Go与eBPF系列

欢迎大家加入！

![](../../assets/b634c86efd3a19cc.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订

阅！

![img{512x368}](../../assets/8974393c1b81f912.jpg)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/d6497e1263ffb6ad.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论