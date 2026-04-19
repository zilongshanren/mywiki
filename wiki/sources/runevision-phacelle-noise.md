---
tags: [source, rendering, noise, procedural, shader, 2026]
date: 2026-04-19
sources: 1
---

# Rune Skovbo Johansen - Phacelle: Cheap Directional Noise

[[rune-skovbo-johansen]] 于 2026 年 1 月 22 日发布的噪声技术笔记。文章在发布后不久经 Phasor Noise 两位作者（Thibault Tricard 与 Fabrice Neyret）参与的 Discord 讨论，新增了一大段"Phacelle 与 Phasor 到底有何差异"。

## 摘要

为了做山地侵蚀滤波器，作者发展出一种**便宜的方向性噪声**——Phacelle Noise（phase + cell）。核心洞察是：把每个 kernel 当作 (cos, sin) 双通道同时插值，结果可被视为单位圆上的向量；对插值后的向量做归一化就能恢复出相位，进而产生方波/三角波/锯齿波等任意条纹形状，同时保证幅度恒为 1。作者提供两个变种：Simple Phacelle（方向场作函数参数，每像素采样 1 次，循环 16 次）、Sampled Phacelle（每 cell 自采样方向场，每像素 16 次）。相比 Phasor 的 144~400 次内循环，Phacelle 显著便宜，也提供了更干净的 API。Phasor 作者承认 2D 效果相似但"没有 Phasor 的频域保证"；作者本就不打算发表，只想要一个命名和可复用实现。

## 关键要点

- **(cos, sin) 双通道 → 单位圆向量 → 归一化 → 相位**：这是全篇最重要的一步，它把"插值后振幅塌缩"变成"恒定振幅 1 + 任意 profile"的能力。
- **方向场采样位置**决定了变种：每像素一次（Simple）还是每 splat 一次（Sampled）。
- **每 cell 单 splat** + 4×4 窗口即可，而 Phasor 通常每 cell 多 splat × 5×5 或 3×3 窗口。
- **权重函数归零**：`exp` 减去一个常数让 cell 边界处权重真正到 0，消除 grid-aligned 伪像（Phasor 的高斯权重不归零）。
- **链式可组合**：Simple 版不需要中间 buffer，可把方向场的结果直接接到下一层，复杂度线性增长；Phasor 做不到这一点。
- 被 Phasor 作者评为"是技术选择讨论而非新方法"——可投 JCGT/Graphics Gems 类期刊。
- 作者借机吐槽 Shadertoy 的 *代码混乱无注释、实现与展示混在一起* 的文化。

## 链接到的概念

- [[phacelle-noise]]
- [[directional-noise]]
- [[erosion-filter-procedural]]
- [[worley-voronoi-noise]]
- [[classic-shader-noise]]
- [[turbulence-domain-warping]]

## 原文

- URL：https://blog.runevision.com/2026/01/phacelle-cheap-directional-noise.html
- 本地：`raw/articles/blog.runevision.com/2026-01-22_phacelle-cheap-directional-noise.md`
- 同期重复抓取 skip：`2026-01-22_runevision-blog.md`（月页），`2026-01-22_runevision-blog-2.md`（归档页）
