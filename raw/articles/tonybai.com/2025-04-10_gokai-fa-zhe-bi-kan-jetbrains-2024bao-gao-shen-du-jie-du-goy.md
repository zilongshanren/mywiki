---
title: Go开发者必看！JetBrains 2024报告深度解读：Go语言现状、趋势与未来机遇
url: https://tonybai.com/2025/04/10/jetbrains-2024-go-report-analysis/
published: '2025-04-10'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go开发者必看！JetBrains 2024报告深度解读：Go语言现状、趋势与未来机遇

![](../../assets/9c544ea7d8c2623f.jpg)


[本文永久链接](https://tonybai.com/2025/04/10/jetbrains-2024-go-report-analysis) – https://tonybai.com/2025/04/10/jetbrains-2024-go-report-analysis

嘿，各位Gopher！

你是否也在关心Go语言的最新动态？它还在快速增长吗？薪资水平如何？未来方向在哪？

**这是我看到的关于2024年Go语言发展趋势最全面、数据最翔实的一份报告解读。** JetBrains，这家开发者们都非常熟悉的工具公司，最近发布了《[Is Golang Still Growing? Go Language Popularity Trends in 2024](https://blog.jetbrains.com/research/2025/04/is-golang-still-growing-go-language-popularity-trends-in-2024/)》的研究报告文章。如果你是Go开发者，或者正在关注Go生态，**这篇文章就是为你准备的，强烈推荐阅读！**

在深入细节之前，先为你**快速提炼报告的核心发现**，让你高效把握重点：

**Go开发者规模依旧庞大且专业：**全球专业Go开发者估算超**400万**，且持续增长。**云原生主战场地位稳固：**Web服务、云服务、IT基础设施是Go应用核心领域。**“钱景”诱人：**Go开发者薪资普遍处于**行业较高水平**。**各大榜单表现亮眼：**在TIOBE、GitHub Octoverse等多个权威榜单中，Go排名**稳定或显著上升**。**与Rust互补而非替代：**两者定位不同，常被结合使用。**未来聚焦：**持续深耕**云原生**，并在**GenAI基础设施**领域崭露头角。

## Go开发者画像：规模、角色与“钱景”

报告显示，全球使用Go的专业开发者规模可观。JetBrains估计近一年有**410万**专业人士使用Go，其中**180万**将其作为主要语言之一。[SlashData的估算则更高](https://dashboard-tool-report.cdn.prismic.io/dashboard-tool-report/ZmMmh5m069VX1jxc_-W.Kodluyoruz-Programminglanguagecommunities.pdf)，达到**470万**（包含学生和爱好者），而最新的Stack Overflow和SlashData数据推算更是达到了**580万**。

![](../../assets/9b35d5761f5773b0.jpg)


从上图中展示的开发者从事的软件类型来看：

- Web服务 (无GUI):
**744,000** - 网站:
**732,000** - 云服务:
**681,000**

![](../../assets/60e90c8a6c993b4f.jpg)


开发者角色方面(如上图)，除了大量的**软件工程师/程序员 (约160万)**外，**DevOps/基础设施工程师(约50万)**的比例也相当高，这凸显了Go在云原生基础设施和运维领域的巨大需求。

更让Gopher们关心的是薪资。报告明确指出，Go开发者是**业内薪资最高的人群之一**。美国Go开发者的平均年薪约为**$76,000**，经验丰富者甚至可达**$500,000**。

## Go的应用版图：核心场景与行业分布

Go最常见的两大用例依然是：

**API/RPC服务(75%)****命令行工具(62%)**

哪些行业在重度使用Go呢？

**科技 (超过40%):**Google, DataDog, K8s, HashiCorp, Dropbox, Salesforce, Apple…**金融服务 (13%):**Monzo, American Express, Mercado Libre…**交通与零售 (10%):**Amazon, Uber, DeliveryHero, HelloFresh…**媒体/游戏 (7%):**Netflix, Bytedance, Tencent, Reddit, Snap…

## 多维数据透视：Go在各大榜单上的表现

担心Go的热度？来看看它在各大权威榜单上的表现吧：

**JetBrains语言潜力指数:**Go排名**第4**，仅次于TypeScript, Rust, Python，显示出强大的增长潜力和用户粘性。**Stack Overflow开发者调查:**在“受喜爱和期望” (Admired and Desired) 榜单中，Go从去年的第9位**跃升至第7位**，超过了C#和Shell。**GitHub Octoverse:**稳定保持在**Top 10**编程语言之列，并且是**Top 3增长最快的语言之一**(开源项目活跃度)。**Cloudflare Radar (API客户端语言):**Go在2024年**超越Node.js**，成为自动化API请求最常用的语言，占比约**12%**(去年为8.4%)。**TIOBE指数:**Go从2023年的第13位**大幅攀升至第7位**，达到自2009年以来的最高排名！**

![](../../assets/84953c753ab2e0d9.png)



**这些数据有力地证明，Go语言不仅没有衰退，反而在多个维度上保持着强劲的势头。**

## Go vs Rust：是对手还是队友？

报告特别提到了Go与同样热门的Rust的关系。结论是：**它们更多是互补，而非直接竞争**。

**Go:**更易上手，开发效率高，非常适合云服务、微服务、API、CLI开发，强调**快速开发和可伸缩性**。**Rust:**性能极致，适用于性能密集型、底层嵌入式开发，但**复杂性更高，开发成本和时间也更高**。

许多公司会同时使用这两种语言，根据场景需求选择最合适的工具。对Rust感兴趣的Go开发者增多，并不意味着Go市场份额的下降。

## Go的未来之路：聚焦云原生与拥抱GenAI

展望未来，Go团队将继续**聚焦云原生领域**，满足其对**开发效率 (time to value)、可靠性和可伸缩性**的核心需求。

一个令人兴奋的新方向是**生成式AI (GenAI) 基础设施**。虽然Go在传统机器学习领域不如Python，但其在性能和可伸缩性上的优势，使其成为构建**AI模型服务 (model serving)**等生产级AI基础设施的理想选择。

- 主流AI平台 (OpenAI, Google AI等) 已提供
**Go SDK**。 - Go的GenAI生态正在成长，涌现出如
[Ollama](https://github.com/ollama/ollama/),[LangChain Go](https://github.com/tmc/langchaingo),[kserve](https://github.com/kserve/kserve)等工具。 **GenAI基础设施本身，就像云基础设施一样，正在越来越多地用Go编写。**

报告还提到，[Go项目领导层虽有变动](https://tonybai.com/2024/10/10/pass-torch-to-go-new-leadership-team/)（Russ Cox卸任，Austin Clements和Cherry Mui接任），但新领导层对Go的理念和目标有深刻理解，确保了项目的连续性和稳定性。[Go 1.24](https://tonybai.com/2025/02/16/some-changes-in-go-1-24/)已于2025年2月发布，未来可期。

## 总结：黄金时代，未来可期

总而言之，JetBrains这份详尽的报告描绘了一个清晰的画面：

**2024年，Go语言不仅保持了稳定发展，更在云原生领域巩固了核心地位，并在GenAI基础设施等新兴领域展现出强劲潜力。它正步入一个成熟且充满机遇的“黄金时代”**。

对于Gopher们来说，持续深耕云原生，关注Go在AI基础设施的应用，无疑是明智的选择。

那么，**你认为Go语言的下一个增长点会在哪里？你对Go的未来有什么看法？**

**欢迎在评论区留下你的真知灼见，一起交流探讨！**

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2025年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。并且，2025年将在星球首发“Gopher的AI原生应用开发第一课”、“Go陷阱与缺陷”和“Go原理课”专栏！此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格6$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

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