---
title: Go语言之父谈Go编程语言与环境
url: https://tonybai.com/2021/10/06/the-go-programming-language-and-environment/
published: '2021-10-06'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go语言之父谈Go编程语言与环境

[本文永久链接](https://tonybai.com/2021/10/06/the-go-programming-language-and-environment) – https://tonybai.com/2021/10/06/the-go-programming-language-and-environment

![](../../assets/aa25407f3b89c926.png)


2021年中旬，Go语言联合创始人Rob Pike应邀在线出席由UNSW Computing(悉尼新南威尔士大学计算机)组织主办的[John Lions Distinguished Lectures](https://www.youtube.com/channel/UCghXRiDxEojP599HKE_nRZg)，会上Rob Pike以Go之父身份讲述了究竟是什么将Go语言塑造成今天的这个样子以及进入Go生态系统的其他一些事物。

![](../../assets/0b9b16b7161f8932.png)


Rob Pike关于Go的观点总是高屋建瓴的，从[这个talk](https://www.youtube.com/watch?v=YXV7sa4oM4I)中我们可以了解Go语言演化的来龙去脉，这对于我们理解Go、理解Go演化方向、理解Go生态会有较大帮助。由于仅有视频资料，这里将视频中的slide截图按顺序贴在这里，并配以slide中没有但talk中有的一些rob pike的重要观点，供大家参考。

![](../../assets/5128e11b5c56a638.png)


Rob Pike：

- (谦虚的说)Go还不能算是主流语言，但Go在全世界范围的影响力与发展远超当初预期。
- 我们知道：在众多编程语言中，Go可能不是那种interesting的语言。在当时，Go甚至不是一种有技术优势的语言。我们并没有试图推动编程语言理论或设计甚至实践的进步。我们对此并不介意，因为这不是我们的目标。
- 不知何故，这种语言已经成功地接管了云世界。它是主导docker、kubernetes以及基本上云原生计算基金会中的所有东西的开发语言，当然也包括这之外的其他很多项目。
- 多年前，有人预测Go是云计算基础设施语言，但现在这已经成为现实。

那么问题来了：一种本质上无人喜欢的语言是如何最终变得如此重要了呢？究竟发生了什么？

![](../../assets/8e36e4bcf0830688.png)


Rob Pike给出答案：

- 一门编程语言的成功取决于很多东西，而不仅仅是语言本身。
- Go团队从一开始就知道这一点，于是他们不再局限于创造一门新编程语言，而是将目标定为
**创造一种编写软件的更好的方法上**。因此这门新编程语言将被用于处理当时所用语言所解决不了的诸多问题：包括上面slide中列举的诸多问题。 - 虽然编程语言本身可以解决上面的一些问题，但仅语言本身还远不够。

![](../../assets/5a841a0e92050207.png)


Rob Pike：

- 我们遇到的一个最大的问题就是scale，并且scale拥有多个维度(数轴axes)，包括concurrency、engineering、dependencies。

![](../../assets/54b686b04bd8bcf1.png)


![](../../assets/a359af647e41a246.png)


![](../../assets/a17e0586cfd8056f.png)


![](../../assets/54344212a4ab5cd9.png)


Rob Pike：

- 这就是我们几个第一次碰面设计一门新编程语言时讨论的话题。

![](../../assets/95d0bf4724d4d396.png)


Rob Pike：

- 这就是Go实现的一个生产就绪的Web server的代码。

- 下面探讨fmt.Fprintf的第一个参数的类型，它很特殊，它是一个io.Writer接口类型。

![](../../assets/cbcd4c4f79d58e56.png)


Rob Pike：

- Go代码中充满了这种仅有一两个方法甚至是零个方法的接口类型，这些构成了Go文化之一。

- 我们相信，接口不应该为你所构建的整个世界预先定义，而应该在程序开发过程中有机地产生。让编译器解决一个接口是否好的问题，实际上是比强迫程序员优先解决这些问题更有效的进行软件演化的方式。(because we believe that interfaces should not be predefined for the entire world you are building. but instead should arise organically through program development. and having the compiler work out whether an interface is good or not is an actually more effective way to grow software than forcing the programmers to work it all out a priori)。

![](../../assets/82e241dfbc9e348e.png)


Rob Pike：

- 不同于其他编程语言，这些整型不能混合在一起运算(译注：需显式转型)。

![](../../assets/1584f6fcf3d4aa05.png)


![](../../assets/fd75dbe271dbb83b.png)


Rob Pike：

- 我们的想法是，从概念上讲，处理并行性和并发性的开销在Go中是非常轻的。这是该语言的一个重要卖点。

![](../../assets/39da4195f2132c8d.png)


Rob Pike：

- 一旦你把channel/select这些和goroutines结合起来，你就可以完全简单地、正交地把它们放在过程语言(procedure language)之上。并使并发变得简单，让那些以前我承认有时害怕它的人可以使用。

![](../../assets/8a7c8e2bb20fee7c.png)


![](../../assets/278f8072f0faf07f.png)


![](../../assets/f70a7a0604651c71.png)


Rob Pike：

- 我们做了很多努力来建立一套非常好的核心库，允许你做一些事情，如网络、密码学、文本处理、格式化的IO，我们建立了一套核心库，建立在这些简单的接口的想法上，并使用这些接口和其他我们可以使用的机制，如并发性和内存安全属性等等。我们建立了基础库，这样你就可以写一个程序，只使用核心库，这将起到有效的作用，它也可以在生产中启动，并能够处理成千上万并发进行的负载。我们已经看到运行在内部启动的数百万个goroutine的二进制文件，因为它们是轻量级的，它们可以扩展。

![](../../assets/82c13cccdb6f4866.png)


![](../../assets/4c3208bc2b570c07.png)


Rob Pike：

- 也许Go的成功最重要的部分是这种兼容性承诺(Go1兼容性承诺)。
- 更重要的是，我们向用户承诺，如果你的代码今天能用，十年后也能用，而且确实如此。这种对用户社区的承诺是Go应用的一个巨大特点。实际上，在曲线上有一个膝盖型突起，你可以看到采用率的上升，工业界现在可以开始依赖它，因为他们知道，如果他们投资于它，它就会工作。书的作者也可以写书，他们知道十年后书中内容仍然有意义，这是我们故事的一个主要部分。

![](../../assets/3fecbcf7632aa469.png)


![](../../assets/436752f3b8341753.png)


![](../../assets/e24132ef9c0e2a74.png)


Rob Pike：

- 因此，所有这些元素都有一个主题，这个主题就是，如果你想发展一种语言或一个系统，特别是在开源世界中，你必须让别人容易进来。这并不仅仅意味着接受每一个他人提出的pull request，这更意味着创建一个系统，在这个系统中，大家可以很容易使用一种语言，比如：易于解析，易于用支持它的工具进行分析。可以单独工作的库，但被设计成可以相互协作以建立更大的系统。用于高质量工具开发的包，易于理解的开发，高速执行，简单的部署，易于移植。一个模块系统让每个人都能舒适地分享他们的代码，也包括一种鼓励人们共同成长的文化。

![](../../assets/aa51a9eace35f754.png)


Rob Pike：

- 我们已经建立起这个社区，在社区中大家一起构建了一个软件开发环境并且乐趣多多，这个环境不仅是由语言所培育的，更多是因为上面这些更为重要的因素。

![](../../assets/3a0ac2a818012099.png)


![](../../assets/70b55c1042ad3d72.png)


Rob Pike：

- Go是关于软件开发的。它不仅仅是关于编程。我认为这就是为什么它能做得那么好的原因。

![](../../assets/015dab9e15a02e4b.png)


- 泛型会不会改变编写Go代码的方式？

Rob Pike：

我们没有从一开始就把它们放进去，因为我们不明白我们怎么会对它感到不舒服，所以不是我们决定不放它们，而是我们不确定如果我们从一个具有参数化多态性的语言开始，如何在所有这些其他方面实现我们想实现的目标。

我相信这仍然是事实。

我相信关于库的工作方式和互连的工作方式等等的很多事情都会有非常不同的味道。 如果它是一种多态的语言，我不确定它会有多好。

经过Ian Taylor等人十多年的努力，我们现在有了一个设计，我想说的是，我们不是真正的我，但团队有了一个参数化多态性模型的设计，感觉它与语言的其他部分相匹配。我很想知道它是否会打破这个局面，它可能会打破一切，因为程序员会开始考虑用这种方式写代码，我很想知道它的效果。

- Rob Pike的其他观点
- 我认为声明变量的方式有些多。
- 经过我们三人(Rob Pike, Ken Thompson, Robert)达成一致的Go特性已经足够多，足够好了。
- 我们很努力地寻找channel与network一起工作的方式，但我们失败了！


[“Gopher部落”知识星球](https://mp.weixin.qq.com/s/jUqAL7hf2GmMun64BJufEA)正式转正（从试运营星球变成了正式星球）！“gopher部落”旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！部落目前虽小，但持续力很强。在2021年上半年，部落将策划两个专题系列分享，并且是部落独享哦：

- Go技术书籍的书摘和读书体会系列
- Go与eBPF系列

欢迎大家加入！

![](../../assets/b634c86efd3a19cc.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订

阅！

![img{512x368}](../../assets/8974393c1b81f912.jpg)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/d6497e1263ffb6ad.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论