---
title: Go语言对ARM架构的支持与未来[译]
url: https://tonybai.com/2020/12/18/go-ports-until-202012/
published: '2020-12-18'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go语言对ARM架构的支持与未来[译]

本文翻译自Go官方博客文章[《Go on ARM and Beyond》](https://blog.golang.org/ports)(https://blog.golang.org/ports)。

最近业界关于非x86处理器的讨论沸沸扬扬，所以我们认为值得简单的写一篇关于Go语言对这些非x86处理器的支持情况的文章。

对我们来说，[Go的可移植性](https://tonybai.com/2017/06/27/an-intro-about-go-portability/)一直很重要，我们不会过度去适配任何特定的操作系统或架构。[Go最初的开源版本](https://opensource.googleblog.com/2009/11/hey-ho-lets-go.html)包括对两种操作系统（Linux和MacOSX）和三种架构（64位x86、32位x86和32位ARM）的支持。

多年来，我们已经增加了对更多操作系统和架构组合的支持：

- Go1（2012年3月）支持原始系统(译注：上面提到的两种操作系统和三种架构)以及64位和32位x86上的FreeBSD、NetBSD和OpenBSD，以及32位x86上的Plan9。
- Go 1.3（2014年6月）增加了对64位x86上Solaris的支持。
[Go 1.4](https://tonybai.com/2014/11/04/some-changes-in-go-1-4/)（2014年12月）增加了对32位ARM上Android和64位x86上Plan9的支持。[Go 1.5](https://tonybai.com/2015/07/10/some-changes-in-go-1-5/)（2015年8月）增加了对64位ARM和64位PowerPC上的Linux以及32位和64位ARM上的iOS的支持。[Go 1.6](https://tonybai.com/2016/02/21/some-changes-in-go-1-6/)（2016年2月）增加了对64位MIPS上的Linux，以及32位x86上的Android的支持。它还增加了32位ARM上的Linux官方二进制下载，主要用于RaspberryPi系统。[Go 1.7](https://tonybai.com/2016/06/21/some-changes-in-go-1-7/)（2016年8月）增加了对的z系统（S390x）上Linux和32位x86上Plan9的支持。[Go 1.8](https://tonybai.com/2017/02/03/some-changes-in-go-1-8/)（2017年2月）增加了对32位MIPS上Linux的支持，并且它增加了64位PowerPC和z系统上Linux的官方二进制下载。[Go 1.9](https://tonybai.com/2017/07/14/some-changes-in-go-1-9/)（2017年8月）增加了对64位ARM上Linux的官方二进制下载。[Go 1.12](https://tonybai.com/2019/03/02/some-changes-in-go-1-12)（2018年2月）增加了对32位ARM上Windows10 IoT Core的支持，如RaspberryPi3。它还增加了对64位PowerPC上AIX的支持。[Go 1.14](https://tonybai.com/2020/03/08/some-changes-in-go-1-14)（2019年2月）增加了对64位RISC-V上Linux的支持。

虽然x86-64的移植在Go的早期得到了大部分的关注，但今天我们所有的目标架构都得到了我们[基于SSA的编译器后端](https://www.youtube.com/watch?v=uTMvKVma5ms)的良好支持，并生成了优秀的代码。我们一路走来得到了许多贡献者的帮助，包括来自Amazon、ARM、Atos、IBM、Intel和MIPS的工程师。

Go支持对所有这些系统进行开箱即用的[交叉编译](https://tonybai.com/2014/10/20/cross-compilation-with-golang/)，而且只需付出最小的努力。例如，要在一个64位Linux系统中构建一个基于32位x86的Windows应用，我们只需执行下面命令：

```
GOARCH=386 GOOS=windows go build myapp # 编译生成myapp.exe
```


在过去的一年里，几家主要的厂商都宣布了用于服务器、笔记本电脑和开发者机器的新ARM64硬件。Go在这些方面适配的很好。多年来，Go一直在ARM64 Linux服务器上为Docker、Kubernetes和Go生态系统的其他部分，以及ARM64 Android和iOS设备上的移动应用提供支持。

自今年夏天苹果宣布Mac过渡到苹果芯片以来，苹果和谷歌一直在合作，以确保Go和更广泛的Go生态系统在其上运行良好，无论是在Rosetta 2下运行Go x86二进制文件，还是运行原生Go ARM64二进制文件。本周早些时候，我们发布了第一个Go 1.16测试版，其中包括了对使用M1芯片的Mac的原生支持。您可以在[Go下载页面](https://golang.google.cn/dl/#go1.16beta1)上下载并试用适用于M1 Mac和所有其他系统的Go 1.16测试版。当然，这是一个测试版，就像所有的测试版一样，它肯定有我们不知道的bug。如果你遇到任何问题，请在golang.org/issue/new上报告）。

在本地开发中使用与生产中相同的CPU架构总是很好的，这样可以消除两种环境之间的差异。如果你部署到ARM64生产服务器上，Go也可以轻松在ARM64 Linux和Mac系统上进行开发。但当然，无论你是在x86系统上工作并部署到ARM上，还是在Windows上工作并部署到Linux上，或者其他组合，在一个系统上工作并交叉编译部署到另一个系统上仍然和以前一样容易。

我们希望添加支持的下一个目标是ARM64 Windows 10系统。如果你有专业知识并愿意提供帮助，我们正在golang.org/issue/36439上协调工作。

**“Gopher部落”知识星球开球了！**高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！星球首开，福利自然是少不了的！2020年年底之前，8.8折(很吉利吧^_^)加入星球，下方图片扫起来吧！

![](../../assets/d3fad3142fe3cc39.png)


我的Go技术专栏：“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”上线了，欢迎大家订阅学习！

![img{512x368}](../../assets/018ff45f7e150fca.png)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/e9f90df4cc2580e5.png)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家https://tonybai.com/

smspush:可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展；短信内容你来定，不再受约束,接口丰富，支持长短信，签名可选。

2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5GRCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1coreCPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687开启你的DO主机之路。

GopherDaily(Gopher每日新闻)归档仓库-https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github:https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2020, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

可 Go 却不能 out of the box 的交叉编译 ARM 大端，真是伤脑经。