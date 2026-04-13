---
title: Go，14周年[译]
url: https://tonybai.com/2023/11/11/go-opensource-14-years/
published: '2023-11-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go，14周年[译]

![](../../assets/12a1394cb8f2a246.png)


[本文永久链接](https://tonybai.com/2023/11/11/go-opensource-14-years) – https://tonybai.com/2023/11/11/go-opensource-14-years

国内的双十一购物狂欢已没有了当年的那种热闹与喧嚣，但大洋彼岸的Go团队却始终保持稳中有增的开发和语言演进节奏。今晨Go核心团队的[Russ Cox](https://swtch.com/~rsc/)代表Go语言项目团队在Go官博上发表了[《Fourteen Years of Go》](https://go.dev/blog/14years)的博文，纪念[Go语言开源14周年](https://opensource.googleblog.com/2009/11/hey-ho-lets-go.html)，并对2023年以来Go语言的演进进行了归纳总结，并对Go在其第15个年头将要做的改进给予了很高的期望。这里对博文做简单翻译，供大家参考。

今天，我们欢庆[Go语言开源发布十四周年](https://opensource.googleblog.com/2009/11/hey-ho-lets-go.html)！Go在过去一年中取得了巨大的进步，发布了两个功能特性丰富的版本，并达成了其他一些重要的里程碑。

我们在2月发布了[Go 1.20](https://tonybai.com/2023/02/08/some-changes-in-go-1-20/)，在8月发布了[Go 1.21](https://tonybai.com/2023/08/20/some-changes-in-go-1-21/)，在这两个版本中，我们更多地关注实现改进而不是新语言特性。

我们在[Go 1.20版本中发布了Profile-guided optimization(PGO)功能的预览版](https://go.dev/blog/pgo-preview)，并[在Go 1.21中正式发布了该功能](https://go.dev/blog/pgo)，它允许Go编译器读取程序的Profile，然后花更多时间对程序中运行最频繁的部分进行优化。在Go 1.21中，启用PGO后，工作负载的CPU使用率通常可以提高2%到7%。关于PGO的介绍请参阅“[Go 1.21中的Profile-guided optimization](https://go.dev/blog/pgo)”，对PGO的全面说明请参阅“[PGO用户指南](https://go.dev/doc/pgo)”。

Go[从Go 1.2版本开始](https://go.dev/blog/cover)就支持在go test期间收集覆盖率profile数据。Go 1.20版本增加了对go build构建的二进制文件收集测试覆盖率profile数据的支持，这样你就可以在集成测试期间收集测试覆盖率数据，详情请参阅“[Go集成测试的代码覆盖率](https://go.dev/blog/integration-test-coverage)”。

[兼容性一直是Go的重要组成部分](https://tonybai.com/2023/09/10/understand-go-forward-compatibility-and-toolchain-rule/)，我们最初对兼容性的承诺始于“[Go 1和Go程序的未来](https://go.dev/doc/go1compat)”这篇文章。针对那些可能会给现有程序造成破坏但又必须要修正的重要错误，Go 1.21版本通过扩展GODEBUG的约定用法进一步改进了兼容性。请参阅博文“[后向兼容性，Go 1.21和Go 2](https://go.dev/blog/compat)”了解概况，详情请参阅文档“[Go、后向兼容性和GODEBUG](https://go.dev/doc/godebug)”。

Go 1.21还发布了对内置工具链管理的支持，允许你像改变其他依赖的版本一样轻松地改变特定模块(module)中使用的Go工具链版本。请参阅博文“[Go 1.21中的向前兼容性和工具链管理](https://go.dev/blog/toolchain)”，更多详情请参阅文档“[Go工具链](https://go.dev/doc/toolchain)”。

另一个在工具链方面的重要成就是将磁盘索引集成到gopls(Go语言服务器)。这将gopls的启动延迟和内存使用缩短了3-5倍。“[扩展gopls以适应不断增长的Go生态系统](https://go.dev/blog/gopls-scalability)”一文解释了其中的技术细节。你可以通过运行以下命令确保运行最新的gopls:

```
$go install golang.org/x/tools/gopls@latest
```


Go 1.21引入了新的[cmp](https://go.dev/pkg/cmp/)、[maps](https://go.dev/pkg/maps/)和[slices](https://go.dev/pkg/slices/)包 —— Go的第一个泛型标准库 —— 以及扩展了可比较类型(comparable)的集合。详情请参阅博文“[所有可比较的类型](https://go.dev/blog/comparable)”。

总体而言，我们继续完善泛型，并通过会议演讲和撰写博文来解释重要细节。今年两篇值得关注的博文是“[分解类型参数](https://go.dev/blog/deconstructing-type-parameters)”和“[关于类型推断你一直想知道的事情 —— 以及更多](https://go.dev/blog/type-inference)”。

Go 1.21中另一个重要的新包是[log/slog](https://tonybai.com/2023/09/01/slog-a-new-choice-for-logging-in-go)，它为标准库添加了[结构化日志](https://tonybai.com/2023/09/04/slog-in-action-file-logging-rotation-and-kafka-integration/)的官方API。请参阅“[使用slog实现结构化日志](https://go.dev/blog/slog)”了解概况。

在对WebAssembly(Wasm)的移植方面，Go 1.21增加了在WebAssembly System Interface(WASI) preview1版本上运行的支持。WASI preview1是一种新的“操作系统”接口，支持大多数服务器端的Wasm环境。详情请参阅“[Go对WASI的支持](https://go.dev/blog/wasi)”一文。

在安全方面，我们将继续确保Go在帮助开发人员了解其依赖关系和漏洞方面处于领先地位，7月发布的[Govulncheck 1.0](https://tonybai.com/2022/09/10/an-intro-of-govulncheck)正是这样的例子。如果你使用VS Code，可以通过Go扩展直接在编辑器中运行govulncheck。请参阅[govulncheck IDE教程](https://go.dev/doc/tutorial/govulncheck-ide)了解如何开始使用govulncheck。如果你使用GitHub，可以使用[GitHub Action for govulncheck](https://github.com/marketplace/actions/golang-govulncheck-action)将运行govulncheck作为CI/CD流程的一部分。有关检查依赖项漏洞问题的更多信息，请参阅今年的Google I/O大会的演讲“[使用Go和Google构建更安全的应用程序](https://www.youtube.com/watch?v=HSt6FhsPT8c&ab_channel=TheGoProgrammingLanguage)”。

另一个重要的安全里程碑是Go 1.21的高度可重现的工具链构建。详情请参阅“[完全可重现的经验证的Go工具链](https://go.dev/blog/rebuild)”，包括在没有使用任何Linux工具的情况下在Mac上重现Ubuntu Linux Go工具链的演示。

这是非常繁忙的一年!

在Go的第15个年头，我们将继续努力使Go成为最佳的大规模软件工程环境。我们特别兴奋的一个变化是重新定义for循环中”:=”的语义，以消除意外别名bug的可能性。详情请参阅“[在Go 1.22中修复For循环](https://go.dev/blog/loopvar-preview)”，其中包括在Go 1.21中对此更改的预览版的说明。

感谢!

Go项目一直远不止我们在Google的Go小组。感谢所有贡献者和Go社区中的每一个人，使得今天的Go成为可能。我们衷心祝愿大家在未来一年中一切顺利。

[“Gopher部落”知识星球](https://public.zsxq.com/groups/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

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

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

老师你好，请问一下，《Go 语言精进之路》啥时候出第二版？

我和出版社都有这个意向，但具体时间目前还是无法给出:)。

谢谢，非常期待！