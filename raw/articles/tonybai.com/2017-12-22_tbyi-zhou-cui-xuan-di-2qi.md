---
title: TB一周萃选[第2期]
url: https://tonybai.com/2017/12/22/2nd-issue-of-the-tech-weekly-carefully-chosen-by-tonybai/
published: '2017-12-22'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# TB一周萃选[第2期]

本文是首发于[个人微信公众号](https://mp.weixin.qq.com/mp/qrcode?scene=10000005&size=102&__biz=MzIyNzM0MDk0Mg==&mid=2247483848&idx=1&sn=a3cd9182a2b2d3716623cc2c43d59f37&send_time=)的文章**TB一周萃选[第2期]**的归档。

![img{512x368}](../../assets/936e19afc4f323dc.jpg)


封面

“我天性不宜交际。

在多数场合，我不是觉得对方乏味，就是害怕对方觉得我乏味。可是我既不愿忍受对方的乏味，也不愿费劲使自己显得有趣，那都太累了。

我独处时最轻松，因为我不觉得自己乏味，即使乏味，也自己承受，不累及他人，无需感到不安。” ——周国平


本周日晚上就是平安夜了！

[圣诞节](https://en.wikipedia.org/wiki/Christmas)，是西方最重要的节日之一，也是一个公历纪年的最后一个节日。对于中华大地的人们来说，圣诞节这个洋节日影响力倒不是那么大，不过它却是一个重要的日子，它提醒着大家：**这一年要结束了！该总结的总结，该计划的也要开始计划了**。

![img{512x368}](../../assets/399fa7a6d4812e72.jpg)


圣诞节是一个美丽的节日。在西方，绿色的挂满彩饰的圣诞树、创意十足的圣诞贺卡、白胡子红袍子的慈祥的圣诞老人、装满礼物的圣诞袜以及美味的圣诞大餐构成了圣诞节永恒不变的节日主题。不过中国人的过法与西方完全不同，尤其是年轻人。他们喜欢成双成对地在商业街以休闲购物的方式过圣诞节，这不仅是商业元素的引导，可能也是荷尔蒙的需要。对于渐渐步入中年的我而言，家庭的分量更重。守在孩子和老婆身边，更能带来心灵上的温暖。

![img{512x368}](../../assets/dc73afeb009e9a40.jpg)


## 一、一周文章精粹

许式伟是大中华地区Go首席布道者（至少，我还不知道谁使用Go和大力推广Go早过许总^_^），并且身体力行、率先垂范地在自己的项目中、在自己的公司产品全面使用Go技术栈。在这篇文章中，许总回顾了[Go语言10年](http://tonybai.com/2017/09/24/go-ten-years-and-climbing/)来的成长以及他个人使用和推广Go语言的历程。许总对Go有着深刻的理解和洞察力，在这篇文章的结尾处许总再次给出了自己对Go语言未来十年的预测，这里笔者表示不能同意再多了^0^。这里将一段文字摘录如下：

下一个十年会怎样？我知道有一些人很期望 Go 语言特性的迭代。但是如果你抱有这种想法可能会失望，因为下一个十年 Go 不会发生太大的变化。对远期需求变化的预测和把控能力，是 Go 的最大魅力之一。这一点上能够和 Go 相比的是 C 语言（C 语言不同版本的规范差异极少），但因为 Go 要解决的问题更多，做到这一点实际上也更难。下一个十年 Go 仍然会继续深耕服务端开发的生态，同时积极探索其他潜在的应用市场。


原文链接：[“我与Go语言的这十年”](https://mp.weixin.qq.com/s?__biz=MjM5OTcxMzE0MQ==&mid=2653370520&idx=1&sn=69827cc58f3bee76abb9778a8c286915&key=aa4d734c2f5165c43f84c9affec15b08721124970a2831fb8f1fd0bd8e4130234c7a6e9cb300e3a5dccca45b88ba7be73a852e515e8a57c68450ff21b0d47141c160f7a1554c9b532ed449f0fcec8148&ascene=0&uin=MTYwMzM0NjYyMQ%3D%3D&devicetype=iMac+MacBookAir6%2C2+OSX+OSX+10.9.2+build(13C64)&version=11020201&lang=zh_CN&pass_ticket=J6dBgepwYkSeUbwD7vdoXH7qZWH3o0gvnsMESYbiL1opRfDiLSA8owEztxcczj4v)

![img{512x368}](../../assets/6780d7f6a777d6ae.jpg)


图：Go语言的十年

### 2、追求极简：Docker镜像构建演化史

这是笔者在CSDN《程序员杂志》2017.12上投稿的一篇文章。这两年容器技术飞速发展，除了[Docker](http://tonybai.com/tag/docker)之外，又有[Rkt](https://github.com/rkt/rkt)、[kata container](https://katacontainers.io/)等容器引擎或runtime的出现。但Docker依然是容器领域使用最为广泛的主流技术。对于已经接纳和使用Docker技术在日常开发工作中的开发者而言，构建Docker镜像已经是家常便饭。但如何更高效地构建以及构建出Size更小的镜像却是很多Docker技术初学者心中常见的疑问，甚至是一些老手都未曾细致考量过的问题。这篇文章将从一个Docker用户角度来阐述Docker镜像构建的演化史，希望能起到一定的解惑作用。

原文链接：[“Docker镜像构建演化史”](http://tonybai.com/2017/12/21/the-concise-history-of-docker-image-building/)

![img{512x368}](../../assets/a82b00ac7404d8c4.png)


### 3、Service Mesh时代的选边与站队

2017年[KubeCon&CloudNativeCon Austin大会](https://kccncna17.sched.com/)上，作为代表下一代微服务解决方案设计理念的[Service Mesh](https://buoyant.io/2017/04/25/whats-a-service-mesh-and-why-do-i-need-one/)成为“热词”而被众人追捧。国内的ServiceMesh也是刚刚起步，方兴未艾。这篇“Service Mesh时代的选边与站队 ”就是发表在国内[ServiceMesh社区](http://www.servicemesh.cn/)上的一篇文章。文章脉络大致如下：

- Service Mesh的地位与生态格局
- 大公司间关于Service Mesh的布局与斗争策略
- istio尚未发布1.0时，最早提出Service Mesh概念的小公司
[buoyant](https://buoyant.io)的努力喘息 - Service Mesh的2018

![img{512x368}](../../assets/d58d6899cc954a59.png)


![img{512x368}](../../assets/adb9b087dac40293.png)


### 4、全文检索数据库Bleve简介

去年年末在做一个全文检索查询功能时曾用过陈辉的[wukong引擎](http://tonybai.com/2016/12/06/an-intro-to-wukong-fulltext-search-engine/)，不过wukong引擎由于作者的日理万机，无闲打理，已经不再维护。而在Go语言实现的全文检索工具领域，国外社区更流行的是[Bleve](https://github.com/blevesearch/bleve)。这篇文章介绍了作者所在公司为何用bleve替换solr，并对bleve中概念、使用方法进行了介绍，算是Bleve的入门文章。不过对于中文分词和全文检索的支持好坏，还需验证。

### 5、十年专业写博经验谈

Andrew Chen是硅谷的一位企业家，创业顾问，“[Growth Hacker is the new VP of Marketing](http://andrewchen.co/how-to-be-a-growth-hacker-an-airbnbcraigslist-case-study/)”一文作者，目前就职于uber。他还是一位拥有10年写博经验的博主。在“十年专业写博经验谈”一文中，他总结了10年来写博的经验教训，并逐条给出详细的亲历讲解。

### 6、Go数据科学Data Sheet

Go语言在数据科学领域算得上是一个年轻，但却极具潜力的选手。近一年来，Go语言在大数据领域已经有了[gonum](https://github.com/gonum/gonum)、[gorgonia](https://github.com/gorgonia/gorgonia)等用于数值计算和数据分析的library。gorgonia项目的作者Chewxy这篇”Data Science In Go: A Cheat Sheet”就是使用gonum和gorgonia进行数据科学计算和统计计算的速查手册。

原文链接：[“Data Science In Go: A Cheat Sheet”](https://www.cheatography.com/chewxy/cheat-sheets/data-science-in-go-a/)

![img{512x368}](../../assets/6af95ddba51f0f2b.jpg)


## 二、一周资料分享

[Go正式发布8年](https://blog.golang.org/8years)后，市面上关于Go语言入门的书籍和课程资料已经出现很多了，无论免费的还是收费。和其他语言的技术资料一样，很多资料质量良莠不齐。hackr.io针对Go语言的教程发起了社区投票，在这里我们可以看到社区对这些资料的质量甄别，同时这也是一份很好的Go书籍资料集合。这个投票是open的，你也可以提交list上尚没有的gobook，并根据你的阅读体验贡献你的vote。

## 三、一周工具推荐

### 1、135editor

之前将blog内容同步到微信公众号的时候，多为简单的复制粘贴，导致很多朋友抱怨公众号文章格式太粗糙，尤其是贴代码部分。自从有了做“TB一周萃选”这个weekly issue后，我就在市面上搜寻好用的微信公号文章编辑器。之前用的是微信编辑器(www.wxbj.cn)，简洁易用。但不知何故，该站点现在似乎变成了“易企秀”。于是我将编辑器换成了[135editor](http://www.135editor.com/)，这个似乎更加强大，就是左栏下方的广告推广多了一些。

**135editor**还支持在绑定公众号后的素材库同步，省了一步copy的动作。

## 四、一周书籍推荐

### 1、Kubernetes Handbook

[Kubernetes](http://tonybai.com/tag/kubernetes)赢得了与mesos、docker swarm的关于容器管理和服务编排引擎的“战争”，[成为这个领域当之无愧的领头羊](https://techcrunch.com/2017/12/18/as-kubernetes-surged-in-popularity-in-2017-it-created-a-vibrant-ecosystem/)。越来越多的公司开始试用Kubernetes，这里推荐一个有关于Kubernetes的开源书《Kubernetes Handbook》，是由talkingdata的jimmy song编写整理的。该书的最大特点就是全面，从K8s的基本概念、运维手段到k8s的领域应用，并且有详细的实践操作讲解。

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

Good one. Thanks for the article.