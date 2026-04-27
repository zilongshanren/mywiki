---
tags: [source, rendering, depth-buffer, opengl, precision]
date: 2026-04-27
sources: 1
---

# Logarithmic Depth Buffer Optimizations & Fixes（Outerra）

[[people/outerra-team]] 发表于 2013 年 7 月的更新文章，对早期对数深度缓冲实现进行精炼，修正若干边界情况并提升着色器效率。

## 摘要

文章给出精炼后的顶点着色器方程：`gl_Position.z = log2(max(1e-6, 1.0 + gl_Position.w)) * Fcoef - 1.0`，其中 `Fcoef = 2.0 / log2(farplane + 1.0)`。相比 2012 年版本，三处改动：将 `log` 换成 `log2`（GPU 内部用 log2 指令，避免额外乘法）；以 `max(1e-6, ...)` 钳制输入，修复顶点恰好越过摄像机近平面时整个三角形被意外裁剪的 bug；明确说明使用 `gl_Position.w`（MVP 后等于摄像机空间正深度），不再需要额外计算。透视插值误差的修复方式同样更新：传出 `flogz = 1.0 + gl_Position.w`，片段着色器写 `gl_FragDepth = log2(flogz) * Fcoef_half`。

## 关键要点

- 用 `log2` 替代 `log`，消除一次乘法指令。
- `max(1e-6, ...)` 钳制是修复"长三角形穿摄像机近平面被整个丢弃"bug 的最简方案。
- 精炼后移除了 C 参数（实践中精度余量充足，C=1 已足够）。
- `gl_Position.w` 在标准投影后直接等于摄像机深度，无需额外变换。
- 片段深度写使用 `Fcoef_half = 0.5 * Fcoef` 避免乘法。

## 链接到的概念

- [[logarithmic-depth-buffer]]
- [[z-buffer]]
- [[conservative-depth]]

## 原文

- 链接：https://outerra.blogspot.com/2013/07/logarithmic-depth-buffer-optimizations.html
- 本地：`raw/articles/outerra.blogspot.com/2013-07-18_logarithmic-depth-buffer-optimizations-fixes.md`
