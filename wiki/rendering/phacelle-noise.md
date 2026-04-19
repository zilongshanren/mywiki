---
tags: [rendering, noise, procedural, shader, directional-noise]
date: 2026-04-19
sources: 1
---

# Phacelle Noise

Phacelle Noise 是 [[rune-skovbo-johansen]] 于 2026 年公开的一种**方向性噪声**（directional noise），名字是 *phase* 与 *cell* 的合成词。它在功能上与 Phasor Noise / Gabor Noise 相近——都用于生成沿指定方向走向的条纹（stripes），每个像素可单独求值——但实现思路更简单、采样更少、API 更友好。作者提出它时主要用于山体侵蚀的 gully 图案生成，后又将这段代码独立为可复用的噪声函数。

## 核心思路

把每一个条纹 kernel（即"splat"）同时当作一对余弦波与正弦波求值并插值。由于 `(cos, sin)` 本身是单位圆上的点，插值结果可被看作是一个二维向量，其长度因 kernel 相位不一致而塌缩小于 1——直接把这个向量 **归一化** 后再取 atan2 就能恢复出相位，继而套用方波、三角波、锯齿波等任意 profile。作者把这一层认知当作 Phacelle 相比前身（[[worley-voronoi-noise|Voronoi]]、Gabor、clayjohn 的 `erosion` 函数、Fewes 的 Terrain Erosion Noise）的最关键跨越。

## 两个变种

- **Simple Phacelle Noise**：把"每像素的条纹方向"作为**函数参数**传入——所有 kernel 在该点处共享同一方向，不同位置的方向来自方向场 `f(pos)`，像素内每个 kernel 只差相位。每像素只需采样方向场 1 次。
- **Sampled Phacelle Noise**：每个 kernel 各自在其中心处采样方向场一次（每像素 16 次），对方向场剧变区域更平滑，但失去了"自包含函数"的简洁性。

作者承认 Simple 变种其实也是 Phasor 论文图 20 所用的"trick"——Phasor 第一作者 Tricard 称之为 *ghost knowledge*（藏在圈内却未写入论文的知识）。作者的立场是：当输入方向场变化比波长更快时（例如山峰附近），两者输出差异显著，而且这才是它的**主要用法**而非 trick。

## 与 Phasor Noise 的差异

| 维度 | Phasor (Chermain 修正版) | Simple Phacelle | Sampled Phacelle |
| --- | --- | --- | --- |
| 每像素内循环 | 3×3×16 = 144 | 4×4 = 16 | 4×4 = 16 |
| 方向场采样/像素 | 144 | **1** | 16 |
| 每 cell 的 splat 数 | 多个 | 1 | 1 |
| 权重函数 | 高斯（不归零） | 减去常数使其在 cell 边界归零 | 同左 |
| 链式调用可行性 | 需 buffer | 直接嵌套 | 需 buffer |

Phasor 作者的最终评语是："视觉上相似但更便宜；没有频域保证（这在纹理合成/各向异性过滤里很重要）；若要发表会是技术选择讨论（类似 JCGT / Graphics Gems 的定位），但不算新方法。"作者对此坦然接受——他本就不打算发表。

## 可读性主张

作者在博文末尾借 Phacelle 的实现发起了一次对 Shadertoy 文化的抱怨：变量名单字母、无注释、把实现和展示代码混在一起，使得别人几乎无法复用。他自己的两份 Shadertoy 使用了描述性变量名和大量注释，宣称这本身就足以让"方法+实现"有独立命名的价值。这与 [[john-ousterhout]] 在 *A Philosophy of Software Design* 里关于注释、命名、[[deep-modules|深模块]]的主张一脉相承。

## 相关

- [[erosion-filter-procedural]] — Phacelle Noise 最初脱胎于这里
- [[worley-voronoi-noise]] — "4×4 moving window of cells" 的思想来源
- [[directional-noise]] — 方向性噪声这一类技术的总览
- [[turbulence-domain-warping]]

## Sources

- [[sources/runevision-phacelle-noise]]
