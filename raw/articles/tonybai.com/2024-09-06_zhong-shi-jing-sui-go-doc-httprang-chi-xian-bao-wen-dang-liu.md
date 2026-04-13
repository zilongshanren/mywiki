---
title: 重拾精髓：go doc -http让离线包文档浏览更便捷
url: https://tonybai.com/2024/09/06/go-doc-add-http-support/
published: '2024-09-06'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 重拾精髓：go doc -http让离线包文档浏览更便捷

![](../../assets/a2615ebcfb00a8f9.png)


[本文永久链接](https://tonybai.com/2024/09/06/go-doc-add-http-support) – https://tonybai.com/2024/09/06/go-doc-add-http-support

Go语言团队近期接受了Go团队成员、Go圣经《[The Go Programming Language](http://www.gopl.io/)》合著者[Alan Donovan](https://github.com/adonovan)的[新提案](https://github.com/golang/go/issues/68106)，旨在进一步提升开发者体验。这个提案为[go doc命令](https://mp.weixin.qq.com/s/ypK-2wGHGj9_n4o8y-clXg)新增了一个强大的功能：通过go doc -http，开发者可以快速启动一个本地的文档服务器，并自动在浏览器中打开Go包的参考文档。该功能为开发者提供了类似[pkg.go.dev](https://pkg.go.dev/)的离线文档展示形式，同时增强了查看本地文档的交叉引用功能。看到这个提案功能，屏幕前的资深Gopher是不是感觉似曾相识呢:)。

早在去年，我就写过一篇有关go包文档查看方式对比的文章《[聊聊godoc、go doc与pkgsite](https://mp.weixin.qq.com/s/ypK-2wGHGj9_n4o8y-clXg)》，在那篇文章中，我就对当前Go包文档查看的几种方式做了详细说明，如果你是Go初学者，不妨点击链接移步过去仔细阅读一番。当然，这里也会简单地再介绍一下Go包文档离线查看工具的演进。

Go语言的包文档查看工具经历了三个重要阶段的演进，分别是**godoc**、**go doc**和**pkgsite**。以下是这些工具的发展历程：

godoc是Go语言最早用于查看包文档的工具。它支持通过命令行查看文档，也可以通过-http参数启动一个本地文档服务器，用户在浏览器中以网页形式查看文档。这个工具提供了较为完整的Go包文档浏览体验，支持交叉引用和导航。但随着Go的发展，逐渐不再是官方推荐的工具，并且不再随Go安装包一并发布了！

随着Go的升级与演进，go doc逐渐取代了godoc成为查看包文档的主要工具。go doc主要提供了通过命令行输出包详细文档的能力，对应简单的包查询，这种方式更为高效：

```
$go doc -h
Usage of [go] doc:
go doc
go doc <pkg>
go doc <sym>[.<methodOrField>]
go doc [<pkg>.]<sym>[.<methodOrField>]
go doc [<pkg>.][<sym>.]<methodOrField>
go doc <pkg> <sym>[.<methodOrField>]
For more information run
go help doc
Flags:
-C dir
change to dir before running command
-all
show all documentation for package
-c symbol matching honors case (paths not affected)
-cmd
show symbols with package docs even if package is a command
-short
one-line representation for each symbol
-src
show source code for symbol
-u show unexported symbols as well as exported
```


然而从上面的usage输出来看，go doc版本去除了godoc堪称精髓能力的-http支持，开发者无法像godoc那样启动本地文档服务器，这在某种程度上减少了它的可视化文档浏览功能。

pkgsite是目前官方推荐的在线Go包文档浏览工具，提供了一个全面、易于导航的网站（[pkg.go.dev](https://pkg.go.dev)），用户可以在浏览器中查看各个Go包的文档、函数、类型等信息。它大大提升了开发者的体验，提供了丰富的交叉引用和包依赖信息。

![](../../assets/7c2bc432aa5e0cfd.png)


但[pkgsite也是go官方站](https://tonybai.com/2019/11/14/what-the-godev-website-bring-to-gophers/)，主要用于在线查看，虽然也支持离线查看功能。但就像Alan Donovan在issue提到的那样：**pkgsite程序目前相当大且启动缓慢**，并且pkgsite最初被设计为一个可以在Google Cloud上运行的长生命周期的服务器，有很多外部依赖和耦合。

为了满足诸多Gopher通过浏览器web方式离线浏览Go包参考手册的需求，弥补pkgsite过于缓慢和庞大的不足，Alan Donovan提出了让离线文档服务能力回归的issue。没错！这个提案其实就是godoc -http这个经典的、精髓功能的“重生”。

这一新增功能有望在Go 1.24或之后的版本中正式推出，届时，新增的go doc -http功能会让离线文档服务的能力回归，为开发者提供了更多选择与灵活性。但目前go doc -http的具体命令接口形式尚未确定，但可以确定的是，通过该命令，用户无需再依赖第三方工具或访问外部网站，即可在本地查看项目的完整文档。这不仅提升了效率，也让开发者更方便地查找包文档以及包间的交叉引用，实现更直观的包依赖管理。Go开发者们可以尽情享受这一强大的本地文档浏览工具。

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

## 评论