---
title: Go 1.24新特性前瞻：语法、编译器与运行时
url: https://tonybai.com/2024/12/16/go-1-24-foresight-part1/
published: '2024-12-16'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.24新特性前瞻：语法、编译器与运行时

![](../../assets/7d5885ed4309af2b.png)


[本文永久链接](https://tonybai.com/2024/12/16/go-1-24-foresight-part1) – https://tonybai.com/2024/12/16/go-1-24-foresight-part1

自2020年底撰写《[Go 1.16版本新特性前瞻](https://tonybai.com/2020/12/12/a-forward-look-to-new-feature-of-go-1-16)》以来，四年转瞬而逝。在这段时间里，每当Go的大版本开发进入新特性冻结(freeze)阶段，我都会为大家带来该版本的特性前瞻，旨在让大家更早地了解和实验这些新特性，从而在版本正式发布时能够准确评估是否应用它们。

11月末，Go 1.24的新特性开发已经冻结，我认为是时候对Go 1.24新特性进行前瞻了。本次前瞻将分为两篇进行，本文，也就是第一篇将讲解语法、编译器与运行时方面的变化，而第二篇将聚焦工具链和标准库。本次前瞻可以引导大家了解即将在明年3月份发布的Go 1.24版本中的重要变化，希望能给大家带去帮助。

注：Go每六个月发布一次。每个

[发布周期]都分为持续约4个月的开发阶段，然后是为期3个月的测试和完善阶段（称为发布冻结期）。当前的发布周期预计于每年一月中旬和七月中旬开始，如下图所示。以Go 1.24为例，2024年7月开始plan，经过4个月开发，11月下旬冻结，再经历3个月的测试完善，预计2025年2月发布。

![](../../assets/644d5618223b5ea3.jpg)



注：大家可以使用

[Go playground]体验dev branch的最新特性，或[在本地安装GoTip版本]进行体验。2024年12月14日，Go 1.24RC1版本发布，大家也可以直接用go install golang.org/dl/go1.24rc1@latest体验，或到Go官方下载站unstable version中直接下载安装。

## 1. 语法

[Go 1.18引入了泛型](https://tonybai.com/2022/04/20/some-changes-in-go-1-18)，[Go 1.21版本](https://tonybai.com/2023/08/20/some-changes-in-go-1-21/)新增了max、min和clear等预定义函数，而[Go 1.23版本](https://tonybai.com/2024/08/19/some-changes-in-go-1-23)则引入了[自定义迭代器](https://tonybai.com/2024/06/24/range-over-func-and-package-iter-in-go-1-23)。与这些创新相比，Go 1.24似乎又回归到了我们熟悉的“静默期”，没有显著的语法特性更新。

唯一一个值得提及的还是Go 1.23版本引入的[实验特性](https://tonybai.com/2024/10/11/go-evolution-dual-insurance-goexperiment-godebug)：“[带有类型参数的type alias](https://github.com/golang/go/issues/46477)”。如果你已经忘记这是一个什么语法特性，下面我就带你简单地回顾一下。

传统的类型别名的形式是这样的：

```
type P = Q
```


在《[“类型名称”在Go语言规范中的演变](https://tonybai.com/2024/09/24/the-evolution-of-type-name-in-go-spec/)》一文中我们介绍过，Q是Named Type，包括Predeclared Type、Anonymous Type、Existing Defined Type以及Existing Alias Type，甚至可以用泛型类型实例化后的类型作为Q，比如：

```
type MySlice[T any] []T
func main() {
type P = MySlice[int] // MySlice[int]作为Q
var p P
fmt.Println(len(p)) // 0
}
```


但P中不能包含类型参数！下面这样的类型别名定义是不合法的：

```
type P[T any] = []T
```


不过[Go 1.23版本](https://tonybai.com/2024/08/19/some-changes-in-go-1-23)以实验特性(需显式使用GOEXPERIMENT=aliastypeparams)支持了带有类型参数的类型别名，在**Go 1.24中，这个实验特性转正了，成为了默认特性**。我们看看下面这个示例：

```
// go1.24-foresight/lang/generic_type_alias.go
package main
import "fmt"
type MySlice[T any] = []T
func main() {
// 使用int类型实例化MySlice
intSlice := MySlice[int]{1, 2, 3, 4, 5}
fmt.Println("Int Slice:", intSlice)
// 使用string类型实例化MySlice
stringSlice := MySlice[string]{"hello", "world"}
fmt.Println("String Slice:", stringSlice)
// 使用自定义类型实例化MySlice
type Person struct {
Name string
Age int
}
personSlice := MySlice[Person]{
{Name: "Alice", Age: 30},
{Name: "Bob", Age: 25},
}
fmt.Println("Person Slice:", personSlice)
}
```


使用Gotip直接运行上面示例，我们可以得到如下结果：

```
Int Slice: [1 2 3 4 5]
String Slice: [hello world]
Person Slice: [{Alice 30} {Bob 25}]
```


怎么理解带有类型参数的类型别名呢？在《[Go 1.23中值得关注的几个变化](https://tonybai.com/2024/08/19/some-changes-in-go-1-23/)》一文中，我们也介绍了Russ Cox给出的理解，即可以将其看成是一种“类型宏”(类似c中的#define)：

```
type MySlice[T any] = []T
```


就是**在任何出现MySlice[T]的地方，将其换成[]T**。

在Go 1.23以实验特性出现的带类型参数的别名还有一些问题，比如下面这个本不该正常运行的示例(int切片类型是不满足comparable的)，在Go 1.23.0版本中是可以正常编译运行的：

```
// go1.24-examples/lang/strict_alias.go
package main
import "fmt"
type MySlice[T any] = []T
type YourSlice[T comparable] = MySlice[T]
func main() {
// 使用int类型实例化MySlice
intSlice := MySlice[int]{1, 2, 3, 4, 5}
fmt.Println("Int Slice:", intSlice)
intsliceSlice := YourSlice[[]int]{
[]int{1, 2, 3},
[]int{4, 5, 6},
}
fmt.Println("IntSlice Slice:", intsliceSlice)
}
```


不过在Go 1.24中该问题被修正，如果你使用gotip运行该示例，你将得到类似下面编译错误：

```
./strict_alias.go:13:29: []int does not satisfy comparable
```


在[gotip版go spec](https://tip.golang.org/ref/spec#Alias_declarations)(截至2024.12.09)中，对带有类型参数的type alias有如下约束：

```
type A[P any] = P // illegal: P is a type parameter
```


即类型别名声明中的右侧已知类型不能是类型参数自身。但目前的gotip实现似乎忽略了这一条，下面代码在gotip下是可以正常编译运行的：

```
package main
import "fmt"
type A[P any] = P
func main() {
var a A[int] = 5 // identical to int
fmt.Println(a) // 5
}
```


此外Go 1.23.0中，带有类型参数的别名类型是不能跨包使用的，但Go 1.24中这条限制被取消了，[带有类型参数的别名类型可以与常规类型别名一样跨包使用](https://github.com/golang/go/issues/68526)。

在Go 1.24中，你也可以通过设置GOEXPERIMENT=noaliastypeparams来禁用这一特性，但该设置将在Go 1.25中被移除。

## 2. 编译器与运行时

### 2.1 运行时性能优化

Go 1.24版本在运行时方面实现了多个优化，包括采用[基于Swiss Tables的原生map实现(#54766)](https://github.com/golang/go/issues/54766)、更高效的小对象内存分配以及[改进的内部互斥锁实现](https://github.com/golang/go/issues/68578)，整体降低了2-3%的CPU开销。

[Swiss Table](https://abseil.io/about/design/swisstables)是由Google工程师于2017年开发的一种高效哈希表实现，旨在优化内存使用和提升性能，解决Google内部代码库中广泛使用的std::unordered_map所面临的性能问题。目前，Swiss Table已被应用于多种编程语言，包括[C++ Abseil库的flat_hash_map(可替换std::unordered_map)](https://abseil.io/about/design/swisstables)、[Rust标准库Hashmap的默认实现](https://github.com/rust-lang/hashbrown)等。在[字节工程师的提案](https://github.com/golang/go/issues/54766)下，Go runtime团队决定替换原生map的底层实现，改为基于Swiss Table。通过基于gotip的实测，大多数测试项中，新版基于swiss table的map的性能都有大幅提升，有些甚至接近50%！之前写过一篇《[Go map使用Swiss Table重新实现，性能最高提升近50%](https://tonybai.com/2024/11/14/go-map-use-swiss-table/)》，大家可以移步到那里了解关于基于Swiss Table实现的map的原理的详情，这里就不赘述了。

另外一个重要的性能优化是[runtime: improve scaling of lock2](https://github.com/golang/go/issues/68578)中的提案，旨在针对当前runtime.lock2实现的问题进行优化，具体的propsal在[design/68578-mutex-spinbit.md](https://github.com/golang/proposal/blob/master/design/68578-mutex-spinbit.md)文件中。下面简略说一下该优化的背景、方案原理以及取得的效果。

当前runtime.lock2的实现通过三态设计（未锁定、锁定、锁定且有等待线程），在高竞争情况下，多个线程反复轮询mutex的状态字，产生大量缓存一致性流量。每个轮询线程需要从内存中加载状态字，并在更新时触发缓存行失效，这导致性能大幅下降。而每次释放锁时，无论是否已有线程在轮询mutex状态字，都会尝试唤醒一个线程，这进一步增加了系统负载。总之，**现有的三态设计不能有效限制线程的忙等待行为。即使锁的临界区操作非常短，线程依然会因为抢占资源而竞争加剧**。

新提案引入“spinbit”机制，扩展mutex状态字，增加一个”spinning”位，表示是否有线程处于忙等待状态。一个线程可以独占此位，在轮询状态字时拥有优先权。其他线程无需忙等待，直接进入休眠。同时提案优化了唤醒逻辑，当unlock2检测到已有线程正在忙等待时，不再唤醒休眠线程，从而减少不必要的线程切换和上下文切换。

目前该优化提供了基于futex和非futex系统调用的两个实现，基于futex的版本适用于Linux平台，通过精细控制休眠线程的列表，进一步减少竞争。

状态字中使用独立的位分别表示锁定状态、休眠线程存在与否、忙等待标志等，并通过位操作和Xchg8原子操作，确保性能和线程安全。

新方案在高竞争状况下取得了显著的可扩展性提升，新实现的spinbit机制能维持性能稳定，而不是像现有实现那样随线程数增加而急剧下降。基准测试表明，在GOMAXPROCS=20时，性能提升达3倍。大部分线程可以按设计预期那样，直接休眠而非忙等待，减少了电力消耗和处理器资源占用。同时，通过对休眠线程的显式管理，可实现有针对性的唤醒，降低线程长期休眠的风险(避免饿死)。

上述的基于Swiss table的map实现以及lock2优化是实验特性，但都是默认生效的，在Go 1.24中，你可以在构建阶段，通过显式设置GOEXPERIMENT=noswissmap和GOEXPERIMENT=nospinbitmutex关闭这两个实验特性。

### 2.2 cgo：优化C代码调用

如果你决定不碰cgo，那么你大可略过这节的说明。

传统cgo机制下调用c函数时，Go会保证传递给C函数的go指针指向的对象位于堆上。但如果C函数不保留Go指针的副本，并且不将该指针传递回Go代码，那么这个保证就是没有必要的。Go 1.24增加了下面注解用于显式告诉go编译器：不会有指针通过特定的C函数逃逸。

```
// #cgo noescape cFunctionName
```


此外，当Go函数调用C函数时，它默认会为C函数中再调用Go函数做好准备，这当然会有一些额外开销。这对于那些不会调回Go函数的C函数也是没有必要的。在Go 1.24中新增的#cgo nocallback注解就是用于告诉编译器这些准备工作不是必需的：

```
// #cgo nocallback cFunctionName
```


更多关于上述cgo优化c代码调用的新机制的说明，请参见[cgo增加#cgo noescape和#cgo nocallback注解(#56378)](https://github.com/golang/go/issues/56378)。

### 2.3 [编译器禁止为C类型别名添加方法](https://github.com/golang/go/issues/60725)

Go 1.24之前，Go编译器允许在C类型的别名上声明方法，虽然某些时候它可以正常工作，如下面示例：

```
package main
/*
typedef int foo;
*/
import "C"
type foo = C.foo
func (foo) method() int { return 123 }
func main() {
var x foo
println(x.method()) // "123"
}
```


但这可能引入了潜在的类型安全性以及运行时错误问题，尽管目前为C类型别名添加方法的情形非常少。

Go 1.24通过引入了一个新的编译器检查修复了该问题，该检查利用了isCgoGeneratedFile函数和类型名称的特征（如_Ctype_前缀）来识别C类型别名，并禁止在C类型别名上声明方法。

## 3. 小结

本文对即将发布的Go 1.24版本的新特性进行了全面的展望。主要内容包括：

语法更新：Go 1.24未显著增加新语法特性，但实验性特性“带有类型参数的类型别名”已转正为默认特性，允许更灵活的类型别名定义。

编译器与运行时优化：

- 运行时性能优化：引入了基于Swiss Tables的新原生map实现，显著提高了性能。还优化了内部互斥锁的实现，改善了高竞争情况下的性能。
- cgo改进：新增了#cgo noescape和#cgo nocallback注解，优化C代码调用的效率。
- 编译器限制：禁止在C类型别名上声明方法，以提高类型安全性。

Go 1.24版本在语法上保持稳定，但在性能和安全性方面进行了多项关键优化，旨在提升开发者的体验和代码的效率。

在接下来的“Go 1.24新特性前瞻：工具链和标准库”一文中，我将继续为大家带来更丰富详尽的Go 1.24新特性，敬请期待！

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/go1.24-foresight)下载。

## 4. 参考资料

[Go 1.24 milestone](https://github.com/golang/go/milestone/322)– https://github.com/golang/go/milestone/322[Go 1.24 Release Notes Draft](https://tip.golang.org/doc/go1.24)– https://tip.golang.org/doc/go1.24[Go Release Dashboard](https://dev.golang.org/release)– https://dev.golang.org/release[Go spec tip](https://tip.golang.org/ref/spec)– https://tip.golang.org/ref/spec

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
- Gopher Daily Feed订阅 – https://gopherdaily.tonybai.com/feed

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论