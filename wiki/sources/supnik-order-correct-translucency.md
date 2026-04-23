---
tags: [source, rendering, transparency, oit]
date: 2026-04-19
sources: 1
---

# Order-Correct Translucency（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 发表于 2011 年 2 月的短文，由 AMD HD5800 的实时 OIT 演示出发，讨论为什么 X-Plane 不会立刻拥抱硬件 OIT，转而给出一种基于三角形平面划分的预排序方案。

## 摘要

Supnik 一度被 AMD 的 OIT 演示震撼，但研究后发现它本质上是**让应用自己写后端**：片元通过 compute-shader 风格的原子操作写入按像素维护的链表，再在后处理 pass 里逐像素排序合成。这对已经在 OpenGL 后端做了大量定制的 X-Plane 来说成本过高；他也评估了 depth peeling 和魔改 blend 方程的折中路径。随后他转向一条更轻量的思路：对于单面且互不相交的三角形集合，总能用两两之间的平面关系导出一个从任意视角都正确的绘制顺序——X-Plane 半透明主要是机舱窗户这种稀疏覆盖场景，这个预排序足以避免大多数伪影。他并不确定这个顺序是否严格构成 strict weak ordering，以工程直觉结尾。

## 关键要点

- 硬件 OIT（AMD 演示）=> per-pixel linked-list，要求 GLSL 里暴露 atomic counter 等 compute 能力
- 老 OpenGL 后端迁移到 compute 风格的代价高于「写一个新渲染器」
- depth peeling 与 accumulate-and-average blend 是工程上更容易落地的折中
- 单面三角形 + 三角形不相交 => 任何视角都存在一个合法的前后序
- 依赖三角形单面性：一个三角形对 V 可见，其背面只对 –V 可见，从而解耦两个相反视角
- 动画变形、跨对象相对顺序仍是未解决问题

## 链接到的概念

- [[order-independent-transparency]]
- [[triangle-plane-sort-translucency]]
- [[alpha-blending]]
- [[alpha-blending-front-to-back]]
- [[cheat-by-solving-less]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/02/order-correct-translucency.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-02-28_order-correct-translucency.md`
