---
tags: [source, chipsandcheese, 图像压缩, jpeg-xl, avif, webp, 编解码]
date: 2026-04-19
sources: 1
---

# Modern Data Compression in 2021 Part 2（BlueSwordM / Chips and Cheese）

[[blueswordm]] 2021 年 2 月发表于 [[chips-and-cheese]] 的图像压缩系列第二篇，承接 Part 1 对 JPEG 管线的介绍，重点对比 JPEG-XL、AVIF（libaom-av1）、WebP（cwebp）和 mozjpeg 的编码质量、速度和多线程能力。

## 摘要

文章从 JPEG 后继者的历史背景出发（JPEG2000、JPEG XT、JPEG XR 均未成功），分析 [[jpeg-xl-format|JPEG-XL]] 和 AVIF 作为下一代标准的技术基础。JPEG-XL 继承了 JPEG 的 DCT 框架但全面升级：可变 DCT 块（4×4 至 256×256）、XYB 感知色彩空间、自适应量化、渐进解码和无损 JPEG 再压缩。AVIF 基于 AV1 视频编码器，带来强大的方向性预测和环路滤波，但由于使用 intra-only 模式（单帧），无法利用运动估计，且 libaom-av1 单线程编码速度比 JPEG-XL 慢约一个数量级。通过多组图像的视觉对比测试，JPEG-XL 在中高 BPP 下综合表现最优；AVIF 在极低 BPP 场景下凭借更少的块状伪影胜出；WebP 基本与 mozjpeg 持平，有损模式优势不明显。

## 关键要点

- **JPEG-XL 解码最快**，渐进解码对网络图像加载友好，多核编码仍有改进空间（当时）
- **AVIF 编码慢**（libaom-av1），但多线程利用率高；极低 BPP 下画质占优
- **WebP 有损部分基于 VP8**，相对 mozjpeg 几乎无优势；无损部分持续优于 PNG
- JPEG-XL 无损重压缩 JPEG：免费压缩约 20%，且可完全还原
- 衡量编码器要同时看：画质、编解码速度、多线程能力、低 BPP 表现

## 链接到的概念

- [[jpeg-xl-format]]
- [[jpeg-codec-pipeline]]
- [[adaptive-arithmetic-coding]]
- [[color-space]]

## 原文

- 链接：https://chipsandcheese.com/p/modern-data-compression-in-2021-part-2-the-battle-to-dethrone-jpeg-with-jpeg-xl-avif-and-webp
- 本地：`raw/articles/chipsandcheese.com/2021-02-28_modern-data-compression-in-2021-part-2-the-battle-to-dethron.md`
