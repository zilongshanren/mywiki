---
tags: [source, 渲染, 算法, shader]
date: 2026-04-14
sources: 1
---

# Mini: JFA（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2023 年 5 月的一篇短文，讲**用 Jump Flooding Algorithm 给贴图生成距离场**。是 GM Shaders Mini 系列里非常实用的一期——用一张普通 RGBA8 surface 就能跑，直接可用于描边、光晕、软阴影一类效果。

## 摘要

JFA 是一种多趟 GPU 算法：每一趟以指数缩小的步长（64 → 32 → 16 → … → 1）采 3×3 邻域，把「离最近不透明像素的相对偏移」沿着样本的样本传播出去。总 pass 数是 `log2(max_radius)`，每趟每像素只读 9 个 texel，非常适合 [[fragment-shader|fragment shader]] 的工作模型。Xor 的实现把偏移压进 RG 通道的 `[-127,+128]` 范围，alpha 顺便存一份反距离。完整示例在 [GM_JFA](https://github.com/XorDev/GM_JFA) 仓库。

## 关键要点

- **对数趟数**：`log2(N)` 次 pass 覆盖任意半径，每趟 9 个样本，纯并行。
- **3×3 × 指数步长**：第一趟 jump=大值，每趟减半，直到 1。信息传播距离每趟翻倍。
- **RG 编码偏移**：`(offset + 127) / 255`，普通 RGBA8 就能跑，代价是最大半径 127 texel。
- **用途**：描边、光晕、软阴影假效果、2D SDF 字体、UI 圆角、流体边界。
- **对比 8SSEDT**：8SSEDT 精度更高但是串行的扫描算法，不适合 GPU；JFA 精度稍差但天然并行。
- 变种：`JFA+1`、`1+JFA` 修正边界漏点；可以用浮点 surface 突破半径限制。

## 链接到的概念

- [[jump-flooding-algorithm]]
- [[fragment-shader]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/gm-shaders-mini-jfa
- 代码：https://github.com/XorDev/GM_JFA
- 本地：`raw/articles/mini.gmshaders.com/2023-05-19_mini-jfa.md`
