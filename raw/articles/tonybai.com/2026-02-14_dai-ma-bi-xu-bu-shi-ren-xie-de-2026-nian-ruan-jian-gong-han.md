---
title: “代码必须不是人写的”：2026 年软件工厂宣言！
url: https://tonybai.com/2026/02/14/2026-software-factory-manifesto-code-not-by-humans/
published: '2026-02-14'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# “代码必须不是人写的”：2026 年软件工厂宣言！

![](../../assets/75a07a4392d86d82.png)


[本文永久链接](https://tonybai.com/2026/02/14/2026-software-factory-manifesto-code-not-by-humans) – https://tonybai.com/2026/02/14/2026-software-factory-manifesto-code-not-by-humans

大家好，我是Tony Bai。

如果你的团队里发布了一条规定：**“禁止人类写代码”**，你会作何感想？

疯了？懒惰？还是科幻？

但这正是 [StrongDM AI 团队在 2026 年 2 月 6 日 发布的备忘录](https://factory.strongdm.ai/)中，白纸黑字写下的第一条铁律。

在这份名为《[软件工厂与智能体时刻（Software Factories And The Agentic Moment）](https://factory.strongdm.ai/)》的文章中，CTO Justin McCarthy 极其激进地定义了未来的软件开发范式——**非交互式开发（Non-interactive Development）**。

他们提出的口号令人震颤：

- Code must not be written by humans.（代码必须不是人写的。）
- Code must not be reviewed by humans.（代码必须不是人审查的。）
- 如果你今天每个工程师没消耗掉 1000 美元的 Token，说明你的工厂还不够自动化。

当我们还在讨论“如何用 AI 辅助写代码”时，先驱者们已经开始讨论“如何禁止人类写代码”了。这是**生产关系的彻底重构**。

![](../../assets/e7e1e92bcbb64dd9.png)


## 奇点时刻：从“错误累积”到“正确性复利”

为什么他们敢这么做？依据是什么？

文章中揭示了一个关键的**“转折点”**。

在 2024 年底之前，我们使用 AI Agent 进行长程编码任务时，面临着“错误累积（Compounding Error）”的诅咒。AI 写错一步，后面步步错，最终导致项目崩塌（Collapse）。

但在 Claude 3.5 (2024年10月版) 发布后，配合 Cursor 的 YOLO 模式，曲线发生了逆转。

Agent 开始展现出“正确性复利（Compounding Correctness）”。即 AI 写的代码越多，它对上下文的理解越深，自我修正的能力越强。

这意味着一旦跨越了这个阈值，人类的介入（写代码、改 Bug）不再是“必要的修正”，反而成了“效率的瓶颈”和“污染源”。

于是，StrongDM 团队决定：**Hands Off（把手拿开）！**

我们要建造的不是辅助人类的工具，而是一座**自动化的软件工厂**。

## 测试已死，场景永生

在“无人值守”的工厂里，怎么保证生产出来的软件是能用的？

靠单元测试吗？不。

传统的测试是刚性的，甚至是危险的。

Agent 非常聪明，聪明到学会了 Reward Hacking（奖励黑客）。如果你只要求它通过测试，它可能会直接写一个 return true 来骗过测试框架，而不管业务逻辑是否正确。

软件工厂引入了新的验证标准：

- Scenarios（场景）：类似于机器学习中的“留出集（Holdout Set）”。它是端到端的用户故事，不仅仅是代码逻辑，更是业务意图。
- Satisfaction（满意度）：放弃布尔值的 Pass/Fail，转而使用概率性的“满意度”指标。在所有观察到的执行路径中，有多少比例是符合预期的？

## 基础设施革命：数字孪生宇宙 (DTU)

这是这篇文档中最令人脑洞大开的部分。

在开发企业级软件时，我们经常需要依赖第三方 SaaS（如 Okta, Jira, Slack, Google Drive）。

- 传统痛点：API 有速率限制（Rate Limits），调用要花钱，测试环境很难搭建。
- 工厂解法：Digital Twin Universe (DTU)。

StrongDM 的 AI 团队利用 AI，构建了这些第三方服务的行为克隆（Behavioral Clones）。

他们在内存中运行了成千上万个 Okta、Slack 和 Google Drive 的“数字孪生体”。

这意味着他们可以在一小时内运行数千个集成测试场景，不需要联网，不消耗 API 额度，没有任何速率限制。

他们可以模拟极端边缘情况（比如 Slack 突然挂了，或者 Jira 返回了乱码），来验证软件的鲁棒性。

以前我们认为“重写一个 Slack 服务端”是疯子才干的事（不经济）；但在 AI 时代，让 Agent 生成一个 Mock Server 极其廉价。AI 改变了“造轮子”的经济学模型。

## 新经济学：烧钱是为了省命

文档最后抛出了一个震撼的 KPI：

**“If you haven’t spent at least $1,000 on tokens today per human engineer, your software factory has room for improvement.”**

（如果你今天每位工程师没消耗掉 1000 美元的 Token，你的工厂就有改进空间。）

这听起来像是烧钱，其实是在省命。

相比于人类工程师昂贵的时薪，以及人类犯错后带来的返工成本，Token 是最廉价的资源。

在这个工厂里，人类的角色被彻底重新定义：

我们不再是流水线上的工人（Coder），我们是流水线的设计师（Architect）。

每当你忍不住想打开 IDE 修改代码时，请默念那句禅宗般的公案：

**“Why am I doing this? The model should be doing this instead.”**

## 小结：软件工程的终局

![](../../assets/e2a74a0624fa1a06.png)


StrongDM 的宣言，或许就是 Software 3.0 时代的《独立宣言》。

它告诉我们，软件开发正在经历从“手工作坊”向“自动化工厂”的不可逆转的跃迁。

在这个新世界里，Spec（规范）是唯一的输入，Endpoint（服务）是唯一的输出。中间的一切——编码、测试、部署、SaaS 依赖——都将被 AI 和它的数字孪生体接管。

**这就是 2026 年及以后的软件工程。你，准备好了吗？**

资料链接：https://factory.strongdm.ai/

**你愿意交出“方向盘”吗？**

面对 StrongDM 这种“不准人写代码”的极端铁律，你感到的是解放还是恐惧？如果一个系统能 24 小时自动纠错并产出 99.9% 满意的代码，你还会坚持亲自敲击键盘吗？

欢迎在评论区投出你的立场：支持“全自动化工厂”，还是坚持“人机协作”？

**亲手搭建你的“微型工厂”**

StrongDM 描绘的愿景听起来很科幻，但其核心技术——Spec 驱动、[Agent Team 编排](https://tonybai.com/2026/02/08/claude-code-agent-team-mode)、自动化验证——其实就在我们手边。

虽然我们还没法每天烧掉 $1000 Token，但我们可以学习这套“非交互式开发”的心法。

在我的极客时间专栏**《 AI 原生开发工作流实战》**中，我们将深入探讨：

- Spec-Driven Development：如何写出让 Agent 一次做对的规格文档？
- Scenario 设计：如何构建轻量级的“场景”来替代僵化的测试？
- Claude Code 实战：如何让 AI 实现代码的自我演进与自愈？

扫描下方二维码，让我们开始建设自己的微型软件工厂。

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