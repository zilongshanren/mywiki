---
title: 从“手搓 Prompt”到“无限循环”：AI 编码的下一个形态是“Ralph”吗？
url: https://tonybai.com/2026/01/21/ai-coding-evolution-from-prompting-to-ralph/
published: '2026-01-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 从“手搓 Prompt”到“无限循环”：AI 编码的下一个形态是“Ralph”吗？

![](../../assets/b02789583d43c43a.png)


[本文永久链接](https://tonybai.com/2026/01/21/ai-coding-evolution-from-prompting-to-ralph) – https://tonybai.com/2026/01/21/ai-coding-evolution-from-prompting-to-ralph

大家好，我是Tony Bai。

“如果你把 AI 放在一个死循环里，给它足够的权限和上下文，会发生什么？”

2025 年底，一个名为 **“ Ralph Wiggum Technique” (Ralph 循环)** 的 AI 编程技巧在硅谷极客圈一夜爆红。它没有复杂的架构，没有花哨的界面，其核心代码甚至只有一行 Bash 脚本。

但就是这个看似简陋、甚至有些“诅咒”意味的技巧，却让开发者们在一夜之间重构了 6 个代码库，构建了全新的编程语言，甚至引发了 Anthropic 官方下场发布插件。

什么是 Ralph？为什么它如此有效？它又预示着怎样的 AI 编程未来？

![](../../assets/f209dd925a924415.png)


## Ralph 的诞生——一行代码的暴力美学

Ralph 的故事始于 Geoff Huntley 的一个疯狂实验。他没有使用复杂的 Agent 框架，而是写下了这样一行 Bash 脚本：

```
while :; do cat PROMPT.md | npx --yes @sourcegraph/amp ; done
```


这就是 Ralph 的全部。

**PROMPT.md**：这是唯一的输入，包含了项目的目标、规范、当前状态的描述（通常由 AI 自动更新）。**@sourcegraph/amp**：这是一个极其简单的 CLI 工具，它读取提示词，调用 LLM，并在当前目录下执行命令（修改文件、运行测试等）。**while :; do … done**：这就是灵魂所在。**无限循环。**

Ralph 不会停下来问你“这样行吗？”。它只是不断地读取目标、执行操作、再次读取目标、再次执行……直到你手动杀掉进程，或者它把代码库变成一团乱麻（所谓的“Overbaking”）。

## 为什么 Ralph 有效？—— Context Engineering 的胜利

乍一看，Ralph 似乎只是一个不可控的随机代码生成器。但实际上，它的成功揭示了 AI 编程的一个核心真理：**上下文工程 (Context Engineering) 远比 Prompt 技巧更重要。**

Ralph 的核心不在于那个 Bash 循环，而在于那个 **PROMPT.md**（或者更高级的“Specs”）。

### 声明式而非命令式

传统的 AI 辅助编程是“命令式”的：你告诉 AI “修改这个函数”、“修复那个 Bug”。

Ralph 是“声明式”的：你在 PROMPT.md 中描述**项目的终局状态**（Desired State），比如“所有的 React 组件必须使用 TypeScript 且没有 default exports”。Ralph 的工作就是不断逼近这个状态。

![](../../assets/74a4405f1476a045.png)


### 小切口，高频迭代

Ralph 并不试图一次性完成所有工作。它在每次循环中只处理一小块任务。这种“切碎”的工作方式，完美契合了 LLM 当前的上下文窗口限制，避免了“一次性生成几千行代码然后全错”的灾难。

### 自动化反馈循环

在 Ralph 的循环中，测试结果、Linter 报错、编译失败信息，都会成为下一个循环的输入。它不仅是在写代码，更是在**自我修复**。

## Ralph 的进化——从玩具到生产力

随着社区的介入，Ralph 迅速从一个 Bash 玩具进化为一种严肃的开发范式。

**重构利器**：这是一次真实的重构经历。面对一个混乱的 React 前端，没有人工介入手动修改，而是花 30 分钟写了一份 REACT_CODING_STANDARDS.md（编码规范），然后让 Ralph 跑了 6 个小时。结果？Ralph 自主完成了一个人类可能需要数天才能完成的枯燥重构。**Cursed Lang**：Geoff 甚至用 Ralph 构建了一门全新的编程语言 Cursed Lang，包含编译器、标准库，且实现了自举。**官方下场**：Anthropic 甚至推出了官方的 Ralph 插件。虽然被社区吐槽“过度设计”且不如 Bash 脚本好用，但这标志着这种模式已被主流认可。

## 警惕“Overbaking”——AI 也会“把菜烧焦”

Ralph 并非完美。它最大的风险在于 **“Overbaking”（过度烘焙）**。

如果你让 Ralph 跑得太久，且 PROMPT.md 的约束不够紧，它可能会开始产生“幻觉”般的优化：添加没人需要的 Post-Quantum 密码学支持、过度拆分文件、甚至为了通过测试而删除测试。

这给我们的启示是：**AI 是强大的引擎，但人类必须是方向盘。**

**写好 Spec**：如果你的 Spec（规格说明书）是垃圾，Ralph 产出的代码也是垃圾。**监控循环**：不要让它无限制地跑下去，设置检查点。**小步快跑**：最好的 Ralph 实践是“一夜重构一个模块”，而不是“一夜重构整个系统”。

## 小结：Agentic Coder 的未来

Ralph Wiggum Technique 可能只是 AI 编程进化史上的一朵浪花，但它留下的遗产是深远的。

它告诉我们，未来的编程可能不再是编写具体的逻辑，而是**编写和维护一份完美的 Spec（规范说明书）**。我们将成为“系统架构师”和“验收测试员”，而将那个枯燥、重复、且容易出错的“编码循环”，交给不知疲倦的 Ralph 们。

所以，下一次当你面对一座巨大的“屎山”代码时，不妨试着写一份清晰的 Spec，然后启动那个神奇的 Bash 循环。

资料链接：

- https://ghuntley.com/ralph/
- https://www.humanlayer.dev/blog/brief-history-of-ralph

**从“暴力循环”到“优雅指挥”**

Ralph Wiggum 的故事让我们看到了 AI 自主编程的雏形：**只要有正确的 Spec（规范）和自动化的 Loop（循环），奇迹就会发生。**

但 Ralph 毕竟只是一个 5 行代码的 Bash 脚本，粗糙且容易“烤糊”。在真实的工程实践中，我们不能只靠运气的“无限循环”，我们需要一套更稳定、更可控、更专业的**AI 原生开发体系**。

如果你不想止步于 Ralph 这样的极客实验，而是想真正掌握驾驭 AI Agent 的系统方法，欢迎加入我的新专栏 **《 AI原生开发工作流实战》**。

这是关于如何构建你的“自动化流水线”：

**告别低效**：不再做“复制粘贴喂 AI”的搬运工，建立自动化闭环。**驾驭神器**：深度实战**Claude Code**等前沿工具，它是比 Ralph 更成熟的“神灯精灵”。**身份跃迁**：从被动的“AI 使用者”，进化为定义规范、掌控全局的**“工作流指挥家”**。

**扫描下方二维码，别让 AI 只有暴力，让我们赋予它工程的优雅。**

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