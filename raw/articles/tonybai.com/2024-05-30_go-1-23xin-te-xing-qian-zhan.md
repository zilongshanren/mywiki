---
title: Go 1.23新特性前瞻
url: https://tonybai.com/2024/05/30/go-1-23-foresight/
published: '2024-05-30'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.23新特性前瞻

![](../../assets/19e8659e4139b71e.png)


[本文永久链接](https://tonybai.com/2024/05/30/go-1-23-foresight) – https://tonybai.com/2024/05/30/go-1-23-foresight

2024年5月22日，[Go 1.23版本](https://github.com/golang/go/milestone/212)功能特性正式冻结，后续将只改bug，不增加新feature。

![](../../assets/92bb4ba12af0061d.png)


对Go团队来说，这意味着开始了Go 1.23rc1的冲刺，对我们普通Gopher而言，这意味着**是时候对Go 1.23新增的功能做一些前瞻了**！

在Go没有发布Go 1.23rc1之前，我们至少可以通过以下两种渠道体验Go 1.23的最新特性：

- 通过go install安装tip版本；
- 使用
[Go playground](https://go.dev/play/)在线体验。

注：关于Go tip的安装方法以及Go playground在线体验的详细说明，这里就不赘述了，

[《Go语言第一课》]专栏的“[03｜配好环境：选择一种最适合你的Go安装方法]”有系统全面的讲解，欢迎订阅阅读。

按照[Go Release cycle](https://go.dev/wiki/Go-Release-Cycle)，Go 1.23将于2024年8月发布！因此目前为时尚早，下面列出的有些变化最终不一定能进入到Go 1.23的最终版本中，有小概率被revert的可能或者推迟到下一个版本(Go 1.24)，所以切记一切变更点要以最终Go 1.23版本发布时为准。

## 1. 语言变化

Go 1.23语言变化较少，除了range over func试验特性转正，再有就是几个悬而未决的spec变更。

### 1.1 range over func试验特性转正([61405](https://github.com/golang/go/issues/61405))

[Go 1.22版本](https://tonybai.com/2024/02/18/some-changes-in-go-1-22/)引入了[range over func](https://go.dev/wiki/RangefuncExperiment)试验特性，通过GOEXPERIMENT=rangefunc，可以实现函数迭代器。这一特性在Go 1.23版本正式转正，下面代码可以直接使用Go 1.23编译运行：

```
// go1.23-foresight/lang/range-over-function-iterator/main.go
package main
import "fmt"
func Backward[E any](s []E) func(func(int, E) bool) {
return func(yield func(int, E) bool) {
for i := len(s) - 1; i >= 0; i-- {
if !yield(i, s[i]) {
return
}
}
return
}
}
func main() {
sl := []string{"hello", "world", "golang"}
for i, s := range Backward(sl) {
fmt.Printf("%d : %s\n", i, s)
}
}
```


使用Go 1.23运行上述示例：

```
$go run main.go
2 : golang
1 : world
0 : hello
```


range over func可以提供一种统一、高效的迭代方式, 为泛型后的自定义容器类提供统一的迭代接口，同时也可以替代部分现有API返回切片的做法, 改为通过迭代器的形式改进性能（通过编译器的优化），甚至还可以为函数式编程风格提供标准迭代机制。

rang over func机制的实现是通过编译器在源码层面的转换，其转换形式大致如下：

```
// 单循环变量
for x := range f1 {
...
}
```


将被转换为：

```
f1(func(x T) bool {
...
})
```


而另外一种常见的双循环变量形式的for range：

```
for expr1, expr2 = range f2 {
...
}
```


将被转换为：

```
f2(func(#p1 T1, #p2 T2) bool {
expr1, expr2 = #p1, #p2
...
})
```


前提是：f1和f2分别要满足标准库中iter包中的下面函数原型形式：

```
// $GOROOT/src/iter/iter.go
type Seq[V any] func(yield func(V) bool) bool
type Seq2[K, V any] func(yield func(K, V) bool) bool
```


此外，for range循环体中如果有break，将被转换为f1/f2中的return false，而如果有continue，则会被转换为return true。当然这只是大致的形式，实际的转换远比这个要复杂很多，要考虑的情况也是十分复杂。更为具体、复杂的转换可以参考[Go编译器的实现源码rewrite.go](https://github.com/golang/go/blob/master/src/cmd/compile/internal/rangefunc/rewrite.go)

函数迭代器虽然转正，但肯定尚未成熟，后续还会有诸多问题(比如一些corner case)需要解决，比如Russ Cox新开的[issue 65236](https://github.com/golang/go/issues/65236)就在讨论是否允许忽略迭代变量；[issue 65237](https://github.com/golang/go/issues/65237)将跟踪spec中与range over func相关内容的变更。

### 1.2 spec：几个悬而未决的issue

这个issue来自我提出的《[Go 1.22引入的包级变量初始化次序问题](https://tonybai.com/2024/03/29/the-issue-in-pkg-level-var-init-order-in-go-1-22/)》，Go 1.23已经修正了该问题，并保持与Go 1.22之前的版本一致，但[go spec](https://go.dev/ref/spec)中尚未就此给出明确的说明。

[澄清”严格可比较”(strictly comparable)和”类型约束”(type constraints)等术语 (issue 59104)](https://github.com/golang/go/issues/59104)[修改关于”类型参数是接口”的说明，避免引起混淆(issue 57310)](https://github.com/golang/go/issues/57310)[禁止匿名接口类型的循环定义(issue 56103)](https://github.com/golang/go/issues/56103)

一些issue已经“跳票”多次，不能确定以上issue都能最终在Go 1.23得以解决！

## 2. 编译器与运行时

### 2.1 优化了[PGO(Profile Guided Optimization)](https://go.dev/doc/pgo)带来的处理开销 ([issue 58102](https://github.com/golang/go/issues/58102))

Go社区发现启用PGO后，每个cmd/compile调用都会解析完整的PGO pprof配置文件，构建完整的权重图，然后确定与该包相关的内容。这类工作项有很多，并且随着Profile文件的大小和构建包的数量的扩展，构建开销也会增大。尤其是对于那些特别大的项目，PGO Profile很大，这可能会导致构建时间增加100%以上。

Go 1.23对这个问题进行了优化，PGO开销被降到了个位数百分比。

### 2.2 限制将来对linkname的使用([67401](https://github.com/golang/go/issues/67401))

在Go语言中，//go:linkname指令可以用来链接到标准库或其他包中的未导出符号。比如我们想访问runtime包中的一个未导出函数，例如runtime.nanotime。这个函数返回当前时间的纳秒数。我们可以通过//go:linkname指令链接到这个符号。下面我用一个示例来演示一下这点：

```
// go1.23-foresight/compiler/golinkname/main.go
package main
import (
"fmt"
_ "unsafe" // 必须导入 unsafe 包以使用 //go:linkname
)
// 声明符号链接
//
//go:linkname nanotime runtime.nanotime
func nanotime() int64
func main() {
// 调用未导出的 runtime.nanotime 函数
fmt.Println("Current time in nanoseconds:", nanotime())
}
```


运行该示例：

```
$go run main.go
Current time in nanoseconds: 374424337532051
```


这种做法一般不推荐，因为它可能导致程序不稳定，并且未来版本的Go可能会改变内部实现（比如nanotime被改名或被删除），破坏你的代码。

Go团队已经意识到这一点，并发现现存开源代码中有很多代码都通过//go:linkname依赖Go项目的internal下的包或Go标准库的未导出符号。这显然不是Go团队想看到的事儿，于是Russ Cox发起issue 67401，旨在考虑限制对//go:linkname的使用。

该issue虽然在Go 1.23 milestone中，但最终是否能落在Go 1.23中还不确定，毕竟这样的调整会导致一些现存代码无法正常编译运行。

### 2.3 其他一些优化

- 优化内存分配器的行为，减少了大内存(带有指针)分配时的长暂停 (
[issue 31222](https://github.com/golang/go/issues/31222)) - 修复Windows下time.Sleep的精度问题(
[issue 44343](https://github.com/golang/go/issues/44343)) - 增加了设置崩溃输出的API runtime/debug.SetCrashOutput(
[issue 42888](https://github.com/golang/go/issues/42888)) - 对内联器继续进行大修：重构优化 (
[issue 61502](https://github.com/golang/go/issues/61502))，这是一个长期任务，估计后续版本还会继续。

## 3. 工具链

### 3.1 新增go telemetry子命令，改进go工具链的遥测能力 ([issue 67111](https://github.com/golang/go/issues/67111))

Russ Cox去年初就在个人博客上发布了[四篇有关Go Telemetry的文章](https://research.swtch.com/telemetry)，在2023 GopherCon大会上，Russ Cox也谈到了[Go Telemetry对基于数据驱动进行Go演进决策的重要性](https://tonybai.com/2023/12/10/go-changes/)。Russ Cox亲自创建的[“all: add opt-in transparent telemetry to Go toolchain”](https://github.com/golang/go/issues/58894)提案也被Go项目接受。

Go工具链中的telemetry是数据驱动的重要一环，最初[golang.org/x/telemetry实验项目](https://github.com/golang/telemetry)被建立。在Go 1.23中，go工具链新增了go telemetry子命令，该子命令就是基于golang.org/x/telemetry实验项目，这也是Go团队实现某一个特性的一贯套路。

go telemetry子命令用法大致如下(以最终版本的doc为准)：

```
go telemetry - 打印telemetry mode: on, off or local；
go telemetry on - 设置mode为on；即开启telemetry且上传遥测数据。
go telemetry local - 设置mode为local；即telemetry数据仅存储在本地，但不上传。
go telemetry off - 设置mode为off。即关闭telemetry
go clean -telemetry - 清理本地的遥测数据目录。
```


### 3.2 其他一些改变

- go build(-json)支持以json形式输出构建结果(
[issue 62067](https://github.com/golang/go/issues/62067))，让构建结果更结构化 - 移除了对GOROOT_FINAL的支持 (
[issue 62047](https://github.com/golang/go/issues/62047))，估计很多人不知道或完全没用过GOROOT_FINAL，我也是如此。

## 4. 标准库

### 4.1 Timer/Ticker变化

timer/ticker的stop/reset问题一直困扰Go团队，Go 1.23的两个重要fix期望能从根本上解决这个问题：

- Timer/Ticker的GC不再需要Stop(
[issue 61542](https://github.com/golang/go/issues/61542))

程序不再引用的Timer和Ticker将立即有资格进行垃圾回收，即使它们的Stop方法尚未被调用。Go的早期版本直到触发后才会收集未停止的Timer，并且从未收集未停止的Ticker。

- Timer/Ticker的Stop/Reset后不再接收旧值(
[issue 37196](https://github.com/golang/go/issues/37196))

与Timer或Ticker关联的计时器channel现在改为无缓冲的了，即容量为0 。此更改的主要效果是Go现在保证任何对Reset或Stop方法的调用，调用之前不会发送或接收任何陈旧值。 Go的早期版本使用带有缓冲区的channel，因此很难正确使用Reset和Stop。此更改的一个明显效果是计时器channel的len和cap现在返回0而不是1，这可能会影响轮询长度以确定是否在计时器channel上接收的程序。通过GODEBUG设置asynctimerchan=1可恢复异步通道行为。

### 4.2 新增unique包([issue 62483](https://github.com/golang/go/issues/62483))

unique包的灵感来自于第三方包[go4.org/intern](https://github.com/go4org/intern)，也是为了弥补Go语言缺乏对[interning](https://en.wikipedia.org/wiki/Interning_(computer_science))内置支持的空缺。

根据wikipedia的描述，interning是按需重复使用具有同等值对象的技术，减少创建新对象的动作。这种创建模式经常用于不同编程语言中的数和字符串，可以避免不必要的对象重复分配的开销。

Go unique包即是Go的interning机制的实现，unique包提供了一种高效的值去重和快速比较的机制，可以用于优化某些特定场景下的程序性能。

unique包提供给开发人员的API接口非常简单：Make用来创建Handle实例，Handle的方法Value用于获取值的拷贝。下面是一个使用unique包的典型示例：

```
// go1.23-foresight/lib/unique/main.go
package main
import (
"fmt"
"unique"
)
func main() {
// 创建唯一Handle
s1 := unique.Make("hello")
s2 := unique.Make("world")
s3 := unique.Make("hello")
// s1和s3是相等的，因为它们是同一个字符串值
fmt.Println(s1 == s3) // true
fmt.Println(s1 == s2) // false
// 从Handle获取原始值
fmt.Println(s1.Value()) // hello
fmt.Println(s2.Value()) // world
}
```


代码和输出结果都不难理解，这类就不赘述了。

### 4.3 函数迭代器相关

前面说过，函数迭代器转正了。标准库中有一些包立即就提供了一些便利的、可以与函数迭代器一起使用的函数，以slices、maps两个后加入Go标准库的泛型容器包为主。

其中slices包增加了：All、Values、Backward、Collect、AppendSeq、Sortted、SortedFunc、SortedStableFunc和Chunk。maps包增加了All、Keys、Values、Insert和Collect。

我们以slices包的All和Backward来构建一个示例，直观感受一下：

```
// go1.23-foresight/lib/slices/main.go
package main
import (
"fmt"
"slices"
)
func main() {
sl := []string{"hello", "world", "golang"}
for i, s := range slices.All(sl) {
fmt.Printf("%d : %s\n", i, s)
}
for i, s := range slices.Backward(sl) {
fmt.Printf("%d : %s\n", i, s)
}
}
```


运行该示例：

```
$go run main.go
0 : hello
1 : world
2 : golang
2 : golang
1 : world
0 : hello
```


和以往一样，Go标准库是变化最多的一块儿，但篇幅有限，这里不便枚举，大家可以自行查看Go 1.23里程碑，选择自己关注的标准库变化，并深入研究。

## 5. 小结

本文主要预览了Go 1.23版本即将带来的新特性和变化。

首先在语言层面，range over func试验特性正式转正，提供统一高效的迭代方式；同时也会修复之前一些悬而未决的规范问题。

其次，在编译器和运行时方面，Go 1.23将优化PGO带来的开销，限制对linkname的使用，优化内存分配器和内联器等。工具链方面，新增telemetry子命令改进遥测能力。

标准库也有不少变化，比如Timer/Ticker的相关修复，新增unique包实现interning机制，以及为函数迭代器新增一些辅助函数。

Go 1.23的Release Notes的编写方式也做了调整，详细内容可参考我的公号文章[《Go 1.23 Release Notes编写方式改进！》](https://mp.weixin.qq.com/s/FgNepRmRJlw-7RBnSiywQA)。

总的来说，Go 1.23包含了语法、编译器、运行时、工具链和标准库等多方面的改进，其中最主要集中在编译器性能优化、PGO特性增强、新编译器功能实现以及标准库增强等方面。

不过由于Go 1.23尚未发布，文中部分变化还可能被修改或推迟到下个版本。最终还是以正式发布版为准。文末也列出了一些相关资源链接，方便读者深入了解。

截至发文时，Go 1.23 milestone已经完成59%(https://github.com/golang/go/milestone/212)，还有188个open的issue待解决。究竟Go 1.23最终会做出哪些改变，让我们拭目以待！

最后，感谢Go团队以及所有Go 1.23贡献者做出的伟大工作！

文本涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/go1.23-foresight)下载。

## 6. 参考资料

[Go 1.23版本里程碑](https://github.com/golang/go/milestone/212)– https://github.com/golang/go/milestone/212[Next Release Notes Draft](https://tip.golang.org/doc/next)– https://tip.golang.org/doc/next[Go Release Dashboard](https://dev.golang.org/release)– https://dev.golang.org/release

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2024年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。同时，我们也会加强代码质量和最佳实践的分享，包括如何编写简洁、可读、可测试的Go代码。此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

移除了对GOROOT_FINAL的支持 (issue 62047)：这个 issue id 是不是贴错了？

链接到的issue的确错了，已改正，感谢指出:)