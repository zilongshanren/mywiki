---
title: 坚守内核，拥抱变量：我的 2025 年终复盘与 2026 展望
url: https://tonybai.com/2026/01/04/stick-to-the-core-embrace-variables-2025-review-2026-outlook/
published: '2026-01-04'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 坚守内核，拥抱变量：我的 2025 年终复盘与 2026 展望

![](../../assets/ffd64c243edf883c.png)


[本文永久链接](https://tonybai.com/2026/01/04/stick-to-the-core-embrace-variables-2025-review-2026-outlook) – https://tonybai.com/2026/01/04/stick-to-the-core-embrace-variables-2025-review-2026-outlook

大家好，我是Tony Bai。

当时钟[拨向 2026 年](https://mp.weixin.qq.com/s/6U3cnqjCve9WIn07g0Y_Og)，我不禁回望刚刚过去的 2025。

在技术史上，这注定会被定义为**“分水岭”**的一年。如果说之前我们还在观望 AI 能画出什么样的图，生成怎样的代码，那么在 2025 年，我们真切地感受到了它对软件工程核心领地的冲击与重塑——[从 Google 三巨头定义“AI Agent 元年”](https://tonybai.com/2025/12/26/google-2025-research-breakthroughs/)，到[ CodeRabbit 报告揭示 AI 代码的质量隐忧](https://tonybai.com/2025/12/28/state-of-ai-vs-human-code-generation-report/)，再到 [Rob Pike 对那封AI “致谢信”的罕见愤怒](https://tonybai.com/2025/12/27/rob-pike-outburst-denounces-ai-companies-hypocritical-thanks/)。

在这样的洪流中，保持定力并不容易。回顾这一年，我庆幸自己做对了一件事：**在变化的浪潮中，依然坚持系统性地输出“不变”的价值。**

今天，在这个2026年元旦后开工的第一天，我想和大家聊聊我的 2025，以及**我对 2026 的硬核规划**。

![](../../assets/f3973191ef9d6abe.png)


## 2025：一场“微专栏”的内容实验

2025 年，我做了一个重要的决定：**重塑公众号的内容形态**。

在碎片化阅读盛行的当下，我深感很多技术痛点——如并发调度、网络协议、系统底层——是无法通过单篇千字文章讲透的。于是，我推出了**“微专栏”**模式：**用 3-10 篇的体量，像写书一样去深度拆解一个技术专题。**

这是一次冒险，但结果令人欣慰。这一年，我们通过 16 个微专栏，构建了一张从底层原理到 AI 前沿的完整技术拼图：

**第一块拼图：攻克 Go 并发的“深水区”**

并发是 Go 的灵魂，也是最容易出错的地方。

我们通过 ** 《Go并发调度艺术》**，跟随 Dmitry Vyukov 的视角亲历了 GMP 模型的演进；通过

**，完成了从“共享内存”到“信道通信”的思维转变；更为关键的是，**

[《Go并发心智模型课》](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIyNzM0MDk0Mg==&action=getalbum&album_id=4105816518230016005#wechat_redirect)**让我们终于掌握了驯服 Flaky Test 的新武器。**

[《征服Go并发测试》](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIyNzM0MDk0Mg==&action=getalbum&album_id=4017357519222882315#wechat_redirect)**第二块拼图：夯实系统编程与工程底座**

在应用层之下，是冰山般的底层细节。

我们潜入内核，在 ** 《Go系统编程：揭秘进程控制、I/O与IPC》** 中手写系统级工具；在

**中打通了网络协议栈的任督二脉。**

[《Go网络编程全解：从Socket到HTTP/3》](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIyNzM0MDk0Mg==&action=getalbum&album_id=4199064345390874624#wechat_redirect)同时，我们补齐了工程化的关键短板：通过 ** 《Go Context解惑》** 掌握了生命周期管理，通过

**走出了依赖地狱，用**

[《Go模块构建与依赖管理》](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIyNzM0MDk0Mg==&action=getalbum&album_id=4225702928272949254#wechat_redirect)**和**

[《Go密码学101》](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIyNzM0MDk0Mg==&action=getalbum&album_id=4082448928904577033#wechat_redirect)**强化了基本功，并用**

[《用Go解锁位运算之美》](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIyNzM0MDk0Mg==&action=getalbum&album_id=4116476795552268292#wechat_redirect)**建立了交付信心。**

[《Go 测试之道》](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIyNzM0MDk0Mg==&action=getalbum&album_id=4256541133263962115#wechat_redirect)**第三块拼图：架构设计与交互体验**

当 Coding 能力溢出，设计能力便决定了上限。

我们探讨了 ** 《API 设计之道：从设计模式到 Gin 工程化实现》** 和

**，拒绝面条代码。甚至，我们还玩了一把复古与现代结合的**

[《Go开发者的数据库设计之道》](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIyNzM0MDk0Mg==&action=getalbum&album_id=4174451166274912264#wechat_redirect)**，让命令行工具也能拥有惊艳的交互。**

[《重塑终端：Go TUI开发入门课》](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIyNzM0MDk0Mg==&action=getalbum&album_id=4108702531688333316#wechat_redirect)**第四块拼图：Gopher 的 AI 破局**

这一年，我们不再旁观，而是下场实战。

从 ** 《AI应用开发第一课》** 入门，到掌握

**，再到硬核的**

[《Gemini CLI：重新定义命令行AI开发》](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIyNzM0MDk0Mg==&action=getalbum&album_id=4067128336651386882#wechat_redirect)**，我们证明了 Go 在 AI 时代的无限可能。**

[《Google ADK 实战：用 Go 构建可靠的 AI Agent》](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIyNzM0MDk0Mg==&action=getalbum&album_id=4266729696274251779#wechat_redirect)**除了微专栏，2025 年也是我“系统化输出”的大年。**

在极客时间，** 《Go语言进阶课》** 正式上线，帮助无数 Gopher 完成了从熟练到精通的跨越。

更让我惊喜的是，

**在上架短短一个多月内就获得了**

[《AI原生开发工作流实战》](http://gk.link/a/12EPd)**3600+**订阅。这说明大家已经意识到：

**AI 不仅仅是工具，更是一种全新的开发范式。**

与此同时，** 《Go语言第一课》纸质书**也在这一年正式出版，为这一年的“内容实验”画上了一个厚重的句号。

这一系列的产出证明了：**在浮躁的时代，深度、系统化的内容依然有着旺盛的生命力。**

## 2025：在喧嚣中寻找信号

翻看我 2025 年的[博客列表](https://tonybai.com/articles/)，你会发现我的关注点始终在**“底层原理”**与**“前沿变革”**之间穿梭。

**关于 Go，我们不仅向前看，也向后看。**

Go 团队在这一年对底层的打磨可谓大刀阔斧。我们见证了 GC 的重大演进，** 《Go新垃圾回收器登场：Green Tea GC》** 详细剖析了它如何通过内存感知降低 CPU 开销，

**则进一步揭示了其架构演进。在性能压榨上，**

[《深入 Go Green Tea GC》](https://tonybai.com/2025/10/31/deep-into-go-green-tea-gc/)**让我们看到了 Go 在高性能计算领域的野心，尽管**

[《解锁CPU终极性能：Go原生SIMD包预览版初探》](https://tonybai.com/2025/08/22/go-simd-package-preview/)**也提醒了我们随之而来的复杂性。**

[《连 Rob Pike 都感到“担忧”》](https://tonybai.com/2025/11/06/proposal-simd-cpu-feature-vet-check/)同时，我们也向后进行了“Go 考古”，探究了 ** 《错误处理的“语法糖”之战》**，以及

**中扩容策略的演变。我们还深入探讨了**

[《Slice 的“隐秘角落”》](https://tonybai.com/2025/10/02/go-archaeology-slice/)**中的语法糖 new(expr)，以及**

[《Go 1.26 新特性前瞻》](https://tonybai.com/2025/12/16/go-1-26-foresight/)**的语言规范修正。**

[《Go 编译器崩溃背后》](https://tonybai.com/2025/11/30/ice-assertion-failed-with-append/)**关于软件工程，我们保持清醒。**

当业界盲目推崇微服务时，我们通过 ** 《“6 个月，47 个微服务”：一场由“简历驱动”引发的架构灾难》** 发出了警示；当所有人都在由 AI 生成代码时，我们解读了

**。我们探讨了**

[《Bug 激增 1.7 倍！AI 写代码：是速度的蜜糖，还是质量的砒霜？》](https://tonybai.com/2025/12/28/state-of-ai-vs-human-code-generation-report/)**，也重温了**

[《无聊设计的终极奥义》](https://tonybai.com/2025/08/31/the-simplest-thing-that-could-possibly-work/)**。**

[《Code Review 已死？Kent Beck：当 AI 成为“副驾驶”，我们该如何审查代码？》](https://tonybai.com/2025/12/27/code-review-hell-in-ai-age/)**关于 AI，我们从旁观走向入局。**

这一年，我不再满足于仅仅介绍 AI 工具，而是开始探索 **Go 与 AI 的结合点**。从 ** 《Google I/O 2025 Go 语言进展》** 看到的 AI 赋能，到

**中 Go 在自动化 API 领域的统治力，再到**

[《Cloudflare 2025 年度报告》](https://tonybai.com/2025/12/17/cloudflare-2025-report-go-language-api-traffic-ai-surge/)**带来的基础设施变革，我们看到了 Gopher 在 AI 时代的巨大机会。**

[《MCP协议注册中心发布》](https://tonybai.com/2025/09/10/introducing-the-mcp-registry/)## 2026：Coding 廉价，眼光无价

如果说 2025 年是 AI 辅助编程进入Agent模式（Copilot、Cursor、Claude Code、Gemini cli等）的普及年，那么 2026 年，将是 **自主智能系统（Agentic System）** 的爆发年。

在 AI 能以百倍速度生成代码的时代，单纯的 Coding 能力正在不可避免地贬值。但**架构设计的能力、技术选型的眼光、以及构建复杂系统的智慧，将变得无价**。

基于此，在 2026 年，我将在**公众号（付费微专栏）**和**知识星球（免费畅读）**双线并行，重点规划以下三大战役：

### 战役一：AI 原生工程与 Agent 实战

这不再是写几个 Prompt 的游戏，而是真正软件工程范式的变革。

**自主智能系统 (Agentic System) 构建实战**：我们将深入研究如何构建真正的 AI Agent。不仅仅是调用 API，而是设计能够感知环境、规划任务、使用工具、具有记忆并能自我修正的智能系统。**以Claude Code为例的AI编码进阶实战**：作为当前最强的 AI 编码 Agent，Claude Code 的潜力远未被挖掘。我们将探索如何用它[实现L4级工作流](https://time.geekbang.org/column/article/924970)，即AI 作为自主软件工程师，能够独立地、端到端地完成从需求理解到部署上线的整个软件开发生命周期，实现端到端的自动应用构建。同时我们还要考虑AI使用的经济性(省token，省money)。**AI 时代的软件工程探索**：当代码主要由机器生成时，我们的 CI/CD、Code Review 以及测试策略该如何演进？这将是我们探索的重点。

### 战役二：架构设计与系统思维

当“怎么写”变得容易，“写什么”和“怎么设计”就决定了你的上限。

**分布式系统与架构设计微专栏**：我们将跳出语言细节，探讨高可用架构、一致性难题、分布式事务等硬核话题。**最佳实践与反模式**：从微服务拆分到单体演进，从 数据表查询性能设计到领域建模（DDD），我们将沉淀出一套经得起时间考验的工程智慧。

### 战役三：Go 语言的深耕与重塑

Go 依然是我们的基本盘，但在 2026 年，我们要换个玩法。

**AI 时代的角色转换**：Go 在 AI 基础设施（推理服务、向量检索、Agent 后端）中的核心地位愈发稳固。我们将关注 Go 如何更好地服务于 AI 负载。**硬核实战：Porting（移植）系列**：这是我今年最想做的一件事。我们将通过**用 Go 复刻经典系统**（如编写一个**Mini-Kafka**或**Mini-DB**），来深入理解存储引擎、网络协议和分布式共识的底层原理。这是掌握系统编程最扎实的路。**传统艺能**：Go 的**极致性能优化**与**可观测性**依然是很多读者的刚需，也是Go生产事件中的重中之重。我们将继续关注 Go Runtime 的演进（如 Green Tea GC、SIMD），确保我们始终站在性能的最前沿。

当然，作为系统编程的双子星之一，**Rust** 依然会在我的技术雷达范围内，作为我们拓宽技术视野的重要补充。

## 小结

2026 年的画卷已经展开。

这是一个技术人最焦虑的时代，也是最令人兴奋的时代。焦虑在于旧经验的快速折旧，兴奋在于个体生产力的无限放大。

新的一年，我希望通过这些**深度微专栏**和**知识星球的陪伴**，帮你建立起抵御技术通胀的护城河。

让我们左手握着 Go 与架构设计的**工程底气**，右手举起 AI Agent 的**效率火把**，从“代码工人”进化为“系统构建者”。

祝大家在 2026 年，代码无 Bug，架构有灵魂，人生有增量！

扫码加入我的知识星球，2026 全年微专栏以及存量微专栏免费畅读！

![img{512x368}](../../assets/46c6ee234c360d9a.jpg)


**你的 2025 关键词**

我的 2025 是“坚守与拥抱”。**回顾你的 2025，如果用一个词或一句话来总结，会是什么？对于即将到来的 2026，你最大的技术期待又是什么？**

**欢迎在评论区留下你的年度关键词，让我们一起记录这段不平凡的时光！**

**如果这篇文章给了你前行的力量，别忘了点个【赞】和【在看】，并转发给你的朋友，让我们在 2026 顶峰相见！**

还在为“复制粘贴喂AI”而烦恼？我的新专栏 **《 AI原生开发工作流实战》** 将带你：

- 告别低效，重塑开发范式
- 驾驭AI Agent(Claude Code)，实现工作流自动化
- 从“AI使用者”进化为规范驱动开发的“工作流指挥家”

扫描下方二维码，开启你的AI原生开发之旅。

![](../../assets/305ffd23f32ce780.png)


你的Go技能，是否也卡在了“熟练”到“精通”的瓶颈期？

- 想写出更地道、更健壮的Go代码，却总在细节上踩坑？
- 渴望提升软件设计能力，驾驭复杂Go项目却缺乏章法？
- 想打造生产级的Go服务，却在工程化实践中屡屡受挫？

继《[Go语言第一课](http://gk.link/a/10AVZ)》后，我的《[Go语言进阶课](http://gk.link/a/12yGY)》终于在极客时间与大家见面了！

我的全新极客时间专栏 《[Tony Bai·Go语言进阶课](http://gk.link/a/12yGY)》就是为这样的你量身打造！30+讲硬核内容，带你夯实语法认知，提升设计思维，锻造工程实践能力，更有实战项目串讲。

目标只有一个：助你完成从“Go熟练工”到“Go专家”的蜕变！ 现在就加入，让你的Go技能再上一个新台阶！

![](../../assets/32b03e4c457f472e.gif)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2026, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

请问知识星球中，可以免费阅读微专栏的内容吗？

可以的。星球里包含了所有公众号微专栏的内容，加入星球后，无需额外在公众号付费就能在星球里阅读微专栏了。 当然星球不仅包含微专栏，还有其他一些服务内容。此外，有些微专栏仅在星球发，可能不会在公众号发。