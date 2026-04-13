---
title: Go 1.17新特性详解：支持将切片转换为数组指针
url: https://tonybai.com/2021/08/18/go-language-specs-changes-in-go-1-17/
published: '2021-08-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.17新特性详解：支持将切片转换为数组指针

![](../../assets/281c50f116ed642d.png)


[本文永久链接](https://tonybai.com/2021/08/18/go-language-specs-changes-in-go-1-17) – https://tonybai.com/2021/08/18/go-language-specs-changes-in-go-1-17

[Go属于那种极简的语言](https://www.imooc.com/read/87/article/2321)，从诞生到现在语言自身特性变化很小，不会像其他主流语言那样走“你有的我也要有”的特性融合路线。因此新语言特性对于Gopher来说属于“稀缺品”，属于“供不应求”那类事物^_^。这也直接导致了每次Go新版本发布，我们都要首先看看语言特性是否有变更，每个新加入语言的特性都值得我们去投入更多关注，去深入研究。下面我们就来深入[Go 1.17版本](https://mp.weixin.qq.com/s/y_pC6GYeZnKuHG8ycNy6rg)中语言规范的一些变化！

### 1. 支持将切片转换为数组指针

在Go 1.17版本之前，我们可以将数组转换为切片，数组将成为转换后的切片底层存储数组，因此，通过切片可以直接改变数组中的元素，就像下面代码这样：

```
// github.com/bigwhite/experiments/tree/master/go1.17-examples/lang/slice2arrayptr/main.go
func array2slice() {
var a = [5]int{11, 12, 13, 14, 15}
var b = a[0:len(a)] // or var b = a[:]
b[1] += 10
fmt.Printf("%v\n", b) // [11 22 13 14 15]
}
```


但反过来则不行，Go不支持将切片再转换回数组类型，编译器会报下面错误信息：

```
// github.com/bigwhite/experiments/tree/master/go1.17-examples/lang/slice2arrayptr/main.go
func slice2array() {
var b = []int{11, 12, 13}
var a = [3]int(b) // cannot convert b (type []int) to type [3]int
fmt.Printf("%v\n", a)
}
```


那么在Go中我们就没法将切片转换为数组了么？也不是绝对的。我们可以通过unsafe包以hack的方式实现这样的转换，如下面代码所示：

```
// github.com/bigwhite/experiments/tree/master/go1.17-examples/lang/slice2arrayptr/main.go
func slice2arrayWithHack() {
var b = []int{11, 12, 13}
var a = *(*[3]int)(unsafe.Pointer(&b[0]))
a[1] += 10
fmt.Printf("%v\n", b) // [11 12 13]
}
```


上面代码中，我们实际上得到是切片底层数组的一份拷贝，修改该拷贝中的元素值，切片中的元素将不会受到影响。如果想通过数组修改切片中元素，我们还得通过获取数组指针的方式，如下面代码所示。

```
// github.com/bigwhite/experiments/tree/master/go1.17-examples/lang/slice2arrayptr/main.go
func slice2arrayptrWithHack() {
var b = []int{11, 12, 13}
var p = (*[3]int)(unsafe.Pointer(&b[0]))
p[1] += 10
fmt.Printf("%v\n", b) // [11 22 13]
}
```


但是使用unsafe，一如其名，其安全性没有编译器和runtime层的保证，只能由开发者自己保证，Gopher在通常情况下应该避免使用。

于是在2009年末，也就是[Go语言宣布开源](https://www.imooc.com/read/87/article/2320)后不久（那时Go 1.0版本尚未发布），[Roger Peppe](https://github.com/rogpeppe)便提出一个issue（那时go的开发还没有如今这么规范，没有proposal流程）：[“spec: use (*[4]int)(x) to convert slice x into array pointer”](https://github.com/golang/go/issues/395)。最初该issue的提出仅仅是因为语法层面缺失了从切片到数组的转换语法，同时希望这种转换以及转换后的数组使用时的下标边界能得到编译器和runtime的协助检查。这个issue得到了当时Go核心开发组成员的支持，Russ Cox还提出将Roger Peppe提议的语法形式做如下变动：

```
从
b := a.[0:4]
变为
b := (*[4]int)(a[0:4])
```


但不知何故，该issue始终没有被纳入Go主干中，直到Go 1.17版本，该issue又被重新提出来了。Go 1.17直接** 支持将切片转换为数组指针**，我们可以在Go 1.17中编写和运行如下面这样的代码，而无需再借助unsafe的hack：

```
// github.com/bigwhite/experiments/tree/master/go1.17-examples/lang/slice2arrayptr/main.go
func slice2arrayptr() {
var b = []int{11, 12, 13}
var p = (*[3]int)(b)
p[1] = p[1] + 10
fmt.Printf("%v\n", b) // [11 22 13]
}
```


Go通过运行时对这类切片到数组指针的转换代码做检查，如果发现越界行为，就会通过运行时panic予以处理。Go运行时实施检查的一条原则就是“转换后的数组长度不能大于原切片的长度”，注意这里是切片的长度(len)，而不是切片的容量(cap)，于是下面的转换有些合法，有些非法：

```
// github.com/bigwhite/experiments/tree/master/go1.17-examples/lang/slice2arrayptr/main.go
var b = []int{11, 12, 13}
var p = (*[4]int)(b) // cannot convert slice with length 3 to pointer to array with length 4
var p = (*[0]int)(b) // ok，*p = []
var p = (*[1]int)(b) // ok，*p = [11]
var p = (*[2]int)(b) // ok，*p = [11, 12]
var p = (*[3]int)(b) // ok，*p = [11, 12, 13]
var p = (*[3]int)(b[:1]) // cannot convert slice with length 1 to pointer to array with length 3
```


关于这个语言特性的应用场合，目前还待Go社区挖掘，不过已经有人提出提出[利用该特性优化go编译器的可行性评估](https://github.com/golang/go/issues/46529)了。

### 2. unsafe包新增了两个“语法糖”函数

Go 1.17中增加了两个“语法糖”函数：[Add](https://github.com/golang/go/issues/40481)和[Slice](https://github.com/golang/go/issues/19367)。这两个函数原型如下：

```
// $GOROOT/src/unsafe.go
func Add(ptr Pointer, len IntegerType) Pointe
func Slice(ptr *ArbitraryType, len IntegerType) []ArbitraryType
```


之所以这两个函数能进入unsafe包，和其他已经存在于unsafe包中的函数的目的是一样的，那就是将Go开发人员一些经常使用的“代码片段模式”升级为unsafe包内置的函数，这样不仅可以降低开发人员误用的比例，还可以让Go runtime提供一些检查，增加类型安全性。

#### unsafe.Add函数

由于go原生不允许指针加减操作，因此我们在特定场景下不得不使用unsafe包来做指针加减，比如下面代码：

```
// github.com/bigwhite/experiments/tree/master/go1.17-examples/lang/unsafe/add/main.go
const intLen = unsafe.Sizeof(int(8))
func foo() {
var a = [5]int{11, 12, 13, 14, 15}
for i := 0; i < 5; i++ {
p := (*int)(unsafe.Pointer(uintptr(unsafe.Pointer(&a[0])) + uintptr(uintptr(i)*intLen)))
*p = *p + 10
}
fmt.Println(a)// [21 22 23 24 25]
}
```


上面代码中间变量p声明同时赋值那行是在Go 1.17之前unsafe包最常见的一种用法和代码模式。大家都这么用，但用起来还那么繁琐，于是便有了unsafe.Add。如果用unsafe.Add改造上面代码，便能简略一些，如下面代码所示：

```
// github.com/bigwhite/experiments/tree/master/go1.17-examples/lang/unsafe/add/main.go
const intLen = unsafe.Sizeof(int(8))
func bar() {
var a = [5]int{11, 12, 13, 14, 15}
for i := 0; i < 5; i++ {
p := (*int)(unsafe.Add(unsafe.Pointer(&a[0]), uintptr(i)*intLen))
*p = *p + 10
}
fmt.Println(a)
}
```


本质上unsafe.Add(ptr, len) 就等价于unsafe.Pointer(uintptr(ptr) + uintptr(len))。在之前版本中，runtime的stubs.go中也有个类似的实现：

```
$GOROOT/src/runtime/stubs.go
// Should be a built-in for unsafe.Pointer?
//go:nosplit
func add(p unsafe.Pointer, x uintptr) unsafe.Pointer {
return unsafe.Pointer(uintptr(p) + x)
}
```


Go 1.17有了这个Add函数后，建议大家就多多使用该函数，而尽量不要自己去拼那个“大长串”了。

#### unsafe.Slice函数

unsafe.Slice函数支持基于一个数组创建一个切片，该数组将作为切片的底层存储，它也可以理解为等价于下面常用“代码片段”语法糖函数：

```
func Slice(ptr *ArbitraryType, len IntegerType) []ArbitraryType
<=>
(*[len]ArbitraryType)(unsafe.Pointer(ptr))[:]
```


下面是unsafe.Slice的一个应用例子：

```
// github.com/bigwhite/experiments/tree/master/go1.17-examples/lang/unsafe/slice/main.go
func main() {
var a = [5]int{11, 12, 13, 14, 15}
s1 := a[:]
s2 := unsafe.Slice(&a[0], 5)
fmt.Println(s1) // [11 12 13 14 15]
fmt.Println(s2) // [11 12 13 14 15]
fmt.Printf("the type of s2 is %T\n", s2)
s2[2] += 10
fmt.Println(a) // [11 12 23 14 15]
fmt.Println(s1) // [11 12 23 14 15]
fmt.Println(s2) // [11 12 23 14 15]
}
```


我们看到基于unsafe.Slice与基于数组进行切片得到的两个切片一样的，它们的底层数组都是数组a。因此，无论通过修改哪个切片元素，都会反映到另外一个切片中并反映到底层数组上。

### 3. 小结

在本文中，我们了解到了Go 1.17新增的很少的语言特性，这些个性更多从语言的易用性、安全性等方面考虑才添加的，相较于以往版本，这些新增特性算是不少了。如果要期待语言特性的巨大变更，那还是一起等Go 1.18吧。Go 1.18保证让你爽歪歪。泛型(类型参数)的加入必然让go代码变得比以前更烧脑一些。

本文涉及代码可以在[这里](https://github.com/bigwhite/experiments/tree/master/go1.17-examples/lang)下载：https://github.com/bigwhite/experiments/tree/master/go1.17-examples/lang

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