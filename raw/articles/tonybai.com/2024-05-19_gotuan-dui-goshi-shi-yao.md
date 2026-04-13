---
title: Go团队：Go是什么
url: https://tonybai.com/2024/05/19/what-the-go-team-think-go-is/
published: '2024-05-19'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go团队：Go是什么

![](../../assets/745481b56020297b.png)


[本文永久链接](https://tonybai.com/2024/05/19/what-the-go-team-think-go-is) – https://tonybai.com/2024/05/19/what-the-go-team-think-go-is

2024年的[Google I/O大会](https://io.google/2024/intl/zh/)如期而至。

这届大会的核心主旨毫无疑问是**坚定不移的以AI为中心**：Google先是发布了上下文长度将达到惊人的200万token的[Gemini 1.5 Pro](https://deepmind.google/technologies/gemini/pro/)，然后面对OpenAI GPT-4o的挑衅，谷歌在大会上直接甩出大杀器[Project Astra](https://deepmind.google/technologies/gemini/project-astra/)，视觉识别和语音交互效果，跟[OpenAI的GPT-4o](https://openai.com/index/hello-gpt-4o/)不相上下；接着，谷歌又祭出[文生视频模型Veo](https://deepmind.google/technologies/veo/)硬刚Sora，效果酷炫，时长超过1分钟，打破Sora纪录。最后Google CEO劈柴宣布：谷歌搜索将被Gemini重塑，形态从此彻底改变！用户不再需要自己点进搜索结果，而是由多步骤推理的[AI Overview](https://developers.google.com/search/docs/appearance/ai-overviews)来代办一切。

![](https://tonybai.com/wp-content/uploads/what-the-go-team-think-go-is-2.png)


不过，除了AI之外，Google在移动、Web和Cloud几个平台方面也为开发者带来了诸多精彩的内容，这其中就包括由Google Cloud团队带来的[“Profile-guided optimization with Go”](https://www.youtube.com/watch?v=FwzE5Sdhhdw)的演讲：

![](https://tonybai.com/wp-content/uploads/what-the-go-team-think-go-is-3.png)


注：目前，Go团队已归入Google Cloud团队管理。


该演讲由Cameron Balahan、Michael Pratt和James Ma三个人共同完成。其中长相颇似[电影“源代码”](https://movie.douban.com/subject/3075287/)主角杰克·吉伦哈尔的Cameron Balahan在演讲中首先登场，阐述了**Go团队眼中的Go究竟是什么**。

2022年，[美国计算机学会通讯(Communications of the ACM)](https://cacm.acm.org/)期刊2022年5月第65卷第5期将发表了一篇有关Go语言的综述类Paper：[《Go编程语言与环境》](https://cacm.acm.org//magazines/2022/5/260357-the-go-programming-language-and-environment/fulltext)，这篇文章由Russ Cox，Robert Griesemer，Rob Pike，Ian Lance Taylor和Ken Thompson等Go团队的大佬联合撰写，对10多年来Go演化发展进行了复盘，深入分析了那些对Go的成功最具决定性的设计哲学与决策，这算是Go团队第一次阐述Go究竟是什么。

而Cameron Balahan这次的演讲算是Go团队加入Google Cloud后对Go未来定位和演进上的一次说明，虽然简短，但对Gopher们也极具参考意义。在这篇文章中，我们就来看看Cameron Balahan所代表的的Go团队对Go语言的观点。

## Go是构建生产系统的高效平台

Go团队认为的第一点，也可能是最重要的一点是：**Go不仅仅是一种编程语言，它是一个完整的端到端构建生产系统的平台**。这一直都是Go团队的愿景。Go从一开始就是[为了在规模化的实际软件工程中提供便利](https://go.dev/talks/2012/splash.article)。并且，Go团队在Google内部将该愿景简化成了下面幻灯片中的使命陈述：Go提供了构建生产系统的最高效平台。

![](../../assets/dc78ba5a8fb7e2f6.png)


说Go很高效（Go is productive），是因为Go易于学习和维护，并且可以在团队之间扩展(scale)。

说Go是一个平台（Go is a platform），是因为它不仅仅是一种语言，它是一种端到端的开发者体验，包括IDE集成，构建和部署工具，监控工具，运行时工具，漏洞扫描等等，这些都是开箱即用的。

说Go是生产就绪的（Go is production ready ），是因为它可靠(reliable)、高效(efficient)、稳定(stable)和安全(secure)，这就是为什么大家会在企业中看到它的身影的原因，尤其是在关键业务系统和基础设施中，遍布整个云计算领域。实际上，这也是现代云计算本身建立在Go之上的原因。这并不仅仅指Google Cloud，我指的是所有主要的云服务提供商以及所有其他主要的参与者以及云工具和技术。

## Go的无限双循环

![](https://tonybai.com/wp-content/uploads/what-the-go-team-think-go-is-5.png)


无限双循环是一个很好的思考更广泛的软件开发生命周期的方式。左边的循环是内部开发循环，也就是大家编写代码的地方。你迭代地很快，寻求快速反馈和高效率。而右边的循环可以看作是外部循环，你已经部署了你的代码到生产中，你要监控和操作它。

因此，当Go团队将Go作为一个平台来考虑时，他们将考虑如何端到端地解决这整个过程，包括内部和外部循环。Cameron下面基于这个循环从developer velocity(开发人员效率)、security(安全)和performance(性能)等方面分别举一些Go如何解决这些问题的例子。

### developer velocity(开发人员效率)

![](https://tonybai.com/wp-content/uploads/what-the-go-team-think-go-is-6.png)


Go有一些旨在为了最大化你团队的开发人员效率的语言特性、工具和库。包括了从编写代码到将其推送到生产，再到之后可靠运维的整个过程。

Go团队提供IDE集成，包括为Visual Studio Code开发的插件，使其能够轻松利用其余工具链的特性。Go还提供了强大的并发模型，通过Goroutine实现。Go有内置的格式化工具、内置的测试框架和内置的调试器。Go编译器本身构建静态独立二进制文件，不依赖任何系统范围的依赖项或单独的运行时，这使得部署比其他语言更容易、更安全、更快。这是一种端到端的解决方案，用于获取和维护开发人员效率。

### security(安全)

![](../../assets/5069334a8c93b3ef.png)


Go在安全性方面是领先者，这一点Go也是端到端解决的。如果你在关注最新的XZ软件供应链攻击新闻，你就会知道这是多么重要，也许比以往任何时候都更重要。这是Go团队非常重视的一个领域，因为他们已经看到在其他语言生态系统中，当一个流行的依赖项被破坏时会发生什么。

由于Go被用于云中所有这些关键基础设施，Go团队认识到安全性是Go应该提供的最重要的功能之一。从依赖管理系统开始，Go先后有了Go Module Mirror、Checksum Database和pkg.go.dev网站，它们都会警告你所依赖的库是否被篡改或遭受已知漏洞。

此外，Go的IDE集成很深入。如果你使用Go的VS Code插件，你会在IDE中就收到关于依赖项中的漏洞警告，包括你是否实际上从代码中调用了这些漏洞。这样，在真正依赖它们进入生产环境之前，你就知道了依赖项的安全态势。Go也是唯一一种将[模糊测试](https://tonybai.com/2021/12/01/first-class-fuzzing-in-go-1-18)内置并集成到其工具链中的主流语言。模糊测试就像一种自动化的测试类型，它会智能地操纵你程序的输入，以找出bug和漏洞。

最后，Go有兼容性承诺，从Go 1.0开始就确保没有破坏性更改。这意味着升级很容易，这使保持最新的安全修复变得容易，跟上增强功能也很容易。去年在[Go 1.21](https://tonybai.com/2023/08/20/some-changes-in-go-1-21)中，Go团队在此基础上增加了[向前和向后兼容性特性](https://tonybai.com/2023/09/10/understand-go-forward-compatibility-and-toolchain-rule/)。Go团队确实将兼容性视为不仅仅是一种便利，更是一种关键的安全特性。

### performance(性能)

![](../../assets/50fe2268aa4d61bb.png)


Go的标准库功能丰富且健壮，并针对性能进行了优化。你可以真正构建任何东西，而无需导入一些重型库或框架。Go还有一个自我调优的垃圾收集器。如果你曾经花时间为Java调优垃圾收集器，你就会知道这简直就像是一份全职工作。它可能需要耗费的时间和你最初编写代码一样长。在Go中，垃圾收集器开箱即用，运行高效，并会自动调整以适应你的工作负载需求。 当然，还有[Profile Guided Optimization(PGO)](https://go.dev/doc/pgo)，使用过PGO的开发者都很喜欢它。有些开发者甚至已经看到了令人印象深刻的性能提升。

### 开箱即用(out of the box)

![](../../assets/5359a2fe3e261902.png)


图片中所有这些特性都符合**开箱即用**的端到端解决方案这一框架，正是这使Go成为构建生产系统最高效的平台。

Go团队在做所有这些的同时，也获得了来自用户的非常出色的反馈。大部分Go用户真的很喜欢Go。我们在调查中一直看到这一点，客户满意度水平（93%）实际上在业内是罕见的。

## Go特性与客户价值定位

![](../../assets/39211958ed96463c.png)


第一行可视为与生产力相关的内容。Go支持快速入门、快速迭代、快速构建真正可扩展的生产应用程序。所有这些都转化为你更快获得价值。

第二行是关于可靠性的，包括安全性、兼容性以及所有能够减少你长期维护和运维负担的内容。负担越小，你的总体拥有成本就越低，你就有更多时间和资源专注于推动业务增长的新事物。

第三行是关于云的。Go就像是为云量身定制的一样。Go启用的库、集成和架构都是为云而设计的，而不是后来才重新调整以适应云。因此，你将比使用其他语言时能更快更轻松地实现云的优势。

最后，Go用户是快乐的。他们无论在哪里都很开心。而且在Google Cloud上，他们尤其开心。每个人都喜欢开心的开发人员和运维人员。

## 小结

Google I/O 2024大会上Go团队代表对Go语言及其在软件工程领域的定位做了新的诠释：**Go不仅是一种编程语言，更是一个端到端构建生产系统的高效平台**。

Go团队认为Go易学易维护，可扩展，同时可靠、高效、稳定和安全，适合在企业中使用，尤其是关键业务系统和基础设施领域。

文中介绍了将Go的愿景拆解为Go的”无限双循环”的理念。其中内循环侧重开发效率，外循环侧重可靠运维。Go在开发人员效率、安全性和性能等方面都有出色的解决方案。如IDE集成、并发模型、格式化工具、测试框架、调试器、静态部署等有助提高开发效率；依赖管理、漏洞扫描、模糊测试等确保安全性；垃圾回收、编译优化等提升性能。

此外，Go兼具快速入门、快速迭代、可扩展构建、安全可靠、低运维成本、云原生设计等特性，能让客户快速获得价值、降低总拥有成本、享受云优势，获得高客户满意度。Go可视为构建现代云基础设施的理想语言。

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

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论