---
tags: [source, graphics, image-compression, vector-quantization, notebook]
date: 2026-04-19
sources: 1
---

# Image vector quantization is just like creating a tilemap（Pekka Väänänen / 30fps.net）

[[pekka-vaananen]] 2023 年 4 月的 Jupyter notebook，用 `sklearn.KMeans` 把一张 SMB3 标题画面压成"瓦片图 + 瓦片表"，借此讲清向量量化（VQ）与老主机的瓦片图硬件之间的血缘关系。

## 摘要

Game Boy / NES 没有位图模式，只能靠 pattern table + tilemap 组织画面；任何做 VQ-based 视频编码（如经典 C&C 的 VQA 格式）的人其实是在做"自动生成瓦片表"。notebook 把 RGB 图切成 8×8 块，每块展平成 192 维向量，喂给 `KMeans(n_clusters=180)`——`cluster_centers_` 就是码本（瓦片集），`predict` 输出就是瓦片图索引。解码 `codebook[codes]` 后再 reshape 回图像。重点并不在新算法，而是把 VQ 与复古硬件、现代 ML 聚类接到一条直觉线上。作者列出若干优化：换感知色彩空间、码本按亮度排序便于压缩、索引做熵编码、块大小权衡。

## 关键要点

- VQ 是"块级量化"，调色板量化是"像素级量化"，同一家族不同粒度。
- 压缩比 ≈ `N_blocks / num_codes`，真实开销要加索引体积。
- 块切分用 reshape + transpose 技巧实现，详见 [[numpy-tile-reshape-trick]]。
- 码本排序对索引图的局部性有影响，影响下游熵编码效率。

## 链接到的概念

- [[vector-quantization-tilemap]]
- [[color-quantization-kmeans]]
- [[numpy-tile-reshape-trick]]
- [[color-quantization-retro]]

## 原文

- 链接：<https://30fps.net/notebooks/image-vq>
- 本地：`raw/articles/30fps.net/2023-04-30_image-vector-quantization-is-just-like-creating-a-tilemapp.md`
