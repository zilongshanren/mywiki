---
title: Go项目组织：在单一repo中管理多个Go module指南
url: https://tonybai.com/2023/05/10/a-guide-of-managing-multiple-go-modules-in-mono-repo/
published: '2023-05-10'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go项目组织：在单一repo中管理多个Go module指南

![](../../assets/21a1c11bbacff63f.png)


[本文永久链接](https://tonybai.com/2023/05/10/a-guide-of-managing-multiple-go-modules-in-mono-repo) – https://tonybai.com/2023/05/10/a-guide-of-managing-multiple-go-modules-in-mono-repo

## 0. 单repo单module管理回顾

众所周知，[Go在1.11版本中引入了go module](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)，随着近几年Go module机制的逐渐成熟，它已经被Go团队确定为**Go标准的依赖管理与构建方案**，原先的GOPATH mode已经被彻底废弃。

在Go module模式下，最常见的Go项目组织方式就是**一个repo(代码仓库)对应一个Go module**。repo的根路径中放置go.mod文件，repo的根路径也是module root directory。该Go module下的package的导入路径则由go.mod中的module path以及该package相对于module root directory的路径共同构成。

以“example.com/go”这一module path为例，如果某个package存放在foo/bar下，那么bar下的package的导入路径就是“example.com/go/foo/bar”；如果是v2版本，那么导入路径为“example.com/go/v2/foo/bar”。

在一个repo对应一个Go module的策略下，Go module的版本管理和发布也相对容易，通常我们[采用分支方式来进行major号升级](https://tonybai.com/2019/06/03/the-practice-of-upgrading-major-version-under-go-module)(如下图)，[通过tag来进行版本发布](https://tonybai.com/2020/12/26/how-to-deprecate-a-published-version-of-some-specific-go-module)。

![](../../assets/2f0e078c91f837ef.png)


上图是单repo单module的分支管理方案，两种方案均可。

左侧的方案中：master分支承载v0-v1，每升级一个major号，建立一个vN分支，default分支指向最高major号的分支，方便开发者clone repo时直接拿到最新的代码。

注：左侧方案有一个问题，那就是一旦default分支执行最高major号分支vN，那么你如果要go get master分支的最近更新，需要显式指定master分支，比如: go get example.com/go/foo/bar@master。使用latest或不加任何分支名都无法获取到master上的最新更新。


右侧的方案也是建立vN分支，但不同的是，该方案会将master分支作为active开发分支，也是默认分支并定期将稳定后的feature同步到最高major号分支，这也是我个人比较喜欢的方式。前不久刚刚被官宣为redis官方Go客户端的[go-redis](https://github.com/redis/go-redis)采用的就是这个方案(下面是go-redis的vN分支情况)：

![](../../assets/a51c4fb9688c9fdf.png)


注：在单一repo中管理一个go module的方法十分成熟了。我在专栏

[《Go语言第一课》]的06和07讲对此做了系统的讲解，感兴趣的小伙伴可以去阅读一下。

有了单repo单module的项目组织方式，就会有单repo多module的组织方式，比如著名的[etcd项目](https://github.com/etcd-io/etcd/)，就是在一个repo中管理多个go module的典型例子。

那么为什么要在一个repo中管理多个go module呢？我们继续往下看。

## 1. 为什么要在一个repo中管理多个Go module

其实这个问题的本质是**monorepo与multiple repo之间的“战争”**。那么上述问题也就变成了一个monorepo与multiple repo的优劣对比。我个人从未真正使用过monorepo这种所有项目代码都放在一个单一仓库中的组织形式，不过从网上的公开资料来看，monorepo有如下的一些优点：

- 容易看到

如果你正在做一个调用其他微服务的微服务，你可以看一下代码，了解它是如何工作的，并确定bug是来自你自己的代码还是其他团队的微服务。

- 代码共享

团队为微服务重复编写代码会产生额外的工作开销。有了monorepo，团队可以更容易地分享代码。

- 改进协作

有了monorepo，就更容易在各团队之间实现代码和工具的标准化。

- 标准化

单一代码仓库使得跨团队的代码和工具的标准化更加容易。

- 可发现性

有了monorepo，更容易找到你需要的代码。

- 发布管理

单一版本使我们更容易地管理跨多个服务的发布。

- 更容易重构

重构代码在单版本中更容易，因为所有的代码都在一个地方。

当然，使用单一代码仓库也有一些缺点，这些缺点也足以让很多组织和开发团队对其望而却步：

- 增加仓库的大小

一个单库通常会比只包含一个项目的版本库大。这可能会导致更长的构建时间和更多的磁盘空间使用。

- 增加复杂性

单一代码仓库的管理比只包含一个项目的版本库更复杂。这是因为有更多的代码需要跟踪和管理。

- 增加冲突的风险

当多个开发者在单一仓库中处理相同的代码时，会有更大的冲突风险。这是因为开发人员可能在同一个代码的不同版本上工作。

- 不能限制访问

monorepo不允许有选择的分享。

- 陡峭的学习曲线

当新的开发者开始与已经有monorepo的组织合作时，他们通常需要足够长的时间来适应所有紧密耦合的依赖关系。

总的来说，使用monorepo既有优点也有缺点，是否使用monorepo最终还是要取决于项目和团队的具体需求。

不过，monorepo下的多module是实际存在的，并且Google内部就是如此，显然go module也一定要对此做很好的支持的，下面我们就来看看go是如何支持mono repo下的多个go module的。

我们先来看看mono repo下各个go module的导入路径的确定。

## 2. monorepo中各个go module下的package的导入路径

在前面回顾单repo单module的项目组织方式下，module下的package的导入路径为：**module path+package在module root directory下的相对路径**。那么monorepo中各个go module下的package的导入路径又是什么呢？

首先monorepo下的各个go module的module root路径并非monorepo的root路径，以下面的结构举例；

```
example.com
└── go/
├── mqtt/
│ ├── bar/
│ │ └── go.mod
│ └── foo/
│ └── go.mod
└── vehicle/
├── baz/
│ └── go.mod
└── zoo/
└── go.mod
```


我们看到在example.com这个顶层目录下并没有go module，go modules分布在example.com下的各个子目录中。以mqtt/bar下的go module为例，它的module path应该为**repo根路径+bar的相对路径**，即example.com/go/mqtt/bar，这样bar下面的package pkg1，它的导入路径就为example.com/go/mqtt/bar/pkg1，如果bar这个go module升级到v2版本，则pkg1的导入路径就会变为example.com/go/mqtt/bar/v2/pkg1。其余的go module下的packge的导入路径以此类推。

## 3. monorepo下各个go module的版本发布

在单repo单module下，我们通过打vx.y.z标签的方式发布module，但是在monorepo多module下，再在repo上针对repo打整体的、诸如v1.0.1这样的标签就没有太大意义了(当然为了整体管理的需要，依然可以打整体标签，比如像etcd那样打v3.5.8)，并且对于monorepo下的多个go module而言，go get也不会识别这种整体标签，那么我们该如何发布monorepo下的go module呢？

其实也很简单，我们为module单独打标签来发布。以上面的example.com/go/mqtt/bar这个module为例，如果我们要为其发布v1.0.0版本，我们需要为example.com这个repo打上tag：go/mqtt/bar/v1.0.0；如果它要发布v1.1.0版本了，我们则需为example.com这个repo打上tag：go/mqtt/bar/v1.1.0。也就是说要发布哪个module，就**用module相对于monorepo根的相对路径+版本号作为tag号**。

## 4. monorepo下各个go module的major版本变更

了解了上述monorepo下各个go module的版本发布方式后，我们就可以将monorepo下的每个go module像单repo单module那样单独对待了！以example.com/go/mqtt/bar为例，当major版本变更时，我们可以建立类似go/mqtt/bar/v1分支，然后将master分支的go.mod中的module path改为example.com/go/mqtt/bar/v2，这样我们就可以在go/mqtt/bar/v1分支继续维护v1版本的bar module，并打tag：go/mqtt/bar/v1.x.y；在master分支维护v2版本的bar module，并打tag：go/mqtt/bar/v2.x.y。

当然go还支持另外一种major版本的维护方式，那就是通过目录隔离。当major版本要升级为v2时，我们可以在go/mqtt/bar下面建立v2目录(像v2这类目录被称为major version subdirectories)，然后在v2目录下维护major为v2的版本，这种方式下你就无需建立vN分支了，可以**在master上通过目录隔离的方式同时维护多个major版本**。发布时，同样打go/mqtt/bar/v2.x.y标签。这种方式一个最大的好处就是与GOPATH mode可以“无缝衔接”，因为GOPATH mode下，go工具链就是通过路径查找package的。

不过这种major version subdirectories的方式并不常用，即便在开源项目中也是比较少见的。

## 5. 小结

本文介绍了go module的基础概念，回顾了单repo单module的包管理方法，包括版本发布、major号升级等。接下来，我们介绍了monorepo下管理多个go module的方案，除了在打tag时要注意带上相对路径外，monorepo下module的包管理方法与单repo单module本质上是一致的。

## 6. 参考资料

- REPO STYLE WARS: MONO VS MULTI – https://gigamonkeys.com/mono-vs-multi/
- Mono Repo vs Multi Repo: Deep Dive Into The Neverending Debate – https://speakerdeck.com/lemiorhan/mono-repo-vs-multi-repo-deep-dive-into-the-neverending-debate

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论