---
tags: [渲染, 光栅化, GPU, 算法]
date: 2026-04-14
sources: 1
---

# Pineda 边方程光栅化

「现代 GPU 怎么把一个三角形变成像素」的算法答案，几乎都源自 **Juan Pineda 1988 年的论文**——一种基于边方程的、整数加法器友好、自然并行、容易写硬件的光栅化方法。它取代了软件时代盛行的 [[scanline-rasterization|scanline 增量算法]]（Chris Hecker 的纹理映射系列），成为今天所有桌面 GPU 的事实标准。

## 基本观察

一个 2D 三角形的内部，是「点同时位于三条边的同侧」的所有点。每条边可以写成线性方程

```
E(x, y) = a·x + b·y + c
```

`E` 的符号告诉你点在边的哪一侧。三角形内部 = `E₀ ≥ 0 ∧ E₁ ≥ 0 ∧ E₂ ≥ 0`（具体不等式方向由顶点顺序决定）。

## 增量结构

在 `(x, y)` 上一旦算出三个 `E` 的值，向右走一格只是 `E += a`，向下走一格只是 `E += b`。这意味着覆盖测试 = **整数加法 + 取符号位**——再没有比这更便宜的硬件了。乘法只在每个三角形开始时算一次（这正是 [[triangle-setup|triangle setup]] 做的事）。

## 天然 SIMD

要把一个 8×8 像素块整体测试，只需要：

1. 算出左上角的 `(E₀, E₁, E₂)`；
2. 把三个 `(a·dx + b·dy)` 步进表预先准备好；
3. **64 个并行加法器** 同时做 64 次加；
4. 取每个结果的符号位 → 64-bit 覆盖掩码。

这比 scanline 算法对硬件友好得多——后者在 `x` 和 `y` 方向不对称、不容易 SIMD、quad（2×2）分组也不自然。Pineda 算法天然就是按块工作的。

## 整数 + 子像素 = 完美严密

之所以前一阶段（geometry processing）要把顶点 snap 到 fixed-point 子像素栅格：snap 之后所有边方程都是整数运算，**没有浮点舍入**，意味着两个共享边的三角形的覆盖结果可以做到位级一致。所谓「watertight rasterization」就是这么来的。

## Top-left 填充规则

为了避免共享边被双绘或漏绘，D3D 和 OpenGL 都采用 **top-left 规则**——靠 `c` 项上 `−1` 这种小修正即可在 Pineda 框架里干净实现。Hecker 当年要在 scanline 算法里手动处理的边界 case，在边方程算法里几乎是免费的。

## MSAA 也不再难

不在规则栅格上的多采样位置（jittered MSAA pattern）对 scanline 算法是噩梦——但在 Pineda 算法里只是「每个 pixel 多算几个 `E` 偏移、取符号」，硬件上几乎免费。

## 局限：sliver 三角形

Pineda 算法对长条形（sliver）三角形效率很差：你要遍历大量 8×8 块，每块只覆盖几个像素。这是 GPU 厂商至今仍在反复提醒「不要画 sliver」的根源。改善只能靠 [[hierarchical-rasterization|coarse rasterization]] 在前面 cull 掉空 tile。

## 相关

- [[rasterization]]
- [[triangle-setup]]
- [[hierarchical-rasterization]]
- [[triangle-primitives]]
- [[rendering-pipeline]]
- [[fabian-giesen]]

## Sources

- [[sources/ryg-trip-through-graphics-pipeline-2011-part-6]]
