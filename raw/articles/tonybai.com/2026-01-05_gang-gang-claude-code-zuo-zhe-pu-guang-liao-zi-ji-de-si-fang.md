---
title: 刚刚，Claude Code 作者曝光了自己的“私房”配置：原来顶尖高手是这样用 AI 写代码的！
url: https://tonybai.com/2026/01/05/httpstonybai-com20260105claude-code-author-reveals-private-ai-coding-config/
published: '2026-01-05'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 刚刚，Claude Code 作者曝光了自己的“私房”配置：原来顶尖高手是这样用 AI 写代码的！

![](../../assets/0d0a230d3aa53d9a.png)


[本文永久链接](https://tonybai.com/2026/01/05/claude-code-author-reveals-private-ai-coding-config) – https://tonybai.com/2026/01/05/claude-code-author-reveals-private-ai-coding-config

大家好，我是Tony Bai。

自从 Claude Code 发布以来，我和大家一样，都在探索这个“终端里的 AI 智能体”到底能爆发出多大的能量。

就在昨天，Claude Code 的创造者、Anthropic 的核心工程师 **Boris Cherny** 在社交媒体上毫无保留地[晒出了他自己的 Claude Code Setup（配置与工作流）](https://x.com/bcherny/status/2007179832300581177)。

看完他的分享，我最大的感受是：**英雄所见略同！**

Boris 的很多“私房技巧”，不仅验证了 AI 原生开发的高效性，更令人惊喜的是，**其中 80% 的核心实践，竟然都与我的专栏《 AI 原生开发工作流实战》中的教学内容完美印证。**

今天，我就带大家深度拆解一下这位“Claude Code 之父”的开发心法，结合他晒出的真实配置代码，看看Claude Code作者们都是如何驾驭 AI 的。

![img{512x368}](../../assets/f209dd925a924415.png)


## 心法一：多线程并发 —— 做 AI 的“指挥家”

Boris 分享的第一个技巧就非常硬核：


“I run 5 Claudes in parallel in my terminal… I also run 5-10 Claudes on claude.ai/code.”

（我在终端里并行运行 5 个 Claude… 同时在网页端也运行 5-10 个。）

这意味着什么？这意味着他把自己变成了一个“任务调度器”。

这正是我们在专栏 **“ 概念篇”** 中反复强调的开发者角色转型：

**从“代码的生产者”转变为“工作流的指挥家”**。

在 Boris 的截图中，我们可以清晰地看到他正在运行多个独立的 Session，其中一个正在处理复杂的类型检查和构建任务：

```
Bash(bun run typecheck 2>&1 | head -100)
Bash(bun run build:agent-sdk-typings && tsc ...)
# ... AI 正在自主修复类型错误 ...
```


在 AI 原生时代，我们的生产力不再受限于打字速度，而是受限于**并发管理能力**。你可以同时开启多个 Session：1 号 Claude 负责修 Bug，2 号 Claude 负责写测试，3 号 Claude 负责重构。你不再是自己在写代码，你是在指挥一个“虚拟团队”。

## 心法二：上下文的艺术 —— 极简主义的 CLAUDE.md

Boris 也晒出了他的 CLAUDE.md 文件。出乎意料的是，它非常简洁，没有任何冗余的废话。

**Boris 的 CLAUDE.md 真实代码：**

```
# Development Workflow
**Always use bun, not npm.**
```sh
# 1. Make changes
# 2. Typecheck (fast)
bun run typecheck
# 3. Run tests
bun run test -- -t "test name" # Single suite
bun run test:file -- "glob" # Specific files
# 4. Lint before committing
bun run lint:file -- "file1.ts" # Specific files
bun run lint # All files
# 5. Before creating PR
bun run lint:claude && bun run test
```


这完美印证了我们在专栏 **第 06 讲《 上下文的艺术（上）：详解CLAUDE.md 与 AGENTS.md》** 中的观点：

**CLAUDE.md 是 AI 的操作手册，必须精准、可执行。**

注意看他的第一句：**Always use bun, not npm.** —— 这是一个典型的“负向约束”。他在教 AI “做什么”的同时，更明确了“不做什么”，这能极大地减少 AI 犯错的概率。

## 心法三：将经验“代码化” —— Slash Commands 与 Sub-agents

Boris 提到他极度依赖 **Slash Commands（斜杠指令）** 和 **Sub-agents（子智能体）**：


“I use slash commands for every ‘inner loop’ workflow… This saves me from repeated prompting.”

（我把所有高频工作流都封装成了 Slash Commands，这让我免于重复写 Prompt。）

他展示的 .claude/commands/ 目录结构简直就是我们专栏 ** 第 08 讲 自定义指令：精通Slash Commands，打造你的私人命令集** 的最佳教具：

```
.claude/
commands/
build-validator.md # 专门负责构建验证的指令
code-architect.md # 专门负责架构设计的指令
agents/
code-simplifier.md # 一个专门负责简化代码的 Sub-agent
verify-app.md # 一个专门负责全链路测试的 Sub-agent
```


他把“架构设计”、“代码简化”、“应用验证”这些复杂的脑力劳动，全部封装成了可一键调用的指令和专家分身。**把你的经验变成代码，让 AI 替你执行经验**，这才是高阶玩家的玩法。

## 心法四：自动化收尾 —— Hooks 的妙用

这也是我最喜欢的一部分。Boris 展示了一个非常漂亮的 **PostToolUse Hook** 配置，用来解决代码格式化问题：

**Boris 的 settings.json 配置片段：**

```
"PostToolUse": [
{
"matcher": "Write|Edit",
"hooks": [
{
"type": "command",
"command": "bun run format || true"
}
]
}
]
```


**这段配置的含义是：** 每当 AI 使用 Write 或 Edit 工具修改了文件后，**立刻、自动**执行 bun run format。

他的逻辑非常清晰：**AI 负责写逻辑，Hook 负责格式化。** AI 生成的代码可能有格式问题，但通过 Hook 自动运行 prettier 或 gofmt，就能解决这“最后的 10%”。

这完全对应了我们专栏 **第 11 讲《 事件驱动：详解Hooks机制，让AI在关键节点自动触发》** 的实战案例。我们当时也演示了如何用 Hook 实现 Go 代码的自动格式化，简直是异曲同工！

## 心法五：安全第一 —— 拒绝 YOLO

最后，Boris 特别展示了他的权限配置搜索界面，并强调：


“I don’t use –dangerously-skip-permissions. Instead, I use /permissions.”

（我从不使用危险的跳过权限模式，而是使用权限白名单。）

即使是工具的开发者本人，也对安全保持着绝对的敬畏。他展示的权限白名单列表（Allowlist）非常详细：

```
Bash(bq query:*)
Bash(bun run build:*)
Bash(bun run lint:*)
Bash(bun run test:*)
...
Bash(cc:*)
Bash(comm:*)
```


他宁愿多花点时间把常用的 bun run、bq query 命令一条条加入白名单，也不愿意让 AI 在“裸奔”状态下运行。

这也正是我们在 **第 09 讲《 安全基石（上）：用权限控制与沙箱为AI戴上“安全镣铐”》** 中苦口婆心强调的：

**没有安全，就没有生产力。**盲目追求全自动（YOLO 模式），是在给未来埋雷。

## 小结：未来已来，你准备好了吗？

看完 Boris 的分享，我更加确信：**我们正在经历一场软件工程范式的彻底重塑。**

Boris Cherny 是这个工具的创造者，他定义了“**上限**”；而我们作为使用者，需要通过系统的学习，去触达这个上限。

如果你也想：

- 像 Boris 一样，构建一套属于自己的
**AI 驾驶舱**； - 掌握
**Slash Commands**和**Hooks**，让 AI 乖乖听话； - 学会
**SDD（规约驱动开发）**，让代码生成一次做对； - 搭建
**Headless 自动化流水线**，让 AI 在你睡觉时也能干活…

那么，欢迎加入我的极客时间新专栏 **《 AI 原生开发工作流实战》**。

在这门课里，我不只会教你工具的用法，更会带你像 Boris 一样思考——**如何用 AI 重塑你的开发习惯，成为新一代的“AI 架构师”**。

**扫描下方二维码，让我们一起，站在巨人的肩膀上，开启 AI 原生开发之旅！**

![](../../assets/305ffd23f32ce780.png)


*(P.S. 专栏内容偏实战，以 Go 语言项目为例，但方法论通用于所有语言。Claude Code 也是一个刚刚诞生不到一年的新物种，我们都是探索者，期待在课程里与你交流碰撞！)*

资料链接：https://x.com/bcherny/status/2007179832300581177

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