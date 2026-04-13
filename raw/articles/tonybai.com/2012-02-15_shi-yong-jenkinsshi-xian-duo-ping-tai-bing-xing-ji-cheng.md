---
title: 使用Jenkins实现多平台并行集成
url: https://tonybai.com/2012/02/15/intergating-on-multiple-platforms-simultaneously-using-jenkins/
published: '2012-02-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用Jenkins实现多平台并行集成

我们的后端[C应用](http://tonybai.com/tag/C)都是支持跨平台的，至少目前在[Linux](http://tonybai.com/2011/04/29/feel-experience-after-using-ubuntu-for-one-year/)和[Solaris](http://tonybai.com/2009/09/10/something-about-installing-solaris-10/)上运行是没有问题的，这样一来我们在配置持续集成环境时就要考虑如何实现在代码Commit后触发多平台并行(同时)集成这个需求。

之前使用[Buildbot](http://tonybai.com/2011/05/18/set-up-ci-environment-with-buildbot/)时是通过为一个Scheduler配置多个Builder满足这个需求的。但现在要换成[Jenkins](http://jenkins-ci.org)，我们如何来实现呢？昨天在[折腾Jenkins](http://tonybai.com/2012/02/14/install-and-configure-jenkins/)时我把问题想简单了，今天细致查看了一下Build Log后才发现之前的配置并未真正实现多平台并行集成。

最初的Jenkins配置大致是这样的：我在Jenkins上添加了两个节点(Slave Node)，分别为x86-linux-ci-slave和x86-solaris-ci-slave，并且为这两个节点设置了一个相同的标签"foo-ci-slaves"。之后我创建了一个新Job – "foo-multiplatform-ci"，选择的是"构建一个自由风格的软件项目(Build a free-style software project)"。为了使得该Job执行并行集成，我选择了"Restrict where this project can be run"，在"Label Expression"中填上了"foo-ci-slaves"，其他配置这里就不赘述了。

按照我最初的理解，这样配置后点击"立即构建"，两个Slave Node上就会同时进行相关的集成。但Build Log告诉我事实并非我想象的那样：Jenkins只是在一个Slave Node上执行了Job。那使用Jenkins如何来实现前面所说的多平台并行集成呢？查来查去，我发现原来是我在创建Job时选错了配置，我应该选择"构建一个多配置项目(Build multiconfiguration project)"。

与free-style project相比，multiconfiguration project的配置页面中不见了"Restrict where this project can be run"配置选项，但却多出了一个"Configuration Matrix"配置区域。在该区域中，我们可以选择Slaves，在Node/Label中，我们可以看到当前Jenkins中配置的所有Label和Nodes。选择一个Label是无法满足我们的要求的，那样Jenkins只会从Label中的若干个节点中选择一个来执行集成。所以我选择Nodes，将x86-linux-ci-slave和x86-solaris-ci-slave都选上，保存后我们就会在"foo-multiplatform-ci" Job的主页面上看到两个configuration: x86-linux-ci-slave和x86-solaris-ci-slave。点击"立即构建"，这两个configuration对应的小球标志就会同时闪动，这说明"foo-multiplatform-ci"正在两个Slave Node上并行运行呢，这才是我想要的结果。

支持多平台并行集成只是Multiconfiguration Project的一个用途之一，《[Jenkins: The Definitive Guide](http://book.douban.com/subject/6434790/)》一书对此有更为细致的讲解，你可以结合自定义Axis(坐标轴)以及parameterized Build实现更为复杂的构建需求。但目前我尚未遇到类似需求，所以这里也不敢乱说^_^。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

请教一个问题，照您的方法配置后，确实可以同时在多个node上同时跑同一个job,但是每台机器的workspace项目目录下会多一级以节点名命名的目录，此目录下才是构建产物，请问有什么方法可以去掉多出来的那一级节点名目录吗？

为何要去掉这一级节点名目录呢？一般来说，jenkins生成什么数据，我们不需要关注啊，我们只是关注ci是否ok就好了或者哪块出现了问题。