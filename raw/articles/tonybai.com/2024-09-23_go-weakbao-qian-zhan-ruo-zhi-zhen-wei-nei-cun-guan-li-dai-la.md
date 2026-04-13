---
title: Go weak包前瞻：弱指针为内存管理带来新选择
url: https://tonybai.com/2024/09/23/go-weak-package-preview/
published: '2024-09-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go weak包前瞻：弱指针为内存管理带来新选择

![](../../assets/cb8c2b79653d0f62.png)


[本文永久链接](https://tonybai.com/2024/09/23/go-weak-package-preview) – https://tonybai.com/2024/09/23/go-weak-package-preview

在介绍[Go 1.23](https://tonybai.com/2024/08/19/some-changes-in-go-1-23)引入的unique包的《[Go unique包：突破字符串局限的通用值Interning技术实现](https://tonybai.com/2024/09/18/understand-go-unique-package-by-example/)》一文中，我们知道了unique包底层是基于internal/weak包实现的，internal/weak是一个弱指针功能的Go实现。所谓弱指针(Weak Pointer，也称为弱引用)是与强指针相对而言的，强指针(Strong Pointer，也可称作强引用)就是下面代码片段中的这种常规指针：

```
var p *T = new(T) // 假设T类型对象被分配到堆上
```


只要p指向堆上的T对象，那么T对象就无法被GC回收。但弱指针并非如此，它也可以指向堆上的某个内存对象(比如T类型对象)，但它无法像强指针那样阻止GC回收该对象。

Go unique包的实现者[Michael Knyszek近期提议在标准库引入weak包](https://github.com/golang/go/issues/67552)(实际上是将internal/weak公开暴露给Go开发者)，该提议被Russ Cox代表的Go提案评审委员会所接受，最早将于Go 1.24版本落地。

在这篇短文中，我们来前瞻一下weak包的API设计、原理、应用场景以及社区对该提案一些观点。

注：weak包尚未落地，本文中的代码在Go 1.23中均无法运行，可以视作伪代码。


## 1. weak包的API

weak包的核心是Pointer[T]类型，它代表了对类型T的弱指针。以下目前Michael Knyszek为weak包设计的主要API：

```
type Pointer[T any] struct { ... }
func Make[T any](ptr *T) Pointer[T]
func (p Pointer[T]) Value() *T
```


Make函数用于创建一个弱指针，而Value方法则用于获取弱指针指向的实际值。如果原始对象已被垃圾回收，Value方法将返回nil。这个设计秉承了Go一贯的简洁，允许开发者轻松创建和使用弱指针，同时保持了Go语言的类型安全特性。

## 2. weak包弱指针的工作原理

在开篇时，我已经对弱指针的作用做了简单说明，这里结合上述weak包的API和提案中的设计原理再扩展一下。

弱指针的核心思想是允许引用内存而不阻止垃圾回收器回收它。垃圾回收器在回收对象时，会自动将所有指向该对象的弱指针设置为nil。这确保了弱指针不会产生悬空引用(dangling pointer)。

下图是weak包弱指针的工作原理示意图，展示了weak pointer的核心工作原理，包括间接对象的使用和垃圾回收时的行为：

![](../../assets/22933cfff81ab652.png)


简单看一下这张图：程序创建一个对象并通过weak.Make创建一个weak.Pointer(弱指针)，在Go运行时内部，weak.Pointer通过8字节的间接对象引用原始对象。这个间接对象是weak.Pointer的内部字段，按当前internal/weak的实现来看，该字段是一个unsafe.Pointer。这个间接对象包含了实际的弱引用。

值得注意的是，弱指针的比较基于它们最初创建时使用的指针。即使原始对象被回收，两个由相同指针创建的弱指针仍然会被认为是相等的。这个特性使得弱指针可以安全地用作map的键。

## 3. weak包的典型使用场景

weak包的引入将为Go带来更灵活的内存管理机制，它允许开发者创建不会阻止垃圾回收的引用，从而在保持内存效率的同时，实现更复杂的数据结构和算法。特别是在处理缓存、[规范化映射(Canonicalization mapping)](https://wiki.c2.com/?CanonicalizedMapping)等场景时。

以缓存为例，使用弱指针，我们可以创建不会阻止被缓存对象被垃圾回收的缓存系统，这对于管理内存敏感的大型缓存系统特别有用。下面提案中Russ Cox举的一个使用weak包实现简单缓存的示例(可理解为伪代码)：

```
type Cache[K any, V any] struct {
f func(*K) V
m atomic.Map[uintptr, func() V]
}
func NewCache[K comparable, V any](f func(*K)V) *Cache[K, V] {
return &Cache[K, V]{f: f}
}
func (c *Cache[K, V]) Get(k *K) V {
kw := uintptr(unsafe.Pointer((k))
vf, ok := c.m.Load(kw)
if ok {
return vf()
}
vf = sync.OnceValue(func() V { return c.f(k) })
vf, loaded := c.m.LoadOrStore(kw, vf) // 原issue中似乎少了第二个参数vf
if !loaded {
// Stored kw→vf to c.m; add the cleanup.
runtime.AddCleanup(k, c.cleanup, kw)
}
return vf()
}
func (c *Cache[K, V]) cleanup(kw uintptr) {
c.m.Delete(kw)
}
var cached = NewCache(expensiveComputation)
```


这段代码定义了一个泛型缓存结构Cache，它有两个类型参数K和V，以及两个成员字段f和m：

- f是一个函数，接受*K类型的指针，返回V类型的值，这是用于计算缓存值的函数。
- m是一个原子映射，键是K类型的弱指针，值是返回V的函数。

NewCache是缓存的创建函数，接受一个计算函数f，返回初始化的Cache指针。

Cache类型的Get方法用于获取缓存的值，它首先创建键k的弱指针kw，然后以该弱指针为键尝试从缓存(atomicMap)中加载值。如果找到，直接返回缓存的值。如果未找到，使用sync.OnceValue创建一个只执行一次的函数，调用c.f(k)计算值。之后，尝试将新计算的函数存储到缓存中。 如果成功存储（即之前没有这个键），添加一个清理函数，最后返回计算后的Value值。

这个实现允许缓存中的键在不再被程序其他部分引用时被垃圾回收，从而避免了内存长期占用或是泄漏。

## 4. 社区声音

针对该weak包提案，Go社区的主要声音是支持的，认为weak包将为Go带来更灵活的内存管理机制，但也表示了对无法用好weak包这个低级机制的担忧，希望在正式文档或Go Tour中包含更多使用关于weak包的示例和最佳实践。

Go新版GC的主要设计者[Richard L. Hudson](https://github.com/RLH)提出了对sweeping storms和清理大型缓存中过时weak条目的担忧，并提出了使用[ephemerons](https://dl.acm.org/doi/pdf/10.1145/263698.263733)（一种更复杂的弱引用机制）的可能性，但也认识到其实现复杂度和性能开销较高。

也有一些Go社区开发者保持了对weak包的谨慎态度，比如[fasthttp](https://tonybai.com/2021/04/25/server-side-performance-nethttp-vs-fasthttp)的维护者、[VictorialMetrics](https://github.com/VictoriaMetrics/VictoriaMetrics)的联创[Aliaksandr Valialkin](https://github.com/valyala) 就建议：在决定如何在Go中实现弱指针之前，最好先分析其他编程语言中弱指针的最常见的生产用例，并首先思考一下在标准库中为这些实际用例提供更高级别的解决方案而不是暴露较低级别的弱指针的方案是否会更好。

也有gopher提出：能否在提案中添加2-3个没有弱指针就无法解决的实际问题的例子，但Michael Knyszek并未回应。

## 5. 小结

weak包的引入让Go的工具箱更加完整，它为开发者提供了更细粒度的内存控制，同时其核心API也保持了Go简单易用的特性。

对于Go开发者来说，weak包使得某些复杂的内存管理场景变得更容易处理，但也需要开发者更好地理解垃圾回收机制和弱引用的工作原理。

社区对weak包的引入持积极态度，但也关注其实现细节、性能影响和最佳实践，同时也意识到了使用weak指针时可能面临的挑战。

不过，开发者在使用weak包时还是需要谨慎，毕竟过度使用弱指针可能会使代码变得难以理解和维护，最好的方法是将它用在最适合的场景下。

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

是不是每次GC，总是 会回收掉弱指针的内存空间？

在依然有强指针引用的时候，gc不会回收。如果没有强指针，只剩下弱指针，gc会回收其指向的内存对象。

能否在提案中添加2-3个没有弱指针就无法解决的实际问题的例子

这个确实有必要，毕竟要说添加的话，Go可以添加的东西太多了