---
title: 这可能是最权威、最全面的Go语言编码风格规范了！
url: https://tonybai.com/2022/11/26/intro-of-google-go-style/
published: '2022-11-26'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 这可能是最权威、最全面的Go语言编码风格规范了！

![](../../assets/9e6134bbc036be7b.png)


[本文永久链接](https://tonybai.com/2022/11/26/intro-of-google-go-style) – https://tonybai.com/2022/11/26/intro-of-google-go-style

每种编程语言除了固定的语法之外，都会有属于自己的**地道的(idiomatic)写法**。其实，自然语言也不例外，你想，你用心想想是不是这样。

语言的设计者们希望开发人员都能编写统一风格的地道的代码，这样不仅代码可读性好，便于社区统一代码风格，而且针对惯用法的优化也可能会让地道的代码拥有更好的运行效率。语言团队也会不遗余力的通过各种方式([文档](https://go.dev/doc)、[blog](https://go.dev/blog)、[演讲](https://go.dev/talks)、[书籍](http://www.gopl.io)、视频等)向开发者传授如何写出更地道、更高效、可读性更好的代码。

以Go语言为例，为了能让Gopher更好的了解如何写出高效、地道的Go代码，Go开源伊始就编写了[《Effective Go》](https://go.dev/doc/effective_go)和[《Go FAQ》](https://go.dev/doc/faq)两篇文档。前者负责介绍Go惯用法，后者则担负着将Go语言设计层面的问题以及解决思路与Gopher进行对齐的重任：

![](../../assets/68b3ce7dd535b4ee.png)


同时，Go语言之父们以及Go团队核心成员们在早期十分活跃并不遗余力的向Go社区推广Go的惯用法，Go官方站点上积累的各个早期的[blog文章](https://go.dev/blog/all)以及[各个talk资料](https://go.dev/talks/)也成为了gopher学习地道Go编码的重要参考：

![](../../assets/7b11e2f1797436b0.png)


这些资料为了全世界Gopher的Go编码风格建立了基线。大多数情况下只要遵循这些资料并借助gofmt工具的自动格式化就可以写出风格比较地道的Go代码了。

然而《Effective Go》更像是说明地道风格Go代码的总体原则，不能“面面俱到”的覆盖每个编码的细节，而大公司对内部代码的风格一致性有着严格的要求。这不仅是高质量的要求，也是内部高效协作的要求。于是在若干年后，一些较早接纳Go且成为Go重度用户的大厂和初创公司结合自己的工程实践纷纷推出了公司内使用的Go编码风格规范，这里就包含我们耳熟能详的[Uber](https://tonybai.com/2019/10/12/uber-go-style-guide/)、[鹅厂](https://github.com/Tencent/secguide)、[sourcegraph](https://about.sourcegraph.com/handbook/engineering/go_style_guide)、[CockroachDB](https://github.com/cockroachdb/cockroach/blob/master/docs/style.md)、[gitlab](https://docs.gitlab.com/ee/development/go_guide/) 等。这些Go代码风格指南也成为Go社区开发人员在代码风格规范性方面的**重要参考**。

不过，这些公司推出的代码风格指南有一个共同特点，那就是**规范性有余，但权威性和全面性不足**。Go社区都期待这Go语言的发源地：Google公司的Go编码风格规范的推出。之前，Google已经在其[style guide站点](https://google.github.io/styleguide/)上推出了其内部使用的很多主流编程语言的style guide，包括：[C++](https://google.github.io/styleguide/cppguide.html)、[Java](https://google.github.io/styleguide/javaguide.html)、[C#](https://google.github.io/styleguide/csharp-style.html)、[JavaScript](https://google.github.io/styleguide/jsguide.html)、[Python](https://google.github.io/styleguide/pyguide.html)、[Shell](https://google.github.io/styleguide/shellguide.html)等。

![](../../assets/c3d5a0e8986e41ec.png)


在2022年11月份中旬，就在Go刚刚过完其[第13个生日](https://tonybai.com/2022/11/11/go-opensource-13-years)而步入青少年成长阶段之际，[Google内部的Go语言编码风格规范](https://google.github.io/styleguide/go/)终于出现在其style guide站点上了！

![](../../assets/de98ed1ce05b0b6f.png)


不过，在介绍Google Go style guide前，我们首先要知道有关google style guide的几点内容：

- 这些guide的主要目的是Google内部自用，所有开发人员、代码审查人员、代码可读性导师必须要遵守并达成一致；
- 所有语言的style guide都会随着语言的演进而持续更新优化；
- 各个语言的style guide的结构布局与写作风格都不相同；
- 这些style guide都不接受Google之外人员的pr。

如上图，Google内部的Go语言编码风格规范系列文档目前由四个部分组成，它们分别是概述、指南、决定和最佳实践。根据概述篇的内容我们可以大体知道每篇文档的功用。这一系列文档汇集了当前编写可读的且地道的(idiomatic)Go代码的最佳方法，其目的是使刚接触这门语言的开发者能够避免常见的错误，同时也为那些在Google内部审查Go代码的人提供统一的风格。

这些文档的重要性略有不同：

-
[指南篇](https://tonybai.com/google-go-style/google-go-style-guide)（https://google.github.io/styleguide/go/guide）概述了Google的Go编码风格的基础。这份文件是权威性的，并被用作**风格决定**和**最佳实践**两个文档中建议的基础。 -
[决定篇](https://tonybai.com/google-go-style/google-go-style-decisions)(https://google.github.io/styleguide/go/decisions) 是一份内容更详细的文档，总结了关于特定风格点的决定，并在适当的地方讨论了决定背后的理由。这些决定可能偶尔会根据新的数据、新的语言特性、新的库或新出现的模式而改变。 -
[最佳实践篇](https://tonybai.com/google-go-style/google-go-style-best-practices)（https://google.github.io/styleguide/go/best-practices）记录了一些随着时间的推移而发展起来的模式，这些模式可以解决常见的问题，且可读性好并足够健壮，可以满足对代码可维护性的要求。

初步阅读了一下，这系列文档份的确算是目前最权威、最全面的Go语言编码风格规范了！其中决定篇和最佳实践篇涵盖的内容非常全面，内容和例子也非常到位。只不过，这套规范由于刚刚推出，还有很多改善优化和标记todo的地方。并且，其中有些内容是与Google是强相关的，但这依然是一份值得每个gopher认真阅读的资料。

此外，整套文档中经常引用一个名为“Go tips”的文档，不过该文档尚未放出，但从行文中引用的go tips的章节标题来看，很值得期待！

本博客正在将这套文档翻译为中文供大家参考，目前[概述篇](https://tonybai.com/google-go-style)、[指南篇](https://tonybai.com/google-go-style/google-go-style-guide)和[决定篇](https://tonybai.com/google-go-style/google-go-style-decisions)和[最佳实践篇](https://tonybai.com/google-go-style/google-go-style-best-practices)均已经初步翻译完毕(机翻辅助)。待go tips文档发布后，这里也会将其译为中文。

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

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