---
title: 官宣：Go专栏“改善Go语言编程质量的50个有效实践”上线了
url: https://tonybai.com/2020/09/08/imooc-go-column-is-available/
published: '2020-09-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 官宣：Go专栏“改善Go语言编程质量的50个有效实践”上线了

断断续续写了一年多的[Go专栏：《改善Go语言编程质量的50个有效实践》](https://www.imooc.com/read/87)今天终于正式上线了！- https://www.imooc.com/read/87

![img{512x368}](../../assets/018ff45f7e150fca.png)



[Go语言](https://tonybai.com/tag/go)是Google大牛团队(Robert Griesemer、Rob Pike以及Ken Thompson)设计的一种静态类型、编译型编程语言，支持垃圾回收和轻量级并发，它于2009年11月诞生，一面世就以语法简单、原生支持并发、标准库强大、工具链丰富等优点吸引了大量开发者。经过[10余年演化和发展](https://tonybai.com/2019/11/09/go-opensource-10-years/)，Go如今已成为[云基础架构的标准编程语言](https://tonybai.com/2020/05/01/rob-pike-interview-go-become-the-language-of-cloud-infrastructure/)，很多云原生时代的杀手级平台、中间件、协议和应用都是采用Go语言开发的，比如：[Docker](https://tonybai.com/tag/docker)、[Kubernetes](https://coding.imooc.com/class/chapter/284.html)、[以太坊](http://ethereum.org/)、[Hyperledger Fabric超级账本](https://github.com/hyperledger/fabric)、新一代互联网基础设施协议[ipfs](https://github.com/ipfs/ipfs)等。

Go是一门**特别容易入门**的编程语言，无论是刚出校门的新手还是从其他编程语言转过来的成手，都可以在短时间内快速掌握Go语法并投入到Go代码的编写中。但笔者在日常收到很多Go初学者的疑问：**Go入门容易，但进阶难，怎么才能像Go团队那样写出符合Go思维和语言惯例(idiomatic)的高质量代码呢？**

这个问题也引发了我的思考。在[2017年GopherChina大会](https://tonybai.com/2017/04/06/an-interview-with-me-as-a-lecturer-of-gopherchina-2017)上笔者以[演讲的形式初次尝试回答这个问题](https://tonybai.com/2017/04/20/go-coding-in-go-way)，但鉴于演讲的时长有限，很多内容难于展开，效果不甚理想。而这个慕课网专栏则是我对解答这个问题作出的第二次尝试。

这次解答的思路有两个：

- 思维层面：写出高质量Go代码的前提是思维方式的进阶，即
**使用Go语言的思维去写Go代码**； - 实践技巧层面：Go标准库、优秀Go开源库是一个挖倔高质量、符合Go惯用法的Go代码的宝库，对其进行阅读、挖掘和整理归纳，我们
**可以得到一些帮助我们快速进阶的有效实践**。

**本专栏正是基于上面思路为想实现Go进阶但又不知从何入手的你而设的**。

首届图灵奖得主、著名计算机科学家艾伦·佩利(Alan J. Perlis)曾经说过：**“不能影响到你的编程思维方式的编程语言不值得去学习和使用”**，足见编程思维对编程语言学习和应用的重要性。只有真正领悟了一门编程语言的设计哲学和编程思维，并将其应用到日常编程当中去，你才算是真正地实现了在这门编程语言上的进阶。

因此，本专栏首先将带领大家回顾Go语言的演化历史，一起了解并深刻体会Go大牛们在设计Go语言时的所思所想，与大牛们实现思维上的共鸣，理清那些看似随意的，实则经过深思熟虑的设计的背后的付出。

接下来，本专栏将基于笔者对Go核心团队、Go社区高质量代码的分析归纳，从代码风格、基础语法、函数/方法、接口、并发、错误处理、测试调试、标准库、工程实践等多个方面给出改善Go代码质量，写出符合Go思维和惯例的代码的有效实践。

**学习了本专栏的这50条有效实践，你将拥有和Go大牛们一样Go编程思维，写出符合Go惯例风格的高质量Go代码，从众多Go入门选手中脱颖而出，快速实现从Go编程新手到专家的转变！**

本专栏共分10个模块(篇)，50个小节。

- 模块1：设计哲学篇

本专栏的开篇和总起。和读者一起穿越时空，回顾历史，详细了解Go语言的诞生、演化以及今天的发展。归纳总结Go语言的设计哲学和原生编程思维，让读者可以站在语言设计者的高度理解Go语言与众不同的设计，在更高层次，形成共鸣，产生认同。只有强烈认同，才能更上一层楼。

- 模块2：代码风格篇

每种编程语言都有自己惯用的代码风格，而遵循语言惯用风格是高质量Go代码的必要条件。本篇详细介绍了得到公认且广泛使用的Go工程的结构布局、代码风格标准、标识符命名惯例以及变量声明形式等。

- 模块3：基础语法篇

本模块详述在基础语法层面高质量Go代码的惯用法和有效实践，涵盖无类型常量的作用、定义Go的“枚举常量”、“零值可用”类型的意义、切片原理以及其高效的原因、Go包导入路径的真正含义等。

- 模块4：函数与方法篇

函数和方法是Go程序的基本组成单元。本模块聚焦于函数与方法的设计与实现，涵盖init函数的使用、跻身“一等公民”行列的函数有何不同、Go方法的本质等帮助读者深入理解它们的内容。

- 模块5：接口篇

接口是Go语言中的“魔法师”。本模块将聚焦接口，涵盖接口的设计惯例、使用接口类型的注意事项以及接口类型对代码可测试性的影响等。

- 模块6：并发编程篇

Go以其轻量级的并发模型而闻名。本模块将详细介绍Go基本执行单元 – goroutine的调度原理、Go并发模型以及常见并发模式、Go支持并发的原生类型-channel的惯用使用模式等内容。

- 模块7：错误处理篇

Go语言十分重视错误处理，它有着相对保守的设计和显式处理错误的惯例。本模块将涵盖Go错误处理的哲学以及在这套哲学下一些常见错误处理问题的优秀实践方案。

- 模块8：测试与调试篇

Go自带强大且为人所称道的工具链，本模块将详细介绍Go在单元测试、性能测试以及代码调试方面的最佳实践方案。

- 模块9：标准库篇

Go拥有功能强大且质量上乘的标准库，多数情况我们仅使用标准库所提供的功能而不借助第三方库就可实现应用的大部分功能，这大幅降低学习成本以及代码依赖的管理成本。本模块将详细说明高频使用的标准库包，如net/http、strings、bytes、time等的正确使用方式，以及reflect包、cgo在使用时的注意事项。

- 模块10：工程实践篇

本模块将涵盖我们使用Go语言做软件项目过程中很大可能会遇到的一些工程问题的解决方法，包括：使用module进行Go包依赖管理、Go应用容器镜像、Go相关工具使用以及Go语言的避“坑”指南。

从上述专栏结构，我们也能看出本专栏并不是Go入门的最佳选择。如果非要给本专栏划定一个目标人群，或者说哪些读者阅读本专栏后会更多受益，**我觉得是那些已经迈入Go语言世界、但迫切希望进一步提升层次、写出高质量Go代码的Go开发者。**

很多朋友可能会问？你这个专栏有何与众不同之处？在专栏上线前编辑老师也让我编写课程亮点，我觉得下面这几句话可以概括专栏的特点：

- 进阶必备 – 50个有效实践助你掌握高效Go程序设计之道；
- 高屋建瓴 – Go设计哲学与编程思想先行；
- 深入浅出 – 原理深入，例子简明，讲解透彻；
- 图文并茂 – 大量图表辅助学习，重点难点轻松掌控；
- 覆盖全面 – 覆盖高级面试知识点，求职更自信。

本专栏第一次落笔大约在[Go 1.12](https://tonybai.com/2019/03/02/some-changes-in-go-1-12)发布后，大约将在今年10月份，即在[Go 1.15](https://tip.golang.org/doc/go1.15)发布后的第二个月完成。这中间有一定的跨度，因此专栏内的有些内容在各个Go版本间可能会有差异。笔者在内容中已经尽量做了版本适用标识，但难免有疏漏。各位读者在遇到问题时，可以及时反馈给我。

此外，Go语言还在飞速发展，一些当前的惯用表达方式或有效实践可能在日后因语言引入新的特性(比如：[Go泛型](https://tonybai.com/2020/06/18/the-go-generics-is-coming-and-supported-in-go-1-17-at-the-earliest/))而**“过时”**。我会在我的博客上持续关注Go语言的演化，并将最新的Go高效编程实践分享给大家。

最后再来一次自我介绍：**Tony Bai**，Go语言技术专家和鼓吹者，GopherChina大会讲师，Go语言技术博客[tonybai.com](https://tonybai.com)的作者，[GopherDaily(Go日报)项目](https://github.com/bigwhite/gopherdaily)(github.com/bigwhite/gopherdaily)维护者，OSCHINA[源创会技术讲师](https://tonybai.com/2017/10/24/go-evolution-for-ten-years-an-interview-by-osc)，[《七周七语言》](https://book.douban.com/subject/10555435/)译者之一，慕课网[《Kubernetes实战：高可用集群搭建、配置、运维与应用》](https://coding.imooc.com/class/284.html)作者，[开源拥趸](https://github.com/bigwhite)。

作为一名在国内接触Go语言较早(2012年)的Gopher和Go布道师，Tony Bai拥有丰富的Go开发知识和经验。他在个人博客上撰写了大量关于Go语言的文章，并深受Go社区欢迎。目前他正在国内一大型软件公司带领团队使用Go语言构建移动运营商的5G消息平台，这个平台将处理来自全国各地几十万个5G chatbot程序每天发送的几十亿条5G消息请求。

欢迎大家订阅我的专栏! 如有意见和建议，可在我本博文后面的评论中反馈。感谢大家支持。

**专栏涉及的 源码仓库地址**：https://github.com/bigwhite/publication/tree/master/column/imooc/go-50tips/sources

我的Go技术专栏：“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”上线了，欢迎大家订阅学习！

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

© 2020 – 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

请问是否有出版的计划，喜欢纸质书的感觉^_^

有。估计今年底前差不多。纸版内容更为丰富。

一年之后回头来问，大佬你的书出版了吗？

稿已经提交，目前出版社编辑中。

纸版比专栏多了哪些内容啊？

可以说章节编排更系统，每条实践的讲解更全面，实践的个数更多吧。

纸质版书籍还需要多少上市呀？

已经开始印刷了。出版社说2022.1出版。

已上市。两册：https://book.douban.com/subject/35720728/ 和 https://book.douban.com/subject/35720729/