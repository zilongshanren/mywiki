---
tags: [procedural-generation, constraint-solving, wfc, game-development, infinite-generation]
date: 2026-04-27
sources: 2
---

# Modifying in Blocks（分块修改）

Modifying in Blocks 是 Paul Merrell 在 [[model-synthesis]] 中提出、用于解决约束式生成器随输出尺寸增大而频繁遭遇矛盾问题的技术。该思路同样适用于 [[wave-function-collapse]]，Boris The Brave 对其进行了深入研究并将其扩展为支持无限大地图的方案。

## 问题背景

基于约束的生成（WFC / Model Synthesis）天然是 NP-Complete 问题：小面积输出通常能可靠完成，而面积一旦扩大，矛盾概率急剧攀升。两种经典补救方案各有缺陷：

- **重启（Restart）**：矛盾时从零重来。小规模可行，大规模下成功率趋近于零。
- **回溯（Backtracking）**：退到最近的有效状态重试。虽然不像重启那样浪费，但容易陷入"兔子洞"——某个局部解本身不可扩展，却让算法反复在局部变体间探索，最终卡死。

## 核心机制

Modifying in Blocks 把整个生成区域划分为若干**互相重叠的小块（Block）**，然后逐块运行生成器：

1. 每次只解决一个块内的约束，出错只需重启当前块。
2. 每个块在生成时，其**所有边界**都被锁定为约束输入——已生成的相邻块提供对应侧的约束，而对于尚未生成的开放边，固定为一组**预先已知合法的瓦片背景（known-good background）**。
3. 块与块之间存在重叠，使得每个块对已生成邻居的约束确实起效，而固定背景最终会被后续块覆盖。

全局背景的存在是关键：它保证在任何时刻，"至少存在一种合法的填充方案"，因此就算某块生成失败，也可以安全地回退到背景瓦片。

## 无限 Modifying in Blocks

Boris 在此基础上设计了**支持惰性（Lazy）无限生成的变体**，解决了"WFC 不同求值顺序输出不一致"导致无法确定性生成无限地图的问题。其核心技巧是**分层（Layered）块求值**：

- **Layer 1**：在无限平面上按规则网格放置一批间隔稀疏的独立块，彼此无依赖，可任意顺序求值。
- **Layer 2**：在 Layer 1 的基础上偏移半个块宽度，每块恰好依赖 Layer 1 的 2 个块。
- **Layer 3**：在 Layer 2 基础上沿 y 轴偏移半个块高度，依此类推。
- **Layer 4**：最终输出层，覆盖所有瓦片，每个 Layer 4 块的依赖树深度固定为 4 层、总节点数 12，无论块在无限平面上的位置如何。

该设计实现了三个关键特性：

- **确定性（Deterministic）**：求值顺序由依赖树决定，与玩家位置无关。
- **惰性（Lazy）**：只需求值玩家视野附近的块，无需提前计算整个地图。
- **常数时间（Constant-time per block）**：每个输出块的代价固定，不随地图面积增长。

## 局限性

- 整体工作量约为朴素分块的 4 倍（4 层各做一遍）。
- 任何大于单个块尺寸的空间模式无法被正确表达。
- 需要预先定义一组合法的背景瓦片，对某些瓦片集可能难以设计。
- 参数调优（块大小、重叠度、重启次数）较繁琐，普适性不如简单回溯。

## 相关

- [[model-synthesis]] — 该技术的原始来源
- [[wave-function-collapse]] — Modifying in Blocks 同样适用于 WFC
- [[arc-consistency]] — 底层约束传播算法

## Sources

- [[sources/boris-model-synthesis-modifying-blocks]]
- [[sources/boris-infinite-modifying-blocks]]
