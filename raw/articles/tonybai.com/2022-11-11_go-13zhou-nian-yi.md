---
title: Go，13周年[译]
url: https://tonybai.com/2022/11/11/go-opensource-13-years/
published: '2022-11-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go，13周年[译]

![](../../assets/1764573fdc5094b6.png)


[本文永久链接](https://tonybai.com/2022/11/11/go-opensource-13-years) – https://tonybai.com/2022/11/11/go-opensource-13-years

在中华大地的老百姓抱着手机进行双十一购物节狂欢，忙着支付尾款和秒杀的时候，Go核心团队的Russ Cox代表Go语言项目团队在Go官博上发表了[《Thirteen Years of Go》](https://go.dev/blog/13years)的博文，纪念Go语言开源13周年，并对2021年以来Go语言的演进进行了归纳总结，对Go在其第14个年头将要做的改进也做了简单的说明。这里对博文做简单翻译，供大家参考。

今天，我们庆祝Go开源版本的十三岁生日。从今天起，**Go将正式步入青少年阶段**！

译注：teenager：青少年；13岁到19岁的年轻人


对于Go来说，过去的一年是不平凡的一年。在这一年里发生的最重要的事件是[Go 1.18版本在3月份的发布](https://tonybai.com/2022/04/20/some-changes-in-go-1-18)，这个版本带来了许多改进，其中最显着的是[Go工作区](https://tonybai.com/2021/11/12/go-workspace-mode-in-go-1-18)、[模糊测试](https://tonybai.com/2021/12/01/first-class-fuzzing-in-go-1-18)和[Go泛型](https://tonybai.com/2022/03/25/intro-generics)。

Go工作区使得同时处理多个module变得容易，尤其是当你维护一组彼此有依赖关系的module时。若要了解Go工作区，请参阅Beth Brown的博客文章[“熟悉工作区”](https://go.dev/blog/get-familiar-with-workspaces)和[工作区参考文档](https://go.dev/ref/mod#workspaces)。

模糊测试(Fuzzing)是一个新功能特性，它可以帮助你查找出代码无法正确处理的输入。你只需定义一个接受任何输入数据的模糊测试，然后模糊测试会尝试不同的随机输入，这个过程由代码覆盖率指导，并努力尝试使模糊测试执行失败。在开发对任意输入（甚至是攻击者控制的输入）具有鲁棒性的代码时，模糊测试尤其有用。若要了解有关模糊测试的详细信息，请参阅教程[“模糊测试入门”](https://go.dev/doc/tutorial/fuzz)和[模糊测试参考文档](https://go.dev/security/fuzz/)，并留意凯蒂·霍克曼(Katie Hockman)在GopherCon 2022上的演讲“Fuzzing Test made Easy”，这个演进的视频应该很快就会上线的。

泛型，很可能是Go开发者最需要的功能特性(译注：来自Go官方调查数据)，它在Go中增加了参数多态性机制，以支持编写可适配各种不同类型的代码，并且仍不会失去编译时静态检查的保证。要了解有关泛型的更多信息，请参阅教程[“泛型入门”](https://go.dev/doc/tutorial/generics)。更多详细信息，请参阅博客文章[《泛型简介》](https://tonybai.com/2022/03/25/intro-generics) 和[“何时使用泛型”](https://go.dev/blog/when-generics)，或是来自Go Day 2021年谷歌开源直播[“在Go中使用泛型”](https://www.youtube.com/watch?v=nr8EpUO9jhw)以及来自GopherCon 2021由Robert Griesemer和Ian Lance Taylor共同的演讲[“Generics”](https://www.youtube.com/watch?v=Pa_e9EeCdy8)。

与Go 1.18版本相比，今年8月份发布的[Go 1.19版本](https://tonybai.com/2022/08/22/some-changes-in-go-1-19)显得有些波澜不惊，这与该版本专注于完善和改进Go 1.18引入的功能特性以及内部稳定性改进和优化不无关系。Go 1.19的一个明显变化是[增加了支持Go文档注释中的链接、列表和标题](https://go.dev/doc/comment)。另一个则是为垃圾回收器[添加了软内存限制(soft memory limit)](https://go.dev/doc/go1.19#runtime)，这在容器工作负载中特别有用。有关最近的垃圾回收器改进的更多信息，参见Michael Knyszek的博客文章[“Go Runtime：4 Years later”](https://go.dev/blog/go119runtime)、他的演讲[“Respecting Memory Limits in Go”](https://www.youtube.com/watch?v=07wduWyWx8M&list=PLtoVuM73AmsJjj5tnZ7BodjN_zIvpULSx) 以及新的[“Go垃圾收集器指南”](https://go.dev/doc/gc-guide)。

我们一直努力让Go代码开发可以更优雅的扩展，支持更大规模的代码库，我们在VS Code Go和Gopls语言服务器上的工作就致力于此。今年，Gopls的工作聚焦于提高稳定性和性能，同时提供了对泛型以及新的代码分析的支持。如果你还没有使用VS Code Go或Gopls，不妨尝试一下。可以看看苏茜·穆勒(Suzy Mueller)的演讲[“使用Go编辑器构建更好的项目”](https://www.youtube.com/watch?v=jMyzsp2E_0U)。 作为奖励，[在VS Code 中调试Go](https://go.dev/s/vscode-go-debug)通过Delve原生对[调试适配器协议(Debug Adapter Protocol)](https://microsoft.github.io/debug-adapter-protocol/)支持而变得更加可靠和强大。最后试试苏茜的[《调试寻宝记》](https://www.youtube.com/watch?v=ZPIPPRjwg7Q)吧！

开发规模的另一部分是项目中依赖项的数量。[Go 12岁生日](https://tonybai.com/2021/11/11/go-opensource-12-years)后的一个月左右，[Log4shell漏洞](https://en.wikipedia.org/wiki/Log4Shell)的出现为行业敲响警钟，关于供应链安全的重要性得以提升。Go的module系统是专门为此而设计的，帮助您了解和跟踪依赖项，确定您正在使用哪些特定的依赖，并确定其中是否有任何已知漏洞。菲利波·瓦尔索达的博客文章[“如何缓解供应链攻击”](https://tonybai.com/2022/04/02/how-go-mitigates-supply-chain-attacks) 概述了我们的方法。9月，我们通过Julie Qiu的博客文章[“Vulnerability Management for Go”](https://tonybai.com/2022/09/10/an-intro-of-govulncheck)发布了Go漏洞管理方法预览版，这项工作的核心是一个新的、精心策划的漏洞数据库 和一个新的[govulncheck命令](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck)，它使用高级静态分析来消除大多数误报。

我们为了了解Go用户而付出的努力之一是我们的年度Go年终调查。今年，我们的用户体验研究人员还增加了一个轻量级的年中Go调查。我们的目标是收集足够的回复，使其具有统计意义，而这也不会成为整个Go社区的负担。有关结果，请参阅Alice Merrick的博客文章[“Go开发者调查2021年结果”](https://go.dev/blog/survey2021-results)和托德·库列萨的文章[“Go开发者调查2022 年第二季度结果”](https://go.dev/blog/survey2022-q2-results)。

随着世界开始恢复更多地旅行，我们也很高兴在2022年的Go技术会议上亲自见到你们中的许多人，特别是7月在柏林举行的GopherCon欧洲大会和10月在芝加哥举行的GopherCon。上周，我们在谷歌开源直播上举办了一年一度的虚拟活动[Go Day](https://opensourcelive.withgoogle.com/events/go-day-2022)。 以下是我们在这些活动上的一些演讲：

[Go是如何成为最好的自己的](https://www.youtube.com/watch?v=vQm_whJZelc)， 作者：Cameron Balahan，在GopherCon Europe。[“Go团队Q&A”](https://www.youtube.com/watch?v=KbOTTU9yEpI)， 与Cameron Balahan，Michael Knyszek和Than McIntosh一起在GopherCon欧洲。[“兼容性：Go程序如何保持工作”](https://www.youtube.com/watch?v=v24wrd3RwGo)， 作者：Russ Cox at GopherCon。[“Go整体体验”](https://www.gophercon.com/agenda/session/998660)， 作者：Cameron Balahan在GopherCon（视频尚未发布）[“Go语言的结构化日志包”](https://tonybai.com/2022/10/30/first-exploration-of-slog)， 作者：Jonathan Amsterdam 在 Go Day 上 Google Open Source Live[“使用Go更快、更安全地编写应用程序”](https://opensourcelive.withgoogle.com/events/go-day-2022/watch?talk=talk3)， 作者：Cody Oss 在 Go Day 上 Google Open Source Live- “
[Go中的内存限制](https://opensourcelive.withgoogle.com/events/go-day-2022/watch?talk=talk4)， 作者：Michael Knyszek 在Go Day上 Google Open Source Live

今年的另一个里程碑是出版了[“Go编程语言和环境”](https://tonybai.com/2022/05/04/the-paper-of-go-programming-language-and-environment)， 作者是Russ Cox、Robert Griesemer、Rob Pike、Ian Lance Taylor和Ken Thompson，文章发表在“ACM通信”中。 这篇文章，由Go的原始设计者和实现者解释了**我们认为是什么让Go如此受欢迎和富有成效**。 简而言之，Go 的工作重点是提供完整的开发环境。针对整个软件开发过程，重点是扩展到大型软件工程工作和大型部署。

在Go的第14个年头，我们将继续努力使Go成为用于大规模软件工程的最好的环境。我们计划特别关注供应链安全，提高兼容性和结构化日志记录，所有这些都已在这篇文章中有链接。当然还会有很多其他改进，包括profile-guided optimization等。

谢谢！Go一直远远超过Google的Go团队所做的。感谢你们所有人——我们的贡献者和Go社区中的每个人——感谢您的帮助使Go成为今天的成功编程环境。我们祝愿你在来年一切顺利。

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

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

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论