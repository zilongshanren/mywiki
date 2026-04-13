---
title: Go官方发布的go.dev给gopher们带来了什么
url: https://tonybai.com/2019/11/14/what-the-godev-website-bring-to-gophers/
published: '2019-11-14'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go官方发布的go.dev给gopher们带来了什么

众所周知，[Go是一个诞生于Google内部的编程语言](https://tonybai.com/2017/09/24/go-ten-years-and-climbing/)，它在[2009年11月份开源](https://tonybai.com/2019/11/09/go-opensource-10-years/)，在开源后立即受到了来自全世界开发人员的关注与贡献。但初期的Go语言的发展依旧是由Go核心团队的若干leader决定的，这种类“民主集中制”的方法延续了若干年。直到Go核心团队逐渐意识到Go应该更多倾听社区的声音，并让更多的gopher参与到Go项目的开发和贡献中来，甚至影响和决定一些语言特定的演化。于是Go团队开始特意为Go社区发展**招兵买马**。像[Steve Francia](https://spf13.com/)、[Francesc Campoy](https://campoy.cat/)（后已经从google离职加入[Dgraph](https://dgraph.io/)）等都是在这个阶段加入Go team的。

Go团队在很长一段时间里尤其重视与社区的互动，比如连续多年发起[Go user调查](https://blog.golang.org/survey2018-results)、[Gophercon大会](https://www.gophercon.com/)后的Go team[与社区的见面会和分组讨论](https://blog.golang.org/contributor-workshop)、[去GOPATH降低Go入门学习曲线](https://tip.golang.org/doc/go1.8#gopath)、[发布Go新品牌标识](https://blog.golang.org/go-brand)、添加[Go module机制](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)、[改善官网](https://golang.org/)等。

在今天Go官博发文：[“Go.dev: a new hub for Go developers”](https://blog.golang.org/go.dev)，正式发布[go.dev站点](https://go.dev/)，该站点被Go核心团队寄望于成为全世界Gopher开发人员的中心。它将告诉gopher（无论新手还是老油条）：谁在使用Go、用Go做什么、怎么学习Go(Go的各种学习资源、受欢迎的Go package都有哪些以及这些package的详细信息）。

![img{512x368}](../../assets/f680fe2e12f21b00.png)


go.dev发布之后，golang.org官网将更加聚焦go开源项目本身的开发、语言演化以及Go版本发布。而go.dev将成为gopher日常使用go语言的中心，包括go学习、go方案、go应用案例等。在这里我们简单探索一下go.dev这个站点究竟给gopher们带来了什么(这仅仅是go.dev的最小功能发布，后续go.dev可能会演化出更多特性、并根据社区反馈更好满足gopher需求)。

## 一. [学习资源](https://learn.go.dev/)聚合

go.dev的一个重要功能就是**帮助首次进入Go世界的开发人员学习Go**。

在go.dev的”learn”栏目下，我们在第一屏就看到了Go新手入门的三个步骤：安装、”Hello World”、Go tour以及[更为详尽文档的入口](https://golang.org/doc/)：

![img{512x368}](../../assets/525990039cf3ab5d.png)


接下来，go.dev提供了这些年口碑较好、受到gopher欢迎的一些初级在线学习资源：

![img{512x368}](../../assets/5570880b1c812317.png)


像gobyexample.com、gophercises.com都在推荐行列。

Go技术类书籍以及培训资源是gopher学习Go过程中不可缺少的：

![img{512x368}](../../assets/34657c498b81c53e.png)


Go.dev在learn栏目下推荐了一些口碑不错的Go书籍，比如：Alan A. A. Donovan和[Brian W. Kernighan](https://www.cs.princeton.edu/~bwk/)合著的[Go圣经：《The Go Programming Language》](http://www.gopl.io/)被在首位推荐。知名Go培训师William Kennedy的[培训](https://www.ardanlabs.com/)也被推荐给了大家。不过口碑不错的书籍[《Go in action》](https://book.douban.com/subject/25858023/)我觉得也应该列入推荐行列。

在Learn栏目最后，是全世界各地近期有关Go的meetup活动的schedule，Gopher可以得到最及时的meetup信息，并选择参加。

## 二. 成熟解决方案参考

![img{512x368}](../../assets/01c17666a5f9c943.png)


go.dev开辟的”solution”栏目旨在提升go的开发过程。栏目从“云原生和网络服务开发”、“命令行程序开发”、“web开发”以及Devops/Site Reliability四个方面提供聚合化的资料。以“云原生和网络服务开发”为例，Go.dev提供了这方面的典型项目和用户、使用方法、关键方案（一些书籍、成熟框架、客户端库以及其他资源）。

go.dev solution栏目还提供了一些Go的典型客户以及这些客户使用Go的典型案例：

![img{512x368}](../../assets/1a199c9e305200fc.png)


## 三、Package信息聚合中心

在go.dev的“explore”栏目下，我们看到的是Go package的信息中心：

![img{512x368}](../../assets/dc5d3d21fddabb16.png)


就如上图所示，这里提供了受欢迎的package和特色package的推荐列表，以及package信息的搜索功能。

以[logrus为例](https://tonybai.com/2018/01/13/the-problems-i-encountered-when-writing-go-code-issue-1st/)：

![img{512x368}](../../assets/219a5f41cdeb1882.png)


在[logrus包](https://github.com/sirupsen/logrus)的主页，我们看到了有关logrus的各种信息，项目repo地址、最新版本号、module名字、开源许可证信息、文档（应该是集成了godoc返回的结果）、它的依赖、以及以它为依赖的项目(见下图)：

![img{512x368}](../../assets/b95cce10dad6f260.png)


## 四. 小结

go.dev目前处于最小产品状态(mvp)，从目前已经提供的栏目来看，go.dev能为gopher提供的帮助已经很全面了。后续go.dev站点的运营好坏（比如：信息更新是否及时等）将决定go.dev是否能达到其预期的期望。

go.dev目前似乎还缺少论坛功能。不过已有的[golang-nuts](https://groups.google.com/forum/#!topic/golang-nuts/)、[gobridge](https://forum.golangbridge.org/)已经承担了这个角色，但如果能有一个官方论坛（一站式）就再好不过了。

go.dev在国内可以访问，就是速度有些慢（可能因地区而异）。

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

2009？

笔误，已改。感谢提醒。

2006我就知道有只大牛叫bigwhite

感谢持续多年的关注:)