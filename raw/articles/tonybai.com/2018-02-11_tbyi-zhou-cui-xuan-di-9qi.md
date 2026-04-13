---
title: TB一周萃选[第9期]
url: https://tonybai.com/2018/02/11/9th-issue-of-the-tech-weekly-carefully-chosen-by-tonybai/
published: '2018-02-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# TB一周萃选[第9期]

本文是首发于[个人微信公众号](https://mp.weixin.qq.com/mp/qrcode?scene=10000005&size=102&__biz=MzIyNzM0MDk0Mg==&mid=2247483848&idx=1&sn=a3cd9182a2b2d3716623cc2c43d59f37&send_time=)的文章**“TB一周萃选[第9期]”**的归档。

![img{512x368}](../../assets/dc9defa7d46f7caf.jpg)


亲情犹如一江剪不断的春水，流动的是游子心中永远的思念；亲情犹如一丘数不尽的细沙，沉淀的是长年堆积的牵挂；亲情犹如夜空中那颗北斗，指引的是那迷路的羔羊回家的方向。忙碌了一年，该回家了，给心放个假，带上媳妇带上你的娃，回家看看那年迈的爸妈，出发！ — 改编自网络


此时此刻，很多人刚刚踏上了春节回家的旅途，有些人更是已经叩开了家的大门。每逢中国传统佳节-[春节](https://en.wikipedia.org/wiki/Chinese_New_Year)，令世界瞩目并为之瞠目结舌的中国式人口大迁移就会发生一次：几亿人熬夜刷票并不辞辛劳地携着夫/妻儿女，经由多种交通工具，跨越高山大河，不远千百里，战胜种种“囧况”，只为一个目的：在春节前回到那个充满熟悉味道的家乡。

这种在一个文明延续5000多年未中断的民族中发生的**全民行为**让西方社会感到十分不解，甚至指责这是对资源的一种浪费；并且也有国内的人发出类似不和谐的声音。但是**它依然在发生着，每年都在发生**，形式有些许变化，但剧情大体雷同。

曾经有国内外学者对中国特有的春节大迁徙的原因进行研究和分析，并给出了各种专业化的理由。但在我看来，对现代人来说，回家过年，是一种**心灵的相互充电**! 而且是**充电7天，“通话”一整年**。

对于一年到头在外奔波劳碌的人们来说，只有回家，才能真实地触摸到自己的“根”，才能切切实实地体会这种归属感，才能在一定程度上纾解那些在工作的城市中涵盖不了的人生寄托。在这种归属感中，哪怕只是获得片刻的身心安宁，也是一种极为重要的精神能量的充电；而对于守候在家乡的父母或者孩童儿，你的回家，让他们将近一年的期盼终于有了一个圆满的结果，这同样为下一个365天的期盼周期提供了强大的动力和希望。

如果非要给这种行为找个理由，那我要说这就是由一个体内延绵数千年的中华民族血脉的中国人的基因所决定的。

![img{512x368}](../../assets/87e3797baed2e45a.jpg)


## 一、一周文章精粹

### 1. Go 1.10发布Party

自从[Go 1.6](http://tonybai.com/2016/02/21/some-changes-in-go-1-6/)开始，每逢偶数版本（一般在每年2、3月发布），Gopher社区都会举办庆祝Release的[全球Party](https://twitter.com/hashtag/goreleaseparty)。在中国农历春节到来之际，也恰逢Go最新版本Go 1.10即将发布之时，Go wiki发布了[Go 1.10 Release Party](https://github.com/golang/go/wiki/Go-1.10-Release-Party)的Schedule和相关资料。截至目前，已经有15个Party已经list到页面上，活动从2月15号一直延续到3月份。

### 2. 避免或减少对Go context Value的使用

context包最初诞生于Google公司内部，并在Google内部项目大量使用。context在golang/x中孵化了多年，并得到了很多开源项目的使用，尤其是一些使用了”middleware”模式的项目中，于是在[Go 1.7发布](http://tonybai.com/2016/06/21/some-changes-in-go-1-7/)时，context包正式加入Go标准库。context加入后，可谓既带来魔力，亦带来了争议，甚至有人将其视为[具有“病毒”属性](https://faiface.github.io/post/context-should-go-away-go2/)，一旦使用，便可轻易传染到项目中代码的各个角落。

Go开发者、培训师Jon Calhoun也在个人网站上撰写了一篇文章，来告诫大家Go context value的一些缺陷，建议大家避免或减少对Go context Value的使用，并给出自己的替代方案。其主要理由是：context.WithValue和Context.Value的使用让我们失去了编译器对类型安全性的检查。

### 3. 来自Google Cloud Platform的12条有关用户账号、授权和密码管理的最佳实践

对于许多开发者来说，账户管理是一个黑暗的角落，没有得到足够的重视。来自Google Cloud Platform的解决方案专家Ian Maddox给我们带来了12条有关此方面的最佳实践，包括：区分用户标识与用户账号、允许用户更改用户名、用户ID大小写敏感、两步验证等。

![img{512x368}](../../assets/cc91e337dc070315.jpg)


### 4. AI界网红-深度学习之父Geoffrey Hinton的传奇学术生涯

这几年最火爆的人工智能技术就是深度学习，可以说当下的主流人工智能就是深度学习，而深度学习的理论基石就是反向传播。和当代物理学类似，最新的计算机应用实际上也是在消化几十年前就已经建立的理论，这不：反向传播就是Geoffrey Hinton与同事David Rumelhart、Ronald Williams在1986年发布的成果，Geoffrey Hinton也因此被誉为深度学习之父。Geoffrey Hinton花了30年在AI前沿的研究，在今天终于开花结果。不过这位现在AI奠基人并没有就此停歇，去年他还提出了“[胶囊理论](https://arxiv.org/abs/1710.09829)”，不过要彻底理解他的理论，不知道AI应用界还要花多久。下面这篇文章是“多伦多生活”上发表的一篇有关Geoffrey Hinton的传奇学术生涯的新闻稿，我们可以通过它一瞥AI超级明星的学术人生。

![img{512x368}](../../assets/c275a6d753b33971.jpg)


图：Geoffrey Hinton

文章链接：[“深度学习之父Geoffrey Hinton的传奇学术生涯”](https://torontolife.com/tech/ai-superstars-google-facebook-apple-studied-guy/)

### 5. Go项目在github上接受PR了

go语言自身的开发一直是在google内部的平台上，github上的golang项目仅仅是其一个mirror。在这之前，golang项目在github上是拒绝pr的，contributor必须注册google的开发账号才能为go语言本身做贡献，这种门槛显然有些高。近期Go项目作出了对社区更为友好的举动：[允许在github上直接提交PR](https://go-review.googlesource.com/c/go/+/92995)。不过代码的review依旧是在google原平台上，github上提交的pr将被GerritBot自动同步到Go team的Gerrit上进行code review。不过这已经是一个不错的开端了。估计会吸引更多开发者为Go做contribution。

文章链接：

* [“doc: remove Pull Request note in README.md”](https://go-review.googlesource.com/c/go/+/92995)

* [“pr流程”](https://github.com/golang/go/wiki/GerritBot)

## 二、一周资料分享

### 1. istio微服务教程 by Redhat

下一代微服务平台日益火爆，比如：[istio](http://tonybai.com/2018/01/03/an-intro-of-microservices-governance-by-istio/)、[conduit](https://conduit.io/)等。近期Redhat开源了一套istio微服务教程，主要是for java microservice，但感觉对其他语言开发的微服务也适用。教程使用的是[istio](https://istio.io/)最新发布的[0.5.0版本](https://github.com/istio/istio/releases/tag/0.5.0)，底层使用的是redhat自身的oc平台(openshift)，但替换成[kubernetes](http://tonybai.com/tag/kubernetes)应该很容易。教程包含的内容还是很全面的，针对包括metrics、tracing、routerule管理、fault injection、retry&timeout、mirroring traffic、access control、rate limiting、circuit breaker、egress等常见的微服务框架治理机制都提供了demo实例。

资料分享链接：[Istio Tutorial for Java Microservices](https://github.com/redhat-developer-demos/istio-tutorial)

## 三、一周项目推荐

### 1. rook：致力于让存储服务成为云原生平台上的“头等”服务

2018年1月30日，云原生[cncf组织](https://www.cncf.io/)下又增加了一位新成员:[rook项目](https://rook.io/)，由于刚入行，其与linkerd、coredns同样处于Inception级别。rook是什么？它解决了哪些问题呢？

如今在Kubernetes上部署的应用在使用存储服务时，多使用k8s集群外提供的外部存储服务。在公有云上，使用较多的是诸如[EBS](https://aws.amazon.com/cn/ebs/)、[S3](https://aws.amazon.com/s3/)等；在定制云/私有云中，使用的则是NFS、[Ceph](http://tonybai.com/tag/ceph)或更为传统的存储解决方案，如下图所示：

![img{512x368}](../../assets/353cad9b4a07f69b.png)


图：使用rook前

Rook存在的意义就是将存储服务移入集群内部，让那些依赖存储服务的应用可以无缝地使用这些服务，这样一来，整个云原生集群环境就可以脱离厂商依赖（比如对amazon、google cloud platform的依赖），实现整体的可移植了，无论是公有云还是私有云。

![img{512x368}](../../assets/c87715b43b9e81bb.png)


图：使用rook后

可以说，Rook**让存储服务成为云原生平台上的“头等”服务**，与其他应用服务一样。

那Rook究竟是什么呢？Rook不是一个像ceph那样的分布式共享存储系统。rook的考虑是：与其花费几年甚至十几年实现一个成熟的、久经考验的分布式存储系统，到不如帮助现有的已经十分成熟的、久经沙场的存储系统更方便的被云原生环境中的应用所使用，比如：[ceph](https://ceph.com/)。于是rook通过将那些专有存储服务管理员的日常操作自动化：包括引导启动、配置、伸缩、升级、迁移、灾难恢复、监控、资源管理，将存储服务包装为云原生应用，无缝运行在云原生环境上，目前主要是在Kubernetes上。

![img{512x368}](../../assets/9874c37eb36ba446.png)


图：rook架构

Rook的出现，迅速得到了来自Redhat、ceph开发者的支持，社区也在日益壮大。目前其最新版本为v0.6.2，按计划在2018年中旬发布第一个production-ready的正式版。

项目地址：[Rook](https://github.com/rook/rook)

## 四、一周图书推荐

### 1.《High Performance Browser Networking》

![img{512x368}](../../assets/737b063407a22ff8.jpg)


Ilya Grigorik是Google性能优化工程师，他在2013出版的这本[《High Performance Browser Networking》](https://book.douban.com/subject/21866396/)堪称当代Web性能调优的圣经。该书以调优为核心，从网络基础(101)讲起，然后深入探讨了无线和移动网络的工作机制。最后，揭示了HTTP 协议的底层细节，同时详细介绍了HTTP 2.0、 XHR、SSE、WebSocket、WebRTC 和DataChannel 等现代浏览器新增的具有革命性的新能力。该书无论是对前端开发，还是后端网络服务开发设计人员都是大有裨益的。

更重要的是该书当时所讲述的诸多浏览器协议技术，比如：HTTP2.0、WebSocket、SSE在如今已经成为标准，并广泛应用于生产实践中。

图书链接：

英文版：[《High Performance Browser Networking》](https://book.douban.com/subject/21866396/)

中文版：[《Web性能权威指南》](https://book.douban.com/subject/25856314/)

免费版：[《High Performance Browser Networking》](https://hpbn.co/)

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

我的联系方式：

微博：http://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/71dbd0d64d261ba9.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作

© 2018, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论