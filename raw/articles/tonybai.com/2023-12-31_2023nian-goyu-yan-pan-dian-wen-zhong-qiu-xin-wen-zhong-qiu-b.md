---
title: 2023年Go语言盘点：稳中求新，稳中求变
url: https://tonybai.com/2023/12/31/the-2023-review-of-go-programming-language/
published: '2023-12-31'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 2023年Go语言盘点：稳中求新，稳中求变

![](../../assets/11ad4ea8d87bd298.png)


[本文永久链接](https://tonybai.com/2023/12/31/the-2023-review-of-go-programming-language) – https://tonybai.com/2023/12/31/the-2023-review-of-go-programming-language

时光荏苒，转眼间已经是2023年的最后一天了。《[2022年Go语言盘点：泛型落地，无趣很好，稳定为王](https://tonybai.com/2022/12/29/the-2022-review-of-go-programming-language)》仿佛就写在昨天。

回首这一年，全球彻底从新冠大流行中得以复苏，Go语言也不例外，最直观的表现就是**全球各地的GopherCon技术大会或小型Meetup都纷纷从停办/线上的状态来到了线下**，并获得Gopher们的热烈欢迎和踊跃参与，比如下图中的[GopherCon](https://www.gophercon.com/)、[GopherCon UK](https://www.gophercon.co.uk/)、[GopherCon Europe](https://gophercon.eu/)、[GopherCon Australia](https://gophercon.com.au/)、[Golab](https://golab.io/)等。

![](../../assets/fa2abb142785004b.png)


尤其值得一提的是我们本土最大的Gopher技术大会[GopherChina 2023](https://mp.weixin.qq.com/s?__biz=MzIyNzM0MDk0Mg==&mid=2247494867&idx=1&sn=9bf0dfa3ef48867da891aac4359a0c5e&chksm=e8600b32df178224428d5ee27fd11e379011afc0bdb7e0445617275c4c43c484f72200b585dc#rd)，今年为了满足不同地域Gopher的需求，GoCN社区在6月和11月分别在北京和上海举办了两次GopherChina大会，这也是历史首次。

Go语言团队的大神们也开始重新“乐此不疲”地参与到上述这些大会中，以推进全球Go社区与生态的建设。就连已经退居二线的[Go语言之父Rob Pike](https://tonybai.com/2023/12/11/simplicity/)也亲自“现身说法”，在年底的GopherCon Australia 2023上发表了“What We Got Right, What We Got Wrong”的主题演讲来回顾Go诞生以来的得与失。

大神回顾一生，我们盘点一年。在这篇文章中，我就和大家一起聊聊Go在2023年的状态、所处的位置以及Go未来演进的机制与策略。

## 1. Go的2023

### 1.1 稳

一如往年，Go在2023年发布了两个大版本，分别是2023年2月份的[Go 1.20](https://tonybai.com/2023/02/08/some-changes-in-go-1-20/)和8月份的[Go 1.21](https://tonybai.com/2023/08/20/some-changes-in-go-1-21)。

在这两个版本中，Go语法特性一如既往的求稳，除了支持**切片类型到数组类型(或数组类型的指针)的类型转换**，其余更是像语法的修修补补，比如：comparable“放宽”了对泛型实参的限制、unsafe包继续添加“语法糖”、增加min、max和clear预定义函数、增强type inference能力等。

这些并不会让Gopher感到“意外”，因为这与[Russ Cox在2022年宣称的“Go is boring”](https://tonybai.com/2022/12/29/the-2022-review-of-go-programming-language)的精神是一脉相承的。

不过，除了Go语法特性变化方面的“寡淡”之外，Go在其他方面还是求新和求变的，接下来我们先来看看Go是如何求新的。

注：求新与求变可能存在交集的地方，边界可能也有一定模糊性，也存在相互促进的情况，希望大家阅读下面内容时不要吹毛求疵:)。


### 1.2 求新

Go在语法特性求稳的同时，在编译器、工具链、运行时以及标准库等方面都在努力优化和打磨，旨在进一步提升Go兼具的生产力与运行时效率，其中很多优化和打磨的措施不乏新颖。

[Go 1.20版本中首次引入的PGO(profile-guided optimization)技术预览版](https://go.dev/blog/pgo-preview)，到Go 1.21版本变为默认开启，Go官方给出的PGO优化的效果数据是：PGO优化带来的性能提升一般是2%~7%，而在[最新的Go 1.22rc1](https://tonybai.com/2023/12/25/go-1-22-foresight)中，这个数字已经变为2%~14%了。

在内存管理方面，[Go 1.20引入了试验特性arena包](https://github.com/golang/go/issues/51317)，虽然它没能在Go 1.21中按时转正，如今处于proposal-hold状态，但这也算是一次在内存管理机制上的求新。

Go是一门面向软件工程的编程语言，在这一年中，Go在软件工程领域的求新例子也是不少。比如：可用于大幅简化Go项目创建的[gonew](https://tonybai.com/2023/08/11/introduction-to-the-gonew-tool)工具，它支持基于go project template clone并创建一个属于你的Go项目；再比如[对应用执行时的代码覆盖率的采集](https://go.dev/blog/integration-test-coverage)，可以帮助开发者更进一步了解最终可执行程序代码执行路径上的测试覆盖情况；而[govulncheck工具](https://tonybai.com/2022/09/10/an-intro-of-govulncheck)则是Go在软件工程与[供应链安全](https://tonybai.com/2022/03/14/software-supply-chain-security-in-go)领域的求新尝试，该工具丰富了我们对Go项目进行安全漏洞检查的手段。

注：关于供应链安全问题，Russ Cox近期有一个专门的Talk：

[Open Source Supply Chain Security at Google]，感兴趣的童鞋可以学习一下。

Go始终对IT界出现的新技术、新趋势以及Go社区的新想法保持open。在WASM出现早期，[Go就提供了对wasm的porting支持](https://tonybai.com/2018/11/19/some-changes-in-go-1-11/)，如今在Go 1.21中，Go还对尚未形成最终规范的[WASI(WebAssembly System Interface)](https://go.dev/blog/wasi)提供了支持。

Go社区的反馈也是Go团队求新的来源，比如一个典型例子就是[log/slog加入标准库](https://tonybai.com/2023/09/01/slog-a-new-choice-for-logging-in-go)，让Go标准库原生支持了结构化日志输出，且日志性能不输[像zap这样的第三方开源log包](https://tonybai.com/2021/07/14/uber-zap-advanced-usage)。

Go社区也跟随Go团队的节奏，走在求新的道路上。2023年，IT界最大的事件就是**以ChatGPT为代表的大语言模型的横空出世**，这很可能是一个百年不遇的、对人类文明进步有着重要里程碑意义的事件。各行各业，言必称大模型，言必称AI。在传统机器学习、深度学习以及[神经网络](https://tonybai.com/2023/05/21/go-and-nn-part1-tensor-operations)方面生态并不丰富的Go，也在尝试与大模型对接，比如：支持快速在本地启动和运行llama2、mistral 7B、codellama、vicuna等大模型的[ollama开源项目](https://github.com/jmorganca/ollama)在短短几个月就收获近30k个小星星的关注；再比如Gemini大模型推出后，Google一并开源了支持与Google各种大模型项目对接的[Google AI Go SDK开源项目](https://github.com/google/generative-ai-go)，并提供了详细的教程[指导Gopher如何通过该SDK与大模型交互](https://ai.google.dev/tutorials/go_quickstart?hl=zh-cn)。

注：Google把Gemini Pro的API免费提供给个人用户了，该模型具备GPT 3.5 级别的能力，32k 上下文，38 种语言支持以及多模态支持，唯一的约束是每分钟60个请求。


在[2023年第二次Go用户调查报告](https://go.dev/blog/survey2023-h2-results)中，Go 开发者表示，他们对改善其编写代码的质量、可靠性和性能的人工智能/机器学习工具感兴趣，而不是编写代码的工具。一位时刻警醒、从不忙碌的专家“审阅者”可能是一种更有帮助的AI开发者辅助形式。Go官方表示了对该调查结果的重视，也许在后续的Go工具链中“AI加持”会成为常态。

### 1.3 求变

2023年8月，在Go 1.21版本刚刚发布后，Go官博就发布了Russ Cox编写的两篇文章：《[Backward Compatibility, Go 1.21, and Go 2](https://go.dev/blog/compat)》和《[Forward Compatibility and Toolchain Management in Go 1.21](https://go.dev/blog/toolchain)》，进一步明确了Go承诺的向后兼容的范围和方案，并[第一次阐述了向前兼容性的具体方案](https://tonybai.com/2023/09/10/understand-go-forward-compatibility-and-toolchain-rule/)，这两篇文章为Go语言后续的“求变”奠定了理论基础。

在向后兼容方面，从Go 1.21开始Russ Cox提出一些举措，比如：Go将扩展和规范化了GODEBUG的使用，其大致思路如下：

- 对于每个在Go1兼容性承诺范围内的且可能会破坏(break)现有代码的新特性/新改变(比如：panic(nil)语义的改变)加入时，Go会向GODEBUG设置

中添加一个新选项(比如GODEBUG=panicnil=1)，以保留采用原语义进行编译的兼容能力； - GODEBUG中新增的选项将至少保留两年(4个Go release版本)，对于一些影响重大的GODEBUG选项(比如http2client和http2server)，保留的时间可能更长，甚至一直保留；
- GODEBUG的选项设置与go.mod的go version是匹配的。例如，即便你现在的工具链是Go 1.21，如果go.mod中的go version为1.20，那么GODEBUG控制的新特性语义将不起作用，依旧保持Go 1.20时的行为。除非你将go.mod中的go version升级为go 1.21.0；
- 在Go 1.21及以后版本中，除了可以使用像GODEBUG=panicnil=1的环境变量恢复原先语义外，还可以在main包中使用//go:debug指示符。

在向前兼容方面，Russ Cox提出的方案有些复杂难懂，这里就不赘述了，感兴趣的童鞋可以阅读一下我之前的文章《[聊聊Go语言的向前兼容性和toolchain规则](https://tonybai.com/2023/09/10/understand-go-forward-compatibility-and-toolchain-rule/)》了解更多细节。

#### 1.3.1 语法填坑

在Go的诸多“求变”中，影响最大的还是对已有语法坑的“修正”，这些“填坑”工作或多或少都会对存量代码带去影响，甚至是break change，Go社区的反对声音也是不少。但无论怎样，这些工作已经在Go 1.21版本拉开帷幕了。比如：改变panic(nil)的语义以及对[循环变量语义的变更](https://go.dev/blog/loopvar-preview)，大家可以在《[Go 1.21中值得关注的几个变化](https://tonybai.com/2023/08/20/some-changes-in-go-1-21/)》一文中了解更多细节。

对现有语法坑的修正也进一步促进了“求新”，比如在修正loopvar语义的同时，for range支持对更多类型表达式的迭代也在进行中，比如Go 1.22中，[for range将支持迭代整型表达式](https://tonybai.com/2023/12/25/go-1-22-foresight/)，并以试验特性提供了对函数迭代器的支持。

#### 1.3.2 标准库v2示范

Go号称是“自带电池”的语言，其高质量的标准库得到了广大Gopher的欢迎。Go团队也一直努力推进Go标准库功能的丰富性，比如：Go 1.22中对http.ServeMux功能进行了增强，使其像第三方的gorilla/mux那样增加对带有通配符路由的匹配。

[Go 1.22中，标准库还首次出现了v2版本包：math/rand/v2](https://tonybai.com/2023/12/25/go-1-22-foresight/)，这为后续标准库的vN方式演进提供了示范，从Go团队的官方issue、discussion中了解到，后续如sync/v2、encoding/json/v2等已经列上日程了。

## 2. Go所处的位置

很多人关注Go当前的状态：国内大厂用的多么？小厂是不是也在广泛采纳。这些问题我在往年的Go语言盘点时也都做过梳理，今年就不再提了。没有哪个大厂在广泛采用一门语言后，会在一年内全部推翻重写的；小厂对Go的采纳也是有惯性的。

今年先从我的两个意外“收获”开始。

### 2.1 两个意外的“收获”

2023年10月中旬，世界知名电动车厂商Tesla发布了[新版fleet API](https://developer.tesla.com/docs/fleet-api)和[vehicle command SDK](https://github.com/teslamotors/vehicle-command)，鉴于本人也在智能网联汽车行业内打拼，于是对Tesla的此次发布做了一些深入了解。在Tesla的github主页上我赫然发现：Go是目前Tesla开源项目的第二大语言。

![](../../assets/c654ae3faa0c597f.png)


相对于传统的主机厂(车厂)，Telsa算是比较开放的了。开放包含两个含义，一是将车端能力的开放，二是项目的开源。就目前了解到，国内主机厂还鲜有将车端能力开放出来的，开源就更是鲜见。但Tesla在这两方面都做到了，既开放了车端API，又做了针对性的开源，虽然目前其开源项目并不多。以前Tesla涉及到云端服务的项目多用[Ruby]，但从2022年开始，Go语言的使用逐渐增多，包括前面提到的Fleet API的[Fleet Telemetry的参考server实现](https://github.com/teslamotors/fleet-telemetry)以及[Tesla车辆远控SDK](https://github.com/teslamotors/vehicle-command)。

我们再来看看Apache基金会。众所周知，Apache基金会的开源项目多以Java语言为主，但一次偶然的机会翻看Apache基金会的github项目主页，我发现Go语言在Apache开源项目中已经悄悄地跻身到第五名，如果仅算后端语言的话，Go排名第三，仅次于Java和Python。

![](../../assets/a2cd9728351a8664.png)


并且，Apache基金会下面的Go项目实际也不少，大家可以通过https://github.com/orgs/apache/repositories?language=go&type=all查询。其中还不乏优秀之作，比如：[构建Q&A知识系统的answer](https://github.com/apache/incubator-answer)、[Apache Dubbo的go实现dubbo-go](https://github.com/apache/dubbo-go)、[CDN实现trafficcontrol](https://github.com/apache/trafficcontrol)、[Kubernetes原生的轻量级企业应用集成框架Camel K](https://github.com/apache/camel-k)、[Apache Arrow的Go实现](https://tonybai.com/2023/06/25/a-guide-of-using-apache-arrow-for-gopher-part1)以及[针对开发过程的聚合数据平台devlake](https://github.com/apache/incubator-devlake)等。

我们知道：Apache项目在企业级应用和平台方面具有广泛的应用，从Go语言在Apache基金会项目中的使用比例的提升现象来看，Go在企业应用市场中的普及度和受欢迎程度确实有所增长。

### 2.2 Go语言排名

编程语言之间的竞争与争议，通常被称为“编程语言战争”(programming language war)，它其实反映了不同技术群体和范式之间的碰撞。这些“火药味”比较浓的语言之争通常比较主观。近10年来，业界出现了一些被广泛接受的编程语言排行榜，它们基于一些相对客观的数据来反映不同编程语言在现实开发中的真实状态。但不同编程语言排行榜都有不同的数据来源和数据模型，单一的排行榜往往是“盲人摸象”，无法反映全貌。但目前又没有一个可以让我们一窥全貌的权威排行榜。因此，要想更客观地、更全面的反映一门编程语言的实际情况，我们需要将多个排行榜参照着看。

下面我们就来看看在目前世界上著名的编程语言排行榜上，Go语言在其中的最新排名情况(请注意：各个榜单的发布时间不同，导致各榜单的数据会有一定时间差)。

#### 2.2.1 [PYPL编程语言排行榜](https://pypl.github.io/PYPL.html)

PYPL编程语言流行指数是通过分析语言教程在谷歌上的搜索频率而创建的。语言教程被搜索的次数越多，说明该语言越受欢迎，原始数据来自Google Trends：

![](../../assets/3e56d35fe179114d.png)



#### 2.2.2 [IEEE Spectrum排行榜](https://spectrum.ieee.org/the-top-programming-languages-2023)

IEEE Spectrum排行榜是通过调查来自全球软件工程师和招聘网站的数据，统计各语言的流行度的：

![](../../assets/65c2b7aac2f12127.png)



#### 2.2.3 [RedMonk编程语言排行榜](https://redmonk.com/sogrady/2023/05/16/language-rankings-1-23/)

RedMonk排行榜是根据GitHub和Stack Overflow这两个开发者社区上的讨论数量来推算语言的受关注度。

![](../../assets/f08de9f8c50e8b1b.png)



#### 2.3.4 [Github Octoverse](https://github.blog/2023-11-08-the-state-of-open-source-and-ai/)

GitHub Octoverse排行榜直观反映了过去一年GitHub上各编程语言的实际使用和流行趋势，是从开源项目量的维度来衡量编程语言活跃度的。在Top 10语言榜单上，2023年Go超越Ruby第一次跻身Github Top10语言：

![](../../assets/0783952f42571023.png)



![](../../assets/884225f33998c864.png)



Github Language Stats是一个个人项目，它基于github公开数据，按时间、pr数量、star数量等维度对各个语言在github上的使用情况进行分析：

![](../../assets/ce3e74381ccd49cb.png)



![](../../assets/56a328722c2d5c32.png)



#### 2.3.6 [TIOBE编程语言排行榜](https://www.tiobe.com/tiobe-index/)

TIOBE编程语言排行榜理论上来说，是世界上最知名的编程语言排行榜，它根据各大搜索引擎编程语言相关的搜索查询量来计算一个综合指数。但这些年TIOBE榜单数据的“上蹿下跳”，让开发者对该榜单是“又爱又恨”。下面是TIOBE index 2023年12月份的榜单：

![](https://tonybai.com/wp-content/uploads/the-2023-review-of-go-programming-language-12.png)


当你看到Fortran排在Go的前面，你就get到该榜单的抽风式的“不靠谱”了:)。

综合上述6个榜单，我们可以看到Go语言的2023基本处于稳定发展状态，没有“大踏步”的前进，也没有意想不到的大幅退步。

今年在国内某乎上总有一些有关“Go在国内是否已凉”的话题，从上面实际情况来看，话题中那些抹黑Go的观点可以不攻自破了。有人会说Rust的强势上升对Go会有一定冲击，这的确不可否认，就像Go当年火速蹿升给Java带去一定冲击一样，这是一门编程语言在演进阶段必会经历的过程，没有什么值得大惊小怪的。5年后，Rust可能同样也会受到来自其他语言的冲击。

Go语言未来会变得如何，关键还要看Go团队对Go未来演进方向的把握是否得当以及Go社区与生态是否给力。2023年，Go团队也明确了未来的演进机制和策略，接下来我们就来看看。

## 3. Go的未来演进

2023年是[Go语言开源的第14个年头](https://tonybai.com/2023/11/11/go-opensource-14-years/)，Go语言早已蜕下了少年期的青涩，进入到了青年期。这意味着它拥有了越来越成熟稳定的语言特性，同时生态系统也日益丰富完善。作为一门青壮年语言，Go语言在系统设计方面展现出的高度工程化思想，使其轻松应对复杂系统的构建。以go module为主的模块化支持帮助大规模程序更加清晰化，丰富的并发控制手段使其可以处理海量请求。与此同时，Go语言生态也在蓬勃成长——各种高质量框架应运而生，无数module可复用，大量的云原生组件可供选择。这为开发者极大减轻了从零开始搭建系统的工作量。

和我们人类一样，一门语言进入青年期后的成熟特征并不能完全掩饰其未来演进的迷茫！在Ken Thompson、Rob Pike相继退休后，Russ Cox成为了Go这艘大船的“掌舵者”，Russ Cox与Go团队对编程语言的思考，对Go语言价值观的判断将直接决定Go未来的航向。

好在，在2023年的GopherCon大会上，我们得到了Russ Cox的答案：那就是[基于共同目标和数据驱动的决策](https://tonybai.com/2023/12/10/go-changes/)。这里借用Russ Cox在演讲中给出的结论来看看具体的演进驱动机制：

- 首先，Go需要不断变化，特别是随着计算世界的变化。
- 其次，任何改变的目标都是为了使Go在软件工程中变得更好，尤其是在规模化(scaling)方面。
- 第三，一旦我们确定了目标，达成共识的下一个最重要的部分是拥有共享数据来做出决策。
- 第四，Go工具链遥测是增补我们现有调查和代码分析数据的重要数据来源。

综上来看，Go团队要“拥抱变化”，但不能“无头苍蝇”一样的胡乱改变，而是严谨地基于广泛的数据反馈，包括来自用户调查、vscode插件运行的用户反馈、全年进行的研究访谈和用户体验研究等，以及来自即将[加入Go工具链的可选遥测(opt-in Telemetry)功能](https://research.swtch.com/telemetry)获取到的更多真实的Go使用数据。

相信在Go工具链的可选遥测(opt-in Telemetry)功能加入后，Go团队能基于这些用户数据拿到更准确地决策依据，继续让Go这艘大船行驶在正确、光明的航向上！

## 4. 小结

在2023年，Go语言继续保持了其稳定性和可靠性的特点。发布了两个大版本，Go 1.20和Go 1.21，其中语法特性的改变相对较少，注重修复和优化。然而，Go语言在其他方面仍然保持着求新和求变的态势。

Go语言团队致力于优化编译器、工具链、运行时和标准库，以提升生产力和运行时效率。引入了一些新的特性和优化措施，例如PGO（profile-guided optimization）技术的引入和优化、内存管理方面的改进等。同时，Go语言在软件工程领域也进行了一些创新，如简化项目创建的gonew工具、代码覆盖率的采集工具、供应链安全领域的govulncheck工具等。

Go语言始终保持对新技术、新趋势和社区的开放姿态。在2023年，Go语言对WASM和WASI的支持得到了进一步加强。同时，Go社区也积极响应并跟随Go团队的步伐，面对IT界出现的大语言模型等新兴技术，Go社区也在不断探索和应用。

总体而言，2023年对于Go语言来说是一个稳中求新、稳中求变的年份。Go语言保持着其简洁、高效和易用的特点，同时积极适应和采纳新的技术和需求，为开发者提供更好的开发体验和工具支持。

展望未来，Go团队已经明确了更加以共识和用户数据为驱动的演进机制，保证Go的发展方向与实际需求保持同步。随着可选的工具链遥测功能加入，相信他们能基于更丰富的用户数据做出更正确、更具预见性的正确决策。

我个人依旧坚持我之前的判断：**Go将进入或已处于自己的黄金5-10年**。

[“Gopher部落”知识星球](https://public.zsxq.com/groups/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

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

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论