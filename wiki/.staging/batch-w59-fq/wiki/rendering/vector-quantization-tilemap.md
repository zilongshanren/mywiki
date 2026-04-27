---
tags: [image-compression, vector-quantization, k-means, tilemap, retro]
date: 2026-04-19
sources: 1
---

# 图像向量量化 = 生成瓦片图

**向量量化**（Vector Quantization, VQ）把图像切成 B×B 的小块，再把每块当成 `B·B·C` 维空间里的一个向量，用 [[color-quantization-kmeans|K-Means]] 等聚类算法压到一个 `num_codes` 大小的 *codebook*（码本）；图像本身就变成一张「把每个位置指向码本索引」的 **tilemap**。[[pekka-vaananen]] 在 *Image vector quantization is just like creating a tilemap* 里用一张 SMB3 标题画面演示了全过程：这正是 Game Boy、NES 这类硬件没有位图模式、只能用瓦片表 + 瓦片索引显示画面的原理；很多 VQ-based 视频编码（以及经典 Command & Conquer 的 VQA 格式）解码快到硬件都能实时跑，就是这个道理。

## 核心流程

1. **切块并展平**：`im.reshape(bh, B, bw, B, 3).transpose(0, 2, 1, 3, 4).reshape(-1, D)`，得到 `[N × D]` 的向量矩阵，其中 `D = B·B·3`。这套 reshape 技巧见 [[numpy-tile-reshape-trick]]。
2. **聚类**：`KMeans(n_clusters=num_codes).fit(X)`。`cluster_centers_` 就是码本（每行一块 B×B·3 的代表图块），`predict(X)` 给出每块在码本里的索引。
3. **解码**：`decoded = codebook[codes]` 按索引把块取回，再反操作 reshape 回 `[H × W × 3]`。

## 关键视角

- VQ 和调色板量化的区别：**调色板**把单像素 RGB 聚到 `N` 种颜色（`D=3`）；**VQ** 把整个块聚类（`D` 可以是几百），压缩率 = `N / num_codes`，结构重复得越厉害压得越狠。
- 压缩比仅算码本，真实开销还要加上 `codes` 索引数组（`⌈log₂ num_codes⌉` bit × N 块）。
- 结果之所以像 NES pattern table，是因为我们做的就是现代版的「为这张图自动生成瓦片表」，只不过 NES 的瓦片表是艺术家手工拆的。

## 改进方向（原文提到的）

- 把块大小 `B` 换成 4 或 16，在码本容量与块多样性间权衡。
- 在 **LAB / [[oklab-color-space|OkLab]]** 空间做距离，减少感知误差。
- 对 `codes` 做熵编码/游程编码，进一步压缩索引。
- 码本按亮度排序会让索引图在局部更平滑，利于后续压缩。

## 相关

- [[color-quantization-kmeans]] —— 单像素粒度的 K-Means
- [[color-quantization-retro]]
- [[numpy-tile-reshape-trick]] —— 本文依赖的块切分技巧
- [[pca-image-compression]]

## Sources

- [[sources/30fps-image-vq]]
