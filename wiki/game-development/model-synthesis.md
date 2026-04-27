---
tags: [procedural-generation, constraint-solving, tileset, game-development, wfc]
date: 2026-04-27
sources: 1
---

# Model Synthesis

Model Synthesis 是 Paul Merrell 于 2007 年在博士论文中提出的约束式程序化生成算法，早于广为人知的 [[wave-function-collapse]] 整整十年。两者的核心思路高度相似，但 WFC 在普及和工程包装上做了诸多改进。

## 基本流程

算法从一张样本瓦片地图出发，学习各瓦片之间的合法邻接关系，构建"模型（Model）"。生成阶段将目标网格的每个格子初始化为所有瓦片均可能的状态，然后进入主循环：

1. 选取一个格子，为其指定某张具体瓦片，其他选项标记为不可能。
2. 用 **AC-4 算法**向邻居传播约束——若某格子某方向的所有合法邻接者均已被排除，则该选项从候选集中删除。
3. 循环直至所有格子唯一确定，或遭遇矛盾。

这与约束传播求解器（CSP solver）本质一致，区别在于每步的选择策略带有随机性——这正是 Merrell 指出的关键洞察：**任何基于约束的求解器都可以通过随机选择改造为约束驱动的生成器**。

## 与 WFC 的比较

- **选格策略**：Model Synthesis 按线性扫描顺序选格；WFC 引入"最小熵启发（Least Entropy）"，优先处理最受约束的格子。
- **关注点**：Model Synthesis 侧重 3D 场景与大块瓦片；WFC 偏向 2D 纹理与逐像素生成。
- **Overlapped 模型**：WFC 新增了重叠模式，约束为"输出中每个 NxN 窗口必须在样本中出现"，能捕捉更远距离的相关性。
- **传播**：**算法本质相同**，Merrell 用 AC-4，WFC 实现通常用 AC-3 或等效的支持计数（support count）。

Model Synthesis 长期默默无闻的原因是多方面的：3D 瓦片设计门槛高、代码用 C++ 且依赖不易配置、官网曾有多年不可访问，以及"Wave Function Collapse"这个名字本身更有传播力。

## Modifying in Blocks

当生成面积增大时，矛盾（contradiction）的概率急剧上升，简单重启策略不再可行。Merrell 为此设计了 **Modifying in Blocks**（分块修改）技术，见 [[modifying-in-blocks]]。

## 相关

- [[wave-function-collapse]] — WFC 在 Model Synthesis 之上的改进与普及
- [[modifying-in-blocks]] — 大规模生成的分块技术
- [[arc-consistency]] — AC-4 约束传播算法背景

## Sources

- [[sources/boris-model-synthesis-modifying-blocks]]
