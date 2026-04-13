---
title: Go 1.18对泛型的支持策略
url: https://tonybai.com/2021/10/28/expectations-for-generics-in-go-1-18/
published: '2021-10-28'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go 1.18对泛型的支持策略

![img{512x368}](../../assets/939f7a71c34487d4.jpeg)


[本文永久链接](https://tonybai.com/2021/10/28/expectations-for-generics-in-go-1.18) – https://tonybai.com/2021/10/28/expectations-for-generics-in-go-1.18

2021年10月中旬，[Go语言之父Rob Pike](https://mp.weixin.qq.com/s/rxzMQPgwLF2CLzyIKuTMMg)在github上的Go项目中发了一条issue：[建议不在Go 1.18的标准库中使用泛型](https://github.com/golang/go/issues/48918)。

不得不说“姜还是老的辣”！Rob Pike的理由很简单，[Go泛型](https://tonybai.com/2021/04/07/go-generics-use-type-sets-to-remove-type-keyword/)是Go诞生以来最大的一次语言变化，Go 1.18版本承载了太多的change，容易出错。并且Go核心开发团队也没有使用新泛型的经验，他建议Go核心开发团队应该多等待、观察和学习。我是十分赞同Rob Pike的建议的，不要把步子迈得太大。Go应该按照自己的节奏稳步前进。

Rob Pike的这个issue引发了Go核心团队与社区的热烈响应。离Go 1.18版本发布还有4个月左右的时间了，后续Go泛型到底如何落地，整个Go社区需要一个明确的方向。

今天，Go核心团队技术负责人[Russ Cox在golang-dev group发文](https://groups.google.com/g/golang-dev/c/iuB22_G9Kbo)，针对Rob Pike的issue介绍了Go 1.18版本与泛型当前进展与后续的支持策略，这确定了Go核心团队与社区的努力方向。这里粗略翻译一下供大家参考。

如果没有意外的严重问题，Go 1.18版本将包含对泛型的支持。泛型是Go1发布以来最重要的变化，当然也是我们有史以来最大的一次[语言变化](https://tip.golang.org/ref/spec)。这封邮件粗略解释了泛型的加入对我们和用户的意义。

任何Go的新功能特性，无论是语言还是库，都带有不确定性，包括不确定如何使用它们，不确定如何不使用它们，以及不确定有哪些微小的bug已经通过了现有的测试集。泛型也不能避免这种不确定性；事实上，因为泛型是一个大型的新功能，所以它的不确定性也相应地更大。

因为我们不知道使用泛型的最佳实践是什么，所以我们的文档将无法就何时使用泛型和何时不使用泛型给出精确、明确的答案。即便我们仍然可以并将给出粗略的泛型使用指南。作为比较，我们是在不间断地写了一整年的Go代码后，才写出了[Effective Go](https://tip.golang.org/doc/effective_go)的最初版本的。我们在泛型方面同样还没有较高水平使用经验，所以我们当然会提供关于如何使用泛型的文档，但我们短期内不能提供任何关于泛型代码风格和最佳实践方面的指南性文档。很简单，因为我们也欠缺这方面的实践与经验。

因为我们不知道编写泛型包的最佳实践是什么，所以我们发布的最初的泛型代码–特别是通过提案程序的maps和slices包–将首先放在golang.org/x/exp中，那里不能保证向后兼容。一旦我们有了更多的经验，我们希望能将其中一些包推广到标准库中。唯一例外的是constraints包，它是编写某些泛型代码的基础，它将在Go 1.18中就被添加到标准库中。

因为我们没有任何关于泛型的生产经验，所以我们会在发布说明中明确指出，在生产中使用泛型的时候应该适当谨慎。这并不是对Go核心团队出色工作的批评。这只是一个观察，泛型与大多数Go的变化不同。当我们[重写垃圾收集器](https://tonybai.com/2015/07/10/some-changes-in-go-1-5)或[改变调用惯例](https://tonybai.com/2021/08/20/using-register-based-calling-convention-in-go-1-17/)时，我们会在测试和生产中使用新的实现来运行谷歌的所有Go程序，这样就能很好地验证变化，揪出难以发现的错误。相比之下，用正在进行中的Go 1.18工具链重建非泛型代码并不能验证对泛型的支持，这意味着我们无法建立同样的信心。

综上所述，Go 1.18与其他Go 1.x版本一样具有向后兼容的承诺：我们不会破坏用Go 1.18构建的代码，包括使用泛型的代码。在最坏的情况下，如果我们发现Go 1.18的语义有一些致命的问题，并需要改变它们（例如在Go 1.19中），我们将使用go.mod文件的go版本指示符来确定该module中的源文件是使用Go 1.18还是Go 1.19+的语义。(我们预计不需要这样做！)

我们预想到一些包的作者可能会急于采用泛型。如果您正在更新您的软件包以使用泛型，请考虑将新的泛型API隔离到自己的文件中，并为其使用Go 1.18的构建标签（//go:build go1.18），以便[Go 1.17](https://mp.weixin.qq.com/s/y_pC6GYeZnKuHG8ycNy6rg)用户可以继续构建和使用非泛型部分。

同样值得注意的是，第三方工具可能不会在Go 1.18发布时完全支持泛型。我们正在与许多工具的作者交谈，并试图确保他们得到适当的更新，但各个工具都有自己的时间表。

我们收到的一个常见的问题是：考虑到所有这些不确定性，为什么不把泛型变成可选项加入Go 1.18？答案是，在这一点上，减少不确定性的唯一方法是让其默认可用。当我们在[Go 1.5版本](https://tonybai.com/2015/07/10/some-changes-in-go-1-5/)中让[vendor机制](https://tonybai.com/2015/07/31/understand-go15-vendor/)作为可选项加入时，发生的情况是几乎没有人真正使用它，直到Go 1.6版本默认开启它。所以Go 1.5版本没有减少我们对Go开发者使用vendor情况的不确定性。另一方面，Go 1.5版本无疑将生态系统分为”在标准Go下运行的代码”和 “在启用vendoring后运行的代码”两个部分。我们希望在这里尽可能地避免这种结果。

这里每个人可以做的最重要的事情就是写一些泛型代码，如果你发现了bug，不清楚的编译器错误等等，请让我们知道。我最近写了一些泛型数据结构，对整体的体验非常满意。我希望你也会这样；如果没有，请提交bug。谢谢!

[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强，欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


![img{512x368}](../../assets/617100c3677e1846.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

![](../../assets/769fc94e8bba6b65.png)


微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论