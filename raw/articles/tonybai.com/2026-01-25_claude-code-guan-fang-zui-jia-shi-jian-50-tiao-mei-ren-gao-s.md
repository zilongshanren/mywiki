---
title: Claude Code 官方最佳实践：50 条没人告诉你的“核心军规”
url: https://tonybai.com/2026/01/25/claude-code-official-best-practices-50-core-rules/
published: '2026-01-25'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Claude Code 官方最佳实践：50 条没人告诉你的“核心军规”

![](../../assets/0d24e668b532b220.png)


[本文永久链接](https://tonybai.com/2026/01/25/claude-code-official-best-practices-50-core-rules) – https://tonybai.com/2026/01/25/claude-code-official-best-practices-50-core-rules

大家好，我是Tony Bai。

在使用 Claude Code 的过程中，你是否遇到过这种情况：

有时候它简直是神，几秒钟就能重构一个复杂的模块；但有时候它又蠢得让人抓狂，甚至会一本正经地写出跑不通的代码，或者把你刚刚纠正过的错误再犯一遍。

为什么？是模型不稳定吗？

不，这通常是因为**你的“打开方式”不对**。

Claude Code 本质上是一个运行在 CLI 环境中的**自主智能体（Agentic Coding Environment）**。它受限于一个核心物理法则：**上下文窗口（Context Window）**。

- 上下文满了，它就会“失忆”。
- 指令不清晰，它就会“幻觉”。
- 没有反馈，它就会“盲目自信”。

为了帮你跨越从“新手”到“高玩”的门槛，我精读了 Anthropic 刚刚发布的[官方最佳实践文档](https://code.claude.com/docs/en/best-practices)，并结合实战经验，提炼出了这 **50 条核心军规**。

掌握了它们，你就是指挥 AI 军团的**编排者（Orchestrator）**了。

![](../../assets/e7e1e92bcbb64dd9.png)


## 基础心法——对抗熵增 (Foundational Tips)

**核心逻辑：** 上下文是稀缺资源，清晰度是最高杠杆。

**Clear Task Framing：**开局第一句话决定成败。明确告诉它：**Role（角色） + Task（任务） + Context（背景）**。**Front Load Instructions：**最重要的约束（比如“绝对不要修改配置文件”），必须放在 Prompt 的最前面。**Verification (最高杠杆)：****这是最重要的 Tip。**必须给 Claude 一个“验证它自己工作”的方法。- ❌ “修复这个 Bug。”
- ✅ “修复这个 Bug，并编写一个测试用例来验证修复是否成功。”

**Provide Screenshots：**涉及 UI 修改，直接粘贴截图。Claude 现在的视觉能力极强，一张图胜过千言万语。**Address Root Causes：**遇到报错，明确告诉它：“不要仅仅消除报错（Suppress），要解决根本原因。”**Plan Mode (Shift+Tab)：**复杂任务（涉及 >2 个文件）必须先进 Plan 模式。**Explore -> Plan -> Implement**。

**Review the Plan：**在它动手写代码前，先 Review 它的计划。这时候纠偏成本最低。**One-shot vs Plan：**改个拼写错误？直接干。重构模块？必须 Plan。**Specific Context：**不要让它通读整个仓库。用 @ 引用具体文件。**Rich Content：**善用 cat error.log | claude，直接把日志管道喂给它。**Clear Context：**任务做完了？立刻运行 /clear。不要在垃圾堆里盖新楼。**Summarize Before Clear：**如果想保留记忆，先让它 /compact（压缩上下文），再继续。

## 工程化配置——给 AI 立规矩 (Configuration)

**核心逻辑：** 不要每次都手动教，把规则固化到文件里。

**CLAUDE.md 是宪法：**在根目录创建 CLAUDE.md，这是它每次启动必读的“员工手册”。**Use /init：**运行 /init 命令，让 Claude 自动分析项目并生成初始的 CLAUDE.md。**Prune Ruthlessly：****CLAUDE.md 不要写废话！**- ❌ “请写出优雅的代码。”（浪费 Token）
- ✅ “使用 npm run test:unit 运行单元测试。”（高价值信息）

**Bash Commands：**在文档里告诉它项目特有的命令（如构建、部署脚本）。**Code Style：**明确约定：用 Tab 还是 Space？用 TypeScript 还是 JS？**Import Rules：**告诉它 @src/ 别名指向哪里，避免它瞎猜路径。**Child Directories：**对于 Monorepo，可以在子目录放单独的 CLAUDE.md，它会自动继承。**Permissions Allowlist：**别做“点点点”工程师。用 /permissions 把 ls, grep, npm test 加入白名单。**Sandbox Mode：**对于不信任的任务，开启 /sandbox，让它在隔离环境中撒欢。**Dangerously Skip：**只有在完全可控（断网/沙箱）时，才使用 –dangerously-skip-permissions。**CLI Tools：**安装 gh (GitHub CLI)，让 Claude 能直接提 PR、看 Issue。**MCP Connect：**使用 claude mcp add 连接 Postgres 或 Notion。数据不再是孤岛。**Learn CLI：**不知道怎么用某个工具？让 Claude 先运行 tool –help 自学。

## 技能与自动化——扩展能力 (Skills & Automation)

**核心逻辑：** 把重复的流程封装成“技能”，把 AI 集成到流水线。

**Skills Definition：**在 .claude/skills/ 下创建 SKILL.md，定义可复用的能力。**Domain Knowledge：**把复杂的业务逻辑（如“订单状态流转规则”）封装成 Skill，用到时才加载。**Disable Model Invocation：**对于高风险 Skill，设置 disable-model-invocation: true，强制人工确认。**Custom Subagents：**定义专门的 .claude/agents/security-reviewer.md。- 让它扮演“安全专家”，只负责 Review，不负责写代码。

**Delegate to Subagents：**在主会话中说：“用 security-reviewer 检查刚才的代码。”**Install Plugins：**运行 /plugin，去市场找现成的技能包（如 Python 代码分析）。**Code Intelligence Plugin：**必装！给 Claude 提供“跳转定义”和“查找引用”的能力（基于 LSP）。**Hooks：**设置 .claude/settings.json 中的 Hooks。- 例如：每次 Auto-fix 后自动运行 Lint。

**Headless Mode：**claude -p “prompt”。这是自动化的神器。**CI Integration：**在 GitHub Actions 里用 Headless Mode 自动 Review PR。**Structured Output：**使用 –output-format json，让脚本能解析 Claude 的回答。**Fan-out Pattern：**批量修改 100 个文件？写个 Shell 脚本循环调用 claude -p。

## 避坑指南——反模式 (Anti-patterns)

**核心逻辑：** 识别“失败的味道”，及时止损。

**The Kitchen Sink Session：**试图在一个 Session 里修 Bug、写新功能、又写文档。**后果：**上下文污染，智商直线下降。**解法：**一事一议，做完就 /clear。

**Over-correcting：**纠正了两次还不对？**后果：**错误路径被强化，越改越错。**解法：**别纠缠！直接 /clear，优化 Prompt 后重来。

**The Trust-then-Verify Gap：**还没测试就觉得“看起来是对的”。**后果：**生产环境事故。**解法：**没有 Pass 测试的代码，一行都别信。

**The Infinite Exploration：**让它“调查一下代码库”，不给范围。**后果：**读了几百个文件，Token 耗尽，还没开始干活。**解法：**限制搜索范围，或者用 Subagent 去做调研。

**Vague Error Reporting：**只说“不行”或“报错了”。**后果：**Claude 只能瞎猜。**解法：**粘贴完整的 Stack Trace。


## 高阶操作——神级技巧 (Pro Moves)

**Resume Session：**昨天没干完？claude –resume 接着聊。**Rename Session：**用 /rename 给会话起个好名字（如 feat-login-oauth），方便找回。**Rewind (Esc+Esc)：**走错方向了？双击 Esc 回滚到上一步，比改代码快。**Let Claude Interview You：**不知道怎么写 Spec？- Prompt：
*“我想做个 X 功能。请作为一个资深架构师，向我提问，直到你觉得信息足够写出 Spec 为止。”*

- Prompt：
**Self-Correction Loop：**让它自己改自己的作业。- Prompt：
*“分析你刚才生成的代码，找出 3 个潜在的 Edge Case，并修复它们。”*

- Prompt：
**Model Tier Selection：**简单的 Lint 修复用 Haiku（快且便宜），架构设计用 Opus（聪明但贵）。**Parallel Sessions：**开两个终端。一个写代码（Writer），一个做 Review（Reviewer）。左右互搏，质量倍增。**Develop Intuition：**最后的建议——多用。建立对“上下文容量”和“模型能力边界”的体感。

## 小结：从 直觉 到 方法论

刚开始使用 Claude Code，你可能靠的是**直觉**。但要在大规模工程中稳定产出，你必须依靠**方法论**。

这 50 条军规，就是从“抽盲盒”走向“工业化生产”的桥梁。掌握了它们，你就不再是被动的 User，而是这支硅基军团的 **Commander**。

资料链接：https://code.claude.com/docs/en/best-practices

**深度实战：构建你的“AI 原生工作流”**

Tip 只是冰山一角。真正的威力在于将这些技巧组合成一套**“开发工作流”**。

在我的极客时间专栏**《 AI 原生开发工作流实战》**中，我将带你实战演示：

- CLAUDE.md 实战：如何从零编写一个完美的、模块化的项目宪法？
- 驾驭Claude Code：实现工作流自动化
- 从“AI使用者”进化为规范驱动开发的“工作流指挥家”

**别再用蛮力写代码了。扫描下方二维码，学会用 AI 的杠杆。**

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