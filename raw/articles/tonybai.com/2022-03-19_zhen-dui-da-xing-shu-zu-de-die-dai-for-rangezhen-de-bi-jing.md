---
title: 针对大型数组的迭代，for range真的比经典for loop慢吗？
url: https://tonybai.com/2022/03/19/for-range-vs-classic-for-loop-when-iterating-large-array/
published: '2022-03-19'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 针对大型数组的迭代，for range真的比经典for loop慢吗？

![](../../assets/7253555b380d05e8.png)


[本文永久链接](https://tonybai.com/2022/03/19/for-range-vs-classic-for-loop-when-iterating-large-array) – https://tonybai.com/2022/03/19/for-range-vs-classic-for-loop-when-iterating-large-array

Go语言推崇“**一件事情仅有一个作法**”！比如：Go仅保留一类循环控制语句，那就是**经典版的for loop**：

```
for i := 0; i < 100; i++ {
... ...
}
```


而像C语言支持的while、do…while等循环控制语句都被排除在Go简洁的语法之外。但为了方便Go开发者对复合数据类型的迭代，比如：数组、切片、channel以及map等，Go提供了一个变种for range loop，甚至对于map、channel进行遍历，仅能使用for range loop，经典版for loop根本不支持。

不过for range 带来了方便的同时，也给Go初学者带来了一些烦恼，比如：for range迭代复合类型变量时就有一些常见的且十分容易掉入的“坑”，这些“坑”我在[《Go语言第一课》](http://gk.link/a/10AVZ)中有全面详细的讲解。这里为了给后面的内容做铺垫，只提一个for range的坑，那就是**参与循环的是range表达式的副本**。

我们来看一个专栏中的例子：

```
func main() {
var a = [5]int{1, 2, 3, 4, 5}
var r [5]int
fmt.Println("original a =", a)
for i, v := range a {
if i == 0 {
a[1] = 12
a[2] = 13
}
r[i] = v
}
fmt.Println("after for range loop, r =", r)
fmt.Println("after for range loop, a =", a)
}
```


大家来猜猜这段代码会输出什么结果？你是不是觉得这段代码会输出如下结果：

```
original a = [1 2 3 4 5]
after for range loop, r = [1 12 13 4 5]
after for range loop, a = [1 12 13 4 5]
```


但实际运行该程序的输出结果却是：

```
original a = [1 2 3 4 5]
after for range loop, r = [1 2 3 4 5]
after for range loop, a = [1 12 13 4 5]
```


我们原以为在第一次迭代过程，也就是i = 0时，我们对a的修改 (a[1] =12,a[2] = 13) 会在第二次、第三次迭代中被v取出，但从结果来看，v 取出的依旧是a被修改前的值：2和3。

为什么会是这种情况呢？原因就是**参与for range循环的是range表达式的副本**。也就是说，在上面这个例子中，真正参与循环的是a的副本，而不是真正的a。

为了方便你理解，我们将上面的例子中的for range循环，用一个等价的伪代码形式重写一下：

```
for i, v := range a' { //a'是a的一个值拷贝
if i == 0 {
a[1] = 12
a[2] = 13
}
r[i] = v
}
```


现在真相终于揭开了：这个例子中，每次迭代的都是从数组a的值拷贝a’中得到的元素。a’是Go临时分配的连续字节序列，与a完全不是一块内存区域。因此无论a被如何修改，它参与循环的副本a’依旧保持原值，因此v从a’中取出的仍旧是a的原值，而不是修改后的值。

好了，问题来了(来自专栏的一位童鞋的留言)！

![](../../assets/670f9b8f9f5fc34d.png)


这位童鞋的核心问题就一个：**对于大型数组，由于参与for range的是该数组的拷贝，那么使用for range是不是会比经典for loop更耗资源且性能更差**？

我们通过benchmark例子来验证一下：**针对大型数组，for range是不是一定就比经典for loop跑得更慢**？我们先看第一个例子：

```
// benchmark1_test.go
package main
import "testing"
func BenchmarkClassicForLoopIntArray(b *testing.B) {
b.ReportAllocs()
var arr [100000]int
for i := 0; i < b.N; i++ {
for j := 0; j < len(arr); j++ {
arr[j] = j
}
}
}
func BenchmarkForRangeIntArray(b *testing.B) {
b.ReportAllocs()
var arr [100000]int
for i := 0; i < b.N; i++ {
for j, v := range arr {
arr[j] = j
_ = v
}
}
}
```


在这个例子中，我们分别用for loop与for range对一个拥有10w个int类型元素的数组进行遍历，我们看看benchmark的结果：

```
// Go 1.18rc1, MacOS
$go test -bench . benchmark1_test.go
goos: darwin
goarch: amd64
cpu: Intel(R) Core(TM) i5-8257U CPU @ 1.40GHz
BenchmarkClassicForLoopIntArray-8 22080 55124 ns/op 0 B/op 0 allocs/op
BenchmarkForRangeIntArray-8 34808 34433 ns/op 0 B/op 0 allocs/op
PASS
ok command-line-arguments 3.321s
```


从输出结果我们看到：for range loop非但未受到large array拷贝操作的影响，其性能居然比for range loop的性能还要好，这显然是在编译器层面(通常是静态单一赋值，即SSA环节)做了优化的结果。

我们关闭优化开关，再运行一下压测：

```
$go test -c -gcflags '-N -l' .
$./demo.test -test.bench .
goos: darwin
goarch: amd64
pkg: demo
cpu: Intel(R) Core(TM) i5-8257U CPU @ 1.40GHz
BenchmarkClassicForLoopIntArray-8 6248 187773 ns/op 0 B/op 0 allocs/op
BenchmarkForRangeIntArray-8 4768 246512 ns/op 0 B/op 0 allocs/op
PASS
```


我们看到：在没有优化的情况下，两种loop的性能都大幅下降，并且for range下降更多，性能显著不如经典for loop。你可以对比一下BenchmarkForRangeIntArray函数在正常优化(go tool compile -S xxx.go)以及关闭优化时(go tool compile -S -N -l)的汇编代码片段，你会发现关闭优化后，汇编代码使用了很多中间变量存储中间结果，而优化后的代码则消除了这些中间状态。

那么接下来你可能会提出这样一个问题：是不是for range迭代任何元素类型的大型数组，其性能都不比经典for loop差呢？我们来看一个对结构体数组遍历的例子：

```
// benchmark3_test.go
package main
import "testing"
type U5 struct {
a, b, c, d, e int
}
type U4 struct {
a, b, c, d int
}
type U3 struct {
b, c, d int
}
type U2 struct {
c, d int
}
type U1 struct {
d int
}
func BenchmarkClassicForLoopLargeStructArrayU5(b *testing.B) {
b.ReportAllocs()
var arr [100000]U5
for i := 0; i < b.N; i++ {
for j := 0; j < len(arr)-1; j++ {
arr[j].d = j
}
}
}
func BenchmarkClassicForLoopLargeStructArrayU4(b *testing.B) {
b.ReportAllocs()
var arr [100000]U4
for i := 0; i < b.N; i++ {
for j := 0; j < len(arr)-1; j++ {
arr[j].d = j
}
}
}
func BenchmarkClassicForLoopLargeStructArrayU3(b *testing.B) {
b.ReportAllocs()
var arr [100000]U3
for i := 0; i < b.N; i++ {
for j := 0; j < len(arr)-1; j++ {
arr[j].d = j
}
}
}
func BenchmarkClassicForLoopLargeStructArrayU2(b *testing.B) {
b.ReportAllocs()
var arr [100000]U2
for i := 0; i < b.N; i++ {
for j := 0; j < len(arr)-1; j++ {
arr[j].d = j
}
}
}
func BenchmarkClassicForLoopLargeStructArrayU1(b *testing.B) {
b.ReportAllocs()
var arr [100000]U1
for i := 0; i < b.N; i++ {
for j := 0; j < len(arr)-1; j++ {
arr[j].d = j
}
}
}
func BenchmarkForRangeLargeStructArrayU5(b *testing.B) {
b.ReportAllocs()
var arr [100000]U5
for i := 0; i < b.N; i++ {
for j, v := range arr {
arr[j].d = j
_ = v
}
}
}
func BenchmarkForRangeLargeStructArrayU4(b *testing.B) {
b.ReportAllocs()
var arr [100000]U4
for i := 0; i < b.N; i++ {
for j, v := range arr {
arr[j].d = j
_ = v
}
}
}
func BenchmarkForRangeLargeStructArrayU3(b *testing.B) {
b.ReportAllocs()
var arr [100000]U3
for i := 0; i < b.N; i++ {
for j, v := range arr {
arr[j].d = j
_ = v
}
}
}
func BenchmarkForRangeLargeStructArrayU2(b *testing.B) {
b.ReportAllocs()
var arr [100000]U2
for i := 0; i < b.N; i++ {
for j, v := range arr {
arr[j].d = j
_ = v
}
}
}
func BenchmarkForRangeLargeStructArrayU1(b *testing.B) {
b.ReportAllocs()
var arr [100000]U1
for i := 0; i < b.N; i++ {
for j, v := range arr {
arr[j].d = j
_ = v
}
}
}
```


在这个例子中，我们定义了5种结构体：U1~U5，它们的不同之处就在于包含的int类型字段的个数不同。我们分别用经典for loop与for range loop对以这些类型为元素的大型数组进行遍历，看看结果如何：

```
$go test -bench . benchmark3_test.go
goos: darwin
goarch: amd64
cpu: Intel(R) Core(TM) i5-8257U CPU @ 1.40GHz
BenchmarkClassicForLoopLargeStructArrayU5-8 22030 54116 ns/op 0 B/op 0 allocs/op
BenchmarkClassicForLoopLargeStructArrayU4-8 22131 54145 ns/op 0 B/op 0 allocs/op
BenchmarkClassicForLoopLargeStructArrayU3-8 22257 54001 ns/op 0 B/op 0 allocs/op
BenchmarkClassicForLoopLargeStructArrayU2-8 22063 54580 ns/op 0 B/op 0 allocs/op
BenchmarkClassicForLoopLargeStructArrayU1-8 22105 54408 ns/op 0 B/op 0 allocs/op
BenchmarkForRangeLargeStructArrayU5-8 3022 391232 ns/op 0 B/op 0 allocs/op
BenchmarkForRangeLargeStructArrayU4-8 4563 265919 ns/op 0 B/op 0 allocs/op
BenchmarkForRangeLargeStructArrayU3-8 6602 182224 ns/op 0 B/op 0 allocs/op
BenchmarkForRangeLargeStructArrayU2-8 10000 111966 ns/op 0 B/op 0 allocs/op
BenchmarkForRangeLargeStructArrayU1-8 35380 34005 ns/op 0 B/op 0 allocs/op
PASS
ok command-line-arguments 15.907s
```


我们看到一个奇怪的现象：无论是哪种结构体类型，经典for loop遍历的性能都是一样的，但**for range的遍历性能却会随着结构体字段数量的增多而下降**。

带着疑惑，我找到了与这个问题有关的一个issue：[cmd/compile: optimize large structs](https://github.com/golang/go/issues/24416)，这个issue大致是说对于包含特定数量字段的结构体类型，目前是**unSSAable**，如果不能SSA，那么就无法通过SSA优化，这也是出现上述benchmark结果的重要原因。

在Go中，几乎所有使用数组的地方都可以用切片替代，笔者还是建议**尽量用迭代切片替换对数组的迭代**，这样总是可以取得一致且稳定的遍历性能。

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


![img{512x368}](../../assets/617100c3677e1846.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论