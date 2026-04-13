---
title: 你的 CLAUDE.md 写错了：为什么指令越多，AI 越笨？
url: https://tonybai.com/2026/01/29/write-a-good-claude-md/
published: '2026-01-29'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 你的 CLAUDE.md 写错了：为什么指令越多，AI 越笨？

![](../../assets/484595a43bd20d44.png)


[本文永久链接](https://tonybai.com/2026/01/29/write-a-good-claude-md) – https://tonybai.com/2026/01/29/write-a-good-claude-md

大家好，我是Tony Bai。

在使用 Claude Code、Cursor 或 Gemini Cli 等 AI 编程工具时，你是否遇到过这样的情况：

明明在项目根目录写了 CLAUDE.md（或 AGENTS.md），洋洋洒洒列了几十条项目规范：*“使用 TypeScript”、“不要用 any”、“单元测试覆盖率要达标”*……

但 AI 就像个叛逆的实习生，经常对这些指令视而不见，反复犯同样的低级错误。

是你写的 Prompt 不够严厉吗？还是模型不够聪明？

最近，HumanLayer 团队发布的一篇[深度分析文章](https://www.humanlayer.dev/blog/writing-a-good-claude-md)揭示了真相：

**问题恰恰在于你写得太多了。**

Claude Code 的内部机制会给模型注入一条系统级提醒：


“IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant.”

（重要：此上下文可能与您的任务无关。除非高度相关，否则请忽略。）

这意味着，你的 CLAUDE.md 越臃肿，包含的无关信息越多，它被系统判定为“噪音”并整体忽略的概率就越大。

今天，我们来聊聊如何用工程化的思维，重构你的 AI 上下文管理。

![](../../assets/e7e1e92bcbb64dd9.png)


## 第一性原理：AI 是无状态的“新员工”

要写好 CLAUDE.md，首先要理解 LLM 的本质：**它是无状态的（Stateless）**。

每次你开启一个新的 Session，对于 AI 来说，都是**入职第一天**。它对你的代码库一无所知。CLAUDE.md 是它唯一的“入职手册”和“长期记忆”。

但这并不意味着你要把公司历史全塞给它。一个优秀的入职手册应该包含什么？

HumanLayer 的文章中 总结了 **“The Trinity”（三要素）**：

**WHAT（地图）：**技术栈是什么？项目结构是怎样的？（特别是 Monorepo，告诉它哪里是 App，哪里是 Lib）。**WHY（目标）：**这个项目的核心价值是什么？核心模块的职责边界在哪里？**HOW（工具）：**怎么构建？怎么跑测试？用 npm 还是 bun？

除此之外的任何废话，都是在消耗 AI 宝贵的注意力。

## 最佳实践一：少即是多 (Less is More)

研究表明，即便是最前沿的推理模型（Thinking Models），能稳定遵循的指令上限也就在 **150-200 条**左右。而小模型（如 Haiku 或 GPT-4o-mini）的遵循能力随着指令数量增加呈**指数级下降**。

更糟糕的是 **“位置偏见（Position Bias）”**。LLM 高度关注开头（System Prompt）和结尾（最新对话），夹在中间的 CLAUDE.md 如果过长，极易沦为“被遗忘的中间层”。

因此，请遵循以下黄金法则：

- 不要试图涵盖所有边缘情况。
- 将根目录的 CLAUDE.md 控制在
**300 行以内**，HumanLayer 的生产环境甚至控制在**60 行以内**。 - 每一行都要问自己：
*“如果没有这句话，AI 真的干不了活吗？”*

## 最佳实践二：渐进式披露 (Progressive Disclosure)

如果你确实有很多规范要交代，怎么办？

答案是：**不要把所有鸡蛋放在一个篮子里。**

想象一下，HR 会在入职第一天把 500 页的《数据库运维手册》扔给一个前端开发吗？不会。

你需要构建一套**“渐进式”**的文档体系：

**1. 建立文档库：**

在项目中创建一个 .ai/docs/ 目录，存放特定领域的指南：

- testing.md：详细的测试编写与运行指南。
- database.md：Schema 定义与迁移规范。
- architecture.md：核心架构图与数据流。

**2. 建立索引：**

在主 CLAUDE.md 中，只保留“触发器”：


“编写或运行测试前，请务必阅读 .ai/docs/testing.md。”“涉及数据库变更时，请参考 .ai/docs/database.md。”

这样，当 AI 只是在写一个前端组件时，它的上下文窗口就不会被无关的后端 Schema 污染。保持注意力的纯净，是提升 AI 智商的关键。

## 最佳实践三：别把 AI 当 Linter 用

这是最常见的资源浪费：在 CLAUDE.md 里写了 50 行关于代码风格的规定——*“缩进用 2 个空格”、“花括号不换行”、“变量名用驼峰”*……

**请记住：LLM 是昂贵的推理引擎，不是廉价的格式化工具。**

让 AI 去关注缩进，就像让法拉利去送外卖，既贵又慢。而且，AI 即使知道规则，也经常因为概率性生成而“手滑”。

**正确的解法是：Tooling > Prompting。**

**配置工具：**使用 Prettier, Biome, ESLint, govet 等确定性工具来处理格式。**设置 Hook：**配置 Claude Code 的 Stop Hook。如果 AI 生成的代码格式不对，让 Linter 报错，把错误信息喂回给 AI。*AI: (生成代码)**System: “Lint Error: Missing semicolon.”**AI: “Ah, fixing it.”*


AI 极其擅长**修复报错**，但并不擅长凭空遵守**“隐形的规则”**。

## 小结：杠杆的层级

在 AI 原生开发中，CLAUDE.md 处于**“杠杆层级”**的顶端。

- 写错一行代码 = 1 个 Bug。
- 写错一行 CLAUDE.md =
**成百上千次错误的规划、错误的检索、错误的代码。**

不要盲目依赖 /init 自动生成的文件，那只是个起点。你需要像维护核心代码一样，精心雕琢你的 CLAUDE.md。

现在，打开你的项目，检查一下那个文件。

删掉那些废话，把长文档拆分，把格式化交给工具。

**给你的数字员工减负，它才能跑得更快。**

资料链接：https://www.humanlayer.dev/blog/writing-a-good-claude-md

**你的 CLAUDE.md 有几行？**

读完这篇文章，不妨现在就去检查一下你项目里的 CLAUDE.md。它是清爽的“入职手册”，还是臃肿的“裹脚布”？你目前的行数是多少？

欢迎在评论区晒出你的“瘦身”成果！让我们一起给 AI 减负。

如果这篇文章帮你解决了 AI “不听话”的难题，别忘了点个【赞】和【在看】，并转发给你的团队，规范大家的 Prompt 工程！

**构建工程化的 AI 工作流**

CLAUDE.md 只是构建 AI 原生工作流的起点。

- 如何配置
**Hooks**来实现自动化代码审查？ - 如何编写
**Sub-Agents**来处理隔离的脏活累活？ - 如何设计
**Slash Commands**来固化团队的 SOP？

如果你想深入掌握 Claude Code 的高阶玩法，不仅仅是写 Prompt，而是构建一套**“自动纠错、按需加载”**的工程化体系。

欢迎关注我的极客时间专栏**《 AI 原生开发工作流实战》**。

我们不聊虚的，只讲能在生产环境中落地的 AI 工程实践。

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