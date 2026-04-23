---
tags: [source, 工具链, 热重载, 引擎架构, manifesto, 迭代速度]
date: 2026-04-19
sources: 1
---

# International movement for code rights（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 2010 年 9 月的一篇半戏谑半正经的宣言，口号是「代码和数据应享有平等权利」。这是他 2010 一连串 live-editing / tools / dependencies 贴文的**纲领性总结**。

## 摘要

Pesce 列出五项诉求：

1. **Ease of change**：美术换贴图 / 模型零摩擦；代码为什么要忍 code rot？
2. **Ease of scale**：每代主机投数据规模，却没人投代码规模（编译、链接、可执行体积）。
3. **Ease of iteration**：美术有 hot-reload，代码只有 shader 和 script 两个特权通道；**代码应有 live-editing**。
4. **Tools**：schema、静态检查、运行时可视化——像审视贴图一样审视代码的输入输出状态。
5. **Equal dignity**：代码应当是艺术，是独一份的；不必全部为复用而存在。

核心提案：**Fuck OOP**——角色不该从 mesh → 3dobject 继承，应当是**一组独一份的行为函数**（load/update/render），和它的美术组件一样 ad-hoc。**轻量框架 + 厚重应用**代替厚框架 + 瘦应用。接口 / 契约 / 反射 / 运行时可视化作为基础设施。

结尾用 _Modern Warfare 2_ 战役模式的**机制密度**作证据：高度独特、不重复的玩法是游戏最打动他的点——「我们应当是艺术家，造 GAMES，不是造 frameworks / tools」。

评论区有读者抓语法错，Pesce（意大利人）回复欢迎指正，随后更新了文章。

## 关键要点

- **五项诉求**合起来就是一句话：把投资在美术工具链的精力按比例投给代码工具链。
- **Fuck OOP**是口号，实质主张是**拒绝为强求复用牺牲独特性**。
- **轻框架 + 厚应用**：框架只负责编码人体工学（热换、live-edit、可视化），不负责抽象树。
- **接口 / 契约 / 反射**作为代码一等公民的基础设施。
- **MW2 机制密度**作为「独特代码 > 复用代码」的实例论证。
- 文风在 2010 年是**挑衅式预测**；2026 年行业部分兑现（ImGui、[[binary-hot-reload]]、Rust 契约），但 3A 仍是「巨型引擎 + 少量独特脚本」结构。

## 链接到的概念

- [[code-as-art-manifesto]]
- [[live-editing-taxonomy-2010]]
- [[pesce-2010-engine-layer-sketch]]
- [[scene-graph-unnecessary-in-engine]]
- [[binary-hot-reload]]
- [[tools-first-iteration-loop]]
- [[angelo-pesce]]

## 原文

- 链接：https://c0de517e.blogspot.com/2010/09/international-movement-for-code-rights.html
- 本地：`raw/articles/c0de517e.blogspot.com/2010-09-01_international-movement-for-code-rights.md`
