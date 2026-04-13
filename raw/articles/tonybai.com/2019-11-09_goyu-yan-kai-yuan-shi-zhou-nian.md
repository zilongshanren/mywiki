---
title: Go语言开源十周年
url: https://tonybai.com/2019/11/09/go-opensource-10-years/
published: '2019-11-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go语言开源十周年

本文翻译自[Go官方博客](https://blog.golang.org)上[Russ Cox](https://research.swtch.com/)代表Go核心团队发表的[“Go Turns 10″](https://blog.golang.org/10years)一文。

**生日快乐，Go！**

这个周末，我们庆祝[Go正式对外发布](https://opensource.googleblog.com/2009/11/hey-ho-lets-go.html)10周年，即Go作为开源编程语言和构建现代网络软件生态系统的10周年诞辰。

为了纪念这一时刻，[Go gopher](https://blog.golang.org/gopher)的创建者[Renee French](https://twitter.com/reneefrench)(用下面的新作)描绘了这个令人愉快的场景：

![img{512x368}](../../assets/0d4e022bf94a0deb.jpg)


庆祝Go十周年让我回想起2009年11月上旬，那时我们正准备与世界分享Go。我们不知道会发生什么样的反应，是否有人会关心这种新生的小语言。我希望即使没有人最终使用Go，我们也至少会引起人们对一些好的想法的关注，尤其是Go的并发和接口，这些想法可能会[影响后续语言](https://tonybai.com/2019/11/04/the-legacy-of-go/)。

当看到人们对Go感到兴奋，我便查看了[C](https://tonybai.com/tag/c)、[C++](https://tonybai.com/tag/cpp)、Perl、[Python](https://tonybai.com/tag/python)和Ruby等流行语言的历史，并研究了每种语言花了多长时间才被广泛采用。例如，在我看来，Perl在1990年代中后期就已经完全形成了，带有CGI脚本和Web，但它于1987年首次发布。这种模式在我所研究的几乎所有语言中都重现了：在新语言真正腾飞之前，需要大约十年的时间进行安静、稳定的改进和传播。

(当时的)我想知道：十年后的Go会在哪里？

今天，我们可以回答这个问题：Go无处不在，全世界[至少有100万开发人员](https://research.swtch.com/gophercount)在使用它。

Go最初的目标是网络系统基础架构，现在我们称为云软件(cloud software)。如今，每个主要的云计算平台提供商都使用用Go语言编写的核心云基础架构，例如[Docker](https://tonybai.com/tag/docker)，[Etcd]https://etcd.io/，[Istio](https://tonybai.com/2018/01/03/an-intro-of-microservices-governance-by-istio/)，[Kubernetes](https://coding.imooc.com/class/284.html)，[Prometheus](https://prometheus.io/)和[Terraform](https://www.terraform.io/)。[Cloud Native Computing Foundation](https://www.cncf.io/)的大多数项目都是用Go编写的。无数公司也在使用Go将自己的工作迁移到云上，从初创公司从头开始构建到大企业更新软件堆栈。Go还发现对其的采用已经远远超出了最初的云计算目标，其使用范围从使用[GoBot](https://gobot.io/)和[TinyGo](https://tinygo.org/)控制小型嵌入式系统到[使用GRAIL进行大规模的大数据分析和机器学习](https://medium.com/grail-eng/bigslice-a-cluster-computing-system-for-go-7e03acd2419b)进行癌症检测，以及介于两者之间的所有内容。

这一切都说明Go超越了我们最疯狂的梦想。Go的成功不仅仅在于语言。这是关于语言，生态系统，尤其是社区的共同努力。

在2009年，该语言是一个不错的主意，并带有一个实现的工作草图。那时候go命令还不存在：我们使用命令6g编译源码和6l链接二进制文件，并借助Makefile实现这个过程的自动化。我们在语句末尾键入分号。整个程序在垃圾回收期间停止，然后努力利用两个CPU核。当时Go只能在Linux和Mac，32位和64位x86和32位ARM上运行。

在过去的十年中，在世界各地的Go开发人员的帮助下，我们已经将这一想法和草图发展为拥有出色的工具，生产级质量实现，[先进的垃圾收集器](https://blog.golang.org/ismmkeynote)和得到广泛移植的高效语言，Go支持[12种操作系统和10种CPU体系结构](https://golang.org/doc/install/source#introduction)。

任何编程语言都需要蓬勃发展的生态系统的支持。开源发布是该生态系统的种子，但是自那时以来，许多人贡献了自己的时间和才干，用出色的教程，书籍，课程，博客文章，播客，工具，集成以及可重复使用的、支持go get的Go包来填充Go生态系统。没有这个生态系统的支持，Go永远不可能成功。

当然，生态系统需要蓬勃发展的社区的支持。在2019年，全球有数十个Go（技术）会议，以及[超过150个Go聚会组织和90000名参会人员](https://www.meetup.com/pro/go)。 [GoBridge](https://golangbridge.org/)和[Going Who Go](https://medium.com/@carolynvs/www-loves-gobridge-ccb26309f667)通过指导，培训和会议奖学金帮助将新的声音带入Go社区。仅今年一年，他们就在讲习班上向数百名来自传统团体的人们进行了培训，在这些讲习班上，社区成员教导和指导刚接触Go的人。

全球有[超过一百万的Go开发人员](https://research.swtch.com/gophercount)，全球各地的公司都在寻求雇用更多的人。实际上，人们经常告诉我们，学习Go帮助他们获得了技术行业的第一份工作。最后，我们为Go感到最自豪的不是设计完善的功能或巧妙的代码，而是Go在这么多人的生活中产生的积极影响。我们旨在创建一种可以帮助我们成为更好的开发人员的语言，我们很高兴Go帮助了许多其他人。

恰逢Go开源十周年的时刻，我希望每个人都花一点时间来庆祝Go社区以及我们所取得的一切。我代表Google的整个Go团队，感谢过去十年来加入我们的每个人。让我们开启下一个更加不可思议的十年吧！

![img{512x368}](../../assets/61df8cbcb9a5407f.jpg)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2019, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论