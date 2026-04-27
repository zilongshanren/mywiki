---
tags: [procedural-generation, graph-rewriting, level-generation, game-development]
date: 2026-04-27
sources: 1
---

# 图改写（Graph Rewriting）用于程序化关卡生成

图改写（Graph Rewriting）是一种将图论中的子图模式匹配与替换思想应用于内容生成的技术。在学术界已有系统研究，但在游戏关卡生成领域属于小众选择——尽管表达力相当强大。

## 核心机制

图改写的逻辑与文本查找替换高度类似：定义一组**改写规则**，每条规则包含**左侧模式**（LHS，描述要匹配的子图结构）和**右侧替换**（RHS，描述如何替换匹配到的子图）。算法不断在当前图中扫描能匹配 LHS 的子图，将其替换为 RHS 指定的新结构，并保留图中未被匹配到的边和节点，如此循环直至满足终止条件。

相较于 L-System（只能处理线性字符串替换），图改写能直接生成带环拓扑、多路分叉、复杂连通等非线性结构，从而更忠实地模拟游戏关卡中钥匙-锁、任务分支、区域连通等空间关系。这也是 [[game-development/mission-graph]] 类方法通常选用图改写的核心原因。

## 典型应用

Joris Dormans 是将图改写引入游戏关卡生成的主要推动者。他的工具 **PhantomGrammar** 和 **Ludoscope** 对基础图改写做了大量工程扩展，用于驱动 **Unexplored**（2017）的 Zelda 风格地牢生成。同年，Enter the Gungeon 也使用了简化版图替换规则来变化关卡内容，但其匹配模式仅限于单节点，远不及 PhantomGrammar 的表达力。**Dungeon Architect**（Unity/Unreal 插件）支持复杂 LHS 模式但不允许环，属于二者之间的折中方案。

Boris 在分析 Unexplored 生成系统的系列文章中，将图改写定位为理解该游戏关卡生成的关键前置知识，也是 [[game-development/procedural-dungeon-generation]] 中表达任务-空间双层结构的核心工具。

## 与其他技术的关系

图改写通常在**任务图（Mission Graph）**层运作，产出高层拓扑；再由底层空间生成器（如 WFC、BSP 树等）将节点映射到实际房间和走廊。这种双层设计使宏观叙事结构与局部细节生成解耦，是 Boris 系列文章反复强调的组合策略。

## Sources

- [[sources/boris-graph-rewriting-proc-gen]]
- [[sources/boris-phantomgrammar-ludoscope]]
