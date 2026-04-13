---
title: 继 MCP 之后，Anthropic 再放大招：Agent Skills 正式发布为开放标准！
url: https://tonybai.com/2025/12/19/anthropic-agent-skills-open-standard-launch/
published: '2025-12-19'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 继 MCP 之后，Anthropic 再放大招：Agent Skills 正式发布为开放标准！

![](../../assets/06eafdaa9e576858.png)


[本文永久链接](https://tonybai.com/2025/12/19/anthropic-agent-skills-open-standard-launch) – https://tonybai.com/2025/12/19/anthropic-agent-skills-open-standard-launch

大家好，我是Tony Bai。

就在刚刚（美国时间2025年12月18日），Anthropic 正式宣布将 **Agent Skills** 发布为开放标准。

这是继2024年末推出 **MCP (Model Context Protocol)标准** 之后，Anthropic 在构建 AI 开放生态上的又一记重拳，彻底补齐了 AI 原生应用的**“能力层”**拼图。

如果说 **MCP** 是 AI 时代的 **“USB 接口”**，解决了大模型连接外部工具与数据（如 GitHub, Google Drive）的标准化问题；

那么 **Agent Skills** 就是 AI 时代的 **“通用驱动程序”**，它定义了 AI 该**如何使用**这些工具来完成复杂的业务流程。

OpenCode, Cursor, Letta 等头部开发工具已率先宣布支持。这意味着，开发者编写一套 Skill，就可以在所有支持该标准的 AI 平台（Claude, Cursor 等）上无缝运行。

**AI 开发终于告别了“手搓 Prompt”的草莽时代，进入了“标准化封装”的工业时代。**

![](../../assets/5b15b2fa46955458.png)


## 什么是 Agent Skill？

简单来说，**Skill 就是一个可移植的“能力包”**。

在物理形态上，它就是一个文件夹，里面包含了让 AI 完成特定任务所需的**指令（SKILL.md）、脚本（Scripts）和资源（Resources）**。

你可以把它想象成给 AI 安装的一个**“APP”**或**“岗位 SOP”**。

根据 agentskills.io 的官方规范，Skill 拥有一个极具工程价值的特性：**渐进式披露 (Progressive Disclosure)**。

**Metadata First：**系统只需加载约 100 tokens 的元数据，让 AI 知道“我学会了/拥有什么技能”。**On-Demand Loading：**只有当 AI 真正决定使用该技能时，才会加载完整的指令（<5k tokens）和相关脚本。

这意味着你可以给一个 Agent 装备 1000 个技能（从写 SQL 到 查财报），但平时只占用极少的上下文（Context），只有在干活时才调用相关记忆。这完美解决了长期以来困扰开发者的**Token 浪费**和**上下文干扰**问题。

## 开发者最关心的 3 个问题

在研究了 Anthropic 的技术文档后，我整理了开发者最容易混淆的几个概念：

**Q1: Skill 和 Prompt 有什么区别？**

**Prompt (提示词)：**是**反应式**的、一次性的。比如“帮我润色这段代码”。它通常不跨会话持久化。**Skill (技能)：**是**主动式**的、持久化的。比如“公司 Java 编码规范与 CR 指南”。一旦安装，AI 在任何对话中都知道应当遵守这套规范。

**Q2: Skill 和 MCP 到底怎么分工？（关键）**

这是一个经典的“硬件 vs 软件”的关系。

**MCP (连接层)：**它是**管道**。它让 Claude等大模型 能“连上”你的 PostgreSQL 数据库等。它解决的是**“能不能访问”**的问题。**Skill (能力层)：**它是**逻辑**。它教 Claude等大模型 “在查询这个数据库时，必须先检查权限，且不能使用 SELECT *”。它解决的是**“做得对不对”**的问题。**最佳实践：**用 MCP 建立连接，用 Skill 定义流程。

**Q3: 我该如何开始？**

Skill 的格式非常简单且开放。你只需要创建一个包含 SKILL.md 的目录。

```
---
name: code-review
description: Analyze code based on OWASP top 10 standards.
---
# Instructions
1. Check for SQL injection...
```


这种**“以文档定义能力”**的轻量级模式，正是 **SDD (Spec-Driven Development)** 理念的极致体现。

## 意义：生态闭环已成

随着 Agent Skills 的发布，AI 原生应用的架构分层终于清晰了。我们可以用一张图来看懂这个全新的生态栈：

![](../../assets/439b4d82360fa3fb.png)


对于开发者而言，**“Prompt Engineering”正在消亡，而“Skill Engineering”正在兴起。**

未来的高价值开发者，不再是那些会写漂亮提示词的人，而是那些能将企业隐性知识（Tacit Knowledge），封装成标准化的、可移植的 Agent Skills 的人。

## 如何集成？

Anthropic 提供了三种极简的集成路径：

**Claude Apps 用户：**直接在 Settings > Capabilities > Skills 中浏览目录并启用（类似安装 Chrome 插件）。**Claude Code 用户：**将 Skill 文件夹放入项目目录，或从插件市场安装。**API 开发者：**通过 /v1/skills 端点动态挂载技能。

## 深度实战：编写你的第一个 Agent Skill

标准已经发布，工具已经就绪。现在的问题是：**你如何编写出让 AI 精准执行、不产生幻觉的 Skill 文档？**

在我的极客时间专栏**《AI 原生开发工作流实战》**中，我已第一时间更新关于 **Agent Skills** 的实战内容。

我们将深入剖析 agentskills.io 的官方规范，并带你进行硬核实战：

**深度拆解官方 Skill：**分析标准 Skill 的目录结构与元数据设计技巧。**Go 代码 Review Skill 实战：**手把手编写一个专用于 Go 语言项目的 Code Review Skill，定义从 Lint 检查到逻辑验证的完整 SOP，并将其部署到开发环境中。

让你亲身体验从**“指挥 AI（Prompting）”**到**“配置 AI（Configuring）”**的质变。

**别让你的 AI 只有“蛮力”，给它安装“驱动”。扫描下方卡片，跟上 AI 工程化的最新浪潮。**

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


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论