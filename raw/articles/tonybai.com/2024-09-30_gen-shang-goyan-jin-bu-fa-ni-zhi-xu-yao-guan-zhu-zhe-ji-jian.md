---
title: 跟上Go演进步伐，你只需要关注这几件事儿
url: https://tonybai.com/2024/09/30/how-to-keep-up-with-go-evolution/
published: '2024-09-30'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 跟上Go演进步伐，你只需要关注这几件事儿

![](../../assets/0a1cc6ba311c10ff.png)


[本文永久链接](https://tonybai.com/2024/09/30/how-to-keep-up-with-go-evolution) – https://tonybai.com/2024/09/30/how-to-keep-up-with-go-evolution

Go语言以其简洁、高效和强大的特性赢得了众多开发者的青睐。与许多主流编程语言有着明确的演进Roadmap或下一个版本spec不同，Go的演进过程更加独特、灵活与开放。这种看起来不那么正式和严肃的演进方式却也能让Go快速响应开发者的需求，同时保持语言的稳定性和一致性。

作为一名Go开发者，跟上Go的演进步伐，甚至是参与到这个激动人心的过程中来，不仅能让你更好地利用语言的新特性，还能帮助你更深入地理解Go的设计哲学。

但很多Go开发者只知道每年Go有两次的大版本Release，并通过大版本的Release Notes来了解Go的演进。这无可厚非，但对于那些想及时跟进Go演进的Gopher来说，光有一年两次的Release Notes还是不够的的，很难及时跟进Go的演进决策。

但如果直接到Go语言项目的issue中去翻阅，面对Go丰富的社区讨论和频繁的更新，你可能会感到无从下手。别担心，本文将为你指明方向，让你只需关注几个关键点，就能轻松跟上Go的演进步伐。

## 1. 开发计划早知道

Go的版本规划具有很高的灵活性。每个Go 1.x版本在开发前，Go语言项目相关人员都会在[golang-dev讨论组](https://groups.google.com/g/golang-dev/)上发布一个帖子，这个帖子通常的标题为”Planning Go 1.x”，例如”Planning Go 1.23″，如下图：

![](../../assets/7ee16201dd5f5d57.png)


很多contributor，无论是Go团队的，还是外部贡献者的，会在该帖子下面留下自己的plan(注意：这些plan中的特性可不一定会在最终的版本中发布)，然后等main tree开放后，就会将已经准备完毕的[cl(changelist)](https://google.github.io/eng-practices/review/developer/) merge到main tree中去，或开始提交cl，等待Go团队或社区的开发者进行评审。

当然对于Go 1.x这样的大版本，Go团队会在github建立专门的[milestone](https://github.com/golang/go/milestones)跟踪，大家也可以在对应的milestone中看到该版本带来的新特性等，下图是目前正在积极开发的[Go 1.24版本里程碑](https://github.com/golang/go/milestone/322)：

![](../../assets/abeec126b6833e23.png)


通过查看这些Plan或定期查看Go 1.x里程碑，你可以提前了解Go的发展方向，为新版本的到来做好准备。

当然如果要了解那些更早的Go演进的决策，我们还得关注和跟踪下面的Proposal Project看板和三个关键的issue。

## 2. Proposal Project看板和三个关键的Issue

Go在早期并没有规范的proposal提案流程，更多是由Rob Pike、Robert Griesemer等三个Go语言之父，外加Ian Taylor和Russ Cox讨论确定，这一状态在[Russ Cox建立明确的Go proposal提案流程](https://github.com/golang/proposal/)后结束，提案流程是Go团队审查提案并决定接受或拒绝提案的过程。Russ Cox在提案流程中明确了Go项目的开发过程是设计驱动(design-driven)的，必须首先对语言、库或工具的重大更改进行讨论（包括Go语言项目主仓库和所有golang.org/x仓库中的API更改，以及对go command的命令行更改），并在实现这些设计之前进行正式记录。

Go团队目前使用Proposal Project看板和GitHub Issues来追踪语言的演进，下面我们来看看这个看板和值得关注的三个Issue。

Proposal Project看板是Go团队跟踪proposal的全局视图，当然要理解该看板，我们需要先来简单看看Go的proposal流程以及每个提案的生命周期是怎样的。

Go Proposal流程并不复杂，可以概括为下面这个示意图：

![](../../assets/7c814afa8198a44e.png)


该流程图展示了Go提案流程的几个主要步骤：

- 任何人都可以作为提案作者，在Go项目上创建一个简短的issue来描述提案。
- Go团队成员以及任何Go社区成员在issue上进行初步讨论，由一组人组成的
**Go提案审核委员会**决定是接受提案、拒绝提案，还是需要进一步的设计文档。 - 如果需要进一步的设计文档，提案作者会撰写一个详细的设计文档。
- 在设计文档的评论减少/收敛后(意见趋于一致后)，由Go提案审核委员会会进行最终讨论，决定接受或拒绝提案。

Go提案审查委员会使用GitHub项目看板来跟踪提案的状态并管理提案的生命周期(如下图所示)：

![](../../assets/cd7bf65e209bf344.png)


该看板针对每个提案issue设置了几个生命周期状态：

- Incoming：新提交的提案
- Active：正在积极讨论的提案
- Likely Accept / Likely Decline：可能被接受或拒绝的提案
- Accepted / Declined：已被接受或拒绝的提案
- Hold：需要设计修订或需要几周或更长时间才能获得附加信息的提案，这类提案一旦准备就绪，还会回到Active状态

了解了上述Go提案与审核流程，再看下面的几个关键Issue就容易多了。

![](../../assets/c3dd38b6a8833b20.png)


该issue于2019年8月创建，其创建者为前Go团队技术负责人Russ Cox。这是目前Go语言项目最核心的追踪Issue，它记录了Go提案审查会议的纪要，通常每周更新一次(如下图所示)：

![](../../assets/5f11945851b61e92.png)


我们看到内容包括：

- 发布当周已经决策为Accepted和Declined的proposal列表
- 后续Likely Accept和Likely Decline的proposal列表
- 正处于Active讨论的proposal列表
- 当前处于Hold状态的proposal列表

和Go提案看板不同，该issue是对提案Issue的状态变更的记录，Gopher可以第一时间看到每周Go提案的状态更新。

由于[Russ Cox已经辞去了Go团队技术负责人的头衔](https://mp.weixin.qq.com/s/2Sy6K_dU1j3tZZiyyfCTDQ)，从2024年9月下旬开始，Go团队新的技术负责人[Austin Clements](https://github.com/aclements)将继续主持提案审核会议，并更新该Issue。

除了Review meeting minutes这个重要的issue外，还有两个issue值得我们关注，通过它们，我们可以及时了解到Go编译器和运行时的演进以及Go语法特性的演进。

Go编译器和运行时团队定期（大约每周）召开会议，讨论Go编译器和运行时的后续开发和演进事宜，该会议是Google Go团队的内部会议，但Go团队觉得Go社区有必要了解这个会议上的一些讨论议题、过程与会议结论，从而知道Go编译器和运行时团队正在以及将要做什么。

于是前Go团队成员[Jeremy Faller](https://github.com/jeremyfaller)于2021年1月创建了该Issue，向Go社区发布Go编译器和运行时的最新演进动向。

![](../../assets/b7fa8a2d12d79f14.png)


之前Go编译器和运行时团队的负责人是Austin Clements，如今是[CherryMui](https://github.com/cherrymui)。

编译器和运行时之外，Gopher最关心的就是Go语法的演进以及Go语言规范的变更，这个事儿是由Go语言之父之一的Robert Griesemer亲自抓的。在2019年8月，Robert Griesemer就建立了跟踪Go语法变化的issue，当然最初是要跟踪Go2的演进，后来Go泛型落地后，Go2彻底融入了Go1，该issue也就变成了跟踪Go语法演进的Issue。Robert Griesemer主持的Go语言变更审查会议每月举行一次，并将会议讨论的记录发布到该Issue上。

![](../../assets/bafb812f30d8e8e1.png)


## 3. Discussion与Russ Cox博客

关于Go语言演进的动向，还有两个渠道可以关注，一个是[Go团队在github repo上发起的discussion](https://github.com/golang/go/discussions)，[Russ Cox在2021年7月启用了discussion](https://github.com/golang/go/discussions/47139)，旨在寻找一个地方来扩大许多人可能想要参与的讨论。当前，该discussion仅针对非常有限的事项添加讨论，并且只有少数Go核心团队的人才有发起discussion的权限。一些在前几个版本的重要语言特性变化以及标准库的变化，都在这里进行了充分的讨论，比如[loopvar语义修正](https://tonybai.com/2024/02/18/some-changes-in-go-1-22)、[自定义iterator](https://tonybai.com/2024/06/24/range-over-func-and-package-iter-in-go-1-23)、[开启标准库major版本更新的math/rand/v2](https://tonybai.com/2024/02/18/some-changes-in-go-1-22)以及[gonew工具](https://tonybai.com/2023/08/11/introduction-to-the-gonew-tool)等。

![](../../assets/e074ed6b5cbdefbc.png)


另外一个则是[Russ Cox的博客](https://research.swtch.com/)，作为Go项目团队前技术负责人，作为Rob Pike的接班人，Russ Cox很好地完成了承上启下的作用，并为Go的演进和发展确立了演进框架、方法以及方向。Russ Cox经常在自己的博客上先“憋大招，做铺垫”！最典型的就是[vgo](https://research.swtch.com/vgo)，也就是go module的前身，在短短几周内Russ Cox在博客上发表了7篇关于vgo的设计思路文章，为后来Go module的落地奠定了基础，至此基本上不再有Gopher抱怨Go依赖管理了。Russ Cox现已辞去Go技术负责人的头衔，后续是否还能在他的博客上看到Go相关的新特性的设计，让我们拭目以待！

## 4. 小结

在快速发展的技术环境中，Go语言以其独特的演进方式和灵活的开发计划，吸引了越来越多的开发者。本文介绍了如何及时有效地跟踪Go的演进的方法，包括关注大版本开发计划、Proposal Project看板和关键的issue，帮助Gopher及时了解语言的新特性与设计决策。通过参与讨论和关注Go团队的动态，开发者不仅能掌握最新的语言更新，还能深入理解Go的设计哲学和发展方向。希望每位Gopher都能抓住这些资源，与Go语言共同成长，提升自己的开发技能。

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