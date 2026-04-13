---
title: vendor目录是否需要提交到代码库中？答案全在这一篇
url: https://tonybai.com/2020/12/03/should-you-commit-the-vendor-folder-in-go/
published: '2020-12-03'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# vendor目录是否需要提交到代码库中？答案全在这一篇

![img{512x368}](../../assets/4310199ce8456115.png)


如果您还在使用vendor机制管理依赖包，那么说明您肯定是处于下面两种情况之一！

- 还工作在传统的GOPATH模式下(使用Go 1.10及之前版本；或Go 1.11及之后版本，但GO111MODULE=off)，利用vendor管理目标包的特定依赖；
- 工作在go module模式下，但仍然利用vendor管理目标module的特定依赖并使用go build -mod=vendor来构建。

那么**我们是否应该将项目中存储依赖包的vendor目录提交到源代码仓库进行管理呢**？如果让笔者给出答案，那就是：**应该**。

要想理解为什么“应该”，我们看看下面Go语言包依赖管理的演化过程就知道了。

Go语言在构建设计方面深受Google内部开发实践模型的影响。

![img{512x368}](../../assets/62f91277d1772de9.png)


Google内部基于主干的开发模型：


– 所有开发人员基于主干trunk/mainline开发：提交到trunk或从trunk获取最新的代码（同步到本地workspace）

– 版本发布时，建立Release branch，release branch实质上就是某一个时刻主干代码的快照；

– 必须同步到release branch上的bug fix和增强改进代码也通常是先在主干上提交(commit)，然后再cherry-pick到release branch上

Go最初的构建管理以及go get就采用了基于[Google内部单一代码仓库(single monorepo)和基于主干(trunk/mainline based)的开发构建模型](https://cacm.acm.org/magazines/2016/7/204032-why-google-stores-billions-of-lines-of-code-in-a-single-repository/pdf)。具体逻辑是：在[Go 1.5版本](https://tonybai.com/2015/07/10/some-changes-in-go-1-5/)之前，go get获取的都是各个Go包所在仓库的trunk/mainline的最新代码。go get会将获取的最新代码放在\$GOPATH/src下面，而go build会在\$GOROOT/src和\$GOPATH/src下面按照包导入路径(import path)去搜索这些包并执行构建操作。

我们看到1.5版本之前Go编译器都是基于目标Go程序依赖包的trunk/mainline上的最新代码去编译的，这样的机制带来的问题是显而易见的，至少包括几点：

- 因依赖包的trunk的变化，导致不同人获取和编译你的包/程序时得到的结果实质是不同的，即构建结果不能重现；
- 因依赖包的trunk的变化，引入不兼容的实现，导致你的包/程序无法通过编译；
- 因依赖包演进而无法通过编译，导致你的包/程序无法通过编译。

为了实现**可重现的构建(reproduceable build)**，Go语言于1.5版本引入了[vendor机制](https://tonybai.com/2015/07/31/understand-go15-vendor/)：即Go编译器会优先在vendor目录下搜索依赖的第三方包，这样如果开发者将特定版本的依赖包存放在vendor下面并提交到代码仓库，那么所有人理论上都会得到同样的编译结果，从而实现可重现的构建。

在Go 1.5发布后的若干年，Gopher们把注意力都集中在如何利用vendor解决包依赖问题，从手工添加依赖到vendor、手工更新依赖，到一众包依赖管理工具的诞生：比如: [govendor](https://github.com/kardianos/govendor)、[glide](https://github.com/Masterminds/glide)以及当时号称准官方工具的[dep](https://github.com/golang/dep)，都在努力地尝试着按照当今主流思路解决着诸如：“钻石型依赖”等难题。

但Go核心开发团队没有走寻常路，而是另辟蹊径地在[Go 1.11](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)中引入了采用了[最小版本选择(mvs)](https://tonybai.com/2019/12/21/go-modules-minimal-version-selection/)的go module。至此，Go的构建模式被一分为二：gopath mode和module-aware mode。在module-aware mode下，Go构建工具链默认不再使用传统GOPATH下或顶层vendor下面的包了，而是使用\$GOPATH/pkg/mod下面的第三方依赖Go module的local cache。理论上，go module真正实现了“可重复的构建”，我们无需再使用Go 1.5引入的vendor机制了。但社区的反馈让Go核心开发团队[将module顶层目录下的vendor目录保留了下来](https://groups.google.com/g/golang-dev/c/FTMScX1fsYk/m/uEUSjBAHAwAJ)，主要考虑vendor还能在下面场合“发光发热”：

- 保持Go1兼容性

可继续支持[Go 1.5](https://tonybai.com/2015/07/10/some-changes-in-go-1-5/)以后，[Go 1.10](https://tonybai.com/2018/02/17/some-changes-in-go-1-10/)之前的Go版本编译Go 1.11后续版本的源码(仅限于：启用了module并带有vendor)。

- 支持离线构建(offline build)

module/包构建所需的全部依赖都放入了vendor目录，这样即便在无网络连接的情况下，我们依然可以进行module的构建。这尤其适合企业内部执行CI/CD的那些可能没有外网访问权限的主机。

- 提高构建性能，缩短CI/CD时间

在CI/CD时，由于每次都是重新构建，在module-aware模式(非vendor)下，每次都需要重新下载依赖的module到本地，这样十分耗时。而采用vendor方式则无需下载依赖module，提高了构建性能，缩短CI/CD的时间。

- 解决“消失的包/module”的问题

一些module/包在经年岁月后可能被从github等托管站点删除了，这时我们如果依赖这些module/包，我们将遇到构建错误（Go Proxy的存在显然让这种可能行极大的降低了）。而使用vendor已经将包/module存放到了本地(以及自己的代码仓库中)，可以解决“包/module消失”的问题。

- 快速分发module的所有依赖包

vendor目录下存放了当面module的所有依赖包(及版本)，易于打包并分发。尤其对一些无法通过go get获取到的依赖包/module，这尤为适用。

上述“演化简史”反复提到了**“可重复构建”**，这就是Go核心团队先后推出vendor、go module所基于的核心“痛点”。并且“可重复构建”不单单是个人行为，更多是一个“团队(可以扩展到整个Go社区)”行为：**让团队所有人拿到同样的代码并构建出同样的成果物**。这样来看，**如果不将vendor提交到源码仓库，我们就无法实现这一目标**。

在将vendor提交到代码仓库过程中，你也许会抱怨依赖的代码包太多、依赖变化频繁的问题。但go module所使用的[“最小版本选择”](https://tonybai.com/2019/12/21/go-modules-minimal-version-selection/)已经将依赖变动降低到不能再低的程度了，至少比采用主流“依赖管理”思路的其他语言，比如js，构建时面临的变动要少很多了。另外降低依赖的代码包的数量也是你自己的责任，[Go是“自带电池”的编程语言](https://www.imooc.com/read/87/article/2341)，其标准库中有很多优秀的包可用，尽量使用标准库包以降低过多的“依赖”。

更多关于Go module和包依赖管理的内容，请查看技术专栏[《改善Go语言编程质量的50个有效实践》](https://www.imooc.com/read/87/)。

![](http://image.tonybai.com/img/202011/qgo-column-pgo-with-qr-and-text.png)


**“Gopher部落”知识星球开球了！**高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！星球首开，福利自然是少不了的！2020年年底之前，8.8折(很吉利吧^_^)加入星球，下方图片扫起来吧！

![](../../assets/d3fad3142fe3cc39.png)


我的Go技术专栏：“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”上线了，欢迎大家订阅学习！

![img{512x368}](../../assets/018ff45f7e150fca.png)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/e9f90df4cc2580e5.png)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

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

© 2020, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论