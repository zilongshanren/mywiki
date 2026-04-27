---
tags: [source, numpy, performance, image-processing, notebook]
date: 2026-04-19
sources: 1
---

# Efficiently split a NumPy array into tiles（Pekka Väänänen / 30fps.net）

[[pekka-vaananen]] 2024 年 11 月 notebook，讨论把图像切成 `B × B` 瓦片的最快写法——两行 reshape + transpose 比 for 循环快 1000×，比 scikit-image 的 `view_as_blocks` 还快 15×。

## 摘要

朴素双重 for 循环切图在大图上慢得离谱；作者给出的最优解是 `img.reshape(bh, B, bw, B, C).transpose(0, 2, 1, 3, 4)`，得到 `[bh, bw, B, B, C]` 的**无拷贝 view**。关键是 reshape 必须先拆"行轴 + 列轴"再 transpose 把块坐标挪前面；如果直接 `reshape(bh, bw, B, B, C)` 会得到 64×1 切片而非方块，因为 NumPy 默认按 C-order 存数据。scikit-image 的 `view_as_blocks` 内部用 `np.lib.stride_tricks.as_strided`，逻辑上也是零拷贝，但跨步非连续导致下游任何 reshape 都会隐式拷贝，实际反而慢。作者附上逆操作 `merge_tiles_to_image` 和转换成 `[N × D]` 向量矩阵的写法——正是 [[vector-quantization-tilemap]] 的输入。

## 关键要点

- 真正的速度来自 **C-contiguous reshape 能复用原指针**，这是 `as_strided` 做不到的。
- 返回是 view，想写必须 `.copy()`。
- H/W 不是 B 的整数倍要先裁边。
- 同一 trick 适合 batched image tiling、卷积的 im2col 等下游操作。

## 链接到的概念

- [[numpy-tile-reshape-trick]]
- [[vector-quantization-tilemap]]

## 原文

- 链接：<https://30fps.net/notebooks/split-to-tiles>
- 本地：`raw/articles/30fps.net/2024-11-07_efficiently-split-a-numpy-array-into-tilesp.md`
