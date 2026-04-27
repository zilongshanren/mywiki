---
tags: [procedural-generation, wfc, constraint-solving, level-generation, game-development]
date: 2026-04-27
sources: 1
---

# Driven WFC（受驱动的波函数坍缩）

Driven WFC 是将 [[game-development/wave-function-collapse]] 从"完整关卡生成器"退化为"局部瓦片选择器"的设计模式，通过外部来源决定宏观结构，再用 WFC 处理细节连接。

## 问题背景

WFC 的核心优势在于它能把瓦片集缝合得非常自然，但它本质上只能感知局部约束，无法保证大尺度结构——独立运行时，大型关卡往往显得单调重复、缺乏叙事感。一种直觉的修补方式是给 WFC 加入更多全局约束，但这会大幅提高求解难度，甚至导致无解。

Driven WFC 的解法更直接：**不让 WFC 负责它不擅长的部分**。宏观决策（哪里是实体、哪里是空洞、哪里是主路）交给其他机制处理，WFC 只负责将这些高层意图翻译成视觉上连贯的瓦片排列。

## 工作方式

实现上极为简单。WFC 算法在开始前，每个格子的候选瓦片集等于完整瓦片集。Driven WFC 只需在启动前**对候选集做预过滤**：根据宏观决策，排除掉不符合该位置语义的瓦片，其余流程与标准 WFC 完全相同。这本质上等同于对 CSP 变量的初始域施加额外约束，在 [[game-development/arc-consistency]] 传播层面没有任何额外代价。

## 典型案例

**Townscaper** 是 Driven WFC 最广为人知的实现。用户只需在顶点网格上绘制"填充/留空"布尔图，这些布尔值转换为每个格子的瓦片候选集约束，再跑 WFC 变体生成最终建筑网格。瓦片集本身基于 Marching Cubes，但包含大量手工细节变体，WFC 确保这些变体之间无缝拼合。

**Marian42 的 White City** 使用高度图作为粗粒度驱动信号，每 8 个格子才施加一次约束。这种稀疏驱动策略在结构控制与 WFC 自由度之间取得平衡，同时也便于按 chunk 分块生成无限场景。

Boris 在自己的工具 Tessera 中也探索过类似机制，并以"For Keep's Sake"项目验证了填充布局驱动方案的可行性。

## 与 Marching Cubes 的关系

Boris 将 Driven WFC 比作增强版的 [[rendering/marching-cubes]]：两者都是"给定体素填充状态，选择合适的几何瓦片"，但 Marching Cubes 只看紧邻邻居，而 WFC 能向更远处看，从而选出全局更和谐的变体组合。

## Sources

- [[sources/boris-driven-wfc]]
