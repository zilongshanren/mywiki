---
title: 2024年Go语言盘点：排名历史新高，团队新老传承
url: https://tonybai.com/2025/01/06/the-2024-review-of-go-programming-language/
published: '2025-01-06'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 2024年Go语言盘点：排名历史新高，团队新老传承

![](../../assets/9850778a00b7d77b.png)


[本文永久链接](https://tonybai.com/2024/01/06/the-2024-review-of-go-programming-language) – https://tonybai.com/2024/01/06/the-2024-review-of-go-programming-language

2024年底，由于感染了甲流，我在家卧床休息了两天，原定于2024年进行的Go语言盘点写作因此被迫推迟。不过，我始终相信：迟到但不会缺席。在2025年元旦的第一天，我终于开始了这篇博客的撰写。

时间过得真快，《[2023年Go语言盘点：稳中求新，稳中求变](https://tonybai.com/2023/12/31/the-2023-review-of-go-progrmming-language/)》依然历历在目。转眼之间，一年365天过去了，发生了许多事情，甚至有些记忆已在脑海中模糊或消逝。在这里，我将带你盘点那些关于Go的重要时刻，唤起你对Go的美好回忆。

回顾整个2024年，如果非要用一句话来形容Go语言的状态，我会选择：**Go完成了 技术成熟度曲线中的“稳步爬升复苏期”，开始进入“生产成熟期”**。这一点在Go的排名中得到了直接体现，并在Go社区的活跃度方面得到了间接的印证。而

[Go的年中换帅](https://tonybai.com/2024/10/10/pass-torch-to-go-new-leadership-team)似乎也

**预示着这是一个新的起点**！在过去一年中，得益于Go团队和社区的共同努力，Go发布了许多值得关注的新特性。

接下来，我将为大家逐一详细介绍！

## 1. Go排名创历史新高

说到编程语言排名，程序员们首先想到的就是TIOBE！在2024年的[TIOBE排行榜](https://www.tiobe.com/tiobe-index/)上，尽管Go语言没有像[AI时代](https://tonybai.com/2024/10/14/programming-in-ai-era)的霸主语言Python那样耀眼，但跻身前十并站稳第七名这一成绩也足以让其他语言羡慕不已！

![](../../assets/91d7ff731422771c.png)



而从2009年开源至今，Go在TIOBE排名走势如下：

![](../../assets/729139e85d219d77.png)



了解Go历史的朋友都知道，Go语言真正具备生产级成熟度是从2015年的Go 1.5版本开始的。按照技术成熟度曲线的划分，2015年之前及其后的一段时间可以视为技术萌芽期。从曲线中可以看出，2017年时达到了期望膨胀期的峰值。此后，Go经历了一段“漫长”的泡沫破裂低谷期以及稳步爬升的复苏期。从2023年开始，到2024年末，Go语言复苏的速度日益加快！目前来看，如无意外，Go将进入技术成熟度曲线的下一阶段：生产成熟期！我曾提到过：**绝大多数主流编程语言将在其诞生后的第15至第20年间大步前进**。按照这个编程语言的一般规律，刚刚[迈过开源第15个年头的Go](https://tonybai.com/2024/11/12/go-turns-15)刚刚迈进自己的黄金5-10年。

当然，单看TIOBE单一榜单似乎说服力不足，我们再来看看[今年的Github octoverse报告](https://github.blog/news-insights/octoverse/octoverse-2024/#the-most-popular-programming-languages)。在这份报告中，Go依旧稳居github热门编程语言前10(如下图)，这一位置已经保持了三年多了！

![](../../assets/2cb315d8e2bb237f.png)



此外，在2024年年中发布的“[IEEE Spectrum 2024编程语言排行榜](https://mp.weixin.qq.com/s/nLgg18iG3ZIt-ojHqPuqRA)”中，Go在Spectrum排名和Trending排名中分列第8位和第7位。

除了排行榜之外，通过Reddit中编程语言论坛的活跃度也可以看出Go语言在全球的受欢迎程度和用户广度。以下是2025年1月1日Reddit上最活跃的9门编程语言子论坛的实时状态截图：

![](../../assets/f3a57792f3c4c9f3.png)



我们看到Go子论坛在成员数量和某一时刻的在线人数上都表现良好。此外，如果你是长期关注Reddit Go论坛的Gopher，一定注意到自2024年初以来，Go论坛的人气迅速增长，日均帖子数相比前两年显著增加，其中很多都是新加入Go阵营的初学者！

注：

[Rust]的人气是真高啊，online人数断崖领先！

编程语言技术大会是衡量语言流行度和受欢迎程度的另一重要风向标。自从全球从新冠疫情中恢复后，GopherCon逐渐在各地线下恢复，到了2024年基本回到了疫情前的状态，甚至在一些地方的GopherCon还超越了以往的受欢迎程度。例如，2024年GopherCon欧洲大会破例举办了两次。此外，[首届在非洲举行的GopherCon Africa](https://dev.to/johneliud/my-experience-attending-gophercon-africa-2024-171e)也于2024年10月份在肯尼亚首都内罗毕成功举行！唯一的遗憾是**GopherChina在2024年缺席**，这或许与国内的经济形势有关。

Go的增长趋势来的有些快，不知道是否是得益于AI应用的快速发展！但就像Go团队前成员[Jaana Dogan(Rakyll)](https://github.com/rakyll)所说的那样：

![](../../assets/e0086140e9e18a39.png)


Go将成为AI时代重要的AI应用开发语言！AI大模型三强：OpenAI、Claude和Google都提供了对Go SDK的官方支持：

- OpenAI Go SDK – https://github.com/openai/openai-go
- Claude GO SDK – https://github.com/anthropics/anthropic-sdk-go
- Google AI Go SDK – https://github.com/google/generative-ai-go

此外，提到Go和AI大模型，我们不得不提及一个重量级的开源项目——[Ollama](https://ollama.com/)，它可以说是当前私有部署和使用开源大模型的事实标准！在[2024年的用户调查报告](https://go.dev/blog/survey2024-h1-results)中，Go团队还特别关注了用户对使用Go开发AI应用的需求，并将AI应用开发视为Go应用的下一个重要赛道。此外，Russ Cox也积极参与这一领域，开源了专[用于开源项目运营维护的AI机器人：Oscar](https://mp.weixin.qq.com/s/dbuR1oRavvaemUPA7uhyag)，同时探索Go在AI领域的应用。

如果说Go的排名再创新高让Gopher和Go社区对Go充满了更多自信，那么Go团队的换帅则向整个编程语言界展示了团队的传承与发展！

## 2. [Go团队换帅展示团队传承](https://mp.weixin.qq.com/s/2Sy6K_dU1j3tZZiyyfCTDQ)

对于Go团队来说，2024年的最大的事件不是[Go 1.22](https://tonybai.com/2024/02/18/some-changes-in-go-1-22)或[Go 1.23](https://tonybai.com/2024/08/19/some-changes-in-go-1-23/)的发布，而是**团队换帅**。

2024年中旬，Go团队的技术负责人Russ Cox宣布，他将于2024年9月1日起卸任Go项目的技术领导职务。自2008年参与Go项目以来，Russ于2012年成为其技术负责人。在过去的12年里，他引领Go语言从一个实验性项目成长为当今最受欢迎的编程语言之一。在他的带领下，Go凭借简洁的语法、高效的并发模型和强大的标准库赢得了众多开发者的青睐，并在云计算、微服务和DevOps等领域得到了广泛应用。

Russ分享了他卸任的想法，表示这一决定是经过深思熟虑的，是自然发展的结果。他认为，尽管长期稳定的领导对大型项目至关重要，但领导层的变动也能为项目注入新的活力和视角。他强调，定期更换领导者是非常重要的，这有助于引入新思想并防止项目陷入停滞。

接替Russ Cox的是Austin Clements，他将成为新的Go技术负责人，同时领导Google的Go团队和整个Go项目。Austin自2014年起就在Google从事与Go相关的工作，拥有丰富的经验和深厚的技术背景。同时，Cherry Mui将接手负责编译器和运行时等“Go核心”领域的工作。Cherry自2016年加入Google，在Go的核心开发领域表现出色。Russ Cox对这两位新领导给予了高度评价，称赞他们具备卓越的判断力以及对Go语言和其运行系统的广泛而深入的理解。

通过9月份到12月份的角色过期期的观察来看，两位“新负责人”的表现是中规中矩，沿袭了Russ Cox之前确定的Go项目管理框架，Cherry Mui在Go core领域表现的十分积极，这从”[Go compiler and runtime meeting notes](https://github.com/golang/go/issues/43930)“的记录中可见一斑！

在[第333期GoTime播客](https://changelog.com/gotime/333)中，两位新leader也初步分享了他们对后续Go演进的一些想法。

Austin强调，虽然Go保持着稳定和简洁，但它必须继续演进。他的首要目标之一是改善Go的可扩展性，无论是在开发过程中还是在背后的工程流程中。他希望通过提高透明度和扩大社区参与度，赋能社区，创建一个能够更好整合用户反馈的平台（可能是一个论坛），使贡献者能够开发与核心团队目标一致的工具和解决方案。在性能改进方面，Austin长期致力于优化Go的垃圾回收系统，目前正在试验一种新算法，幽默地称其为“绿茶”，旨在优化资源使用，进一步提升Go在越来越大系统上的扩展能力。

Cherry则指出，Go的用户基础正在快速增长，而核心团队的资源却有限。她的任务是确保Go平台能够支持这一日益增长的社区，无论是通过构建更好的API还是平台，帮助用户在Go的基础上开发更强大的工具和解决方案。在技术扩展性方面，Cherry也表达了自己的关注。随着计算能力的提升，核心数量和内存容量不断增加，Go需要适应，以高效处理更大的工作负载。Cherry表示，她非常期待与社区中的工程师合作，解决这些挑战，保持Go简单且可扩展的声誉。

从两位领导的想法与目标中，我们可以看到Go团队传承的文化。对于这样的“换帅”，Go社区应充满信心。

## 3. Go Release新特性一览

对于已经过了15个生日的Go来说，其演进的节奏已经非常稳定和成熟了。2024年，Go平稳地发布了两个重要版本：Go 1.22和Go 1.23。下面我们就来简单浏览一下这两个版本的主要新特性。

### 3.1 Go 1.22主要新特性

#### 语言特性

- loopvar语义修正：for循环中通过短声明定义的循环变量，由整个循环共享一个实例变为每次迭代定义一个实例。这是 Go 语言发展历史上第一次真正的填语义层面的“坑”。
- for range支持整型表达式：for range循环可以遍历整型范围，如for i := range 10。

#### 编译器和运行时

- PGO优化增强：基于PGO的构建可以实现更高比例的调用去虚拟化(devirtualize)，带来性能提升。
- 编译器优化：编译器可以更多地运用devirtualize和inline技术进行优化。
- 运行时优化：运行时可以使基于类型的垃圾收集的元数据更接近每个堆对象，从而降低CPU和内存开销。

#### 工具链

- go work支持vendor：go work命令可以管理vendor目录，并且支持使用go build -mod=vendor构建。
- go mod init改进：不再尝试导入其他vendor工具(比如Gopkg)的配置文件。
- go test -cover改进： 对于没有测试文件的包，会报告覆盖率为0.0%。

#### 标准库

- math/rand/v2: 标准库第一个V2版本包。
- 增强http.ServeMux的表达能力: 新版ServeMux支持静态路由、通配符、主机匹配和变量捕获。

### 3.2 Go 1.23 主要新特性

#### 语言特性

- 自定义函数迭代器：for range语句支持遍历用户自定义的集合类型，需要定义满足特定签名的迭代器函数。
- 别名中增加泛型参数：支持在类型别名定义中使用类型参数，如：

```
type MySlice[T any] = []T
```


#### 编译器与运行时

- PGO构建速度提升: 该版本优化后，PGO带来的编译开销显著降低。
- 限制对linkname的使用: Go 1.23禁止使用linkname指令引用标准库中未标记的内部符号。

#### 工具链

- Telemetry (遥测): go工具链程序收集性能和使用数据的系统，且支持go telemetry on|off|local命令。
- go env -changed: go env子命令增加-changed选项，可以查看当前Go环境中设置的Go环境变量值与默认值有差异的项的值。
- go mod tidy -diff: go mod tidy增加-diff选项，只打印更新信息但不做实际更新。
- go.mod中增加godebug指示符: 可以通过该指示符设置特定的GODEBUG选项。

#### 标准库

- Timer/Ticker变化: Timer和Ticker的GC不再需要Stop方法，Stop/Reset后不再接收旧值。
- structs包: 添加一个零size的类型HostLayout，用于控制编译器对结构体类型的布局方式。
- unique包: 新增了unique包，用于处理唯一值的集合。
- iter包: 新增了iter包，并增加了函数迭代器相关的实用函数到maps、slices等包中。

更多更详细关于Go新特性的内容，请阅读《[Go 1.22中值得关注的几个变化](https://tonybai.com/2024/02/18/some-changes-in-go-1-22/)》和《[Go 1.23中值得关注的几个变化](https://tonybai.com/2024/08/19/some-changes-in-go-1-23/)》。

## 4. 2025展望

按照Go演进的一贯风格，我本不该对Go抱有过多期待^_^，但还是忍不住想说几句。

[Go已经稳稳地占据了云计算领域的头部后端编程语言地位](https://tonybai.com/2024/08/17/go-the-c-language-of-the-internet-era-come-true/)，在多个编程语言排行榜上名列前茅，Go社区也在健康快速地发展。然而，机遇与风险总是并存。

虽然Go在云原生、Web服务、微服务、API和CLI开发方面拥有明显优势，但也面临着来自Rust等语言的挑战。Go需要进一步巩固其在这些优势领域的地位，同时探索一些能够发挥自身优势的新方向，例如AI应用开发等。

同时，我们期待新一代Go团队领导者，尤其是来自Go编译器和运行时组的领导者们，能够**深入打磨和优化Go语言的编译器、运行时性能以及语言互操作性**。毕竟，谁不喜欢那种因性能自然增长而带来的愉悦感，以及借助其他语言优势生态快速完成功能的灵活性呢!

最后，感谢Go团队和Go社区在Go语言演进发展上做出的贡献，希望Go越走越好！

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2024年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。同时，我们也会加强代码质量和最佳实践的分享，包括如何编写简洁、可读、可测试的Go代码。此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily
- Gopher Daily Feed订阅 – https://gopherdaily.tonybai.com/feed

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论