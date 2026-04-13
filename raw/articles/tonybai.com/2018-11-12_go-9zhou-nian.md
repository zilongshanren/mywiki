---
title: Go，9周年
url: https://tonybai.com/2018/11/12/go-opensource-9-years/
published: '2018-11-12'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go，9周年

本文翻译自Go官方博客：[《Nine years of Go》](https://blog.golang.org/9years)。

### 介绍

今天是我们的[Go语言](https://tonybai.com)初始版本开源的第九个[周年纪念日](https://tonybai.com/2017/09/24/go-ten-years-and-climbing)。在每个周年纪念日上，我们都希望花些时间思考过去一年发生的事情。过去12个月对Go语言和Go社区来说是突破性的一年。

### 对Go的爱和接纳

感谢你们所有人，2018年对Go来说是美好的一年！在多个行业调查中，Gopher们表达了他们使用Go的快乐程度，并且许多非Go开发者也表示了他们打算在其他语言之前优先学习Go。

在[Stack Overflow的2018年开发者调查](https://insights.stackoverflow.com/survey/2018#most-loved-dreaded-and-wanted)中，Go保持住了其在**最受欢迎**和**最想用**的5种编程语言排行榜中的位置。使用过Go的人继续喜欢它，而不曾使用过Go的人则要开始尝试它。

在[ActiveState的2018年开发者调查](https://www.activestate.com/developer-survey-2018-open-source-runtime-pains)中，Go占据了榜首，36％的用户回应他们使用Go“非常满意”，61％的受访者回复“很满意”或更好。

[JetBrains的2018年开发者调查](https://www.jetbrains.com/research/devecosystem-2018/)将Go评为“最有前途的语言”，其中12％的受访者使用Go，16％的受访者希望将来使用Go。

在[HackerRank的2018年开发者调查](https://research.hackerrank.com/developer-skills/2018/)中，38％的受访开发人员回应说他们打算下一步学习Go。

我们对于所有新gopher的加入都表示最大的欢迎，并继续积极致力于改善我们所提供的Go的教育和社区资源。

### Go社区

很难相信，自第一次Go大会和Go聚会(meetup)至今才仅仅五年。去年，我们看到社区领导力在这一领域取得了重大进展。目前全球有超过20个Go会议 和300多场与Go相关的聚会(meetup)。

多亏了这些会议和聚会的辛勤工作投入，今年已经产生了数百场精彩的主题演讲。以下是我们最喜欢的一些专门针对我们社区的发展以及我们如何更好地支持全球Gophers方面的演讲：

[Writing Accessible Go](https://www.youtube.com/watch?v=cVaDY0ChvOQ)，是由Julia Ferraioli在[GopherCon](https://www.gophercon.com/)上呈现给大家的;[The Importance of Beginners](https://www.youtube.com/watch?v=7yMXs9TRvVI)，来自于GopherCon的Natalie Pistunovich的演讲;[The Legacy of Go, Part 2](https://www.youtube.com/watch?v=I_KcpgxcFyU)，来自于[GothamGo](http://www.gothamgo.com/)的Carmen Andoh的演讲;[Growing a Community of Gophers](https://www.youtube.com/watch?v=dl1mCGKwlYY)，来自于[Gopherpalooza](http://www.gopherpalooza.com/)的Cassandra Salisbury。

在这个主题上，今年我们还修改了Go行为准则， 以更好地支持Go社区的包容性。

Go社区是一个真正的全球性社区。今年夏天在冰岛举办的GopherCon Europe大会上，Gophers们真实地**跨越**了各大洲之间的差距。

![img{512x368}](../../assets/6b77c347892fc5a7.jpg)


（照片来自Winter Francia。）

### Go2

在[Go 1](https://golang.org/doc/go1compat)（译注：这里指Go1语言规范兼容性规定)发布并历练了五年之后，我们已经开始考虑我们应该改变什么，以便更好地支持大规模的编程。

去年春天，我们发布了[Go module的设计草案](https://golang.org/design/24301-versioned-go)，它为版本控制和软件包分发提供了集成机制。最新的Go版本Go 1.11包括[对module的初步支持](https://tonybai.com/2018/07/15/hello-go-module/)。

去年夏天，我们发布了关于Go 2如何更好地支持错误值(error value)，错误处理(error handling)和泛型编程(generic programming)的[早期草案设计](https://github.com/golang/proposal/blob/master/design/go2draft.md)。

在我们努力实现Go 2的过程中，我们很高兴能够在社区的帮助下完善这些设计 。

### Go贡献者

Go项目多年来来自社区的贡献一直在增加，并且在2018年第二季度达成了一个重要的里程碑，那就是我们从社区获得的贡献第一次比Go团队的贡献更多。

![img{512x368}](../../assets/fe229b8ca8b0c227.png)


### 谢谢

作为整个Go团队的代表，我要真诚地感谢你们所有人。我们很荣幸能够参与Go项目，并感谢世界各地的gopher加入我们。

我们特别感谢成千上万的志愿者，他们通过指导，组织，贡献和支持您的同伴们来帮助社区发展，是你们把Go变成了今天的样子。

By Steve Francia

我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

我的联系方式：

微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2018, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论