---
title: TB一周萃选[第1期]
url: https://tonybai.com/2017/12/17/1st-issue-of-the-tech-weekly-carefully-chosen-by-tonybai/
published: '2017-12-17'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# TB一周萃选[第1期]

本文是首发于[个人微信公众号](https://mp.weixin.qq.com/mp/qrcode?scene=10000005&size=102&__biz=MzIyNzM0MDk0Mg==&mid=2247483848&idx=1&sn=a3cd9182a2b2d3716623cc2c43d59f37&send_time=)的文章[TB一周萃选[第1期]](https://mp.weixin.qq.com/s?__biz=MzIyNzM0MDk0Mg==&mid=2247483848&idx=1&sn=a3cd9182a2b2d3716623cc2c43d59f37&chksm=e863e629df146f3f421f37672d25400bf6f7f52627bf72e99bf7fb7ff05857459110667600ce&scene=0&key=3c4368fbfacb90f62b01b31c9db501f48366f66e6f2fe6263466a4fde83102554335a4d7a4c039d31a1c0d9c5b6402b6354f47328ea5a8bdc44cb0efa3613732d6e03c5bdabd1f6a14ded92258a05636&ascene=0&uin=MTYwMzM0NjYyMQ%3D%3D&devicetype=iMac+MacBookAir6%2C2+OSX+OSX+10.9.2+build(13C64)&version=11020201&lang=zh_CN&pass_ticket=VzWYzr6BakKr1yXQQOGq0zbwSncZvZ1JO4UH32DDbnZWFakvoMefh9wcEIPjPeWM)的归档(归档版增加了很多资料的索引)。

如果有一天，你不再寻找爱情，只是去爱；你不再渴望成功，只是去做；你不再追逐成长，只是去修行；一切才真正开始。 ——纪伯伦


时间飞逝，转眼间已是年终岁尾。祖国北方大地到处银装素裹，一场场充满诗意的白雪下又无处不透露的新的春的生机。

这里也介绍这个个人公众号的一些小变化。从本周开始，我会在一周所读到的或自创的文章中萃选出3-7篇文章，整理编辑，以文章形式推送给大家，类似一个周刊的形式，定名为**“TB一周萃选”**。口号：**努力成为程序员周末生活中不可缺少的一部分**。

这些文章来自的领域包括：[Go](http://tonybai.com/tag/go)、[Docker](http://tonybai.com/tag/docker)、[Kubernetes](http://tonybai.com/tag/kubernetes)、区块链、智能硬件、无人驾驶、儿童编程、人工智能、开源活动等。这个“周刊”只是个人在工作之外时间的投入，没有团队，鉴于能力和精力有限，难免有错误，望谅解。

本期是第1期，万事开头难。

## 一、一周文章精粹

### 1. Go版密码学入门

[密码学](https://en.wikipedia.org/wiki/Cryptography)即便是在程序员中也属于小众领域。不过[Go语言](http://tonybai.com/tag/go)提供了丰富的有关密码的packages(在$GOROOT/src/crypto下面)。这篇文章是密码学入门基础，介绍了密码与密钥、哈希、数字签名、加密与解密等基础概念，并使用golang语言作为例子对这些概念的应用做了详尽的诠释。

### 2. 服务端I/O性能大比拼：Node vs. PHP vs. Java vs. Go

程序员这个行业属于“高危”行业，除了生理上收到“职业”特点的折磨外，还时不时会加入到一些[“编程语言”的战争](http://tonybai.com/2012/10/08/the-new-age-of-programming-language/)中。但这绝对不是这里我向大家推荐这篇文章的初衷，我崇尚：和平相处，不打嘴仗。编程语言领域几十年来都保持着相对活跃的态势，每隔几年甚至每年都会有新的编程语言进入大家视野。Go从诞生以来，受到了大家的极大关注，自然也就会成为被与其他语言比较的对象。这篇文章从I/O性能的角度横向对比了Go、Nodejs、Java和PHP等几门语言，所得到的数据建议大家做个参考而已。不代表原作者的思路就完全没有问题。

![img{512x368}](../../assets/ae203f9150af8a43.jpg)


### 3. 怼：“从PHP到Go，又回到PHP”

“又来了”！haha。这里不多说了，个人感觉这篇文章的正反观点都值得去仔细体会。PHP是世界最好的语言，Go是新生代的代表之一，求轻虐。

原文链接：[《RE: MOVING FROM PHP TO GO AND BACK AGAIN》](http://blog.breakthru.solutions/re-moving-from-php-to-go-and-back-again/)

### 4.超炫酷Slide的“机器学习入门”

机器学习对于传统程序员来说还是有较高的学习门槛的，学习各种概念也较为枯燥。不过Google Senior Creative工程师Jason Mayes的这门“机器学习的入门课”至少从Slide的表现来看却很炫酷。

![img{512x368}](../../assets/7c0b236915b8424b.png)


## 二、一周资料分享

### 1.KubeCon 2017& CloudNativeCon2017 Austin大会Slides

[KubeCon 2017&CloudNativeCon 2017大会](https://kccncna17.sched.com/)在Austin隆重举行。这次大会的受关注程度也是历史空前。关于K8s和[cncf基金会](https://www.cncf.io/)的最新进展都可以在这次大会上获得。其中不乏像[Service Mesh](https://buoyant.io/2017/04/25/whats-a-service-mesh-and-why-do-i-need-one/)这样的新技术热点。这里分享一下大会的Slides集合，欢迎自行下载阅读和理解。

下载链接：[百度盘](https://pan.baidu.com/s/1qXLJvnI)

## 三、一周工具推荐

### 1.Goland

Jetbrain公司的Go IDE工具[goland](https://www.jetbrains.com/go/)正式release了。Goland凝聚了JetBrain公司在IDE领域的丰富经验，它为Go开发者提供了智能的自动补全、即时检查和快速修复、导航和自动化重构等功能。 正如IntelliJ IDEA为Java开发者提供的体验一样，相信GoLand同样会为Go开发者提供更好的开发体验。

JetBrains员工Andrey Cheptsov 的这篇[《使用Goland进行Go开发》](https://medium.com/@andrey_cheptsov/golands-take-on-go-development-7d2611b14b99)可以带你走进goland的世界。

![img{512x368}](../../assets/02b0e0f0e4b315d3.jpg)


## 四、一周图书推荐

### 1.《Network Programming with Go》

Go语言十分擅长网络编程，但市面上关于Go网络编程的系统性资料非常少。在Go 1.0发布之后不久，一位位于澳大利亚的教师[Jan Newmarch](https://jan.newmarch.name/)就在网上发布了自己的“[Network programming with Go](https://jan.newmarch.name/go/)” 。若干年后，Jan Newmarch将自己的资料整理后，并结合最新的Go语言变化，出版了《Network Programming with Go》一书。纵观这本书，虽然质量谈不上很高，但内容相对系统全面，其有关Socket-level programming的章节内容很有参考价值。

免费版链接(内容可能不全)：http://tumregels.github.io/Network-Programming-with-Go/

图书出版社链接：https://www.apress.com/gp/book/9781484226919

![img{512x368}](../../assets/ca14f72e429d045b.png)


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