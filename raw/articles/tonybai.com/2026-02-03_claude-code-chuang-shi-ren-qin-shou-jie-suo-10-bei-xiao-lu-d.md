---
title: Claude Code 创始人亲授：解锁 10 倍效率的 10 个“隐藏技能”
url: https://tonybai.com/2026/02/03/claude-code-founder-10x-efficiency-10-hidden-skills/
published: '2026-02-03'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Claude Code 创始人亲授：解锁 10 倍效率的 10 个“隐藏技能”

![](../../assets/4c1403144c3d5a8b.png)


[本文永久链接](https://tonybai.com/2026/02/03/claude-code-founder-10x-efficiency-10-hidden-skills) – https://tonybai.com/2026/02/03/claude-code-founder-10x-efficiency-10-hidden-skills

大家好，我是Tony Bai。

Claude Code 发布后，迅速成为了 AI 编程领域的“当红炸子鸡”。

大多数开发者对它的使用方式还停留在：“打开终端 -> 输入需求 -> 等待代码生成”。

但这真的发挥出它的全部潜力了吗？

最近，Claude Code 的创始人 **Boris Cherny** 亲自下场，在社交媒体上[分享了团队内部使用的 Best Practices](https://x.com/bcherny/status/2017742741636321619)。

看完这些技巧，我才意识到：我们以前可能只用了它 10% 的功力。

Boris 揭示了如何将 Claude Code 从一个简单的 CLI 工具，升级为一个支持并行、具备规划能力、能自我进化的“数字研发团队”。

今天，我将这 10 个隐藏技能 拆解给你，助你解锁 10 倍的开发效率。

![](../../assets/e7e1e92bcbb64dd9.png)


## 并行工程——一个人就是一支队伍

**技能 1：多线程并发 (Parallel Worktrees)**

- 痛点：传统的 AI 编程是线性的，AI 写代码时，你只能干等。
- 创始人解法：“Do more in parallel.”

利用 git worktree，你可以瞬间克隆出 3-5 个独立的工作目录。在每个目录里启动一个 Claude Session，分别处理不同的 Feature。- 窗口 1：重构后端 API；
- 窗口 2：编写前端组件；
- 窗口 3：运行全链路测试。


这是最大的生产力解锁。你的大脑带宽不再受限于 AI 的生成速度，而是受限于你的“多任务指挥能力”。

**技能 2：左右互搏 (Agent Review Agent)**

- 痛点：AI 写的代码有时候逻辑不严密，自己 Review 又太累。
- 创始人解法：让 AI 审查 AI。
- Session A (Writer): 负责生成 Plan 和 Code。
- Session B (Reviewer): 扮演 “Staff Engineer”，专门负责挑刺。


Boris 透露：让 Session B 对 A 的产出进行 Review，不仅能发现 Bug，还能显著提升代码的鲁棒性。

## 思维升级——先谋后动

**技能 3：Plan Mode 的“一击必杀”**

- 痛点：直接让 AI 改复杂逻辑，往往改得乱七八糟。
- 创始人解法：“Start every complex task in plan mode.”

面对复杂任务，按两下 Shift+Tab 进入 Plan Mode。把你的精力全部花在打磨 Plan 上。一旦 Plan 完美了，切换回 Execute Mode，让 Claude “One-shot（一击必杀）” 完成实现。

**技能 4：子智能体探索 (Subagents for Exploration)**

- 痛点：面对陌生的巨型代码库，主 Agent 读取太多文件会导致 Context 溢出。
- 创始人解法： “Use 5 subagents to explore the codebase.”

你可以直接下令：use 5 subagents to explore the codebase and map out the dependency graph.

这 5 个子智能体会并行阅读代码，互不干扰，最后将精华信息汇总给主 Agent。这相当于派出了 5 个侦察兵。

## 能力扩展——打造私人技能库

**技能 5：把重复劳动封装为 Skill**

- 痛点：每天都在重复输入相同的 Prompt，比如“扫描一下有没有重复代码”。
- 创始人解法： “Create your own skills.”

如果你发现某件事一天要做两次以上，把它写成 Skill。 比如 创建一个 /techdebt 命令。每次会话结束前运行一下，自动扫描并删除重复代码。

**技能 6：自我进化的 CLAUDE.md**

- 痛点：项目规则太多，写在 Prompt 里太麻烦，写在文档里又懒得更新。
- 创始人解法：“Ruthlessly edit your CLAUDE.md over time.”

不要手写规则，让 Claude 自己写。当它犯错并被你修正后，对它说：*“把这个错误的原因和避免方法，写入 CLAUDE.md，这样你下次就不会再犯了。”* 让你的规则文件像生物一样自行生长、进化。

## 自动化闭环——自修复与自验证

**技能 7：Slack 驱动修 Bug**

- 痛点：看到 Bug -> 复制报错 -> 切换 IDE -> 粘贴报错。太慢了。
- 创始人解法：“Zero context switching.”

配置 Slack MCP。在 Claude Code 里直接粘贴 Slack 上的 Bug 链接，说一句 “Fix”。Claude 会自动读取 Slack 里的讨论上下文，复现问题，并提交修复。

**技能 8：Chrome 驱动验 UI**

- 痛点：前端代码写完了，还是得自己打开浏览器点点点。
- 创始人解法：“Chrome MCP is a game changer.”

配置 Chrome MCP。让 Claude 写完代码后，自己打开浏览器，截图，对比设计稿，甚至自动点击按钮进行验证。**Eye > Code.**

## 高阶 Prompting——把 AI 当人看

**技能 9：压力测试 (Challenge Claude)**

- 痛点：AI 容易顺从你的错误想法。
- 创始人解法：“Grill me on these changes.”（拷问我）

告诉 Claude：*“不要直接合并。直到你通过我的测试之前，不要生成 PR。证明这段代码是有效的。”* 激发 AI 的批判性思维，让它从“执行者”变成“质检员”。

**技能 10：状态栏定制 (Custom Statusline)**

- 痛点：开了 5 个终端，忘了哪个是干嘛的。
- 创始人解法：使用 /statusline 自定义显示内容。

让每个终端的状态栏显示当前的 Git 分支、Context 使用量、以及当前任务的目标。一眼望去，掌控全局。

## 小结：从 Tool 到 Teammate

Boris 的分享向我们展示了 Claude Code 的终极形态：它不仅仅是一个 CLI 工具，它是一个**可编程、可扩展、可并行的数字员工团队**。

![](../../assets/3179f99f7df7ee80.png)


掌握了这 10 个隐藏技能，你就不再是那个盯着屏幕发呆的 Coder，而是运筹帷幄的 Commander。

不要用蛮力去写代码，用架构去生成代码。

资料链接：https://x.com/bcherny/status/2017742741636321619

**你的“提效”利器**

创始人的这 10 个技巧中，哪一个最让你觉得“相见恨晚”？你自己在探索 Claude Code 或其他 AI Agent 时，是否也挖掘出了一些好用的“独门绝技”？

欢迎在评论区分享你的提效秘籍！让我们一起构建最强 AI 工作流。

如果这篇文章为你打开了新世界的大门，别忘了点个【赞】和【在看】，并转发给你的开发战友！

**构建你的“数字特种部队”**

看完这些技巧手痒了吗？

- 如何配置
**Slack MCP**和**Chrome MCP**？ - 如何编写一个能自动修债的
**/techdebt Skill**？ - 如何用
**Worktree**搭建并行流水线？

在我的极客时间专栏《[AI原生开发工作流实战](http://gk.link/a/12EPd)》中，我将带你实战 Boris 提到的一些高阶技巧。我们将手把手配置一个**“一人抵十人”**的超级开发环境。

**扫描下方二维码，让你的开发效率原地起飞。**

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