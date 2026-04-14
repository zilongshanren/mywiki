---
tags: [source, 渲染, GPU, 光栅化]
date: 2026-04-14
sources: 1
---

# A Trip Through the Graphics Pipeline 2011, Part 6（Fabian Giesen）

[[fabian-giesen|Fabian "ryg" Giesen]] 2011 年 7 月发表的「Trip Through the Graphics Pipeline 2011」系列第 6 篇。整个系列是公开材料里关于桌面 GPU 内部最细的描述之一；第 6 篇专门讲 [[rasterization|光栅化]] 算法本身——具体说，**桌面 GPU 用什么算法把三角形变成像素**。

## 摘要

文章先反对「把光栅化器写成 scanline 增量循环」的老软件做法：那种算法在 SIMD/quad 时代 awkward，在 `x` 和 `y` 上不对称、不易并行，对硬件极不友好。然后引出现代答案——**[[pineda-edge-rasterization|Juan Pineda 1988 年的边方程算法]]**：用三条边方程的符号判定点是否在三角形内，相邻像素之间只需要一次整数加法，天然 SIMD 化，64 个像素一次性测试。

光栅化本身分两层：
- **fine rasterizer**：在 8×8 块内执行 Pineda 算法，输出 64-bit 覆盖掩码。
- **coarse rasterizer**：[[hierarchical-rasterization|更上一层]]，提前用 tile 角点的 `E` 上下界剔除整块空 tile。每接受一个 tile 顺手把角点 `E` 传给 fine rast 节省重算。

[[triangle-setup|Triangle setup]] 阶段的工作就是**为这两层计算它们需要的常量**：三条边方程的 `(a, b, c)`、tile 步进 `Δ`、reference corner、第一个参考 tile 的初值（已含 top-left 填充规则修正）。因为顶点已经 snap 到 fixed-point 子像素栅格，所有计算都是整数，因此 watertight、bit-identical。

文章末尾还讨论 scissor rect、MSAA（不规则采样位置在 Pineda 框架里几乎免费）、sliver 三角形的低效、以及为什么硬件不再继续往上堆层级（小三角形固定开销变高、shader 已经是瓶颈）。最后顺带提到 PowerVR 这种 [[tbdr-vs-imr|TBDR]] 架构走的是不同路径——它在所有几何到齐后做 binning，与桌面 GPU 的「sort-last」是不同的设计点。

## 关键要点

- **scanline 算法是软件遗物**：在 SIMD 化的硬件上完全敌不过 Pineda 算法。
- **Pineda 算法的关键是「相邻像素 = 一次整数加法」**：所有大乘法只在 setup 里算一次，光栅化主体只剩并行加法器。
- **2 层就够**：fine + coarse 两层在桌面 GPU 上是甜点；继续往上堆会让小三角形固定开销变高。
- **fixed-point 顶点 = watertight rasterization**：这是相邻三角形不漏不重的根本——评论区 ryg 跟一位读者长篇辩论 T-junction 为什么必然导致 seam。
- **sliver 是硬件 GPU 的痛点**：直到今天，HW 厂商仍反复提醒别画细长三角形——分层光栅化也救不了。
- **fill rule 在边方程框架下几乎免费**：top-left 规则只需要在 `c` 项上减 1，对比 Hecker 的软件 scanline 做法是降维打击。

## 链接到的概念

- [[pineda-edge-rasterization]]
- [[hierarchical-rasterization]]
- [[triangle-setup]]
- [[rasterization]]
- [[rendering-pipeline]]
- [[triangle-primitives]]
- [[tbdr-vs-imr]]
- [[fabian-giesen]]

## 原文

- 链接：https://fgiesen.wordpress.com/2011/07/06/a-trip-through-the-graphics-pipeline-2011-part-6/
- 本地：`raw/articles/fgiesen.wordpress.com/2011-07-06_a-trip-through-the-graphics-pipeline-2011-part-6.md`
