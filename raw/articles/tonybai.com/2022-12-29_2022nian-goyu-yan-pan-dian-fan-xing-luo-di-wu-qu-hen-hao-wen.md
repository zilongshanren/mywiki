---
title: 2022年Go语言盘点：泛型落地，无趣很好，稳定为王
url: https://tonybai.com/2022/12/29/the-2022-review-of-go-programming-language/
published: '2022-12-29'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 2022年Go语言盘点：泛型落地，无趣很好，稳定为王

![](../../assets/7467685efc0fe3d8.png)


[本文永久链接](https://tonybai.com/2022/12/29/the-2022-review-of-go-programming-language) – https://tonybai.com/2022/12/29/the-2022-review-of-go-programming-language

早早就计划好在年前写一个Go语言年度盘点，就像[2020年](https://tonybai.com/2020/12/30/the-2020-review-of-go-programming-language)和[2021年](https://tonybai.com/2022/01/16/the-2021-review-of-go-programming-language)那样。但恰逢国内疫情管控放开，一波阳了之后身体十分容易疲劳，再加上工作上的事情挺多，这篇盘点也就迟迟没能下笔。

今年的盘点思路将围绕三个关键字来展开：**泛型、无趣(boring)和稳定**。下面我们逐一来看看。

### 1. “泛型”靴子落地

2022年3月中旬，Go社区尤其是那些期盼Go加入泛型特性的Gopher终于迎来了[Go 1.18版本的正式发布](https://tonybai.com/2022/03/16/go-1-18-released)，这意味着**Go泛型这只靴子终于落地了**。

其实，从Go开源那一天开始，Go核心团队就没有间断过对泛型的探索，并一直尝试寻找一个理想的泛型设计方案，但始终未能如愿。直到近几年Go团队觉得Go已经逐渐成熟，是时候下决心解决Go社区主要关注的几个问题了，包括泛型、包依赖以及错误处理等。其中泛型常年在Go官方用户调查报告的“你最想要的Go语言特性”这项调查的榜单上霸榜，下图摘自2020年度Go官方用户调查结果：

![](../../assets/d041f9dd190c35dc.png)


之后，Go团队安排伊恩·泰勒和罗伯特·格瑞史莫花费更多精力在泛型的设计方案上，这才有了Go 1.18 版本中泛型语法特性的落地。

个人觉得：Go泛型是Go核心团队对Go社区的一次迎合与妥协，因为泛型与Go的主要设计哲学“简单”是有悖的。泛型这个语法特性会给语言带来复杂性，这种复杂性不仅体现在语法层面上引入了**难于理解和使用**的新的语法元素，也体现在类型系统和运行时层面上为支持泛型进行的复杂的实现。

如果从2010年6月份，伊恩·泰勒提出的[Type Functions设计方案](https://go.googlesource.com/proposal/+/master/design/15292/2010-06-type-functions.md)算起，到2022年3月份的泛型落地，[Go加入泛型之路足足走了近12年](https://time.geekbang.org/column/article/485140)。不过结果还是不错的，经过近12年的努力与不断地自我否定，Go团队终于找到了一个不违背** Go1兼容性承诺(见下图)**的

[泛型实现方案](https://github.com/golang/proposal/blob/master/design/43651-type-parameters.md)：

![](../../assets/db35356153606cd7.png)


从这方面讲，Go对泛型的支持又是十分成功的。在如此语法巨变的情况下，依然保持向后兼容(backforward compatibility)。

不过如果你因为Go加入了对泛型的支持就打算投入Go阵营，这里先给你一些友情提示：**和支持泛型的主流编程语言之间的泛型设计与实现存在差异一样，Go的泛型与其他主流编程语言的泛型也是不同的**。在学习Go泛型之前，可以先了解一下Go泛型设计方案已经明确不支持的若干特性，比如：

- 不支持泛型特化（specialization），即不支持编写一个泛型函数针对某个具体类型的特殊版本；
- 不支持元编程（metaprogramming），即不支持编写在编译时执行的代码来生成在运行时执行的代码；
- 不支持操作符方法（operator method），即只能用普通的方法（method）操作类型实例（比如：getIndex(k)），而不能将操作符视为方法并自定义其实现，比如一个容器类型的下标访问 c[k]；
- 不支持变长的类型参数（type parameters）；
- … …。

这些特性如今不支持，后续大概率也不会支持。所以小伙伴们，尤其是来自Java、C++等语言阵营的小伙伴，在进入Go泛型语法学习之前，你一定要先了解Go团队的这些设计决策。

此外，目前的Go泛型实现和最后一版的[泛型设计方案](https://github.com/golang/proposal/blob/master/design/43651-type-parameters.md)相比还有差距，依旧不是完全版，还有一些特性没有加入，[还有问题亟待解决](https://go101.org/generics/888-the-status-quo-of-go-custom-generics.html)。

就目前笔者观察来看，Go泛型还处于早期阶段，远非成熟。Go module构建模式从[go 1.11版本](https://tonybai.com/2018/11/19/some-changes-in-go-1-11)加入到[go 1.16](https://tonybai.com/2021/02/25/some-changes-in-go-1-16)成为默认并逐渐成熟还花了3年多时间呢，何况是Go泛型。这样来看，初步预测Go泛型要到2025年才会成熟，而成熟的标志无非如下几个：

- 泛型语法特性确定以及稳定下来；
- 语法问题基本都解决；
- Go标准库开始广泛使用泛型；
- Go泛型的运行时性能问题得到基本解决。

目前Go团队对泛型的应用依旧保持谨慎，并在循序渐进地推进泛型在Go团队与Go社区的应用，最新的消息是Go团队已经提出proposal，计划在Go 1.21版本中将用泛型实现的[maps包](https://github.com/golang/go/issues/57436)和[slices包](https://github.com/golang/go/issues/57433)加入Go标准库，这两个包原本计划在Go 1.18版本加入，但因Rob Pike的建议先放到了golang.org/x/exp下面待定。

### 2. 无趣(boring)很好

和其他主流编程语言如C++、Rust等在新版本中不断有新语言特性刺激程序员的神经，让大家阶段性产生兴奋感(exciting)不同，除了早期版本(比如Go 1.1和Go 1.2)以及里程碑的Go 1.5版本的完成自举和大幅降低GC延迟、Go 1.11版本的go module构建模式、Go 1.18版本的泛型落地之外，大部分版本的发布都很难让Gopher们十分兴奋，甚至业界都称**“Go is boring(Go很无趣)”**。

在今年的线下GopherCon大会上，Go核心团队技术Leader Russ Cox发表名为[“Compatibility: How Go Programs Keep Working”](https://www.youtube.com/watch?v=v24wrd3RwGo)的主题演讲，在这个演讲中，Russ Cox借用了Go is boring的这一说法，并称That is good!

![](../../assets/8f9efb4cb119775b.png)


国外新冠管控放开早，经过几波疫情后，与病毒共存了，于是2022年的GopherCon大会又重新恢复线下举办。


Russ Cox的原话是：“boring is good. boring is stable. boring means to be able to focus on your work and not ours… We’ll keep doing everything we can to keep go boring for all of you”。

这几句英文不难，相信大家都能看懂。无趣的Go意味着稳定，意味着大家将注意力都集中在自己的工作上而不是Go核心团队身上(去关注新特性)。Go语言不会像其他编程语言那样堆砌新功能特性。

Russ Cox的这一观点代表了Go核心团队，也代表着Go演进未来演进的主基调。同时，Russ明确给出结论：**不会有Go2了**，Go 1.xy会一直持续下去。Russ甚至提出：**兼容性才是Go最重要的feature**：

![](https://tonybai.com/wp-content/uploads/the-2022-review-of-go-programming-language-6.png)


并且Russ Cox在Go项目的discussion中也给出保持Go兼容性的[backward compatibility](https://github.com/golang/go/discussions/55090)、[forward compatibility](https://github.com/golang/go/discussions/55092)的扩展方案与[一个实例](https://github.com/golang/go/discussions/56010)。

关于“Go is boring”，Russ没有进一步展开说，记得之前译过一篇名为[《Go语言很无聊…其实它妙不可言！》](https://tonybai.com/2021/01/07/go-is-boring)的文章，大家可以看看那篇文章进一步体会一下“Go is boring”的含义。

### 3. “稳定”是主旋律

Go的稳定不仅体现在Go语法特性的演化上，Go语言在各大语言排行榜上的排名也进入了相对稳定区，以[TIOBE index](https://www.tiobe.com/tiobe-index/)为例，下面是2022年12月份的排名截图：

![](https://tonybai.com/wp-content/uploads/the-2022-review-of-go-programming-language-2.png)


我查了一下《

[2021年Go语言盘点：厉兵秣马强技能，蓄势待发新征程]》一文中2022年1月份Go的排名为13名，上图中2021年12月份是19名的数据应该是错误的，相对2021年12月份，Go实际排名上升1位。

我们看到2021年Go从14升到13，今年又从13升到12。按照TIOBE官方编辑说法，在新兴编程语言中，Go是唯一一个可能在未来冲入前十的后端编程语言。

Go语言在实际应用中的表现与上述排名的变化也十分契合，总体来说就是十分稳定，国内外都波澜不惊，国内大厂该用Go的也都用了，腾讯、字节依旧是这方面的领头羊，先后开源了不少Go实现的项目，最受瞩目的应该是字节将内部的Go框架逐一开源了，包括：[netpoll](https://github.com/cloudwego/netpoll)、[kitex(rpc框架)](https://github.com/cloudwego/kitex)、[hertz(http框架)](https://github.com/cloudwego/hertz)等。

为了更好的帮助大家回顾这一年来Go的稳定演化，这里简单整理了2022年Go大事件列表，供大家参考：

- 2022年3月，
[Go 1.18版本正式发布](https://tonybai.com/2022/04/20/some-changes-in-go-1-18)

Go社区等待了多年的泛型语法特性终于加入Go中。

- 2022年4月，Go官方发布了
[2021官方Go用户调查结果](https://go.dev/blog/survey2021-results)

从调查结果中可以看到，Gopher对Go的满意度依然高达92%；81%的受访者对Go项目的长期方向充满信心。

- 2022年5月，ACM期刊发表了
[《Go编程语言与环境》](https://tonybai.com/2022/05/04/the-paper-of-go-programming-language-and-environment)一文

这篇Go语言的综述文章由Russ Cox，Robert Griesemer，Rob Pike，Ian Lance Taylor和Ken Thompson联合撰写，是**Go核心团队对10多年来Go演化发展的复盘**，深入分析了那些对Go的成功最具决定性的设计哲学与决策，是Go诞生十多年来最重要的一篇文章。

- 2022年6月，uber工程博客发布
[《Go语言数据竞争检测与数据竞争模式》](https://tonybai.com/2022/06/21/data-race-detection-and-pattern-in-go)

该文介绍了ThreadSanitizer v2的工作原理，并总结了7类数据竞争模式。

- 2022年8月，
[Go 1.19版本正式发布](https://tonybai.com/2022/08/22/some-changes-in-go-1-19)

相对于Go 1.18版本而言，Go 1.19是一个“小”版本，它主要针对Go 1.18版本中泛型实现的问题做了修改和优化，引入了Soft memory limit，更新了[《Go内存模型》](https://go.dev/ref/mem)文档。

包括sync.Pool的优化、defer性能提升、基于系统信号的抢占式调度(go 1.14)、调度器性能提升、支持[基于寄存器的调用规约](https://tonybai.com/2021/08/20/using-register-based-calling-convention-in-go-1-17)、soft memory limit等。

- 2022年9月，Go官方发布
[govulncheck工具](https://tonybai.com/2022/09/10/an-intro-of-govulncheck)

[软件供应链安全问题](https://tonybai.com/2022/03/14/software-supply-chain-security-in-go)愈发受到各界关注。Go安全团队发布Go官方安全漏洞管理的工具和方案: govulncheck。govulncheck是[Go安全漏洞数据库(Go vulnerability database)](https://vuln.go.dev)的一个**前端**，它通过[Go官方维护的vuln仓库](https://github.com/golang/vuln)下面的[vulncheck包](https://github.com/golang/vuln/tree/master/vulncheck)对你仓库中的Go源码或编译 后的Go应用可执行二进制文件进行扫描，形成源码的调用图(callgraph)和调用栈(callstack)。

- 2022年10月，GopherCon大会在芝加哥线下举行

Russ Cox发表《Compatibility: How Go Programs Keep Working》主题演讲，确定了未来Go语言演进的主基调。

- 2022年11月，Go开源13岁生日

Go官方回顾了2022年Go团队的工作与成果，并简单说明了在新一年的工作，包括继续努力使Go成为用于大规模软件工程的最好的环境。计划特别关注供应链安全，提高兼容性和结构化日志记录([slog](https://tonybai.com/2022/10/30/first-exploration-of-slog))，当然还会有很多其他改进，包括[profile-guided optimization](https://github.com/golang/go/issues/55022)等。

### 4. Go语言2023年展望

目前Go语言的演化与发展与我在[2020年Go盘点](https://tonybai.com/2020/12/30/the-2020-review-of-go-programming-language/)中的预测基本一致。我现在依然坚持我的判断，即我在[《Go语言第一课》专栏](http://gk.link/a/10AVZ)中所说的那样：

绝大多数主流编程语言将在其诞生后的第15至第20年间大步前进。按照这个编程语言的一般规律，已经迈过开源第13个年头的Go，很可能将进入自己的黄金5-10年。2022年泛型落地就是Go语言进入黄金5-10年的起点，待2025年泛型成熟后，Go将取得更快的发展速度。


前途是美好的，但道路的曲折坎坷的。目前Go更多应用于基础设施、中间件领域和基础微服务领域，在企业级业务系统方面，类似spring这样的“全家桶”框架的缺乏和无法达成一致，让开发者在开发复杂业务系统时依旧首选Java。期待Go在这方面能所有进展。

同时，Go演进道路上还存在另外一个风险，在我的[《Go为什么能成功》](https://tonybai.com/2022/12/07/why-go-succeed)一文中，我曾经提到过：“Go成也Google，败也Google”。Go团队目前的治理体系太过于依赖google，这是一门双刃剑。当google发展较好时，Go语言将从中受益。但当google开始走下坡路时，Go是否还能像如今这样风光呢？让我么拭目以待吧！

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

Google 走一段时间的下坡路是无疑的，但应该不至于影响到 Go。 比如 Facebook，哦不， Meta ，都沦为笑柄了，用户下滑也是确定的，但旗下的 React 仍然老当益壮，后来想挑战的框架和库一堆堆， 但没人能掀翻 React 。简洁优秀的设计思想配合壮大的社区生态，活的年头很可能比我长。 而 Go 的设计思想显然也同样是简洁优秀的，只要社区方面再稳步前行，应该仍然是靠谱的选择。

至少现在看来我觉得比 Rust 靠谱……