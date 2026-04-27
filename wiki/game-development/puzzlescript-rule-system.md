---
tags: [game-development, 谜题游戏, 规则系统, 图重写, 游戏设计]
date: 2026-04-27
sources: 1
---

# PuzzleScript 规则系统（PuzzleScript Rule System）

[PuzzleScript](https://www.puzzlescript.net/) 是 increpare 为谜题游戏原型设计的工具，其核心是一套极简的**查找-替换规则**语言。一个文本文件包含图形、关卡、音效与全部游戏逻辑，Sokoban 的完整规则仅需一行。Boris The Brave 在分析 [[game-development/phantomgrammar-ludoscope|Ludoscope]] 等图重写系统之后，专文分析了 PuzzleScript 规则的设计哲学与局限。

## 规则基础

规则形式为：

```
[ 左侧模式 ] -> [ 右侧替换 ]
```

左侧是一行/列单元格的匹配模式，右侧是替换结果。所有规则默认在四个方向上同时生效，从上到下顺序求值。Sokoban 的推箱规则：

```
[ > Player | Crate ] -> [ > Player | > Crate ]
```

仅此一行即可处理四个方向的推动，因为 `>` 表示对象朝当前计算方向移动的标签。

## 冻结运动（Frozen Motion）

PuzzleScript 最重要的设计决策：**运动不是事件，而是状态**。玩家按方向键后，Player 对象被标记为"向该方向移动"；规则匹配并传播运动标签；引擎统一执行真实位移；最后 `late` 规则收尾。

这将"推动"这类动态交互转换为对当前帧对象标签的静态模式匹配，让无状态的查找-替换规则能描述有序的运动序列。Boris 评价这是"将运动视为状态而非变化"的绝妙洞见。

## 扩展特性

**Multipatterns**：一条规则可含多个模式段，仅当所有段在关卡中同时匹配时才触发——可实现"机关触发门"这类远程联动，无需坐标。

**可变尺寸模式（`...`）**：

```
[ > Kitty | ... | Fruit ] -> [ | ... | Kitty ]
```

`...` 表示两端对象之间任意数量的单元格，等价于无限多条固定长度规则的集合。这优雅地解决了 Ludoscope 中难以表达的"任意距离"问题。

**隐藏状态**：透明无碰撞对象可充当变量，配合规则读写，模拟有限状态机而不破坏替换规则范式。

## 局限

规则在对象身份上存在歧义：`[ Player | Crate ] -> [ Crate | Player ]` 在 PuzzleScript 中并非"交换位置"，而是销毁并重建——导致 Crate 会继承 Player 的运动标签，反之亦然。此外，对角线匹配、计数操作、路径查找均需多条规则配合，且难以调试。

## 与图重写的关系

PuzzleScript 规则是[[game-development/graph-rewriting-proc-gen|图重写]]的一维受限版本：模式仅为直线段，无法直接表达二维矩形或任意图结构。这一限制是刻意设计的，使规则语言恰好适配 2D 网格谜题而非通用程序化生成。

## 相关

- [[game-development/graph-rewriting-proc-gen]] — 更通用的图重写系统
- [[game-development/phantomgrammar-ludoscope]] — Boris 之前分析过的类似系统
- [[game-development/arc-consistency]] — 约束求解背景
- [[game-development/mission-graph]] — 关卡逻辑的另一种描述框架

## Sources

- [[sources/boris-puzzlescript-rules]]
