---
tags: [source, rendering, depth-buffer, opengl, precision]
date: 2026-04-27
sources: 1
---

# Maximizing Depth Buffer Range and Precision（Outerra）

[[people/outerra-team]] 发表于 2012 年 11 月的长文，系统讨论如何让深度缓冲同时支持草叶级近平面精度与数十公里级远平面精度，以行星引擎 Outerra 为应用场景。

## 摘要

文章首先分析标准投影矩阵产生的 `a - b/z` 深度函数为何浪费大量精度：近平面附近消耗约一半缓冲范围，四个数量级后精度进入不可用区间。理想的深度函数应对数分布（导数正比于 1/z）。文章依次评估三条路线：（1）反转深度范围（Reversed-Z）配合 32 位浮点缓冲，在 DirectX 上有效，OpenGL 因 NDC 偏置需要 `glDepthRangedNV` 扩展（NVIDIA 专用）；（2）对数深度缓冲（Logarithmic Depth Buffer），顶点着色器直接输出对数值，可用于所有厂商硬件；（3）优化的对数缓冲，通过 C 系数线性化近平面区间避免片段着色器写深度的性能代价，配合 `ARB_conservative_depth` 恢复部分 Early-Z。

## 关键要点

- 标准 32 位浮点 reversed-Z 在 DirectX/Vulkan 下精度约等于 24 位对数深度缓冲；32 位对数缓冲约好 20 倍。
- OpenGL 的 NDC z ∈ [-1,1] 引入 0.5 偏置，锁死浮点指数，令 reversed-Z 在 OpenGL 上不起作用（AMD/Intel 无 `NV_depth_buffer_float` 扩展）。
- 对数深度缓冲顶点着色器一行代码可启用：`gl_Position.z = 2.0*log(gl_Position.w*C+1)/log(far*C+1)-1; gl_Position.z *= gl_Position.w;`
- C 系数控制近平面线性化宽度（C=0.01 约 10 米），可省略片段写深度。
- 保守深度（`depth_less` hint）原理上可节省 Early-Z 代价，但在 Outerra 实测中 speedup 不显著。
- 16 位对数深度缓冲足以覆盖行星尺度，24 位可达宇宙尺度。

## 链接到的概念

- [[logarithmic-depth-buffer]]
- [[reversed-z]]
- [[z-buffer]]
- [[conservative-depth]]

## 原文

- 链接：https://outerra.blogspot.com/2012/11/maximizing-depth-buffer-range-and.html
- 本地：`raw/articles/outerra.blogspot.com/2012-11-28_maximizing-depth-buffer-range-and-precision.md`
