---
title: Google内部是如何使用Go语言的
url: https://tonybai.com/2020/08/30/new-case-studies-about-googles-use-of-go/
published: '2020-08-30'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Google内部是如何使用Go语言的

Go语言始于2007年9月，当时Robert Griesemer，Ken Thompson和我开始讨论设计一种新语言，以解决我们和Google同事在日常工作中面临的工程挑战。我们当时编写的软件通常是一个网络服务器-一个与数百台其他服务器交互的程序-并且在其生命周期内，成千上万的程序员可能会参与编写和维护它。但是我们当时正在使用的语言似乎没有提供正确的工具来解决我们在这种复杂环境中面临的问题。

因此，我们坐了一个下午，开始讨论一种不同的方法。

当我们于2009年11月首次向公众发布Go时，我们不知道该语言是否会被广泛采用或是否会影响未来的编程语言。回顾2020年，Go在这两方面都取得了成功：它在Google内部和外部都得到了广泛使用，其网络并发和软件工程方法对其他语言及其工具产生了显着影响。

事实证明，Go的影响范围比我们预期的要广泛得多。它在行业中的增长令人瞩目，并为Google的许多项目提供了动力。

![img{512x368}](../../assets/b76460b19c2753cf.png)


感谢Renee French提供的Gopher插图。

在Google内部，Go用于生产用途最早出现在2011年，那一年我们在[App Engine](https://blog.golang.org/appengine)上发布了Go，并[开始通过Vitess为YouTube数据库提供流量代理服务](https://www.youtube.com/watch?v=midJ6b1LkA0)。当时，[Vitess](https://github.com/vitessio/vitess)的作者告诉我们，Go正是他们所需要的那种语言- 简单网络编程，高效执行和快速开发的结合，并且如果不使用Go，他们可能根本无法构建这个系统。

第二年，[Go取代Sawzall被用作Google的搜索质量分析](http://www.unofficialgoogledatascience.com/2015/12/replacing-sawzall-case-study-in-domain.html)。当然，Go还推动了Google在2014年[开发和推出Kubernetes](https://cloudplatform.googleblog.com/2014/06/an-update-on-container-support-on-google-cloud-platform.html)。

在过去的一年中，我们发布了来自[十六个来自全球Go用户的案例研究](https://go.dev/solutions)，这些案例讨论了他们如何使用Go大规模构建快速、可靠和高效的软件。今天，我们将添加来自Google内部团队的三个新的案例研究：

-
核心数据解决方案： Google的

[核心数据](https://go.dev/solutions/google/coredata)团队用更灵活的微服务系统取代了用C++编写的整体式索引管道以为Google搜索提供支持，其中大多数服务使用Go编写。 -
Google Chrome：精简模式下的

[Google Chrome](https://go.dev/solutions/google/chrome)移动用户依靠Chrome优化指南服务器来提供提示，以优化其地理区域内知名网站的页面加载。用Go语言编写的服务器每天可为数百万用户提供更快的页面加载速度和更低的数据使用率。 -
Firebase：Google Cloud客户选择

[Firebase](https://go.dev/solutions/google/firebase)作为他们选择的移动和网络托管平台。加入Google后，该团队将其后端服务器从Node.js完全迁移到Go，以实现轻松并发和高效执行。

我们希望这些故事能为Go开发人员和社区提供更深入的见解，以了解Google团队选择Go的原因，使用Go的目的以及团队做出这些决定的不同途径。

如果您想分享有关您的团队或组织如何使用Go的故事，请与我们联系。

杰出工程师[Rob Pike](https://github.com/robpike)提供。

本文翻译自Google官方博客：[《New Case Studies About Google’s Use of Go》](https://opensource.googleblog.com/2020/08/new-case-studies-about-googles-use-of-go.html)。

我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

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

© 2020, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

这些案例很好地展示了Go在并发与工程效率上的优势，难怪能支撑Google和业界的大规模系统。也期待更多迁移细节与性能对比的实战分享。

I’ve been playing The Forge on Roblox for a while, and The Forge Wiki helped me a lot. The ores and weapons guides are super clear and up to date. Definitely worth bookmarking if you’re serious about the game.

看到 Go 逐渐成为支撑大规模系统的关键语言，真是令人振奋，这些案例对社区开发者非常有启发。

I like that RoboLibrary‘s homepage isn’t cluttered with noise. It points me to the right sections fast, and the linked strategy guides are useful when I want deeper detail.