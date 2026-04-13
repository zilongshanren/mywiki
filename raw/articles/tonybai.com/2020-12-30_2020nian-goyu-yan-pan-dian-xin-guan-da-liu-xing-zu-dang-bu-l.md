---
title: 2020年Go语言盘点：新冠大流行阻挡不了Go演进的步伐
url: https://tonybai.com/2020/12/30/the-2020-review-of-go-programming-language/
published: '2020-12-30'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 2020年Go语言盘点：新冠大流行阻挡不了Go演进的步伐

![img{512x368}](../../assets/13adfd095e85164d.png)


2020，这一六十年一遇的庚子年的确“名不虚传”。在这一年发生了很多事，而最受瞩目的事情莫过于**新冠疫情的全球大流行**。疫情给全球的经济带来了近似毁灭性的打击，给人们的生命带来了极大威胁，给人们的生活也带来了很大痛苦及不确定性。好在**这个糟糕的2020年马上就要过去了**！相信此时此刻每个人心中都会有一句呐喊：“**2020，快滚吧**！”。

然而肆虐的新冠疫情并没有阻挡住Go语言前进的坚实步伐。在这艰难的一年中，在Go核心开发团队和Go社区的齐心协力下，Go同样取得了**不俗的成绩**，甚至在2020年3月(那时[Go 1.14版本](https://mp.weixin.qq.com/s/PVxdtvSXgNpiD65TUo-TCg)刚刚发布不到一个月)，Go在[TIOBE的编程语言排行榜](https://tiobe.com/tiobe-index/)中还一度[挤进前十](https://my.oschina.net/u/4593547/blog/4453355)(而2019年同期，Go仅位列18位)：

![img{512x368}](../../assets/88e5101a7e104f28.jpg)


这恰说明Go语言的开发与推广工作得到了更多来自全球的开发者的认可。在这篇文章中，我们就来做一下2020年Go语言的盘点，看看在2020年围绕Go语言、Go社区和Go生态圈都发生了哪些有影响和有意义的事情。

### 1. 面对大流行，Go核心团队给出“定心丸”

大流行始于2020年1月的武汉，但真正的全球大流行则大致始于2020年3月。面对新冠全球大流行，Go核心开发团队于3月25日作出反应，在官博发表文章[《Go, the Go Community, and the Pandemic》](https://blog.golang.org/pandemic)，迅速调整了Go语言2020年的演进计划，给出了大流行期间的工作原则：

- Go始终排在诸如个人和家庭健康与安全之类的基本问题之后；
- 调整全年Go技术会议的计划，推迟或改为线上举办虚拟技术大会，为全球Gopher提供获取这些会议最新信息的渠道服务；
- 为在线培训师、Go职位发布提供便利服务；
- 为新冠病毒提供
[帮助工作台](https://covid-oss-help.org/)：https://covid-oss-help.org/； - 调整Go工作计划，缩减
[Go 1.15](https://mp.weixin.qq.com/s/B5onfyP7BPYCh_rMSBtfcQ)中包含的新特性和改进，但会遵循Go 1.15的发布时间表；重点支持gopls、pkg.go.dev的演进和优化。

Go核心开发团队的这份声明虽然简短，但却给Go社区吃了一颗“定心丸”，为Go语言在2020新冠大流行年中的稳步演进确定了节奏，指明了方向，奠定了基础。

### 2. Go在2020年值得关注的那些变化

2020一年，Go核心开发团队、社区和生态圈做了很多工作，但这里无法一一枚举，仅挑出一些重要的变化列在这里：

-
2020年2月26日，Go 1.14版本发布。主要的变动点包括：

- 嵌入接口的方法集可重叠；
- 基于系统信号机制实现了异步抢占式的goroutine调度；
- defer性能得以继续优化，理论上有30%的性能提升；
- go module已经生产就绪，并支持subversion源码仓库；
- 重新实现了运行时的timer；
- testing包的T和B类型都增加了自己的
**Cleanup**方法。

-
2020年4月20日，发布

[2019年Go开发者调查结果](https://blog.golang.org/survey2019-results)：- 参与2019开发者调查的gopher数量几乎为2018年的2倍，达到10,975人；
- 大多数受访者每天都在使用Go，而且这个数字每年都有上升的趋势；
- Go的使用仍然集中在科技公司，但Go越来越多地出现在更广泛的行业中，如金融和媒体；
- 调查的大部分指标的同比值都很稳定；
- 受访者正在使用Go来解决类似的问题，特别是构建API/RPC服务和CLI，和他们工作的组织规模大小关系不大；
- 大多数团队试图快速更新到最新的Go版本；当第三方供应商迟迟不支持当前的Go版本时，就会给开发者造成采用障碍；
- 现在Go生态系统中几乎所有人都在使用
[go module](https://mp.weixin.qq.com/s/RThCEQOdytQxwrMP7XRTRw)，但围绕包管理的一些混乱仍然存在； - 需要改进的高优先级领域包括调试、go module使用以及与云服务交互的体验改善；
- VS Code和GoLand的使用量持续增加；现在每4个受访者中就有3个首选它们。

-
2020年6月，vscode-go扩展(vscode上的go标准插件)将主代码库从github.com/microsoft/vscode-go迁移到github.com/golang/vscode-go，成为Go官方项目的一部分。

-
同在2020年6月，pkg.go.dev网站开源！该网站是Go团队在Go社区建设方面做出的主要工作，开源后的pkg.go.dev将接收更多来自社区的想法和改进意见，比如：11月，

[pkg.go.dev就发布了新版页面设计](https://blog.golang.org/pkgsite-redesign)；[原godoc.org的请求也被重定向到pkg.go.dev](https://blog.golang.org/godoc.org-redirect)(广大gopher可能需要一段时间来适应这种改变)。 -
2020年8月，

[Go 1.15版本发布](https://mp.weixin.qq.com/s/B5onfyP7BPYCh_rMSBtfcQ)，其主要的变动点包括：- GOPROXY新增以管道符为分隔符的代理列表值；
- module cache的存储路径可设置;
- 改善派生自原生类型的自定义类型变量在panic时的输出形式；
- 将小整数([0,255])转换为interface类型值时将不会额外分配内存；
- 加入更现代化的链接器(linker)，新链接器的性能要提高20%，内存占用减少30%；
- 增加tzdata包。

-
2020年11月初，全球最具影响力的Go语言技术大会

[GopherCon 2020](https://www.gophercon.com/)在线上举行！Austin Clements详细讲解了Go 1.14加入的基于系统信号的抢占式调度器；Go语言之父之一的Robert Griesemer讲解了[Go泛型当前的状态以及未来的计划](https://mp.weixin.qq.com/s/SMT40557JgQ9FjUkswznlA)。会后Russ Cox确认了Go团队将在Go 1.18版本中[加入Go泛型(类型参数)](https://mp.weixin.qq.com/s/14WeOQBdezWTC5OqQrJtfg)作为试验特性； -
2020年11月10日，Russ Cox代表Go核心开发团队发文庆祝

，在文中他回顾了Go这一年来的收获以及对2021年**Go语言发布11周年**[Go 1.16](https://mp.weixin.qq.com/s/JzAQ3r9lDBad8PO6iAerqw)和Go 1.17的展望。文中他还提到了GOPATH的历史使命即将结束，Go将开启全面module-aware模式的Go工具链时代！(下图来自推特)：

![img{512x368}](../../assets/904b0146194e117c.jpeg)


-
2020年12月中旬，Go 1.16beta1发布。在

[Go 1.16](https://mp.weixin.qq.com/s/JzAQ3r9lDBad8PO6iAerqw)中，Go将原生提供对Apple M1芯片(darwin/arm64)的支持；同时，在Go 1.16中go module将成为默认包依赖管理机制；Go 1.16还提供了支持在Go二进制文件中嵌入静态文件的官方原生方案，支持对init函数的执行时间和内存消耗的跟踪，链接器性能得到进一步优化等。 -
2020年12月16日，gopls

[v0.6.0](https://github.com/golang/tools/releases/tag/gopls%2Fv0.6.0)发布。同期，vscode-go也正[计划将gopls作为默认语言服务器](https://github.com/golang/vscode-go/issues/1037)。

### 3. Go语言当前的状态：已来到“稳定爬升的光明期”

今年笔者在知乎上滞留的时间比往年要长一些，看到很多人问与Go相关的一些问题，大致都是询问有关Go语言前景的，比如：

无论上述问题的题目有何不同，其本质的疑问都是“**Go语言前景/钱景如何，值不值得投入去学习?**”。那么是否存在一种成熟的方法能相对客观地描会出Go语言的发展态势并能对未来Go的走势做出指导呢？我想Gartner的[ 技术成熟度曲线（The Hype Cycle）](https://www.gartner.com/en/research/methodologies/gartner-hype-cycle)或许可以一试。

我们知道Gartner的技术成熟度曲线又叫技术循环曲线，是企业用来评估新科技是否要采用或采用时机的一种可视化方法，它利用时间轴与该技术在市面上的可见度(媒体曝光度)决定要不要采用以及何时该种新科技，下面就是一条典型的技术成熟度曲线的形状：

![img{512x368}](../../assets/a8ea0230f1e5f356.png)


同理，将该技术成熟度曲线应用于某种编程语言，比如Go，我们就可以用它来判断该编程语言所处的成熟阶段以辅助决定要不要采用以及何时采用该门语言。我们从知名的[TIOBE编程语言指数排行榜获取Go从2009年开源以来至今的指数曲线图](https://www.tiobe.com/tiobe-index/go/)，并且根据[Go版本发布史](https://tip.golang.org/doc/devel/release.html)在图中标记出了各个时段的Go发布版本：

![img{512x368}](../../assets/081b493d19ba423a.png)


对比上面的Gartner成熟度曲线，相信你肯定有所发现。我们共同来解释一下：

- Go语言从2009年宣布开源以来，经历了两次“高峰”：一次是2009年刚刚宣布开源后，一次是在Go1.7~Go 1.9期间。显然，第一次的高峰实际上是一个“假高峰”，那时的Go连1.0版本都尚未发布，我们完全可以将其“剔除”掉。
- 从图中来看，Go语言的技术萌芽期是比较长的，从2012年的Go 1.0一直持续到2015年的
[Go 1.5](https://tonybai.com/2015/07/10/some-changes-in-go-1-5/)； [Go 1.5版本](https://tonybai.com/2015/07/10/some-changes-in-go-1-5/)的自举以及Go垃圾回收延迟的大幅下降“引爆”了Go的“媒体曝光度”，Go技术的“期望膨胀期”开始，经历从[Go 1.6](https://tonybai.com/2016/02/21/some-changes-in-go-1-6/)到[Go 1.9版本](https://tonybai.com/2017/07/14/some-changes-in-go-1-9/)的发布后，业界对Go的期望达到了峰值；- 从Go 1.10开始，Go似乎变得“仿徨”起来，原本期望Go“一统天下”的愿望没能实现，全面出击失败后，期望的落空导致了人们对
[Go产生了“功能孱弱劣势”的印象](https://mp.weixin.qq.com/s/TJsEvqPA00qvGSRr6a8Emg)，于是Go在Go 1.11发布前跌到了“泡沫破裂”的谷底； [Go 1.11](https://tonybai.com/2018/11/19/some-changes-in-go-1-11)引入了[Go module](https://tonybai.com/2019/06/03/the-practice-of-upgrading-major-version-under-go-module/)，给社区解决[Go包依赖问题](https://tonybai.com/2019/09/21/brief-history-of-go-package-management)打了一剂强心剂，于是Go又开始了缓慢的爬升；- 从TIOBE提供的曲线来看，
[Go 1.12](https://tonybai.com/2019/03/02/some-changes-in-go-1-12)到[Go 1.15版本](https://mp.weixin.qq.com/s/B5onfyP7BPYCh_rMSBtfcQ)的发布让我们有信心认为Go已经进入了“稳步爬升的光明期”。

到此，我相信知乎上的很多问题都应该迎刃而解了，剩下的只是[如何学习Go的细节](https://mp.weixin.qq.com/s/2rsBJbz55nDEDax6vqKE5w)和[如何Go进阶](https://mp.weixin.qq.com/s/RThCEQOdytQxwrMP7XRTRw)了。

不过可能还有很多朋友会问，Go何时能达到**实质生产高峰期**呢？这个问题真不好回答。但进入了“稳步爬升的光明期”后的Go到达实质生产高峰期只是一个时间问题了，也许2022年初发布的[支持Go泛型特性](https://mp.weixin.qq.com/s/SMT40557JgQ9FjUkswznlA)的Go 1.18版本会快速推动Go向更高阶段进发！

### 4. 展望Go的2021：继续蓄力，迎接下一个“引爆点”

促使Go回到“稳步爬升光明期”的go module机制将在2021年年初正式发布的Go 1.16中成为默认包依赖管理机制。而[Go 1.16版本](https://github.com/golang/go/milestone/145)也已经处于特性冻结并发布了beta1版本的阶段，其更多特性可以参考我的[“Go 1.16新功能特性不完全前瞻”](https://mp.weixin.qq.com/s/JzAQ3r9lDBad8PO6iAerqw)一文。

将于2021年八月发布的[Go 1.17的里程碑](https://github.com/golang/go/milestone/163)已经建立, 从里程碑的内容来看，已基本确定加入的功能特性和改进包括：

- 针对x86-64的新的
[基于寄存器的调用约定](https://github.com/golang/go/issues/40724)（不破坏现有程序集！），这将使程序与主流语言的ABI模型保持一致，并且整体更快； [加入build指示器新语法](https://github.com/golang/go/issues/41184)：**//go:build**；[一个十多年前的issue](https://github.com/golang/go/issues/395)被Go团队accept：使用**(*[4]int)(x)**语法将切片x转型为一个数组类型指针(*[4]int)。

当然Go 1.17还会持续优化链接器，更多功能特性和改进还待Go团队策划补充。

而万众期待的Go泛型依然会继续打磨，从2016年Ian Lance Taylor提出[“Go should have generics”](https://github.com/golang/proposal/blob/master/design/15292-generics.md)的设计草案以来，Go泛型草案至今已经讨论了4年多了，这再次证明了Go团队对于这类会显著增加Go复杂性的特性是多么地“慎之又慎”。虽然Go团队初步确定了在Go 1.18版本中将Go泛型（类型参数）落地，但近期Go项目中关于Go泛型的[主issue：proposal: spec: generic programming facilities](https://github.com/golang/go/issues/15292)中仍然有不少反对的声音。Go团队在**“继续保持Go简单”**的道路上真是任重道远啊！

总之，2021年，Go将继续稳步爬升，也许爬的并没有那么快，但在我看来，这是在积蓄力量，等待着下一个引爆点。

### 5. 小结

Go在新冠疫情大流行的历史时期依旧步行稳健，为下一个“引爆点”积极蓄力。Go在自己传统领域依旧存在明显优势，比如：企业级应用、基础设施、中间件、微服务API、命令行应用等，并且在这些领域取得了越来越多开发者的青睐。

Go在其他领域也有“意外收获”，比如：[在黑客工具领域，Go已经逐渐威胁着Python的龙头地位了](https://www.imperva.com/blog/python-and-go-top-the-chart-of-2019s-most-popular-hacking-tools/)，显然[语法简单](https://www.imooc.com/read/87/article/2321)、[原生并发](https://www.imooc.com/read/87/article/2340)、[自带“电池”](https://www.imooc.com/read/87/article/2341)、轻松跨平台的编译以及编译为独立二进制文件的Go与黑客的需求十分契合。不过，在安全领域成为了进攻“武器”，这想必是Go设计者们所意料不到的。

### 6. 福利！2020年本博客最受欢迎Go相关文章TOP10

[Go新泛型设计方案详解](https://mp.weixin.qq.com/s/mkpnR8LYHtauBGzQC-SglQ)[Go语言有哪些“劣势”](https://mp.weixin.qq.com/s/TJsEvqPA00qvGSRr6a8Emg)[Go，11周年](https://mp.weixin.qq.com/s/woQeEQUhOLJ7KSE5rm5q6g)[Go 1.16新功能特性不完全前瞻](https://mp.weixin.qq.com/s/JzAQ3r9lDBad8PO6iAerqw)[Go 1.14中值得关注的几个变化](https://mp.weixin.qq.com/s/PVxdtvSXgNpiD65TUo-TCg)[Go 1.15中值得关注的几个变化](https://mp.weixin.qq.com/s/B5onfyP7BPYCh_rMSBtfcQ)[像跟踪分布式服务调用那样跟踪Go函数调用链](https://mp.weixin.qq.com/s/zrM0I-CsEujAm6ho6AD79g)[系统学习Go语言，有这几本书就够了](https://mp.weixin.qq.com/s/2rsBJbz55nDEDax6vqKE5w)[通过实例深入理解sync.Map的工作原理](https://mp.weixin.qq.com/s/rsDC-6paC5zN4sepWd5LqQ)[Go专栏“改善Go语言编程质量的50个有效实践”上线了](https://mp.weixin.qq.com/s/RThCEQOdytQxwrMP7XRTRw)

**Gopher部落**知识星球已正式转正了！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！星球首开，福利自然是少不了的！2020年年底之前，8.8折加入星球，下方图片扫起来吧，先到先得哦！

![](../../assets/d3fad3142fe3cc39.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订阅！

![](../../assets/d8e58987c0d3be58.png)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/e9f90df4cc2580e5.png)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2020, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论