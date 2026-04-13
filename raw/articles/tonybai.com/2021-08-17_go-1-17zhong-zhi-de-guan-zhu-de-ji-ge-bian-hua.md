---
title: Go 1.17中值得关注的几个变化
url: https://tonybai.com/2021/08/17/some-changes-in-go-1-17/
published: '2021-08-17'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.17中值得关注的几个变化

![](../../assets/9467b9fbd04dd5ac.png)


[本文永久链接](https://tonybai.com/2021/08/17/some-changes-in-go-1-17) – https://tonybai.com/2021/08/17/some-changes-in-go-1-17

Go核心开发团队在[去年GopherCon大会上给Go泛型的定调是在2022年2月份的Go 1.18版本中发布](https://mp.weixin.qq.com/s/SMT40557JgQ9FjUkswznlA)，那可是自[Go诞生](https://mp.weixin.qq.com/s/woQeEQUhOLJ7KSE5rm5q6g)以来语法规范变动最大的一次，这让包括笔者在内的全世界的Gopher们都满怀期待。

不过别忘了，在Go 1.18这个“网红版本”发布前，还有一个“实力派”版本Go 1.17呢！美国当地时间2021年8月16日，[Go 1.17版本在经过两个RC版本之后正式发布](https://blog.golang.org/go1.17)！并且值得庆幸的是Go 1.17版本并没有过多受到Go 1.18版本这个“网红”的影响，Go 1.17默默地加入和优化了着实不少的特性。在这一篇文章中，我们就来看看Go 1.17版本中有哪些值得关注的变化。

### 1. 语言特性变化

[Go属于那种极简的语言](https://www.imooc.com/read/87/article/2321)，从诞生到现在语言自身特性变化很小，不会像其他主流语言那样走“你有的我也要有”的特性融合路线。因此新语言特性对于Gopher来说属于“稀缺品”，属于“供不应求”那类事物^_^。这也直接导致了每次Go新版本发布，我们都要首先看看语言特性是否有变更，每个新加入语言的特性都值得我们去投入更多关注，去深入研究。Go 1.17在语言特性层面做了两方面的小改动，下面我们来看看。

第一个是对语言类型转换规则的扩展，允许从切片到数组指针的转换，下面的代码在Go 1.17版本中是可以正常编译和运行的：

```
// github.com/bigwhite/experiments/tree/master/go1.17-examples/lang/slice2arrayptr/main.go
func slice2arrayptr() {
var b = []int{11, 12, 13}
var p = (*[3]int)(b)
p[1] = p[1] + 10
fmt.Printf("%v\n", b) // [11 22 13]
}
```


Go通过运行时对这类切片到数组指针的转换代码做检查，如果发现越界行为，就会通过运行时panic予以处理。Go运行时实施检查的一条原则就是“转换后的数组长度不能大于原切片的长度”，注意这里是切片的长度(len)，而不是切片的容量(cap)。

第二个变动则是unsafe包增加了两个函数：Add与Slice。使用这两个函数可以让开发人员更容易地写出符合[unsafe包使用的安全规则](https://pkg.go.dev/unsafe#Pointer)的代码。这两个函数原型如下：

```
// $GOROOT/src/unsafe.go
func Add(ptr Pointer, len IntegerType) Pointe
func Slice(ptr *ArbitraryType, len IntegerType) []ArbitraryType
```


unsafe.Add允许更安全的指针运算，而unsafe.Slice允许更安全地将底层存储的指针转换为切片。

### 2. go module的变化

自[Go 1.11版本引入go module](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)以来，每个Go大版本发布时，go module都会有不少的积极变化，这是Go核心团队与社区就go module深入互动的结果。

Go 1.17中go module同样有几处显著变化，其中最最重要的一个变化就是pruned module graph（修剪的module依赖图）。Go 1.17之前的版本某个module的依赖图由该module的直接依赖以及所有间接依赖组成，无论某个间接依赖是否真正为原module的构建做出贡献，这样go命令在解决依赖时会读取每个依赖的go.mod，包括那些没有被真正使用到的module，这样形成的module依赖图被称为**完整module依赖图（complete module graph）**。

Go 1.17不再使用“完整module依赖图”，而是引入了pruned module graph（修剪的module依赖图）。修剪的module依赖图就是在完整module依赖图的基础上将那些“占着茅坑不拉屎”、对构建完全没有“贡献”的间接依赖module修剪后的依赖图。使用修剪后的module依赖图进行构建将有助于避免下载或阅读那些不必要的go.mod文件，这样Go命令可以不去获取那些不相关的依赖关系，从而在日常开发中节省时间。

但module依赖图修剪也带来了一个副作用，那就是go.mod文件size的变大。因为Go 1.17版本后，每次go mod tidy（当go.mod中的go版本为1.17时），go命令都会对main module的依赖做一次深度扫描(deepening scan)，并将main module的所有直接和间接依赖都记录在go.mod中（之前说的版本只记录直接依赖）。考虑到内容较多，go 1.17将直接依赖和间接依赖分别放在两个不同的require块儿中。

### 3. 编译器与运行时的变化

Go 1.17增加了对Windows上64位ARM架构的支持，让开发者可以在更多设备上原生运行Go。但这个版本编译器最大的变化是在amd64架构下率先实现了从基于堆栈的调用惯例到[基于寄存器的调用惯例](https://go.googlesource.com/proposal/+/master/design/40724-register-calling.md)的[切换](https://github.com/golang/go/issues/40724)。

并且，切换到[基于寄存器的调用惯例](https://go.googlesource.com/go/+/refs/heads/dev.regabi/src/cmd/compile/internal-abi.md)后，一组有代表性的Go包和程序的基准测试显示，Go程序的运行性能提高了约5%，二进制文件大小典型减少约2%。也就是说你的Go源码使用Go 1.17版本重新编译一下就能获得大约5%的性能提升，真希望这样的优化越多越好！对更多平台的基于寄存器调用惯例的支持将在未来的版本中出现。

除了改为基于寄存器的调用惯例之外，Go 1.17编译器还支持包含[闭包](https://mp.weixin.qq.com/s/bldzzSw-X0YdRcmN3fPhaw)的函数的内联(inline)了！这样一来，一个带有闭包的函数可能会在函数被内联的每个地方产生一个不同的闭包代码指针，因此，

**Go函数的值不能直接比较**！

Go编译器还在Go 1.17中引入了//go:build形式的构建约束指示符，以替代原先易错的// +build形式。

### 4. 其他变化

- 保留龙芯架构GOARCH值

在Go 1.17版本中，Go编译器保留了中国龙芯cpu架构的GOARCH值 – loong64。关于龙心GOARCH值选用loong64还是loongarch64还有过[一段激烈的争论](https://github.com/golang/go/issues/46229)，最终大多数都赞同的loong64取得了最后的胜利。

- Go test变化

Go test引入-shuffle的洗牌标志位，用以控制单元测试或benchmark的执行顺序。

另外T和B两个类型分别都增加了Setenv方法用于在test和benchmark执行期间设置环境变量。

- time包增加Time对象的GoString形式输出

我们使用%#v输出一个Time对象实例时，Go 1.17之前的版本输出内容如下面：

Go 1.16.5输出：

```
time.Time{wall:0xc03f08c0d06c9ed0, ext:83078, loc:(*time.Location)(0x11620e0)}
```


Go 1.17增加了GoString方法，该方法在Time对象以%#v格式输出时被自动调用，其输出结果如下：

```
time.Date(2021, time.August, 17, 20, 29, 42, 58245000, time.Local)
```


### 5. 小结

除上述变化之外，Go的其他标准库随着新版本的发布也都会有大量的小改动，但每个开发人员对标准库的关注点差别很大，因此，在这个系列中不会详细做说明了，大家还是参考[Go 1.17的发布说明文档](https://tip.golang.org/doc/go1.17)各取所需吧^_^。

与传统的“Go新版本值得关注的几个变化”系列有所不同，本期内容较为简单和概括，因为更多内容，我将在后续的**Go 1.17新特性详解系列**中针对上述值得关注的新特性做进一步说明。详解系列已经写好，不过首发在了[本人运营的星球“Gopher部落”](https://t.zsxq.com/bAuvBu3)上了，如果你迫切想深入了解这些新特性，可以加入星球阅读。

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