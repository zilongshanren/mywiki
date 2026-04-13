---
title: 系统学习Go语言，有这几本书就够了！
url: https://tonybai.com/2020/11/04/the-recommend-books-list-for-learning-go/
published: '2020-11-04'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 系统学习Go语言，有这几本书就够了！

![img{512x368}](../../assets/4ace60a9e366d9f8.png)


### 1. Go语言的发展现状

如果从2007年9月20日那个下午三个“程序员大佬”在[谷歌总部](https://tonybai.com/2020/08/30/new-case-studies-about-googles-use-of-go/)的一间办公室里进行的一次有关设计一门新编程语言的讨论算起，那么Go语言已经度过了自己的[13个年头](https://tonybai.com/2020/05/01/rob-pike-interview-go-become-the-language-of-cloud-infrastructure/)了。

![img{512x368}](../../assets/a1be967144bffe0e.png)


如果从2009年11月10日Go语言[正式开源发布](https://opensource.googleblog.com/2009/11/hey-ho-lets-go.html)算起，Go语言也即将迎来自己的[第11个生日](https://tonybai.com/2019/11/09/go-opensource-10-years/)。

![img{512x368}](../../assets/54785c65bb3ff65d.png)


2020年，Go联合创始人Rob Pike在专访中也认可了[Go确实已成为云基础架构的语言](https://tonybai.com/2020/05/01/rob-pike-interview-go-become-the-language-of-cloud-infrastructure/)。在Go即将迎来自己的11个生日的时候，Hacker News有人发起了[“Go已超过10岁了，你觉得这门语言如何？”](https://news.ycombinator.com/item?id=24887521)的提问，收到了广泛的关注和回答。国内媒体将这些问答整理后得到的结论是：[“人生苦短，我要换Go”](https://mp.weixin.qq.com/s/7rn2eVhPxEKg1rGKPpANyQ)。

Stackoverflow官博11月2日发表的[《Go语言有哪些优点？探讨导致Go语言日益流行的特征 》](https://stackoverflow.blog/2020/11/02/go-golang-learn-fast-programming-languages/)一文对Go语言的发展趋势描述的贴切：**Go语言就像爬行的藤蔓，虽缓慢，但却逐渐占据了开发世界。它正以一种郁郁葱葱的并且在许多方面都很优越的编程能力覆盖着在它之前出现的所有事物**。

![img{512x368}](../../assets/0539f54fb7dc886d.png)


不管你是否承认，Go在IT就业市场已经成为事实上的“香饽饽”之一，就像一贯不激进的慕课网也在今年双11打出了下面的专题：

![img{512x368}](../../assets/14044dfbba282c31.png)


**上车，任何时间都不晚！** 那么怎么才能踏上Go这一强大且稳健前行的车呢？和其他主流编程语言一样，上车的必经之路：**看书**！

### 2. 市面上的Go书籍为何这么少

和C、C++、Java、Python等编程语言在市面上的书籍数量相比，Go流行于市面（大陆）上的图书似乎少了很多。其原因笔者觉得有如下几点：

#### 1) 年轻

我们来看看上述几门主流编程语言的诞生时间：

-
java 1995

-
c 1972

-
c++ 1983

-
python 1991


对于很多IT从业者来说，这些语言诞生的时候他们还没出生呢。而2009年末才正式发布的Go和“最年轻”的java之间还有14年的“年龄差”。

Go在国内真正开始快速流行起来大致在2015年第一届GopherChina大会(2015.4月)之后，当时的[Go是1.4版本](https://tonybai.com/2014/11/04/some-changes-in-go-1-4/))。同一年下半年发布的[Go 1.5](https://tonybai.com/2015/07/10/some-changes-in-go-1-5/)实现自举并让GC延迟大幅下降，这引爆了Go在国内的流行。一批又一批程序员成为Gopher，在大厂、初创实践着Go语言。但知识和技能的沉淀和总结需要时间，相信再有5年，国内作者出版的Go语言相关书籍会像雨后春笋版出现在大家的书架上。

#### 2）以品类代名词的身份占据的“领域”还少

提到Web，人们想到的是Java spring；提到深度学习、机器学习、人工智能，人们想到的是python和tensorflow；提到比特币，嵌入式，人们想到的是C；提到游戏，人们想到的是C++；提到前端，人们想到的是Javascript。这些语言在这些垂直领域早早以杀手级框架入场，使得它们成为了这一领域的“品类代名词”，因此与该垂直领域相关的技术书籍都会采用作为该领域“品类代名词”的编程语言编写书中示例等，这样的书也就会被归类为这类语言方面的书籍。

Go语言诞生晚，入场也较晚。Go虽然通过缓慢的“爬行”，覆盖了一些领域并占据优势地位，但还不能说已经成为了该领域的“品类代名词”，比如：云原生、API、微服务、区块链等，因此被垂直领域书籍关联的机会也不像上面那几门语言多。

同时，由于Go“自带电池”，基于Go标准库我们可以实现大部分功能特性，无需依赖过多框架。即便依赖框架，框架本身也不复杂，很少以“某某框架”为主题编写一本技术书籍，这方面远远无法媲美Java和Spring这对“黄金组合”。

#### 3) 引进国外优秀作品需要时间

相对于国内，国外关于Go语言的作品要多不少，但引进国外图书资料需要时机以及时间(找译者翻译)。

### 3. 系统学习Go语言的书籍列表TOP 5

[笔者接触Go语言较早](https://tonybai.com/2012/08/14/getting-going-with-go/)，Go语言相关的中外文书籍几乎都通读过一遍（经典好书读过可不止一遍哦）。Go语言比较简单，如果单单从系统掌握这门语言的角度来看，阅读下面基本书籍就足够了。如果你要学习某些垂直领域的Go应用和技巧，那么期待我后续对垂直领域Go书籍/资料的推荐吧^_^。

这里参考“天下足球”TOP10栏目的方式推荐我心目中掌握Go语言必读的五大好书（每项满分为5分）！

#### 第五名：[《The Way To Go》](https://book.douban.com/subject/10558892/) – Go语言百科全书

![img{512x368}](../../assets/0258e790b9088e6e.jpg)


《The Way To Go》是我**早期学习Go语言时最喜欢翻看的一本书**。该书成书于2012年3月，恰逢Go 1.0版本刚刚发布，作者承诺书中代码均可在Go 1.0版本上编译通过并运行。该书分为4个部分：

-
为什么学习Go以及Go环境安装入门

-
Go语言核心语法

-
Go高级用法（读写、错误处理、单元测试、并发编程、socket与web编程等)

-
Go应用(常见陷阱、语言应用模式、从性能考量的代码编写建议、现实中的Go应用等)


每部分的每个章节都很精彩，这本书也是目前见到的最全面详实的讲解Go语言的书籍了，我称之为Gopher们的第一本**“Go百科全书”**。

该书作者Ivo Balbaert想必大多数人都不曾耳闻。为了写本文，我特地研究了一下他的作品以及出版时间，发现这个技术作者是很会“抢先机”并且眼光独到。他总是能发现市面刚出现不久但却很有潜力的编程语言并在其他人了解该门语言之前，就编写出类似“The way to Go”这样的为早期语言接纳者提供的详实资料，包括[Julia](https://book.douban.com/subject/26337395/)，[Rust](https://book.douban.com/subject/26426817/)等。在很多人还不知道这些语言名字的时候，他就已经开始学习这些语言，并为这些语言编写出质量很高的“百科全书”式的书籍。

很遗憾，这本书没有中文版。这可能是由于本书出版太早，等国内出版社意识到要引进Go语言方面的书籍时，这本书使用的Go版本又太老了，虽然本书中绝大部分例子依然可以在今天最新的Go编译器下通过编译并运行起来。不过[无闻](https://github.com/Unknwon/the-way-to-go_ZH_CN)在github上发起了这本书的[中译版项目](https://github.com/Unknwon/the-way-to-go_ZH_CN)：https://github.com/Unknwon/the-way-to-go_ZH_CN，感兴趣的gopher可以去在线或下载阅读。

此书虽棒，但毕竟年头“久远”，我只能委屈它一下了，将它列在第五位，下面是其各个指数的评分：

-
作者名气指数：3

-
关注度指数：3

-
内容实用指数：4

-
经典指数：4


**总分：14**

#### 第四名：[《Go 101》](https://go101.org/article/101.html) – Go语言规范全方位解读

![img{512x368}](../../assets/5a11284d7f45b2e2.jpg)


**这是一本在国外人气和关注度比在国内高的中国人编写的英文书**，当然也是有中文版的。

如果仅从书名中的**101**去判断，你很大可能会认为这仅仅是一本讲解Go入门基础的书，但这本书的内容可远远不止入门这么简单。这本书可大致分为三个部分：

-
Go语法基础

-
Go类型系统与运行时实现

-
以专题(topic)形式阐述的Go特性、技巧与实践模式


除了第一部分算是101范畴，其余两个部分都是Go语言的高级话题，也是要精通Go必须要掌握的“知识点”。并且，结合Go语言规范，作者对每个知识点的阐述都细致入微并结合大量示例辅助说明。我们知道有关C和C++语言，市面上有一些由语言作者或标准规范委员会成员编写的annotated或rationale书籍（语言参考手册或标准解读），Go 101这本书也可以理解为**Go语言的标准解读或参考手册**。

Go 101这本书是[开源电子书](https://github.com/go101/go101)，其作者也在国外一些支持自出版的服务商那里做了付费数字出版。这使得这本书相对于其他纸板书有着另外一个优势：**与时俱进**。在作者的不断努力下，该书的知识点更新基本保持与Go的演化同步，目前其内容已经覆盖了最新的[Go 1.15版本](https://tonybai.com/2020/10/11/some-changes-in-go-1-15/)。

该书作者为国内资深工程师[老貘](https://gfw.tapirgames.com/)，他花费三年时间“呕心沥血”完成此书并免费奉献给Go社区，值得大家为其大大的点赞！

下面是本书推荐指数的评分：

-
作者名气指数：3

-
关注度指数：4

-
内容实用指数：4

-
经典指数：4


**总分：15**

#### 第三名：[《Go语言学习笔记》](https://book.douban.com/subject/26832468/) – Go源码剖析与实现原理探索

![img{512x368}](../../assets/16515c4e736003db.jpeg)


这是一本在国内影响力很大和关注度较高的作品。一来其作者[雨痕老师](https://github.com/qyuhen/)是国内资深工程师，也是2015年第一届GopherChina大会讲师；二来，该作品的前期版本是以开源电子书的形式风险给国内Go社区的；三来，作者在Go源码剖析方便可谓之条理清晰，细致入微。

2016年《Go语言学习笔记》纸版书出版，该书覆盖了当时最新的Go 1.5版本，Go 1.5版本在Go语言演化历史中的分量极高，它不仅实现了Go自举，还让Go GC的延迟下降到绝大多数应用可以将其应用到生产的程度。本书整体上分为两大部分：

-
Go语言详解：以短平快、捞干的来的风格对Go语言语法做了说明，能用示例说明的，绝不用文字做过多修饰。

-
Go源码剖析：这是本书精华，也是最受Gopher关注的部分。这部分对Go运行时神秘的内存分配、垃圾回收、并发调度、channel和defer的实现原理、syn.Pool的实现原理做了细致的源码剖析与原理总结。


随着Go语言演化，其语言和运行时实现一直在变化，但Go 1.5版本的实现是后续版本的基础，因此这本书的剖析非常值得每位Gopher阅读。从雨痕老师的[github](https://github.com/qyuhen/book)上最新消息来看，他似乎在编写新版Go语言学习笔记，[基于Go 1.12版本](https://tonybai.com/2019/03/02/some-changes-in-go-1-12/)，剖析源码是枯燥繁琐的，期待新版Go学习笔记早日与Gopher们见面。

下面是本书各个指数的评分：

-
作者名气指数：4

-
关注度指数：4

-
内容实用指数：4

-
经典指数：4


**总分：16**

#### 第二名：[《Go语言实战》](https://book.douban.com/subject/27015617/) – 实战系列(in action)经典之作，紧扣Go语言的精华

![img{512x368}](../../assets/b4aa76510bb02e8e.jpg)


Manning出版社出版的“实战系列(xx in action)”一直是程序员心中高质量和经典的代名词。在出版Go语言实战方面，该出版社也是丝毫不敢怠慢，邀请了Go社区知名的三名明星级作者联合撰写了该书的内容。这三位作者分别是：

-
威廉·肯尼迪 (William Kennedy) – 知名Go培训师，培训机构Ardan Labs的联合创始人，”Ultimate Go”培训的策划实施者。

-
布赖恩·克特森 (Brian Ketelsen) – 世界上最知名的Go技术大会 – GopherCon大会的联合发起人和组织者，

[GopherAcademy](https://gopheracademy.com/)创立者，现微软Azure工程师 -
埃里克·圣马丁 (Erik St.Martin) – 世界上最知名的Go技术大会 – GopherCon大会的联合发起人和组织者


本书并不是大部头，而是薄薄的一本（中文版才200多页），因此你不要期望从本书得到百科全书一样的阅读感。本书的作者们显然也没有想将其写成面面俱到的作品，而是**直击要点**，即挑出Go语言和其他语言相比与众不同的特点进行着重讲解，这些特点构成了本书的结构框架：

-
入门：快速上手搭建、编写、运行一个go程序

-
语法：数组(作为一个类型而存在)、切片和map

-
Go类型系统的与众不同：方法、接口、嵌入类型

-
Go的拿手好戏：并发及并发模式

-
标准库常用包：log、marshal/unmarshal、io(Reader和Writer)

-
原生支持的测试


读完这本书，你就掌握了Go语言的精髓之处，这迎合了多数gopher的内心需求。本书中文版译者Googol Lee也是Go圈子里的资深gopher，翻译质量上乘。

下面对本书各个指数的评分：

-
作者名气指数：5

-
关注度指数：5

-
内容实用指数：4

-
经典指数：4


**总分：18**

#### 第一名：[《Go程序设计语言》](https://book.douban.com/subject/27044219/) – 人手一本的Go语言“圣经”

如果说由[Brian W. Kernighan](https://www.cs.princeton.edu/people/profile/bwk)和[Dennis M. Ritchie](http://en.wikipedia.org/wiki/Dennis_Ritchie)联合编写的[《The C Programming Language》](https://book.douban.com/subject/1882483/)(也称K&R C)是C程序员(甚至是所有程序员)心目中的“圣经”的话，

![img{512x368}](../../assets/06748c725d02a59b.jpg)


那么同样由Brian W. Kernighan(K)参与编写的[《The Go Programming Language》](https://book.douban.com/subject/26337545/)（也称[tgpl](http://www.gopl.io/)）就是Go程序员心目中的“圣经”。

![img{512x368}](../../assets/b6eab2938666a8dc.jpg)


本书模仿并致敬“The C Programming Language”的经典结构，从一个”hello, world”示例开始带领大家开启Go语言之旅。第二章程序结构是Go语言这个“游乐园”的向导图，了解它之后，我们就会迫不及待地奔向各个“景点”细致参观。Go语言规范中的所有“景点”在本书中都被覆盖到了，并且由浅入深，循序渐进：从基础数据类型到复合数据类型、从函数、方法到接口、从创新的并发goroutine到传统的基于共享变量的并发，从包、工具链到测试，从反射到低级编程(unsafe包)。作者行文十分精炼，字字珠玑，这与《The C Programming Language》的风格保持了高度的一致。书中的示例在浅显易懂的同时，又极具实用性并突出Go语言的特点（比如：并发web爬虫、并发非阻塞缓存等）。

读完本书后，你会有一种爱不释手，马上还要从头再读一遍的感觉，也许这就是“圣经”的魅力！

本书出版于2015年10月26日，也是既当年中旬Go 1.5这个里程碑版本发布后，Go社区的又一重大历史事件！并且Brian W. Kernighan老爷子的影响力让更多程序员加入到Go阵营，这也或多或少促成了Go成为下一个年度，即2016年年度[TIOBE最佳编程语言](https://www.tiobe.com/tiobe-index/)。能得到Brian W. Kernighan老爷子青睐的编程语言只有C和Go，这也是Go的幸运。当然了如果老爷子是被Rob Pike或Ken Thompson通过私人关系邀请写书的，那就另当别论了，当然这纯属臆测，别当真^_^。

这本书的另一名作者Alan A. A. Donovan也并非等闲之辈，他是Go核心开发团队的成员，专注于Go工具链方面的开发。

现在唯一遗憾的是Brian W. Kernighan老爷子年事已高，不知道[Go加入泛型](https://tonybai.com/2020/06/18/the-go-generics-is-coming-and-supported-in-go-1-17-at-the-earliest/)后老爷子是否还有精力更新这本圣经。

该书中文版由七牛团队翻译，总体质量是不错的。建议Gopher们人手购置一本圣经“供奉”起来！^_^

下面对本书各个指数的评分：

-
作者名气指数：5

-
关注度指数：5

-
内容实用指数：5

-
经典指数：5


**总分：20**

### 4. 小结

Go书籍绝非“汗牛充栋”，预计Go增加泛型表达力增强后，市面上会有更多的技术书籍出炉。上面的某些经典也许还会出新版。而市面上Go书籍不多从另外一角度也可以理解成Go语言在国内还有巨大的发展空间与潜力。

努力吧，Gopher们！

只有写书者，才能体会到写者的艰辛！[Go专栏：《改善Go语言编程质量的50个有效实践》](https://www.imooc.com/read/87)也是我努力了一年多才打磨雕琢出来的心血之作。自从上线后，收到大家的热烈关注和好评！现在恰逢双11慕课大促，欢迎有意愿在Go这条技术路线上进阶的朋友们订阅，在学习过程中欢迎随时反馈和交流！

![img{512x368}](../../assets/018ff45f7e150fca.png)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中！欢迎小伙伴们学习支持！双十一慕课网优惠空前！别错过机会哦！

![img{512x368}](../../assets/e9f90df4cc2580e5.png)


微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2020, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论