---
title: Go语言map类型变量背后的那些事儿
url: https://tonybai.com/2022/03/15/the-underlying-of-a-map-type-variable/
published: '2022-03-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go语言map类型变量背后的那些事儿

![](../../assets/25b491e067d121e6.png)


[本文永久链接](https://tonybai.com/2022/03/15/the-underlying-of-a-map-type-variable) – https://tonybai.com/2022/03/15/the-underlying-of-a-map-type-variable

切片(slice)和map是Go语言中最常用的两种原生复合数据类型，同时也是最容易使初学者感觉迷惑和“掉坑”的两个类型，这很大程度是因为Go runtime层的存在。什么是Go runtime层？可以参考我在[《Go语言第一课FAQ》](https://tonybai.com/go-course-faq)中的解释。

我们在Go用户源码层看到的切片与map是这样的：

```
var sl = make([]int, 3)
var m = make(map[string]int)
```


但在runtime层，它们又是另一幅“样子”。Go用户源码层的切片和map类型的变量，我常将它们称为**“描述符”**，因为它们和linux平台上通过open系统调用打开的文件描述符的功用十分类似，都是某个大块头儿数据(比如：一个500M的文本数据)的“代言人”，避免了和外界交互时对底层数据的搬动与拷贝。

![](../../assets/e1e300853f235514.png)


很多人知道，在runtime层，切片是一个**三元组**结构（在我的[“Go语言第一课”专栏](http://gk.link/a/10AVZ)中有单独一讲详细讲解），这里假定这个三元组结构为T，那么上面例子中通过make创建的切片m是类型T的实例还是*T的实例呢？很多人都知道答案：**类型T的实例**。

同样看过我的[专栏](http://gk.link/a/10AVZ)或[《Go语言精进之路》](https://tonybai.com/2022/01/15/go-programming-from-beginners-to-masters-is-published)一书的读者也都知道：map类型在runtime层的表示为**runtime.hmap**，那么，上面通过make创建的map[string]int类型变量m究竟就是hmap类型实例还是*hmap类型实例呢？可能有些朋友还不明确，这里我们就来简单探究一下。

注：探究方法同样适用于切片类型。


m是hmap类型实例还是*hmap类型实例呢？最直接的方法是**看runtime包的源码**。在runtime/map.go中，我们找到了对应make(map[string]int)的源码makemap(或makemap_small)：

```
func makemap(t *maptype, hint int, h *hmap) *hmap
func makemap_small() *hmap
```


我们看到：无论哪个函数返回的都是*hmap类型。到这里你的心里似乎有点倾向了，应该是*hmap。但还不那么确认。

我们假设m是*hmap，那么根据Go指针类型的定义(关于Go指针，我在[专栏《聊聊Go语言中的指针》](http://gk.link/a/10AVZ)一讲中有较为全面讲解)，Go为变量m分配的内存块中存储的值就应该是一个hmap实例的地址：

![](../../assets/389c9447f9d17660.png)


也就是说给m分配一块可以存储指针值的内存块儿即可。这样我们就可以**通过相邻变量间的地址间隔来判定m是否仅仅是一个指针大小的内存块了**。我们看下面例子：

```
package main
func main() {
var a int = 5
println("&a=", &a)
var m1 = make(map[string]int)
println("&m1=", &m1)
var m2 = make(map[string]int)
println("&m2=", &m2)
}
```


运行这个程序，输出结果如下：

```
&a= 0xc000046558
&m1= 0xc000046568
&m2= 0xc000046560
```


由于这些变量都分配在栈上(通过go build -gcflags ‘-m’可判断是否逃逸)，我们用一幅图来展示一下上面示例中各个变量的内存块排列情况：

![](../../assets/a959cb29cfd570d2.png)


从m1与m2两个map类型变量的地址间隔情况来看，间隔8个字节，也就是一个指针大小，基本可以断定m2是指针类型实例了。

那么m是否是*hmap类型实例呢？如果是，我们是否可以通过对m的“解引用”得到该实例的值呢？我们下面试一下。

由于hmap是runtime包的非导出类型，所以我们无法在用户层直接使用，考虑到hmap都是由一些基本类型字段组成并且与runtime包的其他类型关联不多，我这里直接将其相关源码copy到示例源码中备用了。

```
package main
import (
"fmt"
"runtime"
"unsafe"
)
type hmap struct {
count int // # live cells == size of map. Must be first (used by len() builtin)
flags uint8
B uint8 // log_2 of # of buckets (can hold up to loadFactor * 2^B items)
noverflow uint16 // approximate number of overflow buckets; see incrnoverflow for details
hash0 uint32 // hash seed
buckets unsafe.Pointer // array of 2^B Buckets. may be nil if count==0.
oldbuckets unsafe.Pointer // previous bucket array of half the size, non-nil only when growing
nevacuate uintptr // progress counter for evacuation (buckets less than this have been evacuated)
extra *mapextra // optional fields
}
// mapextra holds fields that are not present on all maps.
type mapextra struct {
overflow *[]*bmap
oldoverflow *[]*bmap
nextOverflow *bmap
}
// A bucket for a Go map.
type bmap struct {
tophash [bucketCnt]uint8
}
const (
// Maximum number of key/elem pairs a bucket can hold.
bucketCntBits = 3
bucketCnt = 1 << bucketCntBits
)
func main() {
m := make(map[string]int)
m["tony"] = 11
m["bai"] = 12
p := (*hmap)(unsafe.Pointer(*(*uintptr)((unsafe.Pointer)(&m))))
fmt.Printf("%#v\n", *p)
}
```


这个例子中最难理解的就是变量p的声明与赋初值那一行，对于这一行我们分解来讲一下。

首先，前面我们说过：map类型变量m是指针，其存储的是一个hmap类型实例的地址。通过

```
*(*uintptr)((unsafe.Pointer)(&m))
```


我们得到的是m指向的那个hmap类型实例的地址。

然后通过将其转换为*hmap类型，我们就相当于直接得到了一个指向hmap类型实例地址的*hmap类型变量p。通过对p进行解引用，我们就能看到hmap结构体的内容了。运行上面代码我们得到下面输出结果：

```
main.hmap{count:2, flags:0x0, B:0x0, noverflow:0x0, hash0:0x42833520, buckets:(unsafe.Pointer)(0xc000072ea0), oldbuckets:(unsafe.Pointer)(nil), nevacuate:0x0, extra:(*main.mapextra)(nil)}
```


当我们看到输出结果中hmap.count这个字段(表示当前map中存储的键值对的个数)的值为2，我们就可以确定：**m就是一个执行hmap结构体实例的指针**这一结论是正确的。

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