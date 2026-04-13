---
title: 一文告诉你哪些map element类型支持就地更新
url: https://tonybai.com/2023/04/02/map-element-types-support-in-place-update/
published: '2023-04-02'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 一文告诉你哪些map element类型支持就地更新

![](../../assets/12871526670abd48.png)


[本文永久链接](https://tonybai.com/2023/04/02/map-element-types-support-in-place-update) – https://tonybai.com/2023/04/02/map-element-types-support-in-place-update

年初，我代表团队和人民邮电出版社签订了翻译[《Go Fundamentals》](https://gopherguides.com/golang-fundamentals-book)一书的合同，本月底便是四分之一进度的交稿时间点，近期闲时我们都在忙着做交叉review。

上周末我review小伙伴翻译的有关map类型的章节时，看到了书中对map element就地更新的讲解。[Mark Bates](https://github.com/markbates)和[Cory LaNou](https://github.com/corylanou)的这本书属于入门级Go语言书，只是举例说明了一些支持就地更新的map element类型以及不能就地更新的典型类型，但对不能更新的原因并未做深入说明。我觉得这个知识点不错，借这篇文章系统梳理一下。

## 一. 什么是map element的就地更新(in-place update)

我们知道Go中的map类型是一种无序的键值对集合，它的内部实现是基于哈希表的，支持高效地进行插入、查找和删除操作。map的key必须是可以进行相等比较的类型，比如整数、字符串、指针等，而element(也称为value)则可以是任意类型。并且，map是引用类型，它的零值为nil，使用前需要先使用内置函数make或map类型字面值进行空间分配。此外，在使用map时还需要注意并发安全问题，可以使用sync包提供的同步原语中来实现map的并发安全。

更多关于map的入门介绍与原理说明，可以阅读我的极客时间专栏

[《Go语言第一课》的第16讲]。

下面我们就来声明一个简单的map类型变量：

```
m := map[string]int{}
```


m是一个键为string类型、element为int类型的map。我们可以通过下面代码向map中插入一个键值对：

```
m["boy"] = 0
```


我们可以将其想象为一个统计班里男孩子数量的计数器：每数到一个男孩，我们就可以将其加1：

```
n := m["boy"]
n++
m["boy"] = n
```


你可以看到上述代码更新了键”boy”对应的element值(+1)。不过这种方法比较繁琐，要更新键”boy”对应的element值，我们还有下面这个更为简洁的方法：

```
m["boy"]++
```


我们看到和前面一种方法相比，这种方法没有引入额外的变量(比如前面的变量n)，而是直接在map element上进行了更新的操作，这种方法就称为**map element的“就地更新”**。

下面还有一些支持“就地更新”的map element类型的例子，比如：string、切片等：

```
m["boy"] += 1
// element类型为string
m1 := map[int]string{
1 : "hello",
2 : "bye",
} // map[1:hello 2:bye]
m1[1] += ", world" // map[1:hello, world 2:bye]
// element类型为切片
m2 := map[string][]int{
"k1": {1, 2},
"k2": {3, 4},
} // map[k1:[1 2] k2:[3 4]]
m2["k1"][0] = 11 // map[k1:[11 2] k2:[3 4]]
```


不过并非所有类型都支持“就地更新”，比如下面的数组与结构体作为map element类型时就会导致编译错误：

```
m3 := map[int][10]int{
1 : {1,2,3,4,5,6,7,8,9,10},
}
m3[1][0] = 11 // 编译错误：cannot assign to m3[1][0] (value of type int)
type P struct {
a int
b float64
}
m4 := map[int]P {
1 : {1, 3.14},
2 : {2, 6.28},
}
m4[1].a = 11 // 编译错误：cannot assign to struct field m4[1].a in map
```


那么为什么会这样呢？为什么同样作为map element，有的类型可以就地更新，有的类型就不支持呢？我们继续向下看。

## 二. element类型支持就地更新的本质

支持element类型就地更新这种“语法糖”在实际编写代码中体验还是非常好的，避免了下面这种“三行”冗余代码：

```
a := m["boy"]
a++
m["boy"] = a
```


那么，Go究竟是如何实现“就地更新”的呢？我们还以以上面的m变量为例：

```
m := map[string]int{
"boy" : 0,
"girl" : 0,
}
```


当我们执行下面的就地更新语句时：

```
m["boy"]++
```


我们来看一下底层的汇编是啥样的：

![](../../assets/db47aee5e6999ab4.png)


汇编语句不是很好懂，不过我们仅关注一下重点。我们看到汇编调用了runtime.mapassign_faststr这个函数，该函数的语义就是通过传入的key，找到对应的element，并将element的地址传出来。这里element的地址放入了AX寄存器中；接下来我们看到汇编调用INCQ指令将AX寄存器指向的内存块中的数据做了加1操作，从而实现了m["boy"]++这个语句的语义。

如果用伪代码来表示这个过程大致是这样的：

```
// 伪代码，下面的代码无法通过go编译，go在语法层面不支持获取map element的地址
p := &m["boy"]
(*p)++
```


到这里小伙伴们可能会问：为什么Go不针对类型为struct和array的element提供这种语法糖呢？我们假设struct的字段更新也支持就地更新，那么会发生什么呢？

```
type P struct {
a int
b float64
}
m4 := map[int]P {
1 : {1, 3.14},
2 : {2, 6.28},
}
m4[1].a = 11
```


上面的m4[1].a = 11将等价于如下代码：

```
t := &(m4[1])
t.a = 11
```


我们看到与element类型为int或string不同，由于要更新struct内部的字段，我们这次必须**获取element的地址**。一旦可以获取地址，问题就来了！这个地址是map在runtime层维护的内存地址，一旦暴露出来至少会有如下两个问题：

- 并发访问时会导致该element数据的竞争问题；
- map自动扩容后，
**element地址会变更**，通过上述代码获取的地址可能变为无效。

当然第二点更为重要，也正是因为这个原因，**Go决定不支持对map的element取地址**。

不过这似乎也并非是什么不可逾越的“鸿沟”，在runtime层面，element地址还是可以拿到的，就像前面的map[string]int那样。但目前Go团队依旧没有松口，在[Go issue 3117](https://github.com/golang/go/issues/3117)中，Go团队一直跟踪着上述结构体类型作为map element时不能就地更新的问题。该issue并没有close，说明也许未来Go针对这样的行为的处理可能会发生变化。

那是否可以用整体替换的三行代码方案来提供针对struct和array类型的element就地更新语法糖呢？ 以struct为例：

```
m4[1].a = 11
<=>
t := m4[1]
t.a = 11
m4[1] = t
```


即将struct和array作为一个整体，从map中获取副本，然后在临时变量中更新后，再重新覆盖map中的element。

go为什么不提供这种“语法糖”呢？我猜是因为这么做的性能开销较大！struct可以聚合很多字段，array的size也可能很可观，这样的两次copy的开销可能是Go开发者比较顾忌的。

那么目前的替代方案是什么呢? 其实很简单，那就是**element类型使用指针类型**，比如下面element类型为结构体指针类型的代码：

```
type P struct {
a int
b float64
}
m := map[int]*P{
1: {1, 3.14},
2: {2, 6.28},
}
fmt.Println(m[1]) // &{1 3.14}
m[1].a = 11
fmt.Println(m[1]) // &{11 3.14}
```


再比如element类型为数组指针类型的代码：

```
m1 := map[int]*[10]int{
1: {1, 2, 3},
}
fmt.Println(m1[1]) // &[1 2 3 0 0 0 0 0 0 0]
m1[1][0] = 11
fmt.Println(m1[1]) // &[11 2 3 0 0 0 0 0 0 0]
```


对map element“就地更新”的限制也会影响到是否能调用element类型的相关方法，我们再来看下面例子：

```
type P struct {
a int
b float64
}
func (P) normalFunc() {
}
func (p *P) updateInPlace(a int) {
p.a = a
}
func main() {
m1 := map[int]P{
1: {1, 3.14},
2: {2, 6.28},
}
m1[1].normalFunc()
m1[1].updateInPlace(11) // 编译错误：cannot call pointer method updateInPlace on P
m2 := map[int]*P{
1: {1, 3.14},
2: {2, 6.28},
}
fmt.Println(m2[1].a) // 1
m2[1].normalFunc()
m2[1].updateInPlace(11)
fmt.Println(m2[1].a) // 11
}
```


我们看到当element类型为P时，我们无法通过语法糖来调用会对结构体字段进行修改的updateInPlace方法，但可以调用normalFunc。而当element类型为P指针类型时，则无此限制。

那么，我们究竟如何判断哪些类型支持就地更新，哪些不支持呢？我们接下来就来说说。

## 三. 梳理与小结

我们最后来梳理一下Go的主要类型是否支持就地更新。

- 不涉及就地更新的类型

当element类型为布尔类型、函数类型时，我没找出针对这些map element就地更新的写法。

注：函数在Go中是一等公民。


- Go原生的基本类型，比如整型、浮点型、complex类型、string类型等

当这些类型作为map element类型时，它们和整型一样，支持元素的就地更新，其原理与上面的map[string]int也是类似的：

```
// 整型
m1 := map[int]int{
1: 1,
}
m1[1]++
fmt.Println(m1[1]) // 2
// 浮点型
m3 := map[int]float64{
1: 3.14,
}
m3[1]++
fmt.Println(m3[1]) // 4.140000000000001
// complex类型
m4 := map[int]complex128{
1: complex(2, 3), // 2+3i
}
m4[1]++
fmt.Println(m4[1]) // 3+3i
// string类型
m5 := map[int]string{
1: "hello",
}
m5[1] += " world"
fmt.Println(m5[1]) // hello world
```


- 对于指针、map、channel等类型

通过前面的讲解，我们知道**使用指针作为map element类型是支持就地更新的**，这里就不重复举例了。

map类型自身在Go运行时表示中也是一个指针，它也是支持就地更新的：

```
m := map[int]map[int]string{
1: {1: "hello"},
}
m[1][1] += " world"
fmt.Println(m[1][1]) // hello world
```


关于channel类型，如果将向channel写入数据当作“就地更新”的话，那么channel也勉强算是支持：

```
// channel
m1 := map[int]chan int{
1: make(chan int),
}
go func() {
m1[1] <- 11
}()
fmt.Println(<-m1[1]) // 11
```


- 对于切片、接口类型

通过前面的讲解，我们知道**使用切片作为map element类型是支持就地更新的**，这里就不重复举例了。

而对于接口类型，我理解的就地更新场景有两种，一种是通过接口值调用动态类型的方法，一种则是通过type assert来修改某些值。下面这两个场景的示例代码：

```
type MyInterface interface {
normalFunc()
updateInPlace(a int)
}
type P struct {
a int
b float64
}
func (P) normalFunc() {
}
func (p *P) updateInPlace(a int) {
p.a = a
}
func main() {
// interface
m1 := map[int]MyInterface{
1: &P{1, 3.14},
}
m1[1].updateInPlace(11) // 场景1：调用就地更新的方法
p := m1[1].(*P)
fmt.Println(p.a) // 11
(m1[1].(*P)).a = 21 // 场景2：通过type assert设置值
p = m1[1].(*P)
fmt.Println(p.a) // 21
}
```


- 对于数组、struct类型

通过前面的讲解，我们知道**使用数组和struct类型作为map element类型是不支持就地更新的**，这里就不重复举例了。

综上，目前只有当数组和结构体类型作为map元素类型时是不支持就地更新的。不过这种限制不一定一直持续下去，毕竟就地更新这种“语法糖”在编码过程中很好用，让代码变得更加简洁，也更加高效。后面Go团队可能会修改Go编译器以及运行时，让这种“语法糖”适用于所有类型。

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