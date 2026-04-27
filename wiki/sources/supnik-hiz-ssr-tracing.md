---
tags: [source, rendering, ssr, hiz, screen-space-reflections]
date: 2026-04-27
sources: 1
---

# A Tip for HiZ SSR - Parametric 't' Tracing（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 发表于 2020 年 10 月的技巧文章，讲解如何用参数变量 `t` 重构 Hi-Z SSR 射线追踪以解决精度和方向泛化问题。

## 摘要

Hi-Z SSR 的原始实现在 Z 空间里参数化射线——近裁剪面为 0、远处为 1。这带来三个问题：反转浮点 Z（reverse-float Z）下精度在起点处最差；算法假设射线向远处飞，不支持近角度（如俯视水坑）；无法穿越遮挡体。Supnik 提出改用归一化参数 `t`：射线起点始终为 t=0，终点始终为 t=1，与 Z 的实际方向无关。好处是三重合一：起点精度最高（t 值小）、完全不需要条件分支来区分正负 Z 方向、还可以用 min-max Z 缓冲区里的 t 范围重叠测试来穿越遮挡体。

## 关键要点

- Hi-Z SSR 把深度图存成 mip chain，每层用 max 降采样；每次 march 可跳过无遮挡区域，从 O(N) 降为 O(logN)
- 原始 Z 参数化在 reverse-float Z 下会在 march 起点制造大量精度错误
- 参数 `t`（归一化到 [0,1]）让「近」始终高精度，且不需要关心 Z 方向的正负
- `t` 参数化同时支持向相机方向和远离相机方向的 march，免除循环内分支
- 遮挡穿越：将 min-max Z 转换为 min-max t，检测区间重叠即可
- GPU Pro 5 中的原始章节因样本代码缺失而难以理解

## 链接到的概念

- [[hierarchical-z-buffer]]
- [[screenspace-reflections]]
- [[reversed-z]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2020/10/a-tip-for-hiz-ssr-parametric-t-tracing.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2020-10-21_a-tip-for-hiz-ssr-parametric-t-tracing.md`
