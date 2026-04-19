---
tags: [source, chipsandcheese, 图像压缩, 编解码]
date: 2026-04-19
sources: 1
---

# Modern Data Compression in 2021 Part 1（BlueSwordM / Chips and Cheese）

[[blueswordm]] 2021 年 1 月发表于 [[chips-and-cheese]] 的图像压缩入门系列第一篇，主线是 JPEG 的历史地位与编码管线的拆解，为后续对比 JPEG2000 / WebP / HEIF / AVIF / JPEG XL 做铺垫。

## 摘要

文章先用两段篇幅界定了编码/解码/codec 三个术语，以及有损 vs 无损的基本分类。接着按时间线梳理了 1992 年 JPEG 出现之前的业界手段：降分辨率、减色、RGB→YCbCr、chroma 降采样；指出这些手段在高分辨率时代失效，是 JPEG 出现的直接压力。主体部分剖开 [[jpeg-codec-pipeline|JPEG 的三段式编码流程]]：色彩空间变换与 chroma 子采样、8×8 分块 DCT 与量化、Z 字扫描加 Huffman 熵编码。末尾列出 JPEG 之后的主要后继者（PNG、JPEG2000、WebP、HEIF），并点名 JPEG XL 与 AVIF 是最有希望挑战 JPEG 的新一代编码标准，留作下一篇详细对比。

## 关键要点

- **人眼对亮度比色度敏感**——因此 YCbCr + chroma 降采样是几乎所有感知编码器的第一步。
- **8×8 DCT + 量化** 是有损的唯一来源；量化矩阵对高频项施加更大除数，把稀疏的高频系数压成 0。
- **熵编码（Huffman）是无损**，负责把前两步的稀疏表示打包紧凑；现代编码器把这一步换成算术编码再拿一截收益。
- JPEG 的 30 年统治力来自 **解码成本接近 0 + 画质/体积比够好**，挑战者要同时赢压缩比和部署成本。
- 2021 年视角下，**JPEG XL**（JPEG 委员会自己搞的后继者）与基于 AV1 的 **AVIF** 是最可能的继任者。

## 链接到的概念

- [[jpeg-codec-pipeline]]
- [[planar-rotation-dct]]
- [[adaptive-arithmetic-coding]]
- [[color-space]]

## 原文

- 链接：https://chipsandcheese.com/p/modern-data-compression-in-2021-part-1-a-simple-overview-on-the-art-of-image-encoding
- 本地：`raw/articles/chipsandcheese.com/2021-01-30_modern-data-compression-in-2021-part-1-a-simple-overview-on.md`
