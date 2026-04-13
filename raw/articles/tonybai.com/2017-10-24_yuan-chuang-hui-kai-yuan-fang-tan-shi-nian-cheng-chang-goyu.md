---
title: 源创会开源访谈：十年成长，Go语言的演化之路
url: https://tonybai.com/2017/10/24/go-evolution-for-ten-years-an-interview-by-osc/
published: '2017-10-24'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 源创会开源访谈：十年成长，Go语言的演化之路

在参加[源创会沈阳站](http://tonybai.com/2017/10/23/the-speech-script-practice-on-deploying-a-ha-harbor-cluster-for-osc-shenyang-2017/)分享之前，接受了[开源中国社区](https://www.oschina.net/)编辑[王练](https://my.oschina.net/mrtudou)的文字专访，以下是我针对专访稿的内容。

同时该专访稿首发于开源中国开源访谈栏目，大家可以点击[这里](https://www.oschina.net/question/2896879_2268389)看到首发原稿。

### 1、首先请介绍一下自己

大家好！我叫白明（Tony Bai），目前是[东软云科技](http://www.neusoft.com/cn/)的一名架构师，专职于服务端开发，日常工作主要使用[Go语言](https://golang.org)。我算是国内较早接触[Go语言](http://tonybai.com/tag/c)的程序员兼Advocater了，平时在我的[博客](http://tonybai.com)、[微博](http://weibo.com/bigwhite20xx)和微信公众号”iamtonybai”上经常发表一些关于Go语言的文章和Go生态圈内的信息。

在接触Go之前，我主要使用[C语言](http://tonybai.com/tag/c)开发电信领域的一些后端服务系统，拥有多年的电信领域产品研发和技术管理经验。我个人比较喜换钻研和分享技术，是《[七周七语言](https://book.douban.com/subject/10555435/)》一书的译者之一，并且坚持写技术博客十余年。同时我也算是一个开源爱好者，也在[github](https://github.com/bigwhite)上分享过自己开发的几个小工具。

目前的主要研究和关注的领域包括：Go、[Kubernetes](http://tonybai.com/tag/kubernetes)、[Docker](http://tonybai.com/tag/docker)、[区块链](https://en.wikipedia.org/wiki/Blockchain)和儿童编程教育等。

![img{512x368}](../../assets/bc0f2fe6ee6aa208.jpg)


### 2、最初是因为什么接触和使用 Go 语言的？它哪方面的特性吸引了您？

个人赶脚：选编程语言和谈恋爱有些像（虽然我只谈过一次^_^），我个人倾向一见钟情。我个人用的最多的编程语言是[Go](http://tonybai.com/tag/go)、[C](http://tonybai.com/tag/c)，这两门语言算是我在不同时期的“一见钟情”的对象吧，也是最终“领（使）证（用）”的，前提：编程世界是“一夫多妻制”^0^。

当然早期也深入过[C++](http://tonybai.com/tag/cpp)，后来[Java](http://tonybai.com/tag/java)、[Ruby](http://tonybai.com/tag/ruby)、[Common Lisp](http://tonybai.com/tag/clisp)、[Haskell](http://tonybai.com/tag/haskell)、[Python](http://tonybai.com/tag/python)均有涉猎，这些语言算是恋爱对象，但最终都分手了。

最初接触到Go应该是2011年，那是因为看了Rob Pike的[3 Day Go Course](https://pan.baidu.com/s/1kV9VxLP)，那时[Go 1.0版本](https://blog.golang.org/go-version-1-is-released)还没有发布，如果没记错，Rob Pike slide中用的还是Go r60版本的语法。现在大脑中留存的当时的第一感觉就是“一见钟情”！

现在回想起来，大致有这么几点原因：

- Go与C一脉相承，对于出身C程序员的我来说，这一语言传承非常自然，多体现在语法上；
- Go语言非常简单，尤其是GC、并发
[goroutine](http://tonybai.com/2017/06/23/an-intro-about-goroutine-scheduler/)、interface，让我眼前一亮； - Rob Pike的Go Course Slide组织的非常好，看完三篇Slide，基本就入门了。

于是在那之后，又系统阅读了Ivo Balbaert的《[The Way To Go](https://book.douban.com/subject/10558892/)》、《[Programming in Go – Creating Applications for the 21st Century](https://book.douban.com/subject/7070565/)》等基本新鲜出炉的书，于是就走入了Go语言世界。

不过当时Go1尚未发布，Go自身也有较大变化，工作中也无法引入这门语言，2013年对Go的关注有些中断，2014年又恢复，直至今天。现在感觉到：如果工作语言与兴趣语言能保持一致是多么幸福的一件事啊。

### 3、有人说 Go 是互联网时代的 C 语言，对于这两门语言，您是怎么看的？

如果没记错，至少在国内，第一个提出这种观点的是现[七牛](https://www.qiniu.com/)的ceo[许式伟](http://weibo.com/xushiweizh)了，老许是国内第一的Go 鼓吹者，名副其实；而且许式伟的鼓吹不仅停留在嘴上，更是付诸于实践：据说其七牛云的基础设施基本都是Go开发的。因此，对他的“远见卓识”还是钦佩之至的。

[C语言](https://en.wikipedia.org/wiki/C_(programming_language))缔造的软件行业的成就是举世瞩目，也是公认的。其作者[Dennis Ritchie](https://en.wikipedia.org/wiki/Dennis_Ritchie)被[授予图灵奖](https://en.wikipedia.org/wiki/Dennis_Ritchie#cite_note-16)就是对C语言最大的肯定和褒奖。C语言缔造了单机操作系统和基础软件的时代：[Unix](https://en.wikipedia.org/wiki/Unix)、[Linux](http://tonybai.com/tag/linux)、nginx/apache以及无数以*inx世界为中心的工具，是云时代之前最伟大的系统编程语言和基础设施语言。

至于 “Go是互联网时代的 C 语言”这一观点，如果在几年前很多人还会疑惑甚至不懈，但现在来看：事实胜于雄辩。我们来看看当前[CNCF](https://www.cncf.io/)基金会(Cloud Native Computing Foundation)管理的项目中，有一大半都是Go语言开发的，包括[Kubernetes](http://tonybai.com/tag/kubernetes)、[Prometheus](https://github.com/prometheus/prometheus)等炙手可热的项目；这还不包括近两年最火的[docker](http://tonybai.com/tag/docker)项目。事实证明：Go已成为互联网时代、云时代基础设施领域、云服务领域的最具竞争力的编程语言之一。

不过和C不同的是，Go语言还在发展，还在演进，还有巨大的提升空间，Gopher群体还在变大，去年再次成为[Tiboe](https://www.tiobe.com/tiobe-index/)的年度语言就是例证。

当然我们还得辩证的看，Go语言虽然在云时代基础设施领域逐渐继承C语言的衣钵，但是由于语言设计理念和设计哲学上的原因，在操作系统以及嵌入式领域，Go还在努力提升。

### 4、Go 也经常被拿来和 Java、Rust 等语言比较，您认为它最适合的使用场景有哪些？

早期对[Java](http://tonybai.com/tag/java)有所涉猎，但止步于Java体量过重和框架过多；Rust和Go一样是近几年才兴起的一门很有理想、很有抱负的编程语言，其目标就是安全的系统级编程语言，运行性能极佳，用以替代C/C++的，但就像前面所提到的那样，第一眼看到Rust的语法，就没有那种“一见钟情”的赶脚，希望Rust不要像C++那样，演变的那么复杂。

Go从其第一封设计email出炉到如今[已有十年](http://tonybai.com/2017/09/24/go-ten-years-and-climbing/)了，我觉得也不应该由我来告诉大家Go更适合应用在什么领域了，事实摆在那里：“大家都用的地方，总是对的”。这里我只是大致归纳一下：

-
云计算基础设施领域

代表项目：docker、kubernetes、etcd、

[consul](http://tonybai.com/2015/07/06/implement-distributed-services-registery-and-discovery-by-consul/)、cloudflare CDN、七牛云存储等。 -
基础软件

代表项目：

[tidb](https://github.com/pingcap/tidb)、[influxdb](https://github.com/influxdata/influxdb)、[cockroachdb](https://github.com/cockroachdb/cockroach)等。 -
微服务

-
互联网基础设施

代表项目：

[以太坊](https://github.com/ethereum/go-ethereum)、[hyperledger](https://github.com/hyperledger)等。

Go在数据科学、人工智能领域也有较大进展，希望在将来能看到Go在这些领域有杀手级项目出现。

### 5、Go发展已有10 年，其特性随着版本的迭代不断在更新，您觉得它最好的和最需要改进的特性分别有哪些？

每种语言都有自己的设计哲学和设计者的考量。我在[GopherChina 2017](http://gopherchina.org/)的topic中就提到过[Go语言的价值观](http://tonybai.com/2017/04/20/go-coding-in-go-way/)，其中之一就是Simplicity，即简单。相信简单也是让很多开发者走进Gopher世界的重要原因。从今年GopherCon 2017大会上[Russ Cox](https://github.com/rsc)的“[Toward Go 2](https://blog.golang.org/toward-go2)”的主题演讲中，我们也可以看出：Go team并不会单纯地为了迎合community的意愿去堆砌feature，那go势必走上c++的老路，变得日益复杂，Go受欢迎的基础之一就不存在了。

但演进就一定会要付出代价的，尤其是Go1的约束在前。从我个人对Go的应用来看，最想看到的是包管理和error处理方面的体验提升。但我觉得这两点都是可以通过渐进改进实现的，甚至不会影响到Go1兼容性，不会像引入generics机制，实现难度也不会太高。

对于目前的error handling机制，我个人并没有太多的排斥，这可能是因为我出身C程序员的缘故吧。在error handling这块，只是希望能让gopher拥有更好的体验即可，比如说围绕现有的error机制，增加一些设施以帮助gopher更好的获取error cause信息，就像github.com/pkg/errors包那样。

对于社区呼声很高的[generics](https://en.wikipedia.org/wiki/Generic_programming)（泛型），我个人倒是没有什么急切需求。generics虽然可以让大幅提升语言的表现力(expressiveness)，但也给语言自身带来了较大的复杂性。就个人感受而言，C++就是在加入generics后才变得无比庞大和复杂的，同时generics还让很多C++ programmer沉溺于很多magic trick中无法自拔，这对于以“合作分工”为主流的软件开发过程来说，并不是好事情。

### 6、Go 官方团队已发布 2.0 计划，更侧重于兼容性和规模化方面。对此，您怎么理解？Go 否已达到最佳性能？

这个问题和上面的问题有些类似，我的想法差不多。Go team在特性演进方面会十分谨慎，这也是go Team一贯的风格。从Go1到Go2，从现在看来，这个时间跨度不会很短，也许是2-3年也不一定，心急吃不了热豆腐^0^，社区分裂可不是go team想看到的事情，python可是前车之鉴。

另外，Go性能显然还是有改善空间的，尤其是编译性能、GC吞吐和延迟的tradeoff方面；另外goroutine调度器算法方面可能还有改进空间。当前Goroutine调度算法的实现者[Dmitry Vyukov](https://github.com/dvyukov)之前就编写了一个scheduler优化的proposal: [NUMA-aware scheduler for Go](https://docs.google.com/document/d/1d3iI2QWURgDIsSR6G2275vMeQ_X7w-qxM2Vp7iGwwuM/pub)(针对numa体系的优化)，但也许因为重要性、优先级等考量，一直没有实现，也许后续会实现。

### 7、Go 在国内似乎比国外还要火，您认为造成这种现象的原因是什么？

从一些搜索引擎的trend数据来看，Go在中国地区的确十分火热，甚至在热度值上是领先于欧美世界的。个人觉得造成这种现象的原因可能有如下几点：

- 语言本身的接受度高

首先，从Go语言本身考虑。事实证明了：Go语言的设计匹配了国内程序员的行业业务需求和对语言特性的需求(口味)：

a) 语言：[简单、正交组合和并发](http://tonybai.com/2017/04/20/go-coding-in-go-way/)；开发效率和运行效率双高；

b) 自带battery：丰富的标准库和高质量第三方库；

c) 迎合架构趋势：天生适合微服务….

- 引入早且与Go advocator的努力分不开

当前再也不是那个“酒香不怕巷子深”的年代了，再好的编程语言也需要推广和宣称。Go team在[社区建设](https://github.com/golang/go/wiki)、全世界推广方面也是不遗余力。至于国内更是有像许式伟、[Astaxie](https://github.com/astaxie)这样的占据高端IT圈子的advocator在站台宣传。

- 互联网飞速发展推动Go在国内落地

中国已经是事实的移动互联网时代的领军者，大量创业公司如雨后春笋般诞生。而Go对于startup企业来说是极其适合的。开发效率高，满足了Startup企业对产品或服务快速发布的需求；运行效率高可以让startup公司节省初期在硬件方面的投入：一台主机顶住100w并发。

对于那些巨头、大公司而言，Go又是云计算时代基础设施的代表性语言，自然也会投入到Go怀抱，比如：阿里CDN、百度门户入口、滴滴、360等。

### 8、对于刚开始学习 Go ，并期待将其应用在项目中的新人们，您有哪些建议？

学语言，无非实践结合理论。

- 理论：书籍和资料

这里转一下我[在知乎上一个回答](https://www.zhihu.com/question/30461290/answer/142764934)：

强烈推荐：Rob Pike 3-day Go Course，虽然语法过时了，但看大师的slide，收获还是蛮多的。

Go基础: Go圣经《[The Go Programming Language](https://book.douban.com/subject/26337545/)》和《[Go in Action](https://book.douban.com/subject/25858023/)》。

原理学习: 雨痕的《[Go学习笔记](https://book.douban.com/subject/26832468/)》。

Go Web编程: 直接看astaxie在github上的《[Go web编程](https://github.com/astaxie/build-web-application-with-golang)》。

还有一本内容有些旧的，但个人觉得值得一看的书就是《[The Way To Go](https://book.douban.com/subject/10558892/)》，大而全。Github上有部分章节的[中译版](https://github.com/Unknwon/the-way-to-go_ZH_CN)。

另外，建议看一遍官方的[Language specification](https://golang.org/ref/spec)、[effective go](https://golang.org/doc/effective_go.html)和[go faq](https://golang.org/doc/faq)，对学go、理解go设计的来龙去脉大有裨益。

- 实践：多读多写Code

多读代码：首选标准库，因为Go的惯用法和最佳实践在标准库中都有体现。

写代码：这个如果有项目直接实践那是非常的幸福；否则可以从改写一个自己熟悉领域的工具开始。比如：以前我刚接触Go的时候，没啥可写的。就改写一套[cmpp协议实现](https://github.com/bigwhite/gocmpp)。后来做wechat接口，实现了一个简单的[wechat基本协议](https://github.com/bigwhite/gowechat)，当然这两个代码也过于陈旧了，代码设计以及其中的go语言用法不值得大家学习了^0^。

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

有人在golang-dev论坛问了golang核心开发者Ian Lance Taylor， Dmitry Vyukov 设计的 NUMA-aware scheduler for Go的调度器，现在进展怎么样，Ian Lance Taylor回复说没人在做这项工作,Dmitry Vyukovy也不在golang开发组了，好像去搞linux内核优化了，好可惜呀,golang的调度器还是有优化空间的呀

Dmitry Vyukovy好像一直都是“外援”，是google员工，但不是go team 常务member。当初做scheduler时也是“编外”支援。现在scheduler没有大动静，估计也是因为暂时“够用”。一旦到了不“够用”那天，自然就会有大神来优化了。