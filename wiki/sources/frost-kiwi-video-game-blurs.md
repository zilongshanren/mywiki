---
tags: [source, rendering, blur, post-processing]
date: 2026-04-19
sources: 1
---

# Video Game Blurs (and how the best one works)（Frost Kiwi / blog.frost.kiwi）

[[frost-kiwi]] 发表于 2025 年 9 月的长文，在一页交互式 WebGL demo 里串起了游戏图形里所有主流模糊算法的来龙去脉——从朴素 Box Blur 一路走到今天主流的 [[dual-kawase-blur]]。

## 摘要

文章以"你手里这台设备上、一个 NEOTOKYO° 场景的 framebuffer"作为共同起点，让读者逐一亲手对比 Box Blur、Gaussian Blur、Separable Gaussian、Kawase、Dual Kawase 的实时性能与视觉结果。每一次算法升级都有明确的工程动机：Box 为什么出方块边缘；Gaussian 为什么"高斯样"；可分离性怎么把 `N²` 的 tap 降到 `2N`；[[bilinear-sample-blur-optimization|双线性采样]] 怎么把 tap 等价于 4 倍 pixel 的隐含平均；Downsampling 怎么用分辨率本身做低通滤波；Kawase 怎么放弃"严格卷积"换来线性 tap 增长；Dual Kawase 又怎么把 Kawase 和金字塔下采样拼起来得到今天绝大多数游戏和合成器实际在跑的算法。全文在"数学理论"与"硬件现实"的张力中前进，也顺带讲了频域 / 低通滤波器、bilinear tap placement、Bloom 的正确做法等一堆旁支知识。

## 关键要点

- Box Blur 视觉差、大 kernel 下性能灾难——但可以用 `samplePosMultiplier`（偏移倍增）以 artifact 换扩散半径。
- Gaussian 的高斯可分离性是 [[separable-gaussian-blur]] 的数学基础；但一旦脱离整像素 tap，"kernel"的概念就变模糊了。
- 低通滤波本质上是[[convolution-separability-blur|频域里砍掉高频分量]]——Box / Gaussian / Kawase / Dual Kawase 在频域曲线上差别很小，视觉几乎等价。
- [[bilinear-sample-blur-optimization|双线性 tap]] 把 4 像素均值压成 1 次硬件采样，是所有"便宜的 Gaussian-like 模糊"的共同技巧。
- 下采样本身就是低通——进入低分辨率 framebuffer 后再用很少的 tap 就能覆盖大半径。
- [[kawase-blur]] 每 pass 只 4 tap，链式 N pass 得到线性增长的半径。Dual Kawase 把它和金字塔下/上采样结合，带宽-质量 tradeoff 几乎是目前最优的。
- 现代游戏 Bloom 不是"阈值 + Gaussian"，而是多级下采样 + 多级加权回加——Dual Kawase 的金字塔结构天然契合。

## 链接到的概念

- [[dual-kawase-blur]]
- [[kawase-blur]]
- [[convolution-separability-blur]]
- [[separable-gaussian-blur]]
- [[bilinear-sample-blur-optimization]]
- [[image-convolution-kernel]]
- [[bloom-threshold-blur-composite]]

## 原文

- 链接：https://blog.frost.kiwi/dual-kawase/
- 本地：`raw/articles/blog.frost.kiwi/2025-09-03_video-game-blurs-and-how-the-best-one-works.md`
