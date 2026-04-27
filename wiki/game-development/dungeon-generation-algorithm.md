---
tags: [procedural-generation, dungeon-generation, roguelike, game-development]
date: 2026-04-27
sources: 2
---

#地牢生成算法

地牢生成（Dungeon Generation）是 Roguelike 及动作 RPG 中最核心的程序化生成需求之一。通过对 Diablo 1 和 Enter The Gungeon 两款经典游戏的逆向分析，可以归纳出若干反复出现的设计模式。

## 两阶段生成范式

两款游戏都不约而同地采用了**先抽象后具体**的两阶段结构，这是地牢生成最重要的架构原则：

- **第一阶段（结构/预地牢）**：只关心"哪里可走、有哪些房间、连通关系是什么"，完全不涉及视觉。Diablo 1 用二值 bool 数组（Predungeon），Enter The Gungeon 用有向图（Flow）。
- **第二阶段（视觉/空间布局）**：将第一阶段结果转化为实际瓦片或空间坐标。Diablo 1 用 Marching Squares，Gungeon 用出口对齐 + 寻路走廊。

这种分离使得关卡结构设计与美术资产完全解耦，可以独立调试和迭代。

## Diablo 1 的房间算法模式

Diablo 1 的四个章节展示了三种基础的预地牢生成策略：

**递归萌芽（Recursive Budding）**（教堂/地狱）：从一组种子房间出发，向两轴交替延伸矩形房间，每次生成后递归继续扩展。生成结果紧凑、几何感强。

**递归细分（Recursive Subdivision）**（地穴）：将可用区域不断切分，在每个子区域内随机放置房间，相邻房间用走廊连接。生成结果分散，迷宫感强，有大量留白（需要"填空"步骤补充地板密度）。

**随机边缘扩展 + 侵蚀（Organic Expansion）**（洞窟）：从小矩形出发，每次随机保留或丢弃扩展边的格子，再对直线墙和孤立固体块做侵蚀处理。生成结果有机、曲线感强。

所有变体共享：Miniset（局部 find-and-replace）修 bug、加装饰；连通性 Lockout 检查，失败则重试。

## Enter The Gungeon 的图结构方案

Gungeon 的创新在于将**人工设计的节奏意图**编码为 Flow 有向图，让随机性在该图的约束下发生：

- Flow 文件预设了房间类型、单向路径、循环回路的拓扑结构，保证 Boss 距离、奖励循环、战斗节奏符合设计预期。
- **节点注入（Injection）**：条件化地插入可选房间（密室、监狱等），比在瓦片层面做逻辑判断灵活得多。
- **Composite 拆分**：将图分解为最小循环子图和树形子图，循环子图优先布局以保证其紧凑性。
- 循环布局从两端交替延伸，末段用寻路生成走廊闭合，是一个优雅的几何问题解法。

## 共同启示

两款游戏的分析都指向同一结论：**先在抽象层面用简单数据结构（bool 数组/有向图）确定结构与节奏，再做视觉具体化**，是地牢生成系统保持可控、可迭代的关键。局部 find-and-replace（Miniset/Fixup）是一种极低成本的"最后一公里"修缮工具，值得在任何瓦片地图生成器中考虑。

## Sources

- [[sources/boris-diablo1-dungeon]]
- [[sources/boris-gungeon-dungeon]]
