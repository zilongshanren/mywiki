---
tags: [game-development, procedural-generation, dungeon-generation, roguelite, level-design]
date: 2026-04-27
sources: 3
---

# 程序化地牢生成

程序化地牢生成是 roguelite 类游戏的核心技术，目标是每次游戏产出结构不同但游玩体验可控的关卡。Boris The Brave 对多款经典游戏的生成算法做了详细逆向分析。

## 设计原则：布局与内容解耦

多个游戏案例（以撒、Unexplored、Diablo）共同印证了同一结论：**先生成 floorplan（拓扑结构），再填充房间内容**。两步解耦后，布局算法无需关心房间细节，内容系统无需关心地形连通性，各自可独立迭代。

## 典型实现：《以撒的结合》

以撒在 9×8 网格上做 BFS 扩展：从起始房间出发，以 50% 概率向邻格延伸，拒绝已有 2 个以上邻居的格（防止成环），自然产生树形无环地牢。特殊房间靠规则放置：Boss 房取最远死端，密室贴近三个以上房间的交叉点。简单、高效，三个月内完成开发。详见 [[sources/boris-isaac-dungeon]]。

## 高级方案：循环地牢生成（Unexplored）

《Unexplored》的核心是**循环地牢生成（Cyclic Dungeon Generation）**：先画大环，将环分为两段弧，用预定义"主循环类型"（24 种）规定两弧的叙事结构（双路选择、门钥结构、Hub 等），再叠加次级环和死端。循环结构比树形结构天然支持更多有意义的分支与回溯设计。底层实现基于图重写系统（PhantomGrammar + Ludoscope 工具），约 5000 条规则，单人开发可行。详见 [[sources/boris-unexplored-dungeon]]。

## 分析工具：任务图（Mission Graph）

[[mission-graph]] 是分析地牢关卡的核心抽象：将所有锁/钥匙依赖关系提炼为有向图，忽略物理布局，只保留逻辑先后。任务图能揭示关卡的真实线性程度，也是程序化生成中"先生成抽象结构"的理论基础。

## 相关

- [[mission-graph]] — 锁钥关系的图论抽象与分析工具
- [[sources/boris-isaac-dungeon]]
- [[sources/boris-unexplored-dungeon]]
- [[sources/boris-lock-key-dungeons]]

## Sources

- [[sources/boris-isaac-dungeon]]
- [[sources/boris-lock-key-dungeons]]
- [[sources/boris-unexplored-dungeon]]
