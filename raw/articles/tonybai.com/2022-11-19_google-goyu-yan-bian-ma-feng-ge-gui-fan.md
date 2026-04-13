---
title: Google Go语言编码风格规范
url: https://tonybai.com/google-go-style/
published: '2022-11-19'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Google Go语言编码风格规范

![](../../assets/9e6134bbc036be7b.png)


[本文永久链接](https://tonybai.com/google-go-style) – https://tonybai.com/google-go-style

本页面是2022年11月中旬Google发布的[Go语言编码风格规范](https://google.github.io/styleguide/go/index)的中译版。

## 关于

[Go语言编码风格指南(Guide)](https://tonybai.com/google-go-style/google-go-style-guide)系列文档汇集了当前编写可读的且地道的(idiomatic)Go代码的最佳方法。编码风格指南并非要求大家要绝对遵守，同时指南的内容也不能做到面面俱到。我们的目的是将编写可读Go代码的猜测工作(guesswork)降到最低，从而使刚接触这门语言的开发者能够避免常见的错误。这份指南的另外一个目的是为那些在Google内部审查Go代码的人提供统一的风格指导。

![](../../assets/de9e2c9d3bdae521.png)


### 文档

-
[风格指南](https://tonybai.com/google-go-style/google-go-style-guide)（https://google.github.io/styleguide/go/guide）概述了Google的Go编码风格的基础。这份文件是权威性的，并被用作**风格决定**和**最佳实践**两个文档中建议的基础。 -
[风格决定](https://tonybai.com/google-go-style/google-go-style-decisions)(https://google.github.io/styleguide/go/decisions) 是一份内容更详细的文档，总结了关于特定风格点的决定，并在适当的地方讨论了决定背后的理由。

这些决定可能偶尔会根据新的数据、新的语言特性、新的库或新出现的模式而改变，但Google的Go程序员并不需要及时跟进这个文档的变化。

[最佳实践](https://tonybai.com/google-go-style/google-go-style-best-practices)（https://google.github.io/styleguide/go/best-practices）记录了一些随着时间的推移而发展起来的模式，这些模式可以解决常见的问题，可读性好，而且足够健壮，可以满足对代码可维护性的要求。

这些最佳实践并非是权威性的，但我们鼓励Google的Go程序员尽可能使用它们，以保持代码库的统一和一致。

这些文档的目的是：

- 商定一套权衡备选风格的原则
- 记录Go编码风格的既定事项
- 记录并提供地道Go代码的典型例子
- 记录各种编码风格决定的利与弊
- 帮助减少Go可读性代码审查中的意外情况
- 帮助可读性代码指导者使用一致的术语和指南。

这些文档**并不打算**：

- 成为可读性代码审查中可提供的评论的详尽清单
- 列出所有的规则，希望每个人都能记住并随时遵守
- 取代在使用语言特性和风格方面的良好判断
- 为摆脱风格差异而进行的大规模修改提供理由

一个Go程序员和另一个Go程序员之间、一个团队的代码仓库与另一个团队的代码仓库之间总会有差异。然而，为了谷歌和Alphabet的最佳利益，我们的代码库应尽可能地保持一致(关于一致性的更多信息，请参见[指南](https://google.github.io/styleguide/go/guide#consistency))。为此，请自由地进行你认为合适的编码风格改进，但你不需要对你发现的每一个违反该风格指南的行为“吹毛求疵”。特别是，这些文档可能会随着时间的推移而改变，它们更不应该成为在现有的代码库中造成混乱的理由；使用最新的最佳实践编写新的代码，并随着时间的推移解决那个时期附近的问题就足够了。

重要的是要认识到，编码风格问题的本质上是个人的，而且总是有内在的权衡。这些文档中的许多指导意见是主观的，但就像gofmt一样，它们所提供的统一性具有重要价值。因此，不经过适当的讨论，风格建议不会改变，我们鼓励谷歌的程序员遵循风格指南，即使他们可能不同意其中的某些内容。

## 定义

下面是在整个系列文档中都会使用的词汇，其定义如下。

**权威性(Canonical)**：建立规范的和持久性的规则

在这些文档中，“权威性(canonical)”被用来描述一些被认为是所有代码（无论新旧）都应该遵循的标准，并且预计这些标准不会随着时间的推移而发生重大变化。权威性文档中的原则应该被代码作者和代码审查者共同理解，所以包含在权威性文档中的所有内容都必须满足一个高标准。因此，与非权威性的文档相比，权威性文档通常更短，规定的编码风格元素也更少。

https://google.github.io/styleguide/go#canonical

**规范性(Normative)**：旨在建立一致性

在这些文档中，“规范性(normative)”被用来描述一些约定俗成的代码风格元素，供Go代码审查员使用，以确保他们提出的建议、使用的术语和理由具有一致性。这些元素可能会随着时间的推移而改变，这些文档将反映这些变化，以便代码审查人员能够保持一致和最新。Go代码的作者不需要熟悉这些规范性文档，但这些文档将经常被代码审查员在可读性审查中作为参考。

https://google.github.io/styleguide/go#normative

**地道的**：常见的和熟悉的

在这些文档中，“地道的(idiomatic)”指的是在Go代码中普遍存在的东西，并且已经成为一种为人所熟悉的模式，很容易识别。一般来说，如果两者在上下文中起到相同的作用，那么我们应该优先采用地道的代码模式，而不是那些非地道的代码模式，因为地道的代码模式是代码的读者最熟悉的。

https://google.github.io/styleguide/go#idiomatic

## 其他参考

本指南假定读者熟悉[Effective Go](https://go.dev/doc/effective_go)，因为它为整个Go社区的Go代码提供了一个共同的基线。

下面是一些额外的资源，供那些希望自学Go编码风格的人和希望在Go代码审查中提供更多有关审查意见依据的链接的审查员使用。我们并不期望实践Go可读性过程的参与者熟悉这些资源，但它们可能会在代码可读性审查中作为上下文出现。

### 外部参考

### 相关的“厕所内侧”文章

[https://testing.googleblog.com/2017/10/code-health-identifiernamingpostforworl.html](https://testing.googleblog.com/2017/10/code-health-identifiernamingpostforworl.html)[https://testing.googleblog.com/2013/03/testing-on-toilet-testing-state-vs.html](https://testing.googleblog.com/2013/03/testing-on-toilet-testing-state-vs.html)[https://testing.googleblog.com/2014/05/testing-on-toilet-effective-testing.html](https://testing.googleblog.com/2014/05/testing-on-toilet-effective-testing.html)[https://testing.googleblog.com/2014/05/testing-on-toilet-risk-driven-testing.html](https://testing.googleblog.com/2014/05/testing-on-toilet-risk-driven-testing.html)[https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html](https://testing.googleblog.com/2014/05/testing-on-toilet-risk-driven-testing.html)

## 评论