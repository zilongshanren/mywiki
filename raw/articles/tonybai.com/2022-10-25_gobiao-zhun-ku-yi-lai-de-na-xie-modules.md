---
title: Go标准库依赖的那些modules
url: https://tonybai.com/2022/10/25/the-modules-that-go-standard-library-depend-on/
published: '2022-10-25'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go标准库依赖的那些modules

![](../../assets/38566bff1666ae28.png)


[本文永久链接](https://tonybai.com/2022/10/25/the-modules-that-go-standard-library-depend-on) – https://tonybai.com/2022/10/25/the-modules-that-go-standard-library-depend-on

对于程序员来说，编写的代码依赖标准库是“天经地义”的事情。标准库在程序员眼中就是高质量的代名词，也是最值得信赖的非自己所写的代码，当然更是代码包依赖关系链条上的最后一环，即所有直接或间接依赖的第三方module最终都会依赖标准库。

前两天组内[学习rust](https://tonybai.com/2021/03/15/rust-vs-go-why-they-are-better-together)的小伙伴说rust的标准库还依赖第三方库(注：我对rust了解不深，尚未证实)，这引发了我的一个疑问: **Go标准库是否依赖其他modules呢**？在这一短篇中，我就来探究一下

注：本文使用的Go版本为

[Go 1.19]。

众所周知，[Go于1.11版本引入go modules](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)，如今Go module已经完全替代掉原先的gopath构建模式，成为了Go源码的标准构建模式。

相应的，Go标准库也在[Go 1.13版本](https://tonybai.com/2019/10/27/some-changes-in-go-1-13/)中采用了Go module构建，加入了go.mod文件，第一版标准库的go.mod文件内容如下：

```
module std
go 1.12
require (
golang.org/x/crypto v0.0.0-20190611184440-5c40567a22f8
golang.org/x/net v0.0.0-20190813141303-74dc4d7220e7
golang.org/x/sys v0.0.0-20190529130038-5219a1e1c5f8 // indirect
golang.org/x/text v0.3.2 // indirect
)
```


我们看到Go标准库的module path为std。不过就像开篇说的那样，很多gopher认为标准库应该是依赖链的末端，但从go.mod文件的内容来看，**Go标准库也有自己的依赖**。

我们再来看看[Go 1.19版本](https://tonybai.com/2022/08/22/some-changes-in-go-1-19)中go.mod的内容：

```
module std
go 1.19
require (
golang.org/x/crypto v0.0.0-20220516162934-403b01795ae8
golang.org/x/net v0.0.0-20220517181318-183a9ca12b87
)
require (
golang.org/x/sys v0.0.0-20220614162138-6c1b26c55098 // indirect
golang.org/x/text v0.3.8-0.20220509174342-b4bca84b0361 // indirect
)
```


我们看到：和Go 1.13版本相比，Go标准库的go.mod将直接依赖和间接依赖(也叫传递依赖)分开放在不同的require block中，这是因为[Go 1.17版本增加的module依赖图修剪特性](https://tonybai.com/2021/08/19/go-module-changes-in-go-1-17)。

但从Go标准库依赖的modules来看，和Go 1.13相比，Go标准库依赖的modules并没有变化。

Go标准库依赖的是什么modules呢？我们看到其依赖的module都在golang.org/x这个路径下，这是Go核心团队自己维护的非标准库module的[Canonical import paths](https://tonybai.com/2014/11/04/some-changes-in-go-1-4)的前缀路径。golang.org/x这个前缀路径下的包有不少，如下图所示：

![](../../assets/6d0377bd4fad3495.png)


其中，主要的可以被import的功能module包括：

- crypto：额外的密码学软件包
- image：额外的图像处理包
- net：额外的网络相关处理包
- sync：额外的并发同步原语包
- sys：用于进行系统调用的软件包
- text：用于处理文本的软件包
- time：额外的时间处理相关包
- exp：实验性(experimental)的和废弃的(deprecated)软件包

注：exp下面的包尽量不用，或务必谨慎使用，这里实验性包居多，API接口和具体实现变化可能性很大。还有一些是废弃不再维护的。


那Go标准库为什么会直接依赖crypto和net这两个modules呢？

我的理解是网络与密码学是两个变化较快的领域，同时也是两个十分重要的领域，尤其是在如今对安全十分重视的云原生时代。一些新的密码学算法、网络技术规范(RFC)在不断的出现并持续演进，这些技术在未成熟前尚不适合放入标准库，那么在标准库之外由Go核心团队维护一个“与时俱进”的库就十分必要。等成熟后，在标准库中设计并提供稳定接口并引用golang.org/x/abc下的实现就可以很快实现对某成熟网络技术或密码学技术的稳定支持，当年[Go 1.6版本对http/2的支持就是这么做的](https://tonybai.com/2016/02/21/some-changes-in-go-1-6)。

那么Go标准库都依赖了哪些具体的包了呢？我们可以看一下\$GOROOT/src/vendor下面的modules.txt：

```
# golang.org/x/crypto v0.0.0-20220516162934-403b01795ae8
## explicit; go 1.17
golang.org/x/crypto/chacha20
golang.org/x/crypto/chacha20poly1305
golang.org/x/crypto/cryptobyte
golang.org/x/crypto/cryptobyte/asn1
golang.org/x/crypto/curve25519
golang.org/x/crypto/curve25519/internal/field
golang.org/x/crypto/hkdf
golang.org/x/crypto/internal/poly1305
golang.org/x/crypto/internal/subtle
# golang.org/x/net v0.0.0-20220517181318-183a9ca12b87
## explicit; go 1.17
golang.org/x/net/dns/dnsmessage
golang.org/x/net/http/httpguts
golang.org/x/net/http/httpproxy
golang.org/x/net/http2/hpack
golang.org/x/net/idna
golang.org/x/net/lif
golang.org/x/net/nettest
golang.org/x/net/route
# golang.org/x/sys v0.0.0-20220614162138-6c1b26c55098
## explicit; go 1.17
golang.org/x/sys/cpu
# golang.org/x/text v0.3.8-0.20220509174342-b4bca84b0361
## explicit; go 1.17
golang.org/x/text/secure/bidirule
golang.org/x/text/transform
golang.org/x/text/unicode/bidi
golang.org/x/text/unicode/norm
```


modules.txt是go mod vendor命令生成的，也是项目依赖包的完全列表，包括间接依赖的包。

我们可以通过go mod why命令查询为什么标准库要依赖这些module以及package，以golang.org/x/crypto这个module为例：

```
$go mod why -m golang.org/x/crypto
# golang.org/x/crypto
crypto/tls
golang.org/x/crypto/chacha20poly1305
```


我们看到是crypto/tls包依赖了golang.org/x/crypto这个module，但why只会输出标准库中依赖x/crypto module的一个包而已，并非全部。同理我们也可以查看modules.txt某个具体的包为何要被依赖，以golang.org/x/net/dns/dnsmessage为例：

```
$go mod why golang.org/x/net/dns/dnsmessage
# golang.org/x/net/dns/dnsmessage
net
golang.org/x/net/dns/dnsmessage
```


我们看到net包依赖了dnsmessage这个包。

综上，我们知道了Go标准库也是会依赖的，**但其依赖的module被严格限制在Go核心团队自己维护的golang.org/x下面的少数module**，因此我们依然可以完全信任Go标准库，相信后续Go标准库也会一直保证实现的高质量。

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 博客：tonybai.com
- github: https://github.com/bigwhite

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论