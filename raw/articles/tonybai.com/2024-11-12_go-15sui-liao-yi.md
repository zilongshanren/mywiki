---
title: Go，15岁了[译]
url: https://tonybai.com/2024/11/12/go-turns-15/
published: '2024-11-12'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go，15岁了[译]

![](../../assets/0658feefe9959190.png)


[本文永久链接](https://tonybai.com/2024/11/12/go-turns-15) – https://tonybai.com/2024/11/12/go-turns-15

虽然迟到了，但绝不缺席！[新任Go技术负责人Austin Clements](https://tonybai.com/2024/10/10/pass-torch-to-go-new-leadership-team/)在Go语言15岁生日后的第二天，在Go官方博客上发表了庆祝文章“[Go Turns 15](https://go.dev/blog/15years)”。在这篇文章中，Austin回顾了过去一年Go项目和社区的变化，以及Go团队的努力工作，并对Go的未来发展进行了展望。我在此对这篇庆生文进行了翻译，供大家参考。

Go，生日快乐！

周日，我们庆祝了[Go开源15周年](https://opensource.googleblog.com/2009/11/hey-ho-lets-go.html)！

自从[Go诞生10周年](https://go.dev/blog/10years)以来，无论是Go语言本身还是整个世界都经历了巨大的变化。尽管如此，有些方面依然保持不变：**Go始终致力于稳定性、安全性，以及支持软件工程和大规模生产**。

Go语言发展势头强劲！在过去五年中，Go的用户群增加了三倍多(译注：不知道这个数据从何而来)，成为增长最快的编程语言之一。自十五年前诞生以来，[Go已成为十大编程语言](https://mp.weixin.qq.com/s?__biz=MzIyNzM0MDk0Mg==&mid=2247497403&idx=1&sn=03bc972e38163e1539da765249d46586&chksm=e860115adf17984cfe47f9680d8c0fb6370987ad45415ff2d38233d05fe6b315210ce6ada385#rd)之一，并[成为现代云计算的主要语言](https://tonybai.com/2024/08/17/go-the-c-language-of-the-internet-era-come-true/)。

![](../../assets/6fb410ebd69b8f50.png)



![](../../assets/add7527a98e7a831.png)



随着[Go 1.22版本](https://tonybai.com/2024/02/18/some-changes-in-go-1-22/)在二月份发布和[Go 1.23版本](https://tonybai.com/2024/08/19/some-changes-in-go-1-23/)在八月份发布，这一年可被称为“for循环之年”。Go 1.22将for循环中引入变量的作用域[改为每次迭代](https://go.dev/blog/loopvar-preview)，而非整个循环，从而解决了一个长期存在的语言“陷阱”。十多年前，在Go 1发布之前，Go团队对几个语言细节做出了决策，其中就包括for循环是否应该在每次迭代中创建一个新的循环变量。有趣的是，这次讨论非常简短且没有明确的意见。Rob Pike以他一贯的风格结束了讨论，只说了一个字：“stet”（保持原样）。结果也确实如此。尽管当时看似微不足道，但多年的生产经验突显了这一决策的影响。然而，在此期间，我们还构建了强大的工具来理解对Go的变更影响，特别是在整个Google代码库中进行生态系统范围的分析和测试，并建立了与社区合作和获取反馈的流程。在经过广泛的测试、分析和社区讨论后，我们推出了这一变更，并配备了[哈希二分工具](https://go.googlesource.com/proposal/+/master/design/60078-loopvar.md#transition-support-tooling)，以帮助开发者在大规模代码中精确定位受影响的部分。

对for循环的变更仅是是五年演进调整的一部分。这一变更的实现得益于[Go 1.21中引入的向前兼容性](https://tonybai.com/2023/09/10/understand-go-forward-compatibility-and-toolchain-rule/)，而这又建立在四年半前[Go 1.14](https://tonybai.com/2020/03/08/some-changes-in-go-1-14/)发布的[Go模块](https://tonybai.com/tag/gomodule)基础之上。

译注：Go module首次在Go 1.11版本由Russ Cox设计和实现，Go 1.14版本首次宣布Go module具备生产使用的成熟度了。


Go 1.23在此变更的基础上进一步引入了[迭代器和用户定义的for-range循环](https://tonybai.com/2024/06/24/range-over-func-and-package-iter-in-go-1-23/)。结合仅仅两年半前在Go 1.18中引入的泛型！——这为自定义集合和许多其他编程模式奠定了强大而人性化的基础。

这些版本还带来了许多生产就绪方面的改进，包括备受期待的[标准库HTTP路由器增强](https://go.dev/blog/routing-enhancements)、[执行跟踪的全面重构](https://go.dev/blog/execution-traces-2024)，以及[为所有Go应用程序提供更强的随机性](https://go.dev/blog/chacha8rand)。此外，我们的[第一个v2标准库包](https://go.dev/blog/randv2)的引入为未来的标准库演进和现代化建立了模板。

在过去的一年中，我们还谨慎地推出了Go工具的[自愿使用的遥测系统](https://mp.weixin.qq.com/s?__biz=MzIyNzM0MDk0Mg==&mid=2247497282&idx=1&sn=30e10a7091c270d5dcd5e1b3c57bdf2c&chksm=e86011a3df1798b57870fedccbbda20d0a334413e15c768476a18fe9446a89432e776a8fbf1c#rd)。该系统将为Go开发者提供数据，以便他们做出更好的决策，同时保持[完全开放](https://telemetry.go.dev/)和匿名。Go遥测最初出现在gopls（Go语言服务器）中，已经带来了[许多改进](https://github.com/golang/go/issues?q=is%3Aissue+label%3Agopls%2Ftelemetry-wins)。这项努力为使Go编程体验变得更加出色奠定了基础。

展望未来，我们正在不断演进Go，以更好地利用当前和未来硬件的能力。在过去的15年中，硬件发生了巨大的变化。为了确保Go能够在接下来的15年中继续支持高性能、大规模的生产工作负载，我们需要适应大型多核处理器、先进的指令集，以及在non-uniform内存层次结构中日益重要的局部性。其中一些改进将是透明的。Go 1.24将推出全新底层实现的map，以提高在现代CPU上的执行效率。同时，我们正在进行新的垃圾回收算法的原型设计，以适应现代硬件的能力和限制。一些改进将以新的API和工具的形式出现，以便Go开发者更好地利用现代硬件。我们正在研究如何支持最新的向量和矩阵硬件指令，以及应用程序如何构建CPU和内存的局部性。指导我们努力的一个核心原则是**可组合优化(composable optimization)**：优化对代码库的影响应该尽可能局部化，以确保对其余代码库开发的便捷性不受影响。

我们将继续确保Go的标准库在默认情况下是安全的，并在设计上也考虑到安全性。这包括不断努力将内置的、原生支持的FIPS认证加密功能纳入其中，使得需要FIPS加密的应用程序只需简单切换一个命令行标志即可使用。此外，我们还在不断改进Go的标准库包，并借鉴math/rand/v2的例子，考虑在哪里可以引入新的API，以显著提高编写安全和可靠的Go代码的便利性。

我们正在努力使Go在人工智能领域表现更好，同时也让人工智能更好地服务于Go，增强其在AI基础设施、应用程序和开发者辅助工具方面的能力。Go是一种非常适合构建生产系统的语言，我们希望它也能成为[构建生产级AI系统](https://go.dev/blog/llmpowered)的优秀语言。作为云基础设施的可靠语言，Go自然成为[大型语言模型（LLM）基础设施](https://ollama.com/)的理想选择。针对AI应用，我们将继续在流行的AI SDK中为Go提供一流的支持，包括[LangChainGo](https://pkg.go.dev/github.com/tmc/langchaingo)和[Genkit](https://developers.googleblog.com/en/introducing-genkit-for-go-build-scalable-ai-powered-apps-in-go/)。从一开始，Go就旨在改善端到端的软件工程过程，因此我们自然希望引入AI的最新工具和技术，以减少开发者的重复劳动，从而留出更多时间来进行更有趣的编程活动！

感谢您！

所有这一切的实现都离不开Go的杰出贡献者和蓬勃发展的社区。十五年前，我们只能憧憬Go所取得的成功以及围绕Go发展起来的社区。感谢每一位参与其中的人，无论贡献大小。我们祝愿大家在新的一年里一切顺利！

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