---
title: Rust 输了？在 AI Agent 的战场上，TypeScript 才是唯一的“神”
url: https://tonybai.com/2026/01/31/rust-vs-typescript-ai-agent-battleground-winner/
published: '2026-01-31'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Rust 输了？在 AI Agent 的战场上，TypeScript 才是唯一的“神”

![](../../assets/42fd7df731daff4e.png)


[本文永久链接](https://tonybai.com/2026/01/31/rust-vs-typescript-ai-agent-battleground-winner) – https://tonybai.com/2026/01/31/rust-vs-typescript-ai-agent-battleground-winner

大家好，我是Tony Bai。

如果把 2025 年定义为 **Coding Agent（编程智能体）** 的元年，那么刚刚开启的 2026 年，毫无疑问是 **Personal AI Agent（个人助理智能体）** 的元年。

以 [openclaw](https://github.com/openclaw/openclaw)（曾用名Clawdbot/Moltbot）为代表的开源项目，一夜之间席卷了 GitHub，让无数开发者为之疯狂。但在这一片繁荣的景象背后，作为一名敏锐的技术观察者，我发现了一个极其有趣的现象。

请环顾四周，看看那些最顶尖、最流行、体验最好的 AI Agent 项目：

- Claude Code (Anthropic 官方)：TypeScript。
- Gemini CLI (Google 官方)：TypeScript。
- openclaw(100k+ Star)：TypeScript。
[opencode](https://github.com/anomalyco/opencode/)以及配套的[oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode)：TypeScript。

再看看Go语言，虽然没有占据头把交椅，但也稳稳地守住了一席之地。[Gastown](https://tonybai.com/2026/01/25/gas-town-multi-agent-orchestration-ai-programming-revolution)、[crush](https://github.com/charmbracelet/crush) 这些专注于并发和后端服务的 Agent 或Agent编排框架，依然拥有自己的一批拥趸。

但是，那个在过去几年呼声最高、号称“内存安全、性能无敌、将重写一切”的 Rust 去哪了？

在 AI Agent 的应用层战场上，尤其是像上述这些火出圈的AI Agent项目中，Rust 几乎“失声”了。除了 OpenAI 的 **Codex** 这个孤勇者之外，我们很难在主流的开源 Agent 列表中看到 Rust 的身影。

**难道在 AI 时代的Agentic AI(智能体AI应用)阶段，Rust 输了吗？为什么被视作“玩具语言”的 TypeScript，反而成了 AI Agent的“母语”？**

今天，我们不谈信仰，只谈架构。让我们深入剖析这场语言战争背后的第一性原理。

![](../../assets/5b15b2fa46955458.png)


## 数据说话：统治 Agent 界的“TS 军团”

在下结论之前，我们先来看一组数据。

我统计了目前 GitHub Trending 上排名前 20 的 AI Agent 相关项目（排除单纯的模型推理框架，仅统计应用层 Agent），结果令人震惊：

**TypeScript / JavaScript：占比约 75%。**

这是绝对的统治地位。无论是官方的 SDK，还是社区的野生项目，TS 都是默认选项。openclaw的作者[Peter Steinberger](https://tonybai.com/2026/01/30/clawdbot-author-peter-steinberger-full-interview/)本人就是 iOS 和 C++ 出身，但他依然选择了 TS 来构建他的个人AI助理。**Python：占比约 15%。**

依靠着 LangChain 和 AutoGen 的早期积累，Python 依然有存量优势，但在构建**交互式 CLI**和**全栈应用**时，Python 的体验明显不如 TS 丝滑。**Go：占比约 8%。**

Go 凭借其单文件分发（Single Binary）和强大的并发模型，在Agent编排框架、Coding Agent，尤其是 DevOps 类的 Agent（如 K8s 运维助手）中表现亮眼。**Rust：占比 < 2%。**

除了 OpenAI 这种拥有无限工程资源的巨头敢用 Rust 重写 Codex，绝大多数独立开发者和创业公司似乎都对其敬而远之。

**这个数据说明了什么？**

说明在 Agent 这个特定的垂直领域，**开发效率（Velocity）** 已经彻底压倒了 **运行效率（Performance）**。

对于一个每秒钟只能输出 50 个 Token 的 LLM 来说，你的程序是 1ms 响应还是 10ms 响应，用户根本感觉不到区别。但你能否在 1 天内上线一个新功能，用户感知极强。

## 第一性原理：为什么是 TypeScript？

TypeScript 之所以能赢，绝不是因为运气，而是因为它在基因层面契合了 AI Agent 的特性。

### AI 的“母语”是 JSON，而 TS 是 JSON 的亲兄弟

这是最核心的原因之一。

大模型（LLM）与外部世界交互的通用协议是什么？是 **JSON**。

无论是 Tool Calling（函数调用），还是 Structured Output（结构化输出），LLM 吐出来的都是 JSON。

-
**TypeScript:**处理 JSON 是原生的。JSON.parse() 之后，直接当作对象操作。配合 TypeScript 的 Interface 定义，你可以获得极佳的类型提示，但又保留了运行时的灵活性。`// TS: 轻松处理 interface ToolCall { name: string; args: any } const call = JSON.parse(llmOutput) as ToolCall;`

-
**Rust/Go:**你需要定义严格的 Struct。如果 LLM 发疯，多返回了一个字段，或者把 int 写成了 string，你的 serde_json 或 json.Unmarshal 就会直接报错 panic。在 AI 开发中，你需要的是“宽容”，而 Rust/Go 给你的却是“严厉”。

### “Vibe Coding” 需要松弛感

openclaw 作者提到的 **Vibe Coding**，本质上是一种**“心流状态”**。我想到了一个功能，告诉 AI，AI 生成代码，我运行，成功。整个过程行云流水。

**TS 的体验：**AI 生成了一段 TS 代码，可能类型有点小问题，用了 any，但能跑。我先跑起来看看效果，以后再修类型。**It works > It is correct.****Rust 的体验：**AI 生成了一段 Rust 代码。10分钟后编译器报错：*“生命周期不匹配”、“借用检查失败”、“unwrap 可能会 panic”*。你被迫停下来，花 30 分钟和编译器搏斗。你的 Vibe（氛围）瞬间没了。

在探索性开发（Exploratory Development）阶段，Rust 的严格性变成了阻碍。

### 生态位的降维打击：全栈与浏览器

Agent 不仅仅是在终端跑。它需要操作浏览器（比如使用Playwright），需要写 Chrome 插件，需要构建 Web UI。

在这些领域，TS 是**唯一的王**。

如果你的 Agent 需要抓取网页数据，TS 有最成熟的库；如果你的 Agent 需要提供一个可视化的 Dashboard，TS 前后端通吃。

## Rust 的尴尬与反击：退守“基础设施”

那么，Rust 真的输了吗？

**从应用层来看，是的。但从基础设施层来看，Rust 依然是基石。**

我们必须看清一个分层结构：

**L0 (Infrastructure):**向量数据库 (LanceDB, Qdrant)、推理引擎 (像[Candle](https://github.com/huggingface/candle))、高性能网关。**这是 Rust 的领地。****L1 (Application):**Agent 业务逻辑、流程编排、工具调用。**这是 TypeScript 的领地。**

Rust 并没有输，它只是退到了幕后。 Rust 成了 AI 的“地基”之一，而 TS 成了 AI 的“胶水”。

Agent 本质上就是把 LLM、数据库(记忆)、API 粘合在一起的胶水层。在这个层面上，灵活的胶水（TS）永远比坚硬的水泥（Rust）好用。

## Go 的中间路线：CLI 界的“钉子户”

在这场战争中，Go 语言处于一个非常有趣的位置。它不像 TS 那么动态，也不像 Rust 那么死板。

Go 在 Agent 领域依然有一席之地，主要得益于两点：

**Single Binary (单文件分发)：**

如果你写一个 CLI Agent 分发给用户，Go 编译出来就是一个二进制文件，扔过去就能跑。TS 还需要用户装 Node.js，装依赖（npm install 地狱）。对于**openclaw**这种本地工具，其实 Go 也是一个极佳的选择（虽然作者选了 TS）。**并发模型 (Goroutine)：**

当我们需要构建**Agent Swarm (蜂群)**，比如同时启动 100 个 Agent 去爬取数据、分析情报时，Go 的 Goroutine 模型比 TS 的 Promise.all 更轻量、更可控，性能也更佳。

像 Beads 和 Gastown 这样的项目选择 Go，正是看中了它在工程化和并发上的平衡。

## 小结：语言没有优劣，只有“生态位”

Openclaw 的爆火和 Claude Code 的选择，向我们揭示了 AI 时代的一个新真理：

**在 Agent 应用层，灵活性（Flexibility）和容错性（Forgiveness）是第一生产力。**

- 如果你想快速构建一个能够“听懂人话、调用工具”的
**Agent**，请毫不犹豫地选择**TypeScript**。 - 如果你想构建一个高性能的 llm 路由网关、MCP Server 或 并发Agent编排工具，又或是Cli Agent，
**Go**是你不错的好帮手。 - 如果你想造一个新的
**向量数据库**或**推理引擎**，请拥抱**Rust**。

**不要带着旧时代的“语言鄙视链”进入新时代。**

在 AI 眼里，代码只是它实现目标的工具。它写 TS 最顺手，那 TS 就是最好的语言。

**Rust 没有输，它只是太“硬”了，不适合在这个充满幻觉和不确定性的 Agent 世界里跳舞。**

**你的“Agent 母语”**

TypeScript 的统治力看似不可动摇，但技术圈永远不缺变数。在你心目中，开发 AI Agent 的最佳语言是哪一门？你愿意为了开发效率而忍受 TypeScript 的类型体操，还是为了极致性能去啃 Rust 的硬骨头？

欢迎在评论区捍卫你的“本命语言”！让我们看看谁才是真正的 Agent 之王。

如果这篇文章颠覆了你的技术选型观，别忘了点个【赞】和【在看】，并转发给还在纠结学什么的兄弟！

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

## 评论