---
title: 别读代码了，看着它流过就行：ClawdBot 作者的 AI 开发工作流
url: https://tonybai.com/2026/01/28/clawdbot-author-ai-development-workflow/
published: '2026-01-28'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 别读代码了，看着它流过就行：ClawdBot 作者的 AI 开发工作流

![](../../assets/21f437e3168539bd.png)


[本文永久链接](https://tonybai.com/2026/01/28/clawdbot-author-ai-development-workflow) – https://tonybai.com/2026/01/28/clawdbot-author-ai-development-workflow

大家好，我是Tony Bai。

在过去的一年里，我们见证了 AI 编程工具的井喷。从 Copilot 到 Cursor，从 Windsurf 到 [Claude Code](http://gk.link/a/12EPd)、[Gemini CLI](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIyNzM0MDk0Mg==&action=getalbum&album_id=4067128336651386882#wechat_redirect)和Codex，每个人都在寻找那个“完美的开发助手”。

最近，爆火的个人AI助理开源项目 [ClawdBot](https://github.com/clawdbot/clawdbot) 和 [PSPDFKit](https://pspdfkit.com/) 的创始人 [Peter Steinberger](https://steipete.me/) 发布了一系列关于他AI 开发工作流的深度博文。他以一种近乎“未来主义”的视角，描述了一个令传统程序员既兴奋又恐惧的景象：


“I stopped reading code and started watching it stream by.”

（我不再读代码了，我只是看着它流过。）

这可真不是一句狂言，而是一种全新的且现实可行的**工程范式**。

当 AI 的可靠性达到临界点，软件交付的速度不再受限于人类的打字速度，而是受限于模型的**推理速度（Inference Speed）**。

今天，我们结合 Peter 的最新实践，为你拆解这套**“以人为核心、AI 为手脚”**的顶级开发工作流。

![](../../assets/e7e1e92bcbb64dd9.png)


## 质变时刻：学会了“深思熟虑”的模型+工具链的“极简回归”

根据 Peter 的观察，真正的质变发生在 GPT-5.2 这一代模型发布之后。

早期的模型（如 Claude 3.5 Sonnet），虽然聪明但急躁，往往“顾头不顾腚”。而新一代的 Codex 模型学会了**“沉默”**。

在面对一个复杂的重构任务时，模型可能会静默阅读代码长达 10 到 15 分钟，一言不发。这种“Think before Act”的特性，让它能够构建出极其完整的上下文图谱。结果就是：它能**一次性（One-shot）**搞定跨越数十个文件的大型重构，且几乎零 Bug。

这也宣告了 Plan Mode（规划模式）的消亡。以前我们需要强制 AI 先写计划再写代码，那是为了给旧模型的智商打补丁。现在，开发者可以直接与 AI 对话，像与一位资深架构师协作一样流畅。

此外，在尝试了市面上几乎所有工具（VS Code, Zed, Cursor, Gemini）之后，Peter 最终回归了一套极简的组合：

**Ghostty + Claude Code + Minimal Tooling**。

为什么？因为 **“Less is More”**。

**终端的复兴：**他抛弃了不稳定的 VS Code 终端，全面回归**Ghostty**。因为在 AI 时代，终端才是最纯粹的交互界面。**屏幕即战场：**他使用 Dell 40寸带鱼屏（3840×1620），同时平铺**4 个 Claude 实例 + Chrome**。他不需要切换窗口，他像监控仪表盘一样监控着 4 个并发任务的进展。**摒弃复杂 MCP：**他甚至反主流地删除了大部分[MCP（Model Context Protocol）](https://tonybai.com/2025/07/10/mcp-official-go-sdk/)。因为 AI 有时候会自作聪明地启动 Playwright 去抓取网页，而直接读取代码反而更快、更准、更省 Token。

Peter的这些实践告诉我们：不要被花哨的工具迷了眼。一个稳定、高性能的终端，加上一个聪明的 CLI Agent，就是最强大的武器。

## 像工厂一样生产：并行工程学

当“写代码”不再占用人类的脑力带宽时，Peter 的工作方式从“工匠”变成了**“工厂厂长”**。

### 并行处理 (Parallel Processing)

他通常同时推进 **3 到 8 个项目**。

- 窗口 1：重构后端架构；
- 窗口 2：优化前端交互；
- 窗口 3：跑全链路测试。

开发者只需要在这些 Session 之间切换，确认结果，给出下一个指令。

### 线性推进，绝不回滚 (Never Revert)

“软件开发就像登山，走错路了就绕回来，而不是读档重来。”

他几乎不再使用 git reset。如果 AI 写歪了，直接告诉它“换个思路”，它会在现有基础上自我修正。甚至连 **Plan Mode（规划模式）** 都变得不再必要，就像前面提到的，新一代模型（GPT-5.2等）学会了“深思熟虑”，能一次性搞定复杂重构。

### 跨项目“抄作业” (Cross-Referencing)

代码复用从未如此简单。他不再写 Prompt 描述需求，而是直接说：


“Look at ../vibetunnel project, and implement the same logging system here.”

AI 会自动跨目录读取代码，提炼模式，并完美适配到当前项目。

## 基础设施的重构：CLI First

为了配合这种极速开发，Peter 彻底重构了他的技术栈选择逻辑。

### 拥抱 CLI (Command Line Interface)

**“Whatever you build, start with a CLI.”**

无论做什么 App，先做 CLI 版本。因为 Agent 调用 CLI 最方便，测试 CLI 最容易。GUI 只是 CLI 的一层皮。只要内核跑通了，让 AI 套个 React 壳只是分分钟的事。

### Oracle（预言机）

当 Agent 遇到知识盲区（比如最新的 API 变动）时，它会自动调用 [Oracle](https://github.com/steipete/oracle) ——一个Peter开源实现的、联网的、专门负责爬取文档并总结答案的“元智能体”。知识获取的闭环，彻底自动化了。

### 文档驱动 (Docs-Driven)

他不再维护复杂的 Prompt 库，而是维护项目的 docs/ 目录。

想规范 AI 的行为？写一个 docs/architecture.md。

想让 AI 学会用 Vercel？在 CLAUDE.md 里加一行：logs: axiom or vercel cli。

**文档，就是 AI 的“长期记忆”和“员工手册”。**

## 给开发者的启示：核心竞争力迁移

在 Peter 的工作流中，我们看到了程序员核心竞争力的转移：

**系统设计 (System Design) 是王道：**

当前的 AI 搞不定分布式系统设计，搞不定数据库 Schema 的前瞻性规划。这些**“硬骨头”**，才是人类的领地。-
**选择 AI 友好的生态：**

**TypeScript**(Web),**Go**(CLI),**Swift**(App)，这三者是 AI 掌握得最好的。Peter 特别提到了 Go——以前他并不感冒，但后来发现 AI 写 Go 写得极好。为什么？因为 Go 简单的类型系统让 Lint 检查极快，AI 能迅速修正错误。相比之下，那些类型系统过于复杂或编译检查极其严格的语言，可能会增加 AI“一次做对”的难度，拖慢你的推理速度。 -
**自动化一切 (Automate Everything)：**

不要手动注册域名，写个 Skill 让 AI 去做。不要手动发推特，写个 CLI 让 AI 去发。为你自己，也为你的 AI 员工，构建大量的**自定义基建**。

## 小结：享受创造

有人担心 AI 会让程序员失业，但 Peter 的实录告诉我们：**这可能是程序员最好的时代。**

在这个时代，限制你产出的不再是你的手速，也不再是你对某个库的熟悉程度，而仅仅是你的**想象力**。

当你可以以**推理速度**交付软件，当你看着代码像瀑布一样流过屏幕时，编程就不再是枯燥的搬砖，而是一场纯粹的、创造性的**游戏**。

资料链接：

- https://steipete.me/posts/2025/optimal-ai-development-workflow
- https://steipete.me/posts/2025/shipping-at-inference-speed

**你的“未来工作流”**

Peter 的工作流让我们看到了未来的一角。你敢想象自己“不再读代码”的那一天吗？在你的理想中，AI 应该帮你接管哪些“脏活累活”，让你能专注于更高维度的创造？

欢迎在评论区分享你的脑洞或对未来的担忧！让我们一起定义属于自己的 AI 工作流。

如果这篇文章点燃了你对 AI 编程的全新想象，别忘了点个【赞】和【在看】，并转发给你的极客朋友，邀请他们一起见证未来！

**还在为“复制粘贴喂AI”而烦恼？**

Peter 描述的“看着代码流过”的未来并非遥不可及。我的新专栏 **《 AI原生开发工作流实战》** 将带你提前掌握这套高效范式：

**告别低效：**摒弃“聊天式编程”，重塑以文档和 CLI 为核心的开发范式。**驾驭 Agent：**深入实战**Claude Code**，像 Peter 一样构建自动化工作流。**角色进化：**从“手动写代码”进化为“规范驱动开发”的**工作流指挥家**。

扫描下方二维码，开启你的 AI 原生开发之旅。

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