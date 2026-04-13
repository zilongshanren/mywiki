---
title: 一文搞懂Go语言中的切片排序
url: https://tonybai.com/2020/11/26/slice-sort-in-go/
published: '2020-11-26'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 一文搞懂Go语言中的切片排序

![img{512x368}](../../assets/fd88db02f0c5a08d.png)


**切片**是Go语言中引入的用于在大多数场合替代数组的语法元素。切片是长度可变的同类型元素序列，它不支持存储不同类型的元素，当然如果你非用**sl := []interface{}{“hello”, 11, 3.14}**来抬杠^_^，那就另当别论。

**有序列的地方就有排序的需求**。在[各种排序算法都已经成熟](https://book.douban.com/subject/10432347/)的今天，我们完全可以针对特定元素类型的切片**手写排序函数/方法**，但多数情况下不推荐这么做，因为Go标准库内置了**sort**包可以很好地帮助我们实现**原生类型元素切片**以及**自定义类型元素切片**的排序任务。

### 1. sort包的排序原理

截至目前([Go 1.15版本](https://mp.weixin.qq.com/s/B5onfyP7BPYCh_rMSBtfcQ))，Go还不支持[泛型](https://mp.weixin.qq.com/s/SMT40557JgQ9FjUkswznlA)。因此，为了支持**任意元素类型**的切片的排序，标准库sort包定义了一个Interface接口和一个接受该接口类型参数的Sort函数：

```
// $GOROOT/src/sort/sort.go
type Interface interface {
Len() int
Less(i, j int) bool
Swap(i, j int)
}
func Sort(data Interface) {
n := data.Len()
quickSort(data, 0, n, maxDepth(n))
}
```


为了应用这个排序函数Sort，我们需要让被排序的切片类型实现**sort.Interface**接口，以整型切片为例：

```
// slice-sort-in-go/sort_int_slice.go
type IntSlice []int
func (p IntSlice) Len() int { return len(p) }
func (p IntSlice) Less(i, j int) bool { return p[i] < p[j] }
func (p IntSlice) Swap(i, j int) { p[i], p[j] = p[j], p[i] }
func main() {
sl := IntSlice([]int{89, 14, 8, 9, 17, 56, 95, 3})
fmt.Println(sl) // [89 14 8 9 17 56 95 3]
sort.Sort(sl)
fmt.Println(sl) // [3 8 9 14 17 56 89 95]
}
```


从sort.Sort函数的实现来看，它使用的是快速排序(quickSort)。我们知道快速排序是在所有数量级为(o(nlogn))的排序算法中其平均性能最好的算法，但在某些情况下其性能却并非最佳，Go sort包中的quickSort函数也没有严格拘泥于仅使用快排算法，而是以快速排序为主，并根据目标状况在特殊条件下选择了其他不同的排序算法，包括堆排序(heapSort)、插入排序(insertionSort)等。

sort.Sort函数不保证排序是稳定的，要想使用稳定排序，需要使用**sort.Stable**函数。

注：稳定排序：假定在待排序的序列中存在多个具有相同值的元素，若经过排序，这些元素的相对次序保持不变，即在原序列中，若r[i]=r[j]且r[i]在r[j]之前，在排序后的序列中，若r[i]仍在r[j]之前，则称这种排序算法是稳定的(stable)；否则称为不稳定的。


### 2. sort包的“语法糖”排序函数

我们看到，直接使用sort.Sort函数对切片进行排序是比较繁琐的。如果仅仅排序一个原生的整型切片都这么繁琐(要实现三个方法），那么sort包是会被“诟病”惨了的。还好，对于以常见原生类型为元素的切片，sort包提供了类“语法糖”的简化函数，比如：sort.Ints、sort.Float64s和sort.Strings等。上述整型切片的排序代码可以直接改造成下面这个样子：

```
// slice-sort-in-go/sort_int_slice_with_sugar.go
func main() {
sl := []int{89, 14, 8, 9, 17, 56, 95, 3}
fmt.Println(sl) // [89 14 8 9 17 56 95 3]
sort.Ints(sl)
fmt.Println(sl) // [3 8 9 14 17 56 89 95]
}
```


原生类型有“语法糖”可用了，那么对于自定义类型作为元素的切片，是不是每次都得实现Interface接口的三个方法呢？Go团队也想到了这个问题! 所以在[Go 1.8版本](http://mp.weixin.qq.com/s?__biz=MzIyNzM0MDk0Mg==&mid=100000073&idx=1&sn=6800e30bb370d739cfcd9528dc41f37c&chksm=6863e6a85f146fbe8affff789f91ba5c6b2bb1bbf5092d3d4f089dea26cea0384a1a10c5582b#rd)中加入了**sort.Slice**函数，我们只需传入一个比较函数实现即可：

```
// slice-sort-in-go/custom-type-slice-sort-in-go.go
type Lang struct {
Name string
Rank int
}
func main() {
langs := []Lang{
{"rust", 2},
{"go", 1},
{"swift", 3},
}
sort.Slice(langs, func(i, j int) bool { return langs[i].Rank < langs[j].Rank })
fmt.Printf("%v\n", langs) // [{go 1} {rust 2} {swift 3}]
}
```


同理，如果要进行稳定排序，则用sort.SliceStable替换上面的sort.Slice。

### 3. 引入泛型后的切片排序

[Russ Cox已经确认了Go泛型(type parameter)将在Go 1.18版本](https://mp.weixin.qq.com/s/SMT40557JgQ9FjUkswznlA)落地，我们来展望一下在2022年2月Go泛型落地后，切片排序该怎么做。好在现在有https://go2goplay.golang.org/可以用于试验go泛型技术草案中的语法。

在泛型加入后，我们可以按如下方式对原生类型切片进行排序：

```
// https://go2goplay.golang.org/p/lKG3saE-1ek
package main
import (
"fmt"
"sort"
)
type Ordered interface {
type int, int8, int16, int32, int64, uint, uint8, uint16, uint32, uint64, uintptr, float32, float64, string
}
type orderedSlice[T Ordered] []T
func (s orderedSlice[T]) Len() int { return len(s) }
func (s orderedSlice[T]) Less(i, j int) bool { return s[i] < s[j] }
func (s orderedSlice[T]) Swap(i, j int) { s[i], s[j] = s[j], s[i] }
func OrderedSlice[T Ordered](s []T) {
sort.Sort(orderedSlice[T](s))
}
func main() {
s1 := []int32{3, 5, 2}
fmt.Println(s1) // [3 5 2]
OrderedSlice(s1)
fmt.Println(s1) // [2 3 5]
s2 := []string{"jim", "amy", "tom"}
fmt.Println(s2) // [jim amy tom]
OrderedSlice(s2)
fmt.Println(s2) // [amy jim tom]
}
```


上面的Ordered接口类型、orderedSlice[T]切片类型以及OrderdSlice函数都可能会内置到sort包中，我们直接使用sort.OrderSlice函数即可对原生类型元素切片进行排序。

而对于自定义类型，如果我们将其加入到Ordered接口的类型列表(type list)中，像下面这样：

```
type Lang struct {
Name string
Rank int
}
type Ordered interface {
type int, int8, int16, int32, int64, uint, uint8, uint16, uint32, uint64, uintptr, float32, float64, string
}
```


那么，当我们像下面代码这样对元素类型为Lang的切片langs进行排序时，我们会遇到编译错误：

```
func main() {
langs := []Lang{
{"rust", 2},
{"go", 1},
{"swift", 3},
}
OrderedSlice(langs)
fmt.Println(langs)
}
$prog.go2:20:55: cannot compare s[i] < s[j] (operator < not defined for T)
```


由于Lang类型不支持<和>比较，因此我们无法将Lang类型放入Ordered的类型列表中。而根本原因在于Go语言不支持运算符重载，这样我们永远无法让自定义类型支持<和>比较，我们只能另辟蹊径，采用sort.Slice的思路：额外提供一个比较函数！

```
// https://go2goplay.golang.org/p/7K94ZJuaoDc
package main
import (
"fmt"
"sort"
)
type Lang struct {
Name string
Rank int
}
type sliceFn[T any] struct {
s []T
cmp func(T, T) bool
}
func (s sliceFn[T]) Len() int { return len(s.s) }
func (s sliceFn[T]) Less(i, j int) bool { return s.cmp(s.s[i], s.s[j]) }
func (s sliceFn[T]) Swap(i, j int) { s.s[i], s.s[j] = s.s[j], s.s[i] }
func SliceFn[T any](s []T, cmp func(T, T) bool) {
sort.Sort(sliceFn[T]{s, cmp})
}
func main() {
langs := []Lang{
{"rust", 2},
{"go", 1},
{"swift", 3},
}
SliceFn(langs, func(p1, p2 Lang) bool { return p1.Rank < p2.Rank })
fmt.Println(langs) // [{go 1} {rust 2} {swift 3}]
}
```


有人说，SliceFn和非泛型版本的sort.Slice在使用时复杂度似乎也没啥差别啊。**形式上的确如此，但内涵上还是有差别的**。

使用泛型方案， 由于少了到interface{}的装箱和拆箱操作，理论上SliceFn的性能要好于sort.Slice函数。根据[Go语言之父Robert Griesemer对Go泛型的讲解](https://mp.weixin.qq.com/s/SMT40557JgQ9FjUkswznlA)：

```
SliceFn(langs,...)
```


等价于下面过程：

```
sliceFnForLang := SliceFn(Lang) // 编译阶段，sliceFnForLang的函数原型为func(s []Lang, func(Lang, Lang) bool)；
sliceFnForLang(langs) // 运行阶段，和普通函数调用无异，但没有了到interface{}类型装箱和拆箱的损耗。
```


注：本文涉及的源码可以在

[这里]https://github.com/bigwhite/experiments/tree/master/slice-sort-in-go 下载到。

### 延伸阅读

[Go语言的前世今生](https://www.imooc.com/read/87/article/2320)– https://www.imooc.com/read/87/article/2320[Go语言的设计哲学之一：简单](https://www.imooc.com/read/87/article/2321)– https://www.imooc.com/read/87/article/2321[Go语言的设计哲学之二：组合](https://www.imooc.com/read/87/article/2322)– https://www.imooc.com/read/87/article/2322[Go语言的设计哲学之三：并发](https://www.imooc.com/read/87/article/2340)– https://www.imooc.com/read/87/article/2340

**“Gopher部落”知识星球开球了！**高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！星球首开，福利自然是少不了的！2020年年底之前，8.8折(很吉利吧^_^)加入星球，下方图片扫起来吧！

![](http://image.tonybai.com/img/202011/gopher-tribe-zsxq.png)


我的Go技术专栏：“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”上线了，欢迎大家订阅学习！

![img{512x368}](../../assets/018ff45f7e150fca.png)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线>了，感谢小伙伴们学习支持！

![img{512x368}](../../assets/e9f90df4cc2580e5.png)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2020, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论