---
title: Go团队的工作方式
url: https://tonybai.com/2024/06/22/how-things-get-done-on-the-go-team/
published: '2024-06-22'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go团队的工作方式

![](../../assets/532e7dbb368bf0c7.png)


[本文永久链接](https://tonybai.com/2024/06/22/how-things-get-done-on-the-go-team) – https://tonybai.com/2024/06/22/how-things-get-done-on-the-go-team

在[Go 1.23版本](https://tonybai.com/2024/05/30/go-1-23-foresight/)即将发布(2024.8)之前，在[GopherCon 2024](https://www.gophercon.com/)开幕(2024.7)之前，Go团队成员[Cameron Balahan(Go产品负责人)](https://tonybai.com/2024/05/19/what-the-go-team-think-go-is/)、 Sameer Ajmani（Go团队工程总监）和[Russ Cox（Go团队技术负责人）](https://swtch.com/~rsc/)参加了业界知名的播客栏目[GoTime](https://changelog.com/gotime)的最新一期活动，主题是[“How things get done on the Go Team”](https://changelog.com/gotime/318)。在这期活动中，Go团队这三个leader分享了Go团队的工作方式，包括：Go团队的组成、现状与职责划分、与社区互动、决策与规划流程、产品管理等方面。这里基于[这期播客的脚本](https://github.com/thechangelog/transcripts/blob/master/gotime/go-time-318.md)提炼了其中主要的观点，贴到这里供大家参考。

## 1. Go团队组成及职责划分

Go团队从2007年诞生，至今已经有17年了。最初的Go团队由罗伯·派克(Rob Pike)、罗伯特·格瑞史莫(Robert Griesemer)和肯·汤普森（Ken Thompson）三个Go语言之父组成。之后Russ Cox和Ian Lance Taylor加入团队，形成了Go团队最核心的五人组。

Sameer Ajmani在Go 1.0发布前后加入，当时团队有10几个人，我们熟悉的[context包](https://tonybai.com/2022/11/08/understand-go-context-by-example)就是由他和Russ Cox一起设计并实现的。

Cameron Balahan在4年前加入Go团队，他也是今年在Google I/O大会上做“[Go是一个平台](https://tonybai.com/2024/05/19/what-the-go-team-think-go-is)”演讲的Go团队成员。

目前Google内部组织调整后，Go团队划归Google云团队管理，但其工作相对独立。 现在，Go团队由不同小组组成，主要包括三个小组：核心组、工具组和安全组。核心组负责编译器、运行时、链接器以及核心发布流程。工具组负责构建系统、Go命令、[Go VSCode IDE插件](https://code.visualstudio.com/docs/languages/go)以及[gopls语言服务器](https://github.com/golang/tools/tree/master/gopls)等。安全组则专注于[Go的供应链安全性](https://tonybai.com/2022/03/14/software-supply-chain-security-in-go)、[漏洞扫描和修复](https://tonybai.com/2022/09/10/an-intro-of-govulncheck)等方面。

尽管划分了不同的小组，但Go团队在日常工作中感觉就像是一个整体，各小组之间合作紧密。特定任务往往需要几个小组共同参与，例如漏洞检测与修复功能的开发就涉及了核心组、工具组和安全组的工作。

Go团队的工作由核心成员和开源社区两部分组成。核心成员负责构建整体框架与关键功能，而开源社区则为Go语言贡献众多细节上的改进和完善。两者紧密互动，形成良性循环。

## 2. Go团队与Go社区的互动

Go社区对语言发展做出了重大贡献，因此Go团队始终采取非常积极开放的态度与社区互动。包括但不限于使用Slack、邮件列表、Issue跟踪、Go博客等多种渠道倾听Go社区声音，接纳Go社区贡献。任何人都可以参与讨论并提出建议。

目前较为正式的决策途径是“[Go提案流程(Proposal Process)](https://github.com/golang/proposal#the-proposal-process)”。任何人都可以在这一平台上提出建议，供Go团队和全体社区评议。不论大小，只要通过审议，这些建议都可能被纳入语言或生态系统的未来发展规划。

除了直接参与讨论和决策外，Go社区还可以通过编写代码、发现并报告漏洞等方式为Go语言做贡献。Go团队会将高质量的外部代码整合进官方发行版。

## 3. 决策与规划流程

Go团队在做决策时，会优先考虑[目标的一致性](https://tonybai.com/2023/12/10/go-changes/)和充分的信息共享（比如公开利用[Go遥测工具](https://telemetry.go.dev/)采集的数据）。如果出现分歧，通常是由于目标不一致或信息不对称([以类型别名加入Go的过程为例](https://github.com/golang/go/issues/18130))造成的。因此，团队会先明确共同目标，并确保每个人掌握了相同的信息，然后再做出决策。

在规划过程中，Go团队首先要考虑Go语言既定的目标，即能够同时处理”生产规模化”(大量机器与海量数据)和”人力规模化”(大型项目与众多贡献者)。任何需要持续10年以上的重大决策，都必须符合这两个目标。

从长远来看，安全性与开源软件的可持续发展是Go团队需要重点关注的问题。他们将积极主导新标准与新模式，以提高整个行业的供应链安全性水平。

功能规划上，Go团队会同时考虑Go用户/社区和Google内部需求：Go用户和Go社区从Go中寻找价值，比如高生产力、高性能、高可靠和高安全；Google要确保其内部系统运行良好，开发人员满意，其系统可靠，安全，诸如此类。当然，Google也希望外部Go开发人员也这样做。同时，Google也希望那些外部的Go开发人员获得成功和快乐。为此，Go团队会寻求双赢解决方案。比如兼容性工作就是为了满足Kubernetes等重要系统的需求(IP地址解析)。在新特性开发过程中，Go团队会确保功能在整个生态链上保持一致性。

在发布规划上，Go团队需要考虑两个周期，一个是Go团队公开的[Go版本发布周期](https://go.dev/wiki/Go-Release-Cycle)，主版本一年两次。同时，Go团队leader还要考虑内部Google的规划周期，往往有一个年度计划周期，Go团队在其中执行 OKR、目标和关键结果。

## 4. 产品管理与Go的未来展望

作为Go产品负责人，CAMERON BALAHAN认为他会从优先级路线图、愿景角度以及Go团队为用户/社区和Google提供的价值的角度来弄清楚Go是什么，他认为Go是用于开发生产级软件的高效平台。作为编程语言，Go语言的产品管理理念就是构建一个高效且稳定的平台，支撑”生产级软件的高效开发”。

Go在解决云问题方面非常成功。云的大部分基础设施都是用Go编写的，并且Go在这方面做得很好，具有独特优势。Go团队希望Go在这一领域能够提供持续性的方案并取得持续性的成功，这决定了Go团队关注两个核心要素：生产效率和软件质量，这其中包括可靠性、安全性等重要的要素。

此外，Sameer认为人工智能的发展也为Go带来了新的机遇，随着越来越多的大公司、企业和初创公司希望在人工智能模型之上构建系统，而如何使Go成为构建智能基础设施以及基于大模型构建生产级、值得信赖、可靠的AI应用系统的语言，是下一个重要的前沿领域，Go团队将看到对此的大量需求，并认为Go是一个非常合适的选择。Go团队也在拭目以待！

编程语言的采用是一个缓慢的过程。Go语言目前已经到了一个关键的增长点，有望在新兴计算领域(AI)获得更广泛的使用。团队需要持续关注新的计算范式，及时调整以满足新需求。

Go社区对该语言的热爱是Go发展的重要动力。整个Go社区都是建立在Go之上的。Go团队本身无法建造所有东西，Go团队只要确保Go用户能够使用Go构建他们需要构建的东西，积极赋能社区发挥创造力，丰富Go的生态系统，才能继续让Go保持在人们需要的那种前沿，以便建立他们的业务、构建软件、构建他们需要的东西，生产级的高效、安全与可靠。

## 5. 不受欢迎的观点(GoTime常设环节)

- Sameer：context is fine。
- Cameron：I really like Go’s error handling.
- Russ：null pointers are fine. They’re kind of a fundamental fact of computers, is that memory can be zeroed.

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

不受欢迎的观点 很有趣:)