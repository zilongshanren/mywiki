---
title: 为什么有了Go module后“依赖地狱”问题依然存在
url: https://tonybai.com/2022/03/12/dependency-hell-in-go/
published: '2022-03-12'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 为什么有了Go module后“依赖地狱”问题依然存在

![](../../assets/2a8cb0755148ad9e.png)


[本文永久链接](https://tonybai.com/2022/03/12/dependency-hell-in-go) – https://tonybai.com/2022/03/12/dependency-hell-in-go

如果所有Gopher都抛弃GOPATH构建模式，拥抱Go module构建模式；如果所有legacy Go package作者都能为自己的legacy package加上go.mod；如果所有Go module作者都严格遵守[语义版本(semver)规范](https://semver.org)，那么Go将彻底解决[“依赖地狱”问题](https://en.wikipedia.org/wiki/Dependency_hell)。

但现实却没那么乐观！**Go中的“依赖地狱问题”依然存在**。这一篇我们就来聊聊Go中依赖地狱的“发作场景”、原因以及解决方法。

### 1. 什么是“依赖地狱(dependency hell)”？

“依赖地狱”问题不是某种编程语言独有的问题，而是**一个在软件开发和发布领域广泛存在问题**。[维基百科](https://en.wikipedia.org/wiki/Dependency_hell)对该问题的广义诠释是这样的：

当几个软件包对相同的

[共享包或库]有依赖性，但它们依赖于不同的、不兼容的共享包版本时，就会出现依赖性问题。如果共享包或库只能安装一个版本，用户可能需要通过获得较新或较旧版本的依赖包来解决这个问题。反过来，这可能会破坏其他的依赖关系。

在软件开发构建领域，我们会面对同样的“依赖地狱”问题。文字总是很难懂，我们用更为直观的示意图来说明什么是软件构建过程中的“依赖地狱”问题，大家先看看下面这个示意图：

![](../../assets/e125bc2ad5bb0802.png)


我们看到在这幅图中：包P1依赖包P3 V1.5版本，包P2依赖包P3 V2.0版本，App同时依赖包P1和包P2。于是问题出现了：构建工具在构建App这个应用时需要决策究竟要使用包P3的哪个版本：V1.5还是V2.0？当然这个问题存在的一个前提是：**App中只允许包含包P3的一个版本**。

如果P3的V1.5与V2.0版本是不兼容的版本，那么构建工具无论选择包P3的哪个版本，App的构建都会以失败告终。开发人员只能介入手工解决，解决方法无非是将P1对P3的依赖升级到V2.0，或将P2对P3的依赖降级为V1.5版本。但P1、P2多数情况下是第三方开源包，App的开发人员对P1、P2包的作者的影响力有限，因此这种手工解决的成功率也不高。

“依赖地狱”(又称为[“钻石依赖”问题](https://research.swtch.com/vgo-import#dependency_story))由来已久，几十年来各种编程语言都在努力解决这一问题，并也有了几种可以帮助到开发者的不错的方案。我们先来看看Go语言的解决方案。

### 2. Go的解决方案

在GOPATH构建模式时代，Go构建工具是无法自动解决上述“依赖地狱”问题的。[Go 1.11版本引入Go module构建模式](https://tonybai.com/2018/11/19/some-changes-in-go-1-11)后，经过几年的打磨，Go module构建模式逐渐成熟，并已经成为Go构建模式的标准。

Go module构建模式是可以部分解决上述“依赖地狱”问题的。Go module解决这个问题的思路是：**语义导入版本(sematic import versioning)**，**即在包的导入路径上加上包的major version前缀**。关于[“语义导入版本”的详细介绍](https://time.geekbang.org/column/article/429941)，可以参考我的极客时间专栏[“Go语言第一课”](http://gk.link/a/10AVZ)的相关内容。

使用“语义导入版本”后，Go解决上面那个问题的方案如下图：

![](../../assets/882a2a6ab897754f.png)


我们看到：Go通过打破“App中只允许包含包P3的一个版本”这个前提实现了P1和P2各自使用自己依赖的版本。但这样做的前提是P1和P2依赖的P3版本的major版本号是不同的。在Go中，由于采用语义导入版本机制，major版本号不同的module被视为不同的module，即使它们源于同一个repository(比如上面的源于同一个P3的v1.5和v2.0就被视为两个不同的module)。

当然这种解决方案是有代价的！第一个代价就是构建出来的app的二进制文件size变大了，因为二进制文件中包含了多个版本的P3的代码；第二个代价，可能也算不上代价，更多是要注意的是不同版本的module之间的类型、变量、标识符不能混用，我们以[go-redis/redis](https://github.com/go-redis/redis)这个开源项目举个例子。go-redis/redis最新大版本为v8.11.4，没有启用go.mod时的版本为v6.x.x，我们将这两个版本混用在一起：

```
package main
import (
"context"
"github.com/go-redis/redis"
redis8 "github.com/go-redis/redis/v8"
)
func main() {
var rdb *redis8.Client
rdb = redis.NewClient(&redis.Options{
Addr: "localhost:6379",
Password: "", // no password set
DB: 0, // use default DB
})
_ = rdb
}
```


Go编译器在编译这段代码时会报如下错误：

```
cannot use redis.NewClient(&redis.Options{…}) (value of type *"github.com/go-redis/redis".Client) as type *"github.com/go-redis/redis/v8".Client in assignment
```


即redis v8下的Client与redis Client并非一个类型，即使它们的内部字段相同，也不能混用在一起。

那么，是不是说有了Go module构建机制后，“依赖地狱”问题就彻底从Go开发中被移除了呢？不是的。“依赖地狱”问题依旧存在，下面我们就来看看哪些情况下还会出现此类问题。

### 3. 哪些情形下“依赖地狱”依旧存在

#### 1) 依赖不带go.mod的legacy Go包

如今Go语言引入Go module已经多年了，但Go社区仍然存在大量legacy的Go包尚未增加go.mod文件。对于这样的go包，Go命令的处理策略大致是这样的：

- 对于尚未打tag的go包，那么就按等同于v0/v1的方式处理

go命令将go包缓存在本地mod cache时，会合成一个go.mod文件，比如：

```
// $GOMODCACHE/cache/download
go.starlark.net
└── @v
├── list
├── list.lock
├── v0.0.0-20190702223751-32f345186213.mod // 这里是合成的go.mod
├── v0.0.0-20200821142938-949cc6f4b097.info
├── v0.0.0-20200821142938-949cc6f4b097.lock
├── v0.0.0-20200821142938-949cc6f4b097.mod // 这里是合成的go.mod
├── v0.0.0-20200821142938-949cc6f4b097.zip
├── v0.0.0-20200821142938-949cc6f4b097.ziphash
├── v0.0.0-20210901212718-87f333178d59.info
└── v0.0.0-20210901212718-87f333178d59.mod // 这里是合成的go.mod
```


- 对于已经打了tag的go包且tag的major版本号<2，那么也按等同于v0/v1的方式处理

go命令将这样的go包缓存在本地mod cache时，同样会合成一个go.mod文件，比如：

```
// $GOMODCACHE/cache/download
pierrec
|-- lz4
| |-- @v
| | |-- list
| | |-- v1.0.1.info
| | |-- v1.0.1.lock
| | |-- v1.0.1.mod // 这里是合成的go.mod
| | |-- v1.0.1.zip
| | |-- v1.0.1.ziphash
```


- 对于打了tag且tag的major版本号>=2的，Go命令将包下载到mod cache中后，同样会为该go包合成一个go.mod文件，该文件名vX.Y.Z+incompatible.mod，比如下面这个例子：

```
// $GOMODCACHE/cache/download
pierrec
|-- lz4
| |-- @v
| | |-- list
| | |-- v2.6.1+incompatible.info
| | |-- v2.6.1+incompatible.lock
| | |-- v2.6.1+incompatible.mod // 这里是合成的go.mod
| | |-- v2.6.1+incompatible.zip
| | `-- v2.6.1+incompatible.ziphash
```


以上三种情况下，合成的.mod文件中的module root path都是不带vN后缀的，无论是否打tag，也不论tag major版本是否>=2，以v2.6.1+incompatible.mod为例，其内容如下：

```
// v2.6.1+incompatible.mod
module github.com/pierrec/lz4
```


我们看到，该合成的mod文件中也**不包含这个legacy包自身所依赖的第三方包的require代码块**。那么依赖lz4这个legacy包的项目如何确定lz4的第三方依赖的版本呢？并且lz4依赖的第三方包的版本记录在哪里呢？我们以app依赖github.com/pierrec/lz4为例，看下面示意图：

![](../../assets/cbab55a6850e9e8d.png)


go mod命令在做依赖分析时，会根据源码中的import github.com/pierrec/lz4确定lz4的版本，由于没有vN后缀，go命令会找lz4的v2以下的源码中的go.mod，但lz4在这之前都没有添加go.mod，于是只能按照legacy的模式去确定lz4的版本，这里确定的是v2.6.1+incompatible，go命令将其作为app module的直接依赖：

```
require github.com/pierrec/lz4 v2.6.1+incompatible
```


之后go命令还会对lz4的依赖做分析，并将其记录到app module的go.mod中，作为indirect依赖：

```
require github.com/frankban/quicktest v1.14.2 //indirect
```


将直接依赖的legacy包的第三方依赖记录在自己的go.mod中是为了满足基于go.mod的**可重现构建的要求**。

好了！我们了解了go命令处理legacy go包的方式，再来看看如果出现“钻石依赖”情况下，Go命令是如何处理的？直接给结论，如下图：

![](../../assets/ea25ed250c47df3e.png)


在这幅图中，我们让P1依赖lz4的v1.0.1版本，让P2依赖lz4的v2.6.1+incompatible版本，这两个版本都是legacy（未添加go.mod）下打的tag。那么当app既依赖P1又依赖P2时，go命令会如何选择lz4的版本呢？Go命令简单粗暴的选择了同时满足P1和P2的最小版本：v2.6.1+incompatible。这里Go似乎做了一个假设：**legacy包的新版本一定是向前兼容老版本的**。对于lz4这个包来说，这个假设是正确的，我们对App的构建与执行不会遇到问题。

但是**一旦这个假设不成立，比如：lz4的v2.6.1是一个不兼容v1.0.1的发布，那么App的构建将遇到错误**。这种情况go命令是无能为力了，只能进行手工干预！那怎么干预呢？无非以下几种手段：

- 提issue督促P1作者将对lz4的依赖升级到最新v2.6.1版本

这种手段效率低不说，很可能P1的author根本就不会搭理你。

- fork一个P1，自己修改，然后让App依赖你fork后的P1

这种手段可行，但后续就要自己维护一个fork的P1，无形中给自己增加了额外的负担。

- vendor下来，自己修改，在vendor目录下维护

这种手段也可行，但后续只能使用vendor模式构建，且要自己维护一个本地的P1，同样也给自己增加了额外的负担。

那就没有更好的方法了么？真没有！从legacy项目到拥抱go module的项目的过渡过程注定是坎坷的。

#### 2) 采用go module机制的依赖包的冲突问题

看完legacy包后，我们再来看依赖是采用go module机制的包的冲突问题。有了对上面例子理解的基础，理解下面的例子的就更容易了，我们来看下面示意图：

![](../../assets/99c2ac3cc0dac3ed.png)


这个例子也很简单，P1和P2都依赖module P3，分别依赖P3的v1.1.0版本和v1.2.0版本，和之前的例子一样，App既依赖P1，也依赖P2，这样就构成了图中右侧的“钻石结构”。不过，Go module的另外一个机制：最小版本选择(MVS)可以很好的解决这个依赖问题，关于MVS的详情，同样可以参考我的极客时间专栏[“Go语言第一课”](http://gk.link/a/10AVZ)的相关内容。

MVS机制同样是基于语义版本之上的，它会选择满足此App依赖的最小可用版本，这里P3的v1.1.0版本与v1.2.0版本的major版本号相同，因此按照语义版本规范，他们是兼容的版本，于是go命令选择了满足app依赖的最小可用版本为v1.2.0(此时P3的最高版本为v1.7.0，Go命令没有选择最高版本)。

不过**理论约定与实际常常脱节**，一旦P3的author在发布v1.2.0时没有识别出与v1.1.0的不兼容change，那么这种情况下，**不兼容v1.1.0的P3版本会导致对P1包的构建失败**！这就是采用go module机制的依赖包时最常见的“依赖地狱”问题。

可以看到，这个问题的根源还是在于go module的author。识别不兼容的change难吗？也不难，但的确繁琐，费脑子。那么作为module author, 如何尽量避免未按照语义版本规范发布版本号兼容实则不兼容的module版本呢？

Go社区的作法分为两类：

- 极端作法：
- 不发布1.0版本，一直在0.x.y，不承诺新版本兼容老版本；
- 每次发稍大一些的版本都升级major版本号，这样既避免了繁琐的检查是否有不兼容change的问题，也肯定不会给社区带去“依赖地狱”问题。

- 常规作法：
- 检查是否有不兼容change，只有在存在不兼容change的情况下，才升级major版本。


Go官博曾经发表过一篇名为[《Keeping Your Modules Compatible》](https://go.dev/blog/module-compatibility)的文章，以告诉大家如何检查新的change中是否有不兼容的change。文中还提到Go团队已经开发了一个名为[gorelease的工具](https://github.com/golang/exp/tree/master/cmd/gorelease)来帮助Go开发者检测新版本与旧版本之间是否存在不兼容的变化(当然，工具也很可能不能完全扫描出来不兼容性change)，大家可以在[这里查看gorelease的详细用法](https://pkg.go.dev/golang.org/x/exp@v0.0.0-20220307200941-a1099baf94bf/cmd/gorelease)。

### 4. 未来畅想

近几年成长时候也很迅猛的Rust语言在面对“依赖地狱”这一问题上似乎走到了Go的前面，在[《How Rust Solved Dependency Hell》](https://stephencoakley.com/2019/04/24/how-rust-solved-dependency-hell)一文中大致讲解了Rust解决这一问题的方案。其原理大致是利用的**名字修饰**，即同一个依赖的两个不兼容的版本可以共存与一个Rust应用中，每个版本中的标识符在应用中都是独一无二的，Rust通过包名、版本号等作为名字修饰以达到此目的。

那么，未来Go module是否能做到这点呢？笔者认为是可行的，并且是兼容于现在go module的机制的。Go module的引入，实则也是一种“namespace”的概念，具备像Rust那样解决问题的基础。但Go团队是否要这么做就是另当别论了，因为一旦Go语言世界像本文开篇中所提到的那样，那么现有机制也可以很好地解决“依赖地狱”问题。

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

“不发布1.0版本，一直在0.x.y，不承诺新版本兼容老版本；”这不就是k8s社区的做法么，所以rsc搞的go mod甚至无法说服同一个公司的其他产品

k8s的东西太复杂庞大，而且有历史遗留问题。这也是k8s之前提供的一些go包体验不佳的原因。