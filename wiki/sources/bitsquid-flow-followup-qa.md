---
tags: [source, bitsquid, 脚本系统, 可视化编程]
date: 2026-04-19
sources: 1
---

# Flow — Data-Oriented Implementation of a Visual Scripting Language（Q&A 补遗 / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2011 年 5 月的帖子。正文篇幅极短，主体是对 2010 年 9 月 Flow 那篇[[sources/bitsquid-visual-scripting-data-oriented|原文]]的读者 Q&A 与几点补充澄清。

## 摘要

作者回应了三个问题。一是"如何避免可视化脚本意大利面"——他们靠**hierarchical grouping**（节点组折叠成子图）和**copy-paste 复用**（拷贝后修改不会互相传播）。读者建议增加**按主题分 tab 的工作区**（门/钥匙一 tab，电梯一 tab），作者认同未来会做。二是**紫色节点**是什么——query 节点，按需取数据：当它被下游节点（比如 `Particle Effect.Create`）触发时才现场 fetch 对应值（比如 unit 的当前位置），不是每帧采样。三是资源可得性——Bitsquid 的演示 PDF 迁移到了 GitHub niklasfrykholm/blog 的 presentations 目录。

内容本身是 Flow 系统功能细节的 clarification，而非新设计；适合作为 [[flow-graph-data-oriented-runtime]] 页的增量素材。

## 关键要点

- Flow 支持**层级分组**（可视化版的 LOD），把一组节点折叠进子图；
- 通过 **copy-paste** 实现重用，但 copy 不会自动同步改动（和 prefab override 不一样）；
- **多 tab 工作区**：按关卡/主题拆分逻辑，提议已在采纳中；
- **Query 节点**（紫色）按需 fetch 数据，触发时才执行，省去无谓采样；
- 作者把历史演示整理到 GitHub：`niklasfrykholm/blog/tree/master/presentations`。

## 链接到的概念

- [[flow-graph-data-oriented-runtime]]
- [[niklas-frykholm]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2011/05/flow-data-oriented-implementation-of.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2011-05-06_flow-data-oriented-implementation-of-a-visual-scripting-lang.md`
