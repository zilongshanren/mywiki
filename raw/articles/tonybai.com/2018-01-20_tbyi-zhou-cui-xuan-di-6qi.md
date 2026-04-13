---
title: TB一周萃选[第6期]
url: https://tonybai.com/2018/01/20/6th-issue-of-the-tech-weekly-carefully-chosen-by-tonybai/
published: '2018-01-20'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# TB一周萃选[第6期]

本文是首发于[个人微信公众号](https://mp.weixin.qq.com/mp/qrcode?scene=10000005&size=102&__biz=MzIyNzM0MDk0Mg==&mid=2247483848&idx=1&sn=a3cd9182a2b2d3716623cc2c43d59f37&send_time=)的文章**“TB一周萃选[第6期]”**的归档。

![img{512x368}](../../assets/1605d1b1b8858bbb.jpg)


图：第6期封面

凡事欲其成功，必须付出代价——奋斗。


— 美国作家 爱默生

每期挑选“封面图”都是一件颇为“费工夫”的事情，本期的封面图来自于一个投资界大V发送的微博内容，因为当我第一眼看到这幅图片时，感觉它**颇为契合我当时的心境**。

**“未来的一年里，连睡觉都是浪费时间”**这句话的最原始的出处在哪里我还没有查到，但最近与这句话“勾搭”上关系的是小米公司，因为坊间传闻小米公司要开启上市计划了。但小米公司绝对不是这句话的“始作俑者”，因为我查到著名的投资人孙正义先生在2017中旬举行的[SoftBank World大会中的一次演讲](https://www.huxiu.com/article/206194.html)中也提到过：”未来让我激动，感觉睡觉都是在浪费时间”这一同义的说法。

先不管人们对这句话是否感同身受，实际情况是当今人们用于睡觉的时间真的是越来越少了。已经成功的人为了追求更大的成功或让企业长期利于不败之地而殚精竭虑，**他们不能睡**；正走在通往成功道路上的奋斗者们，加班加点，兢兢业业，亲力亲为，**他们不愿睡**；大多安于现状、不愿折腾的打工族们则贪恋红尘，吃喝唱K、刷剧吃鸡、答题聊天的时间还不够呢，哪忍心放下手机或电脑去呼呼大睡呢，**他们不舍得睡**。

由此看来，似乎这个“网红句子”在不同人内心中的含义是可以不同的。但无论怎样，我敢肯定的是这幅图会让那些新的一年中心中目标满满并欲为之奋斗的人振奋不已。大家都说刚刚新年伊始，其实已经过去了半个多月了，时间真的不等人：学习要速度，发展要速度，增长要速度，那么多工作和目标等待着你去完成，抓紧这本应该是睡眠的时间，努力**奋斗**吧。

![img{512x368}](../../assets/8e2256781b3f9de7.jpg)


图：2018.1.18雾凇景观(沈阳)

## 一、一周文章精粹

### 1. [AWS Lambda](https://aws.amazon.com/lambda)正式宣布对Go的支持

在2017年末举办的[AWS re:Invent大会](https://reinvent.awsevents.com/)上，AWS的技术人员就剧透了Lambda将对[Go](http://tonybai.com/tag/go)提供正式支持。本月15号，AWS官方[正式宣布了Lambda对Go的支持](https://aws.amazon.com/cn/blogs/compute/announcing-go-support-for-aws-lambda/)，并在github上发布了[aws-lambda-go](https://github.com/aws/aws-lambda-go)的[1.0.0版本](https://github.com/aws/aws-lambda-go/releases/tag/v1.0.0)。现在全世界的gopher们就可以使用自己心仪的语言来编写自己的第一个[Function as a Service](https://en.wikipedia.org/wiki/Function_as_a_service)例子了。

![img{512x368}](../../assets/2c4d4cdb572dd526.png)


文章链接：[“Announcing Go Support for AWS Lambda”](https://aws.amazon.com/cn/blogs/compute/announcing-go-support-for-aws-lambda/)

### 2. Cloudflare公司的TCP协议栈深入理解系列

Cloudflare是世界知名的CDN服务商，这些年Cloudflare公司的主要技术栈也转移到了Go语言，包括其DNS系统等。Cloudflare在TCP/IP网络方面有了较为深入的理解，其研发人员经常在其官方blog发表有关互联网协议方面的技术文章，这里将其中几篇抽取汇总出来，形成“TCP协议栈深入理解系列”，包括：

[The story of one latency spike](https://blog.cloudflare.com/the-story-of-one-latency-spike/)[This is strictly a violation of the TCP specification](https://blog.cloudflare.com/this-is-strictly-a-violation-of-the-tcp-specification/)[SYN packet handling in the wild](https://blog.cloudflare.com/syn-packet-handling-in-the-wild)

### 3. 高性能Go语言编程

印象中，高性能Go编程这个topic，大胡子[Dave Cheney](https://dave.cheney.net/)在几个技术大会上都讲过，Dave自己关于这方面的认知也在演化，这次在QCon大会上的演讲应该他对Go高性能编程的最新理解。

文章链接：[“High performance Go by Dave Cheney”](https://www.infoq.com/presentations/go-programming-language)

### 4. 为什么Go中会有nil channel?

[Francesc Campoy](https://github.com/campoy/)是Go core team前成员，他的[“just for fun”](https://github.com/campoy/justforfunc/)系列播客在广大Gopher圈里十分受欢迎，其最新一期[“为什么Go中会有nil channel?”](https://medium.com/justforfunc/why-are-there-nil-channels-in-go-9877cc0b2308)讲解了nil channel在实际编码中的妙用。

![img{512x368}](../../assets/2ce2cd5644a2738a.png)


文章链接：[为什么Go中会有nil channel?](https://medium.com/justforfunc/why-are-there-nil-channels-in-go-9877cc0b2308)

### 5. 将Kubernetes集群扩展到2500个节点

容器与Kubernetes等容器管理基础设施的出现改变的不仅仅企业的业务应用架构和开发模式，对近两年火热的人工智能、机器学习也是一种赋能。当前Kubernetes支撑的人工智能/机器学习环境是目前一个流行的趋势，比如发布不久的[Kubeflow](https://github.com/google/kubeflow)。不过2015年末的成立的[openai组织](https://blog.openai.com/scaling-kubernetes-to-2500-nodes/)则早就将Kubernetes运用于人工智能领域的研究，截止目前该组织运行管理的Kubernetes集群已经达到2500个节点。本周openai发表文章讲述了他们是如何将Kubernetes集群管理的节点数量扩展到2500个的，他们的下一个目标是5000个节点。

文章链接：[“Scaling Kubernetes to 2,500 Nodes”](https://blog.openai.com/scaling-kubernetes-to-2500-nodes/)

### 6、Kubernetes的引力

2017年，Kubernetes战胜了swarm和mesos，成为容器管理和服务编排方面的事实标准。

![img{512x368}](../../assets/ccc35bdfdd4a99c9.png)


“Kubernetes引力”这篇文章从标准、容器管理编排、适配多云平台、适用于分布式系统部署等多方面论述Kubernetes对IT世界的改变。

文章链接：[“The Gravity of Kubernetes”](https://www.softwaredaily.com/#/post/5a5a2387f43c8d000457a110)

## 二、一周资料分享

### 1. 人工智能标准化白皮书（2018版）

2018年1月18日，在国家人工智能标准化总体组、专家咨询组成立大会上，大会发布了“人工智能标准化白皮书2018版”，对人工智能技术的历史、发展现状及趋势、人工智能的标准体系以及国内外标准化的现状做了系统的阐述。

人工智能标准化白皮书2018: 链接: https://pan.baidu.com/s/1qZTPyCc 密码: x3qn

## 三、一周项目推荐

### 1. tview

[tview](https://github.com/rivo/tview)是用纯Go语言编写的一款终端UI组件库，用于实现基于terminal的文本式交互界面。类似于传统的C语言[ncurses库](https://www.gnu.org/software/ncurses/)。tview提供了许多widget，并且有对应的demo代码对应，使用起来十分方便：

- 输入框（包括密码字段输入、下拉选择、选择框、按钮）
- 可导航的多色文字视图
- 导航表视图
- 可选列表
- Flexbox和页面布局
- 模态消息窗口

![img{512x368}](../../assets/5417c8e37d6695ba.jpg)


项目地址：[tview](https://github.com/rivo/tview)

### 2. colly

数据在移动互联网时代以及即将到来的AI时代都是具有核心价值的。数据的获取途径之一就是通过爬虫工具获取公共数据，并作为数据价值挖掘的输入。colly就是一款用于编写爬虫工具的框架，它使用Go语言实现，提供优雅、简洁的API接口、高效的性能、并发爬取管理、缓存、robots.txt支持等功能，同时colly还提供了详尽的[使用文档](http://go-colly.org/docs/)以及丰富的[examples](https://github.com/gocolly/colly/tree/master/_examples)。

![img{512x368}](../../assets/e47ab7e9c9eacf27.png)


项目地址：[colly](https://github.com/gocolly/colly)

## 四、一周图书推荐

### 1.《迁移到云原生应用架构》

![img{512x368}](../../assets/6d95bf3d6f4de8d1.png)


图：Migrating to Cloud-Native Application Architectures封面

就好比00后被称为是互联网时代“原住民”一样，近几年的一些应用架构演化模式被称为“云原生”应用(cloud-native application)，换句好理解的话来说，就是这些应用天生就是应该跑在云上的，而且具有诸多契合云计算平台的特征，而不仅仅是简单地将传统单体应用从单机挪到虚拟机或容器中部署。

云原生（Cloud Native）这个概念最初是由[Pivotal公司](https://pivotal.io/)的 [Matt Stine](http://www.mattstine.com/)在 2013年提出的，是他对多年架构和咨询经验进行总结后的一个成果。2015年，他操刀编写了“Migrating to Cloud-Native Application Architectures”，也就是这里推荐的这本短小的开源书。

这本书的脉络十分清晰，首先Matt告诉我们什么是云原生架构以及为什么要用云原生架构。不过Matt并没有给出精确的云原生的定义，而是告诉我们云原生应用架构具有哪些特征，包括：”[twelve factor app](https://12factor.net/zh_cn/)“、微服务、自服务敏捷架构、基于API写作等；接下来Matt告诉我们如果企业要接纳云原生架构，应该如何从文化、组织和技术等三个方面进行变革；最后的一个小章节则是迁移到云原生应用的实操mini手册。

随着[kubernetes](http://tonybai.com/tag/kubernetes)、容器进一步发展以及对应用的进一步赋能，人们对云原生应用的认识还在进一步深刻中，pivotal在[官网](https://pivotal.io/cn/cloud-native)上对cloud-native的概念做了进一步总结归纳，建议结合这本书一并学习一下。

![img{512x368}](../../assets/2ae12d42fc3ad438.png)


图：Pivotal对云原生概念进一步阐述

图书链接：

[《迁移到云原生应用架构》中译版](https://jimmysong.io/migrating-to-cloud-native-application-architectures)

[《Migrating to Cloud-Native Application Architectures》](https://content.pivotal.io/ebooks/migrating-to-cloud-native-application-architectures)

著名云主机服务厂商DigitalOcean于1月17日[发布了其新的主机计划(New Droplet Plan)](https://blog.digitalocean.com/new-droplet-plans/)，此次发布是对其原有主机计划的优化，其中入门级Droplet的内存容量从512M升级为1G，SSD磁盘空间从20G升级到25G，但价格不变，依旧是5$/月。如果你已经使用了DigitalOcean服务，可以到后台手动进行Resize以享受增容后的主机性能。如果您还没有使用DigitalOcean，可以去看看DO的vps plan是否满足你的需求。 链接地址：https://m.do.co/c/bff6eed92687

![img{512x368}](../../assets/32121bcfb7263a6a.png)


图：New Plan的价格表

我的联系方式：

微博：http://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/71dbd0d64d261ba9.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2018, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论