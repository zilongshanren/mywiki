---
tags: [procedural, fractal, l-system, vfx, unity]
date: 2026-04-19
sources: 1
---

# 分形闪电效果（L 系统应用）

[[Ted Sie]] 在 [[l-system-fractals|L 系统基础]] 之上给出的工程化案例：用分形规则生成闪电效果。闪电的"之字"主干和"随机发散"分支，恰好对应两条几何规则。

## 核心规则

**1. 中点偏移（midpoint displacement）**

每次迭代在当前线段的中点插入一个垂直于线段的随机偏移向量，把一条线段拆成两条折线。反复迭代后就形成闪电主干的锯齿形态。这一思路与 [[diamond-square-noise|Diamond-Square]] 的中点置换在数学上同源，只是一维版本。

**2. 随机分支**

每次中点偏移后，以一定概率从新中点向侧方长出一条随机短线段，形成闪电的分叉。

## 发散控制

朴素的随机分支会指数爆炸——迭代五六次后分支多到不可接受。作者给出四条工程化抑制：

- **概率性产生分支**：不是每次都分叉。
- **分支角度调整**：限制在一个合理锥角内。
- **限制单次迭代产生的分支数**。
- **限制整体分支总数**。

## 网格与视觉优化

拿到线段集合之后，按每段的中心点与长度用 `GameObject.CreatePrimitive(Quad)` + GPU Instancing 生成可见网格。工程细节上有几个坑：

- **段间缝隙**：两段 Quad 交界会出现缺口，需要在交界处再补一块 Quad 填缝。
- **大小渐变**：迭代过程中记录每段所属的层级（主干 vs 分支第 N 级），主干按到终点的距离、分支按层级深度查一条 [[shaping-functions|AnimationCurve]] 取得每段宽度。
- **颜色渐变**：同法查 Gradient 取得颜色。

这个案例展示了 L 系统作为 **生成规则** 与游戏引擎具体网格/着色管线之间的衔接方式——分形只解决"形状"，视觉好看还得靠图形学上的包装。

## 相关

- [[l-system-fractals]]
- [[diamond-square-noise]]
- [[shaping-functions]]
- [[procedural-mesh-primitives]]

## Sources

- [[sources/tedsie-l-system-lightning-bolts]]
