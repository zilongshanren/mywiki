---
title: TB一周萃选[第5期]
url: https://tonybai.com/2018/01/14/5th-issue-of-the-tech-weekly-carefully-chosen-by-tonybai/
published: '2018-01-14'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# TB一周萃选[第5期]

本文是首发于[个人微信公众号](https://mp.weixin.qq.com/mp/qrcode?scene=10000005&size=102&__biz=MzIyNzM0MDk0Mg==&mid=2247483848&idx=1&sn=a3cd9182a2b2d3716623cc2c43d59f37&send_time=)的文章**“TB一周萃选[第5期]”**的归档。

![img{512x368}](../../assets/64f4670a49e026c0.jpg)


人生十鉴

大喜易失言


大怒易失礼

大惊易失态

大哀易失颜

大乐易失察

大惧易失节

大思易失爱

大醉易失德

大话易失信

大欲易失命

下雪，是北方城市冬天的“常规操作”，是最不需要被单独关注的的事情。但今年冬天的“雪”却成为了这边的热门话题，原因：**自从入冬以来一直就没下一场像样儿的雪！**

雪的姗姗来迟让病毒细菌异常活跃，医院发热门诊尤其是儿科人满为患，笔者入冬后也是连续感冒了两次。好在2018年元旦后没几天，在三九天到来之前，大家期盼已久的“像样儿的雪”终于落了下来。

![img{512x368}](../../assets/0162a2ee71b0379d.jpg)


图：小区里的初雪

2018年的这第一场雪注定是一场“瑞雪”，它不仅降低了空气的病毒浓度，提升了空气湿度，帮助人们有效抵御病毒入侵人体，而且让缺雪的北方城市瞬间焕发出那冬天独有的“魅力”。

很多事情看起来很难，但一旦捅破了那层窗户纸之后，也就感觉没那么难了。下雪这事儿似乎也是如此，在被第一场雪打了个“样儿”之后，一场场雪便接踵而至了。在笔者撰写本文的时候，窗外还飞舞着洁白的雪花。

## 一、一周文章精粹

### 1. Go“不足够好”文章大集合

就像世界上其他事物一样，编程语言也没有完美的，每一门编程语言都有优点，也有“不够好”的地方。[Go](http://tonybai.com/tag/go)诞生以来，虽然赞美之声此起彼伏，但对Go的“批评”之声也从未中断过。因此有人就整理了Go“不足够好”文章大集合，供Go设计者反思，供Gopher学习，以更好地、更深刻地理解Go这门语言。

### 2. 好的Go代码库应该具备的“特征”

Go是一门[简洁的编程语言](http://tonybai.com/2017/04/20/go-coding-in-go-way/)，入门容易，上手快。但写出好的Go代码还是需要一番功夫的。国外的一名gopher总结了“一个好的Go代码库应该具备的特征”，文章中按照依赖、API、错误处理、并发、调试等几个方面列举了诸如：给库打语义版本标签(semantic versioning tag)、除了标准库之外没有第三方依赖、一旦有非标准库的第三方依赖如何应对、不用使用vendor、使用包依赖管理工具、最小化public functions、接收iterface返回struct、避免创建goroutine、避免在公共API中使用channel等特征，强烈推荐每一个gopher阅读学习。

文章链接：[好的Go代码库应该具备的“特征”](https://medium.com/@cep21/aspects-of-a-good-go-library-7082beabb403)

### 3. Apollo 2.0发布

在2018 [美国消费电子展CES](https://www.ces.tech/)上，百度发布了其无人车平台Apollo的2.0版本，该版本将平台之前宣布的四大模块全部开放，并支持了简单城市道路的自动驾驶。

文章链接：[Apollo 2.0](https://github.com/ApolloAuto/apollo/releases/tag/v2.0.0)

这是我之前写过的一篇文章[Apollo 1.0的入门](http://tonybai.com/2017/08/15/hello-apollo/)，可以帮助你了解Apollo。

![img{512x368}](../../assets/54471157ab77e7fb.png)


### 4. 2018，微服务将结束疯狂

**微服务**近两年在容器和[k8s](http://tonybai.com/tag/kubernetes)的赋能下迅速发展，成为架构师口中的“时尚词汇”，每每涉及系统设计，就会首先问是否要做成微服务。一个新事物的出现和发展，有人唱好，自然就会有人看衰。这不，“2018，微服务将结束疯狂”这篇文章就是给“微服务”泼冷水降温的！文章从微服务架构对开发者、运维人员、devops的影响、需要专家级技能、真实世界系统边界模糊、状态复杂性、通信复杂性、版本管理、分布式事务等方面探讨了微服务的劣势，并给出了一个问题列表，建议大家在决定采用微服务之前，用这些问题问问自己，以避免陷入“微服务”泥潭中去。

文章链接：[《The Death of microservice madness in 2018》](http://www.dwmkerr.com/the-death-of-microservice-madness-in-2018/)

### 5. 2017 Google Brain Team的总结 by Jeff Dean

在人工智能的工程领域，Google大神Jeff Dean领导的Brain Team具有举足轻重的地位，也可以说是世界上最好的人工智能实践和研究团队之一了。在2018年伊始，Jeff Dean代表Google Brain Team撰文对团队在2017年的工作及成果进行了总结：包括AutoML、语言理解、机器学习算法、机器学习系统等核心研究工作，以及开源软件[Tensorflow](http://tonybai.com/2017/02/06/build-your-first-neural-network-with-tensorflow/)、数据集和新的机器学习硬件TPU等方面的最新进展。 对非人工智能领域而言，文章中满满的都是“黑科技”啊，能真正看懂文章中这些内容的朋友你一定也是人工智能领域的大牛了。

![img{512x368}](../../assets/da07618c3de63f62.png)


图：Tensorflow用户分布

文章链接：

[“2017 Google Brain Team的总结- part1″](https://research.googleblog.com/2018/01/the-google-brain-team-looking-back-on.html)

[“2017 Google Brain Team的总结- part2″](https://research.googleblog.com/2018/01/the-google-brain-team-looking-back-on_12.html)

[Part1 中文版](http://t.cn/RQy1RwO)

### 6. Javascript工作原理

[Javascript](https://en.wikipedia.org/wiki/JavaScript)诞生之后，估计没人想到过js能像今天这么流行：统治了前端，渗透到了后端，并成为后端服务开发的重要技术栈之一。Js语言也十分简单，但外延也很大，你要至少要深入理解浏览器原理才能更好地发挥JS的威力。sessionstack公司官方blog曾发表了几篇有关Javascript工作原理的文章，可以系统地帮助Javascript了解Js的运行机制。

![img{512x368}](../../assets/017a09f34ca3efda.png)


文章链接：

[Javascript工作原理: 引擎、运行时与调用栈](https://blog.sessionstack.com/how-does-javascript-actually-work-part-1-b0bacc073cf)

[Javascript工作原理: V8引擎和优化技巧](https://blog.sessionstack.com/how-javascript-works-inside-the-v8-engine-5-tips-on-how-to-write-optimized-code-ac089e62b12e)

[Javascript工作原理: 内存管理与避免内存泄露的技巧](https://blog.sessionstack.com/how-javascript-works-memory-management-how-to-handle-4-common-memory-leaks-3f28b94cfbec)

[Javascript工作原理: event loop与async编程](https://blog.sessionstack.com/how-javascript-works-event-loop-and-the-rise-of-async-programming-5-ways-to-better-coding-with-2f077c4438b5)

## 二、一周资料分享

### 1. 斯坦福大学面向Tensorflow深度学习研究课程

欧美一流大学在计算机技术方面的“与时俱进”的能力与速度真的是十分值得我们学习和借鉴的，尤其是斯坦福这样靠近硅谷的大学，其技术课程更新的速度非常快。[Tensorflow](https://github.com/tensorflow/tensorflow)于2015年末开源，2017年2月正式发布1.0版本。斯坦福大学在2017年就开了一门新课：[“CS 20SI: Tensorflow for Deep Learning Research”](https://web.stanford.edu/class/cs20si/2017/)，教授学生如何使用Tensorflow进行深度学习研究。

这门课程涵盖了用于深入学习研究的Tensorflow基本原理和使用用法。 目标是帮助学生们理解TensorFlow的graphical computational model，探索它提供的各种功能，并学习如何构建最适合深度学习项目的模型。 课程中学生将使用TensorFlow建立不同复杂度的模型，从简单的线性/逻辑回归到卷积神经网络和递归神经网络，解决词嵌入，单词翻译，光学字符识别，强化学习等任务。 学生还将学习到构建模型和研究实验管理的最佳实践。

资料链接：

[CS 20SI: Tensorflow for Deep Learning Research 课程主页](https://web.stanford.edu/class/cs20si/)

[CS 20SI: Tensorflow for Deep Learning Research 2017课程归档](https://web.stanford.edu/class/cs20si/2017/)

## 三、一周工具推荐

### 1. stackedit

自从我的[博客转到使用Markdown格式](http://tonybai.com/2015/09/19/write-blog-in-markdown/)进行编辑后，我就一直使用[stackedit](https://stackedit.io/)提供的在线所见即所得的Markdown编辑器进行内容的编辑。最初的[stackedit v4](https://stackedit.io/editor)表现的还不强大，随着[stackedit v5在线版本](https://stackedit.io/app)的推出，stackedit已经可以满足绝大多数Markdown编辑的功能需求了。

![img{512x368}](../../assets/7722190376640c3d.png)


- 支持在线/离线管理多个markdown文件
- 支持多种文件格式导出，包括HTML、PDF、WORD、EPUB
- 支持文件的云同步，支持Google Drive, Dropbox等主流云存储系统
- 支持将Markdown直接上传到Blogger/Blogspot, WordPress, Zendesk
- 支持将Markdown直接发布到GitHub, Gist, Google Drive, Dropbox

… …

更难得的是stackedit还是一个受关注度极高的开源项目(stars over 1w)，你可以自己本地部署一个专用的stackedit。

工具链接：[stackedit.io](https://stackedit.io)

工具开源项目链接：[stackedit](https://github.com/benweet/stackedit)

## 四、一周图书推荐

### 1.《演讲模式：演讲的技巧与禁忌》

![img{512x368}](../../assets/029e783c7fef8893.jpeg)


技术人升级到一定level后，可能少不了要做些演讲、做些培训之类的活动。但对多数技术人而言，演讲这事并不是“舒适区”范围内。市面上有关介绍演讲技巧方面的书可谓是“汗牛充栋”，但这Neal Ford领衔编写的这本书《演讲模式》却独具特色。Neal Ford是Thoughtworks的大神，其他两位作者也是IT圈中的牛人。与其他作者相比，他们更熟悉IT技术人的思维方式，他们也以IT人独特的思维方式，创造性地将建筑和软件开发领域“模式”的概念引入演讲领域，围绕演讲的全过程总结了能迅速有效提升演讲技能的88个模式（应该掌握的技巧）和反模式（应该避免的不好的做法）。对于IT人而言，“模式”这词再熟悉不过了，因此这本书更像是IT技术人员间地手把手地传道解惑。

图书链接：

中文版：[《演讲模式：演讲的技巧与禁忌》](https://book.douban.com/subject/25873582/)

英文版：[《Presentation Patterns: Techniques for Crafting Better Presentations》](http://presentationpatterns.com)

我的联系方式：

微博：http://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/71dbd0d64d261ba9.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2018, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论