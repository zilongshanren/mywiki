---
tags: [source, rendering, texture-compression, dxt, lzma]
date: 2026-04-14
sources: 1
---

# DXT compression - part 3 - Transposes（Jon Olick, 2013）

[[jon-olick]] 的 DXT 压缩系列第 3 篇（由 Bryan McNett 供稿），发表于 2013 年 7 月。

## 摘要

本篇继续 Firefall 的 DXT 纹理磁盘压缩优化，讨论对 DXT 数据做不同维度 **transpose**（行列重排、端点与选择位分离等）在 LZMA 二次压缩上的效果。抓取到的正文只有一段导语——实际数值与结论通过 [[jonolick-dxt-part4-entropy|Part 4]] 的回顾才能确认：**在 Part 2 的基线 2.28 bpp 上，各种 transpose 方案只能把码率拉到 2.25 bpp，改动收益极小**。这是典型的"这条路走不通"的小结，也正是让 Olick 在后续 Part 4 转向 selection bits 熵压缩的直接动机。

## 关键要点

- 原文抓取不完整（本文仅存简介段）——**数据缺口**，详细对比需参考 Part 4 的追述。
- Transpose 思路虽直觉上能把同类数据聚簇利于 LZ 字典复用，但实测增益只有 ~0.03 bpp。
- 转折点：这验证了单靠数据布局无法突破，需要直接对选择位降熵（Part 4）。

## 链接到的概念

- [[jon-olick]]
- [[dxt-codebooks-sliding-window]]
- [[dxt-entropy-reduction]]

## 原文

- 链接：https://www.jonolick.com/home/dxt-compression-part-3-transposes
- 本地：`raw/articles/jonolick.com/2013-07-16_dxt-compression-part-3-transposes.md`
