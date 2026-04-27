---
tags: [source, 游戏设计, 谜题游戏, 规则系统, 图重写]
date: 2026-04-27
sources: 1
---

# PuzzleScript Rules（Boris The Brave）

[[people/boris-the-brave]] 发表于 2024 年 6 月的文章，分析 PuzzleScript 引擎的规则系统设计及其与图重写语法的关系。

## 摘要

PuzzleScript 是 increpare（Stephen's Sausage Roll 作者）设计的谜题游戏原型工具，以单个文本文件定义图形、关卡、音效与全部规则。其核心是一套**查找-替换规则**：左侧为匹配模式，右侧为替换结果，规则默认考虑四个方向，按从上到下顺序求值。文章重点分析了"冻结运动"机制——通过给对象附加方向标签代替真实移动，将"事件"编码为可被规则匹配的当前状态，让引擎的物理移动阶段负责实际位移。Boris 将此与之前分析过的 Ludoscope 和 Unexplored 的图重写系统对照，肯定了 PuzzleScript 简单规则在 2D 谜题领域的适配度，并指出了对象身份歧义（移动与销毁/重建无区别）和对角线匹配、计数、路径查找等方面的局限。

## 关键要点

- 规则是一维行/列模式的查找-替换，语法极简但可表达复杂行为（Sokoban 仅需一行）
- "冻结运动"：运动意图作为对象标签存储，引擎统一处理碰撞；规则操纵标签而非坐标
- Multipatterns 支持跨关卡多处独立模式同时匹配才触发（类似远程状态联动）
- 可变尺寸模式（`...`）表达对象间任意距离的 inline 匹配，优雅解决了 Ludoscope 的不足
- 隐藏透明对象可充当无碰撞变量，提供 state machine 般的间接状态跟踪
- 局限：对象身份歧义导致位置交换出现标签污染；缺少对角、计数、路径查找的直接支持

## 链接到的概念

- [[game-development/puzzlescript-rule-system]]
- [[game-development/graph-rewriting-proc-gen]]
- [[game-development/phantomgrammar-ludoscope]]

## 原文

- 链接：https://www.boristhebrave.com/2024/06/10/puzzlescript-rules/
- 本地：`raw/articles/boristhebrave.com/2024-06-10_puzzlescript-rules.md`
