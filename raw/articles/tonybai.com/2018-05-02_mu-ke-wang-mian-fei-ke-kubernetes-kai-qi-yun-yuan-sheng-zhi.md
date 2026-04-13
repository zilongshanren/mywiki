---
title: 慕课网免费课“Kubernetes：开启云原生之门”上线
url: https://tonybai.com/2018/05/02/imooc-course-kubernetes-open-the-gate-to-cloudnative-go-online/
published: '2018-05-02'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 慕课网免费课“Kubernetes：开启云原生之门”上线

这两年一直在做一个基于[Kubernetes](https://tonybai.com/tag/kubernetes)的、用于互联网产品运营支撑的类PaaS平台，因此一直把自己定位为一个Kubernetes实践者：以Kubernetes为中心进行[集群搭建](https://tonybai.com/2016/12/30/install-kubernetes-on-ubuntu-with-kubeadm/)、运维、k8s相关技术的理解与应用、k8s新技术的追踪和尝试落地等。不过就Kubernetes的深入程度来说，感觉自己和那些天天与k8s打交道的大厂专家或以容器云为卖点的技术专家还是有差距的。但是大厂专家每周996，闲暇时间不多，这让他们无暇系统化地传道受业解惑，而我却有一些闲暇时间来写写有关Kubernetes的知识和经验。于是在春节前，一次机缘巧合，和慕课网“勾搭上了”并达成一致：在慕课网做一门有关Kubernetes的课程。

按照慕课网的要求，我要先上一门有关Kubernetes的免费公开课。于是经过“漫长”的录制和制作后，我的第一门在线网课[《Kubernetes：开启云原生之门》](https://www.imooc.com/learn/978)于今天在慕课网正式上线了。

**课程链接：https://www.imooc.com/learn/978 **

![img{512x368}](../../assets/ab67120045a49eb7.png)


### 一. 课程介绍

先来简单介绍一下这门不到2小时的[免费课程](https://www.imooc.com/learn/978)。

[容器技术](https://tonybai.com/tag/docker)和Kubernetes重新定义了现在以及未来十年基础设施承载云原生应用的形式，作为[CNCF基金会](https://www.cncf.io/)下面的首席托管项目，Kubernetes在2017年击败swarm和mesos，成为了容器管理与调度编排领域的首选平台和事实标准。今年年初，CNCF又宣布[Kubernetes正式毕业](https://www.cncf.io/announcement/2018/03/06/cloud-native-computing-foundation-announces-kubernetes-first-graduated-project/)，标志着Kubernetes作为一个开源项目已经成熟，并且具有足够的韧性，可以在任何行业和各种规模的公司的生产环境中大规模应用了。Kubernetes存在的意义还不仅仅局限于容器编排解决方案，其最终使命应该是成为云计算时代的新一代应用上云的首选平台，成为支撑云原生应用部署运行的新一代”云平台”。

对于普通开发人员来说，Kubernetes虽然结构简单，但规模“庞大”，所涉技术与生态圈外延较广，学习曲线较为陡峭。我的这门基础课就**定位于帮助大家降低学习门槛，打开通往k8s平台支撑的云原生的大门的**。

这门课程共分为五个部分。

第一部分：了解一下应用部署运行模式的变迁历史，弄清楚每种应用部署运行模式的特点、对开发者的影响以及模式演进的趋势。

第二部分：了解Kubernetes究竟是什么? 我们为什么要使用Kubernetes，它能给开发者带来哪些好处？

第三部分：实际操作如何在Kubernetes集群上部署和管理一个应用。

第四部分：学习一下Kubernetes的架构、组件以及组件功用。

第五部分：以Kubernetes对象模型为主线，一起来学习一下Kubernetes的基本概念。

通过这门课程的学习，我期望大家能掌握如下知识和技能：

1、Kubernetes是什么？

2、为什么要使用Kubernetes? Kubernetes给开发者带来哪些好处？

3、如何在Kubernetes集群上部署和管理一个应用

4、Kubernetes的架构

5、Kubernetes的组件与功用

6、Kubernetes对象模型以及基础概念

课程针对的对象也很宽泛，对于那些对容器、Kubernetes感兴趣的开发、测试、运维人员；架构师和技术决策者；技术爱好者都可以观看一下该课程视频。同时，这个课程也将起到“承上启下”的作用，为后续在慕课网的Kubernetes实战课（录制中）做铺垫。

### 二. 录课心得

这是我第一次录网课，完全没有经验可谈。还好在录课准备期间，慕课网的胡老师给予我很专业的支持。

作为网课讲师，首先要做的其实是学习，即按照委托方对课程的要求，进行ppt结构与形式制作（按照模板）、音视频基础剪辑等方面的学习。一定的剪辑技能可以让你在录制过程中减少很多重复录制，节省不少的精力和时间。

其次，课程定位与内容规划。课程定位是首先要和委托方课程接口人做详细交流，达成一致的，要明确课程难度级别、课程受众对象以及课程的内容重点。内容规划就基本上是你的专业领域的事情了，当然委托方教学接口人会根据他的经验给予你有关课程内容规划的一些很好的建议。

最后就是录制过程了。录制过程其实是“很辛苦”的，要习惯于一个人长时间的独处。由于是利用业余时间录制并且有录制环境要求（至少是安静、无人打扰吧），一周下来其实满足条件的时间窗口并不多。我个人基本上是工作日晚上准备录制脚本、环境和demo例子，周末两天集中录制。录制脚本这块我没有什么诀窍，我的笨招就是将要表述的都写到一个文件中，像台词一样在录制的时候读出来。这样可以保证每段视频是可以被Reproduce的:)。那些实际操作的演示环节，也会按照之前列出的要点进行。

所以录制的这段时间内，基本上是没有周末的，都是待在家里不出门。即便有事的时候，比如陪着孩子去上补习班时，我也是带着笔记本的，编写一些录制脚本或优化一些台词。

### 三. 小结

应用上云，以前都是考虑虚拟机、OpenStack之类的技术栈，现在是时候考虑Kubernetes了。并且在面向容器化应用、云原生应用开发和运维方面，一批旨在降低开发难度、改善开发体验的开源项目正在兴起，比如号称云原生应用标准库的[metaparticle-io](https://github.com/metaparticle-io)、CoreOS的[operator framework](https://coreos.com/blog/introducing-operator-framework)等。

即便你不会亲手搭建和运维Kubernetes集群，而仅仅是使用现成的基于k8s的容器云服务，那么通过本门课程了解一下Kubernetes的基础知识也是大有裨益的。说不定将来”kubernetes first”或”kubernetes-oriented”会成为时髦的技术词汇。

由于是第一次录制网课，在声音和表达技巧方面显得都不够专业，还望理解。同时也欢迎各位小伙伴针对这门课程参与交流讨论，多提宝贵建议和意见。

最后，感谢慕课网胡老师对本门课程的耐心和专业指导。

补充：**本门免费课对应的实战课程 《Kubernetes实战 高可用集群搭建、配置、运维与应用》已经上线，欢迎大家参与学习和交流。**

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

厉害，我一直在关注你的系列文章。DigitalOcean今天也开始测试k8s了

感谢关注，多多交流:)