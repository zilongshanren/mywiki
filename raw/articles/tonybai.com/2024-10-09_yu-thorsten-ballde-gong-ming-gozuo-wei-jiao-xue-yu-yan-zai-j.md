---
title: 与Thorsten Ball的共鸣：Go作为教学语言在技术写作中的优越性
url: https://tonybai.com/2024/10/09/resonating-with-thorsten-ball-on-go-in-technical-writing/
published: '2024-10-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 与Thorsten Ball的共鸣：Go作为教学语言在技术写作中的优越性

![](../../assets/77f4972cb7d30ff3.png)


[本文永久链接](https://tonybai.com/2024/10/09/resonating-with-thorsten-ball-on-go-in-technical-writing) – https://tonybai.com/2024/10/09/resonating-with-thorsten-ball-on-go-in-technical-writing

近日，两本备受好评的畅销书《[用Go语言自制解释器(Writing An Interpreter In Go)](https://book.douban.com/subject/35909085/)》和《[用Go语言自制编译器(Writing A Compiler In Go)](https://book.douban.com/subject/35909089/)》的作者、前[Sourcegraph](https://github.com/sourcegraph/sourcegraph-public-snapshot)工程师[索斯藤·鲍尔（Thorsten Ball）](https://thorstenball.com/)发表了一篇名为“[Glad I did it in Go](https://registerspill.thorstenball.com/p/glad-i-did-it-in-go)”的文章。在这篇文章中，Thorsten表达了他对8年前编写这两本书时选择Go语言作为教学语言的庆幸之情。

![](../../assets/6eba73848cfe4d7b.png)


2021年12月17日，我的第一本Go技术图书[《Go语言精进之路vol1和vol2》](https://item.jd.com/13694000.html)出版了，至今好像是已经是第4次重印了(修正了[勘误表](https://github.com/bigwhite/GoProgrammingFromBeginnerToMaster/blob/main/errata.md)中的所有瑕疵)。作为该书作者，当我读到Thorsten Ball的这篇回顾文章时，我感到了一种强烈的共鸣，其中的许多观点与我的不谋而合。尽管我们的书主题不同，但**我们都体会到了选择Go语言作为教学语言进行技术写作的巨大优势**。

![img{512x368}](../../assets/547482cabd3c0134.png)


在这篇文章中，在《[Go语言精进之路](https://book.douban.com/subject/35720728)》出版即将三年之际，我想借此机会分享我的thoughts，探讨Go语言如何为技术作者提供了独特的优势。

## 1. Go的稳定性和向后兼容性

首当其冲的优势就是Go的稳定性和向后兼容性，它们给我留下了深刻的印象。三年快过去了，当初《Go语言精进之路》中使用[Go 1.16版本](https://tonybai.com/2021/02/25/some-changes-in-go-1-16)编写的[代码示例](https://github.com/bigwhite/GoProgrammingFromBeginnerToMaster/)，在最新的[Go 1.23版本](https://tonybai.com/2024/08/19/some-changes-in-go-1-23/)中仍然可以完美运行，几乎不需要任何修改。这种稳定性不仅让我的书保持了长期的相关性，也让读者能够轻松地在不同版本的Go环境中实践书中的内容。正如Thorsten所提到的，他只需添加一个简单的[go.mod文件](https://go.dev/ref/mod)，就能使8年前的代码适应新的[Go版本依赖管理和构建模式](https://tonybai.com/tag/gomodule)，这种对更新需求的最小化，在快速发展的编程语言世界中，实属难能可贵。

Go的稳定性还体现在语法特性上，《Go语言精进之路》一书中讲解的语法和惯用法在今天依然是完全有效的，除了[loopvar的语义变更](https://tonybai.com/2024/02/18/some-changes-in-go-1-22/)可能会让极少的内容略显“过时”。Thorsten也提到了这种稳定性的好处：8年前的代码运行[golangci-lint](https://github.com/golangci/golangci-lint)得到的警告与当时是相同的(便于读者复现书中的情形)，其书中代码风格仍然符合现在的Go惯例写法。

此外，Thorsten还提及了Go工具链和标准库的稳定性：8年来Go的工具链几乎没有变化，新手容易上手。像Thorsten一样，我也发现Go的开发环境和工具在多年来保持了惊人的一致性。这意味着书中介绍的开发实践和工具使用方法始终有效，大大降低了内容过时的风险。对技术作者来说，这种稳定性是无价的，它允许我们专注于概念和最佳实践，而不是不断更新工具相关的内容。

以上Go的这些稳定性和向后兼容，让我的书中的内容具有了更为持久的生命力，书中内容的价值变得更为长效，也大大减轻了作者对书籍维护和更新的负担，在技术书籍的生命周期中，这一点尤为宝贵。

## 2. Go的简洁性和可读性

其次，在编写《[Go语言精进之路](https://tonybai.com/2022/07/07/gocn-community-go-book-club-issue2-go-programming-from-beginner-to-master)》时，我发现Go的简洁性和可读性为技术写作带来了极大的帮助。许多读者反馈说，即使他们之前没有Go的经验，也能快速上手并理解书中的概念。这种简洁和直观性让Go也成为了编写教程和教学材料的理想选择。此外，正如在项目中所经历的那样，Thorsten也强调了Go语言的语法简单直观在教学过程中的所展现的优势，它既能让初学者快速入门，也能使得书中关于解析器和编译器实现的核心思路能够被清晰地传达给读者，即便在探讨复杂的概念时，也能保持清晰明了。

同时，Thorsten强调内置的gofmt带来的通用风格和测试框架也简化了学习过程，让读者可以专注于理解核心概念和解释器/编译器的实现，而不是纠结于环境设置和代码风格。

## 3. Go代码易于理解和翻译

Thorsten提到许多读者在从未写过Go代码的前提下，能够将他的Go代码轻松翻译成其他语言，这体现了Go在跨语言学习和理解方面的优势，有利于**扩大了书籍的受众群体**，而不仅限于Go开发者。Go社区的多样性和活跃度也为此做出了重要贡献，各种语言背景的开发者都能在Go中找到共鸣。这种跨语言的适应性不仅拓展了书籍的应用范围，也增强了其教育价值。

## 4. 小结

回顾这三年，我与Thorsten一样，越发感慨选择Go作为教学语言进行技术写作是多么明智的决定。当然，我这本书本身就是围绕Go语言展开的^_^，这与Thorsten的书籍主题有所不同。Thorsten在8年前高瞻远瞩地选择Go，才着实令人钦佩，要知道那时的Go刚刚发布[1.6版本](https://tonybai.com/2016/02/21/some-changes-in-go-1-6/)。Go语言不仅是一个强大的编程工具，更是技术作者的得力助手。它的稳定性、简洁性、易理解性和良好的翻译能力，以及稳定优秀的工具链，为我们创造高质量、长寿命的技术内容提供了坚实的基础。

与Thorsten Ball一样，我也为选择Go感到庆幸。看到自己的作品能够持续为读者提供价值，这种成就感是无可比拟的。Go语言在技术写作中展现出的优越性，不仅使我们的书籍能够经受时间的考验，还为整个技术写作领域树立了新的参考标杆。

展望未来，我相信Go语言将继续是技术作者的优秀选择。它不仅是一种编程语言，更是连接作者、读者与技术的桥梁。

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2024年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。同时，我们也会加强代码质量和最佳实践的分享，包括如何编写简洁、可读、可测试的Go代码。此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


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