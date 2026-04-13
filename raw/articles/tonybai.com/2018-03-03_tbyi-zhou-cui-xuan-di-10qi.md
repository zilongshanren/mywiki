---
title: TB一周萃选[第10期]
url: https://tonybai.com/2018/03/03/10th-issue-of-the-tech-weekly-carefully-chosen-by-tonybai/
published: '2018-03-03'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# TB一周萃选[第10期]

本文是首发于[个人微信公众号](https://mp.weixin.qq.com/mp/qrcode?scene=10000005&size=102&__biz=MzIyNzM0MDk0Mg==&mid=2247483848&idx=1&sn=a3cd9182a2b2d3716623cc2c43d59f37&send_time=)的文章**“TB一周萃选[第10期]”**的归档。

![img{512x368}](../../assets/94536c8cba1bcbb9.jpg)


这个世界上最危险的毒药，就是成就感。而解药就是每晚都想一想，明天如何做得更好。 – 英格瓦坎普拉德，宜家创始人


2018年元宵节已过，这个传统意义上的年就算真的过完了，我们的那颗有些闲散、有些懈怠的心需要收一收，是时候为2018年的“事业”做些规划，从2018的起跑线上起跑出去了。就连现在的孩子，在开学第一课时都要对自己的寒假生活做生动的回顾并且对新学期给予展望了。

![img{512x368}](../../assets/72931f979041cd8b.jpg)


春节假期匆忙且短暂，不过在这段时间里还是有很多值得关注的文章、资料、书籍以及项目的。

## 一、一周文章精粹

### 1. Go官方提出新的包依赖管理工具：vgo

就在上周，Go社区里发生了一件“大事”：Go大神Russ Cox一周内连发了[七篇文章](https://research.swtch.com/vgo)，并宣布Go很可能在下一个版本：Go 1.11中加入可选的、“实验性”的新模型： vgo(versioned Go)，以试图解决长期以来Go被广泛诟病的包依赖管理问题。

Russ Cox在设计vgo时参考了当今比较流行的cargo、npm等工具，也从之前Go官方实验[dep](https://tonybai.com/tag/dep)中吸取了足够的实验结论，另辟蹊径，提出了很多很有创新的观点和方法，在社区里引起了广泛的关注和讨论。

vgo的一些主要设计考量如下：

- 接受语义版本(semver)规则
- 使用semantic import versioning规则替代原有的import rule
- 引入module概念（go.mod)
- 使用minimal version selection(最小版本选择)，而不是业界事实标准的maximal version selected（最新版本选择）的方案；
- 去除vendor机制
- 去除GOPATH

Russ Cox还提供了一个[vgo的初步实现](https://github.com/golang/vgo)，供广大Gopher体验。

vgo的公开意味着Go team已经将包依赖管理问题列为高优先级待解决的问题，vgo虽然只是原型，其设计思路也可能不会全部进入到最终的解决方法中，但这毕竟迈出了坚实的一步。

文章链接：[Go & Verisioning](https://research.swtch.com/vgo)

### 2. Go官方2017用户调查结果

本周Go官方在Blog上公布了2017用户调查结果，几个结论值得大家关注：

- 越来越多用户在工作中正式使用Go (67%)
- Web开发、系统编程、Devops、网络编程依旧是Go使用的主要领域，但在移动端、桌面端GUI编程的比例下滑明显
- 在API/RPC服务领域的使用占据榜首，CLI、WebService(返回html)排名2、3
- 包依赖管理以及缺少泛型依然是Gopher最希望Go team解决的两个问题
- Linux、MacOS依然是Gopher主力开发平台
[vscode](https://tonybai.com/tag/vscode)在Go编辑器市场份额升至No.1- 最喜欢的关键字：go、defer、func、select和interface排名top5

文章链接：[“Go 2017用户调查结果”](https://blog.golang.org/survey2017-results)

### 3. 容器术语介绍入门

著名开源公司Redhat近两年拥抱容器的态度十分坚决，近期来收购了coreos。近期Redhat在官博上发表了一篇文章，对容器领域的相关术语概念做了详尽的介绍，强烈推荐。

文章链接：[“容器术语介绍入门”](https://developers.redhat.com/blog/2018/02/22/container-terminology-practical-introduction/)

### 4. Go语言实现的微服务系列

Go语言已经被证明了是当前应用云化、面向微服务的服务端编程的头部语言之一。关于Go与Microservice的文章也有不少。Ewan Valentine的Go语言实现微服务系列（10篇）就是这类文章中难得的全面、细致讲述Go如何实现微服务应用的文章资料。在这一系列文章中，作者谈到的了mongodb, grpc, docker, Google Cloud, Kubernetes, NATS, CircleCI, Terraform、go-micro框架等诸多在编写、部署、运维微服务过程中所能用到的框架、协议、工具等。.

文章链接：[microservice in golang series](https://ewanvalentine.io/microservices-in-golang-part-1/)

### 5. Brian Ketelsen专访：Go取得快速增长的原因

[Brian Ketelsen](https://github.com/bketelsen)是知名Gopher，GopherCon大会、GopherAcademy的联合发起人、《Go in action》一书的联合作者。在Microsoft对其的一篇专访中，Brian Ketelsen谈了对Go语言这些年取得快速成长的看法。

文章链接：[Brian Ketelsen专访：Go取得快速增长的原因](https://open.microsoft.com/2018/02/21/go-lang-brian-ketelsen-explains-fast-growth/)

### 6. 在Linux上使用Go作为脚本语言

Cloudflare公司的很多产品采用的是Go技术栈，公司内部支撑系统亦是。Go的简单特质以及Go tools的使用模式让Go十分适合在Linux系统上被当做“脚本语言”使用（结合shebang行），它的强类型特性又是真正的脚本语言所不具备的。cloudflare的这篇文章讲解了该公司使用go作为脚本语言在Linux上的实践方法，值得借鉴。

文章链接：[《在Linux使用Go作为脚本语言》](https://blog.cloudflare.com/using-go-as-a-scripting-language-in-linux/)

## 二、一周资料分享

### 1. Google机器学习速成教程

![img{512x368}](../../assets/85255aa45e3ffb91.png)


Google公司本周正式推出面向普通开发者、机器学习爱好者的机器学习速成教程资料。粗略浏览了一遍，感觉该教程是目前传统程序员向机器学习、AI领域转型的最优秀资料之一。教程提供了教程中实验的全部资料和实验环境，并给出了前提条件中给出了预备知识的学习教程，包括数学知识、Python编程等。更为可贵的是该教程提供完整的中文版，国内程序员学习起来曲线也降低了不少。唯一不便的可能就是需要**科学上网**才能打开教程。

资料分享链接：[“Google机器学习速成教程”](https://developers.google.com/machine-learning/crash-course/)

## 三、一周项目推荐

### 1. vitess

![img{512x368}](../../assets/e1141c8be2563ac2.png)


之所以推荐vitess这个项目，是因为它在不久前成为了[CNCF基金会](https://www.cncf.io)的[第16个孵化级别项目](https://www.cncf.io/blog/2018/02/05/cncf-host-vitess/)，并且是cncf第二个存储项目。Vitess最初是作为YouTube的一个内部解决方案来处理大量存储的扩展，它是一个数据库编排系统，通过广义分片来对MySQL进行水平缩放。通过封装分片路由逻辑，Vitess允许应用程序代码和数据库查询对于将数据分布到多个分片上保持不变。借助Vitess，组织甚至可以根据需求的增长来分割和合并碎片，原子切割步骤只需要几秒钟。

同时该项目还是[Go语言](https://tonybai.com/tag/go)的早期“尝鲜者”：在2011年就开始使用Go语言开发了。随着vitess用户的增多（包括slack、flipkart等），vitess似乎又进入一个黄金开发的阶段，将较为成熟的、业界广为使用的数据库分片技术继续延续和优化下去，并且vitess与容器、[kubernetes的结合使用](https://vitess.io/getting-started/)也日益成熟，为云原生应用在k8s上提供一个可扩展的存储层。

项目链接：[“vitess”](https://vitess.io/)

## 四、一周图书推荐

### 1.《Master Ethereum》

![img{512x368}](../../assets/35152c340aa012d4.jpg)


随着2017年[比特币](https://www.bitcoin.com/)市场的异常繁荣，2018的[区块链技术](https://en.wikipedia.org/wiki/Blockchain)有迎来爆发的趋势。作为第二代区块链技术代表的[以太坊](https://en.wikipedia.org/wiki/Ethereum)(Ethereum)，它试图实现一个总体上完全无需信任基础的[智能合约](https://en.wikipedia.org/wiki/Smart_contract)平台和庞大的生态圈，受到了区块链业界最为广泛的关注，有关以太坊的技术书籍亦是如此。

《Master Ethereum》，中文名可译为“精通以太坊”，这是一本尚未完成的书，但在编写的过程中就受到了广泛的关注。除了是因为大家对以太坊技术关注之外，该书在github的开源也是其吸引眼球的重要原因。该书的两位作者是bitcoin专家，本书的目标是为开发者提供有关以太坊概念、使用、智能合约(smart contract)、经典以太坊网络、以太坊标准等全面的内容。

图书链接：[《Master Ethereum》](https://github.com/ethereumbook/ethereumbook)

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

## 评论