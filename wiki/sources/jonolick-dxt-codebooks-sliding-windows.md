---
tags: [source, rendering, texture-compression, dxt, lzma]
date: 2026-04-14
sources: 1
---

# DXT Compression, Codebooks and Sliding Windows（Jon Olick, 2013）

[[jon-olick]] 2013 年 2 月写的笔记，记录了他在 Firefall 项目上研究 DXT 纹理磁盘压缩的初始实验。

## 摘要

目标：**无损**地把已有 DXT 纹理在磁盘上再压一轮（因为 DXT 本身已经有块状伪影，不想再叠一层有损）。Olick 对三种方案做了基线对比：原始 DXT + LZMA、对 DXT 数据做 transpose（端点与选择位分离聚簇）后 LZMA、颜色线走 Golomb + DPCM 而选择位走原始 bit 后 LZMA。多数纹理上 transpose 方案胜出。帖子的主干是对 **Zeng codebook 优化** 与 **sliding-window codebook** 两种经典字典压缩手法的梳理，以及 Olick 自己的扩展：把滑窗转义位用来显式指定新条目的插入位置，从而既能像 Zeng 那样重排码表，又能掌控条目的生命周期。文末起点约 3 bpp，留悬念。

## 关键要点

- 三基线：原始 LZMA、transpose LZMA、Golomb+DPCM+raw selectors LZMA；transpose 最常胜。
- Zeng 重排调色板以减小相邻像素 delta → delta 编码 + Golomb 高效。
- Sliding-window codebook：码表 > 256 但索引仍 8 bit，第 256 项作转义。
- 作者新增：第 256 项带位置字节，允许非贪心码表优化 + 控制条目存活时间。
- 参考 crunch（Rich Geldreich）的相关演讲 PDF。

## 链接到的概念

- [[jon-olick]]
- [[dxt-codebooks-sliding-window]]
- [[dxt-entropy-reduction]]

## 原文

- 链接：https://www.jonolick.com/home/dxt-compression-codebooks-and-sliding-windows
- 本地：`raw/articles/jonolick.com/2013-02-07_dxt-compression-codebooks-and-sliding-windows.md`
