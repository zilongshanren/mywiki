---
tags: [source, rendering, g-buffer, 法线编码, 延迟渲染]
date: 2026-04-27
sources: 1
---

# Notes on G-Buffer Normal Encodings（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2015 年 1 月的技术笔记，系统梳理 G-Buffer 法线编码在四个维度上的矛盾：速度（shader 开销）、紧凑性（位数）、可混合性（硬件 blend for 像素 shader decals）、以及稳定性/精度。

## 摘要

文章开门见山地指出，没有任何一种编码能同时满足全部四个目标，必须在其中做取舍。作者详细分析了眼空间（view-space）两通道编码的精度缺陷——量化噪声在视角移动时表现为可见抖动——并提出两种改良路线。第一种是编码空间优化：利用等面积投影（Lambert azimuthal equal-area）、encode-space 裁剪、圆盘到正方形的映射等技巧，在有限位数下提升精度分布。第二种是多基底（multiple bases）方案：来自 Alex Fry（Frostbite）的思路，在 G-Buffer 中用少量 bit（2–4 bit）记录当前像素选用的切线空间基底，解码 decal 时读取这几位以决定投影空间，从而既保留硬件可混合性，又获得比单一视空间编码更高的精度。评论区补充了 Activision/Black Ops 3 的实际落地情况：最终使用 2 bit + Lambert 投影，配合 TAA 蓝噪声 dither 消除 shiny 表面量化条带。

## 关键要点

- 八面体（octahedral）编码与 Crytek best-fit normals 是紧凑性最优的两种方案，但两者均不支持硬件 blend
- view-space 两通道编码的抖动根源是：量化法线精度与 view-to-world 矩阵精度在逐帧变化中相互"打架"
- 每像素使用视向量作为编码空间 z 轴可消除抖动，但计算开销大
- multiple tangent bases 方案的关键洞察：decal 混合时可以只读不写那几个 basis-selection bit，decal 法线只需在选定 basis 里做混合
- 以几何法线（而非 normal-map 后的法线）做 basis 选择是工程上的合理近似

## 链接到的概念

- [[compact-normal-encoding]]
- [[deferred-rendering]]
- [[tangent-space-normal-mapping]]
- [[normal-decal-edge-blending]]

## 原文

- 链接：https://c0de517e.blogspot.com/2015/01/notes-on-g-buffer-normal-encodings.html
- 本地：`raw/articles/c0de517e.blogspot.com/2015-01-24_notes-on-g-buffer-normal-encodings.md`
