---
title: TB一周萃选[第3期]
url: https://tonybai.com/2017/12/30/3rd-issue-of-the-tech-weekly-carefully-chosen-by-tonybai/
published: '2017-12-30'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# TB一周萃选[第3期]

本文是首发于[个人微信公众号](https://mp.weixin.qq.com/mp/qrcode?scene=10000005&size=102&__biz=MzIyNzM0MDk0Mg==&mid=2247483848&idx=1&sn=a3cd9182a2b2d3716623cc2c43d59f37&send_time=)的文章**“TB一周萃选[第3期]”**的归档。

![img{512x368}](../../assets/daacae839090b221.jpg)


`《岁旦》`

宋伯仁 宋代诗人

居间无贺客，早起只如常。桃版随人换，梅花隔岁香。


春风回笑语，云气卜丰穰。柏酒何劳劝，心平寿自长。

本期萃选是2017年的最后一期，也是迎接2018新年“承前启后”的一期。

对于现代中国人来说，公历新年又称为“元旦”。但稍有些历史常识的朋友都会知道：此“元旦”与中国古时的那个“元旦”有所不同。古代中国人把农历大年初一称为元旦，传说古时“元旦”在距今4000多年前“尧舜禹”的时候就已经有了。1911年辛亥革命成功后，当时孙中山领导的国民政府把农历的大年初一称春节，把公历1月1日称元旦，这就是现在元旦的由来。现代中国的元旦，在世界更广的范围内被更多称为“新年”，是全世界人们的一个共同的节日。在这样的一个节日里，人们家庭团聚，亲友重逢，倾诉过往，憧憬新年，祈求平安。

节日，似乎是群居生物的一种典型的行为表现形式，动物有之（可能是以我们无法理解的形式），人类也在进化的几十万年（又或更长的时间）内设定了大大小小的各种节日。这是作为群居动物的人类的一个重要需求，是进化数十万年后依然保留的最古老的基因所表现出的行为倾向。人类通过“节日”来“蓄力”，以迎接新的挑战！不同的是，古代人类挑战的是凶恶的生存环境，现代人类抗争的是现代生活无形的“生活压力”。

不过，人类从来没有屈服于困难！近期火热的电影[《芳华》](https://movie.douban.com/subject/26862829/)向我们直观生动地阐释了这一点，让我们更加明白生活的真谛，珍惜与家人、爱人、朋友在一起的时光，享受现在的生活，乐观的面对人生。

![img{512x368}](../../assets/36c8f0accbae6ce8.jpg)


## 一、一周文章精粹

### 1. Go初学者的类型系统入门

对于[Go](http://tonybai.co/tag/go)初学者而言，尤其是对那些从[OO语言](https://en.wikipedia.org/wiki/Object-oriented_programming)转到Go的开发者，在他们大脑中根深蒂固的OO type hierachy不见了，这让他们似乎一下子失去了着力点或抓手。原Go core team成员[JBD](https://rakyll.org)撰文阐述了Go类型系统的特点，诸如：流程优先、嵌入不是继承、多态、没有构造函数、没有范型等。

原文链接：[《The Go type system for newcomers》](https://rakyll.org/typesystem/)。

### 2. Go反射详解

Go语言提供了反射(reflect)特性，在标准库中很多常见功能都是用反射实现的，比如：encoding/json、fmt包的Println系列等。但日常编程中，直接使用[reflect包](http://tonybai.com/2015/09/17/7-things-you-may-not-pay-attation-to-in-go/)的场合并不多。reflect为Go程序员提供了一种在运行时 “陷入” 的机制，使得Go程序具备了直接操作runtime中类型元数据的能力以及在运行时凭空“制造”变量的能力，因此reflect操作是比较“危险”的。

Sidhartha Mani的“Go反射详解”分为两个part，part1主要讲解type与kind的区别、基于reflect包的type和value进行Go原生类型变量的构造和值的析出；part2则是针对复合类型，比如数组、map、struct等类型变量的构造和值的析出进行讲解，思路十分清晰。

原文链接：

[《Go Reflection: Creating Objects from Types — Part I (Primitive Types)》](https://medium.com/kokster/go-reflection-creating-objects-from-types-part-i-primitive-types-6119e3737f5d)

[《Go Reflection: Creating Objects from Types — Part II (Composite Types)》](https://medium.com/kokster/go-reflection-creating-objects-from-types-part-ii-composite-types-69a0e8134f20)

### 3. 现代网络负载均衡和代理指南

lyft的envoy工程师撰文对高可用分布式网络中的负载均衡和反向代理做了详尽的科普性讲解，内容包含：lb与proxy的区别、L4 lb、L7 lb、lb特性分析、lb的拓扑类型、当前L4-lb技术、L7-lb技术现状的情况、全局lb和集中控制平面等。强烈推荐阅读！

![img{512x368}](../../assets/0123d2ac227aac85.png)


### 4. Go编译器内幕

这是由国内一位就职于ARM公司的开发者在Go dev group上发的topic，这位开发者将自己学习和整理了Go compiler的原理（主要针对ARM平台）放在了一篇slide中，并在Go core team的反馈下，对他的slide进行了修正和优化。这份资料对于想深入了解Go compiler的朋友可能是大有裨益的。

原文链接：[“Golang Compiler Internals for arm64″](https://groups.google.com/forum/m/#!topic/golang-dev/abiLfAtpbKg)

### 5. 年度盘点2017之Service Mesh：群雄逐鹿烽烟起

在Kubecon&CloudNativeCon 2017上大放异彩后，Service Mesh在国内已经渐入火热阶段。Service Mesh的著名Advocator：数人云的架构师敖小剑年终前发了此文，对service mesh的发展历史、来龙去脉、各方开源项目和厂商势力分析以及未来发展做了回顾和展望。如果你还不知道什么是service mesh，那借此文赶紧上车吧:)

原文链接：[“年度盘点2017之Service Mesh：群雄逐鹿烽烟起”](http://www.servicemesh.cn/?/article/27)

## 二、一周资料分享

### 1. Microservice’ing like a unicorn with kubernetes, envoy, and istio

随着传播渠道多元化和传播速度的加快，新技术“火”的速度也变得以前所未有。以Service Mesh概念为例（参考了 [“年度盘点2017之Service Mesh：群雄逐鹿烽烟起”](http://www.servicemesh.cn/?/article/27)）：

- 2016 年 9 月 29 日在 SF Microservices 上，“Service Mesh”这个词汇第一次在公开场合被使用。这标志着“Service Mesh”这个词，从 Buoyant 公司走向社区。
- 2017 年 4 月 25 日，William Morgan 发布博文“What’s a service mesh? And why do I need one?”。正式给 Service Mesh 做了一个权威定义。
- 2017 年 5 月 24 日，Istio 0.1 release 版本发布，Google 和 IBM 高调宣讲，社区反响热烈，很多公司在这时就纷纷站队表示支持 Istio。

[istio](https://istio.io/)的正式发布，成为了service mesh的一个重要里程碑事件。谁能否认istio不是另一个Google内部技术的开源版本呢，就好比当年[Kubernetes](http://tonybai.com/tag/k8s)的开源。微服务框架走向统一的service mesh似乎成了大势所趋的趋势。无论国内外，对service mesh的研究、开发和试验，甚至是商用都在如火如荼地进行当中。

Redhat架构师[Christian Posta](http://blog.christianposta.com/)近日在自己的博客上放出一份**正在构建中**的资料：[Microservice’ing like a unicorn with kubernetes, envoy, and istio](http://blog.christianposta.com/istio-workshop/slides/#/title)，对envoy和istio的原理与使用进行案例式的详尽说明，同时配有对应的[示例源码](https://github.com/christian-posta/istio-workshop)。对于希望学习service mesh技术的朋友们，这是一份不可多得的资料。

![img{512x368}](../../assets/929c86f188d1b7d3.png)


## 三、一周工具推荐

### 1. mdp

今天给大家推荐一个比较有Geek赶脚的present工具：[mdp](https://github.com/visit1985/mdp)。

mdp是一款文稿演示工具，与[go present工具](http://tonybai.com/2015/08/22/how-to-view-golang-tech-slide/)有些类似，都是以一种类markdown格式的文档作为输入。不同之处，后者是将演示文稿渲染到浏览器中，而mdp工具则是将文稿渲染到terminal中，效果参见下面图示：

![img{512x368}](../../assets/89ce638d91953edc.png)


mdp支持标准markdown语法，同时也支持通过一些扩展语法实现的特定渲染效果。mdp同时支持一些快捷键控制命令，比如：h,j,k,l组合的翻页控制等。在Mac上可使用brew工具来install mdp，在其他平台可以通过下载源码并自行编译的方式安装。

工具链接：[mdp](https://github.com/visit1985/mdp)

## 四、一周图书推荐

笔者认为人类正在构建支撑未来20-30年支撑人类社会发展的IT技术“有机生命体”，包括：

- 能量系统(类比于细胞化学反应，提供计算能量) – IT基础设施(云计算、vm、k8s、container)、Cloud Native技术框架：microservice 、service mesh(服务治理网络) 、serverless等。
- 神经通道 – 基础高速互联网、移动网络、区块链（信用网络）
- 大脑 – 人工智能、数据与智能算法
- 肢体与感知 –
[机器人](http://tonybai.com/2017/08/01/hello-ros/)、智能交通工具（比如：[无人汽车](http://tonybai.com/2017/08/15/hello-apollo/)等）、智能硬件、Iot等。

其中[区块链技术](https://en.wikipedia.org/wiki/Blockchain)作为未来社会信用网络的重要基础，IT技术人员都应该认真学习。本期我就推荐一本有关区块链技术的开源书：yesky的[《区块链开发指南》](https://yeasy.gitbooks.io/blockchain_guide/content/)。这是一本关于区块链技术的较为系统的开源书。该书探索了区块链概念的来龙去脉，剥茧抽丝，剖析关键技术原理、典型应用场景、分布式系统核心问题，同时讲解了区块链技术的三大典型应用：比特币、[以太坊](https://en.wikipedia.org/wiki/Ethereum)和[Hyperledger超级账本](https://en.wikipedia.org/wiki/Hyperledger)以及相关应用的开发入门。

开源书链接：[《区块链开发指南》](https://yeasy.gitbooks.io/blockchain_guide/content/)

商业纸板图书链接：[《区块链原理、设计与应用》](https://book.douban.com/subject/27127839/)

我的联系方式：

微博：http://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/71dbd0d64d261ba9.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论