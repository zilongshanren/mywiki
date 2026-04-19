---
tags: [图像处理, 误差扩散, halftone, 结构保留, dither]
date: 2026-04-14
sources: 1
---

# Laplacian 结构感知误差扩散

一种在 [[floyd-steinberg-dithering|Floyd–Steinberg 误差扩散]] 基础上改进的半色调（halftoning）算法，2010 年提出，[[jon-olick|Jon Olick]] 在为某个**二值 mask 内部用途**寻找合适 halftone 方案时重新发现。它属于"把灰度图转为黑白二值图同时尽量保留结构"这一长期问题的现代解。

## 核心思路

经典 Floyd–Steinberg 仅根据**量化误差**做扩散，对均匀纹理和低对比度结构容易糊掉。Laplacian-based Structure-Aware 的改进点是：在扩散误差之前，**用 Laplacian 算子提取局部结构信息**（边缘、纹理走向），让误差扩散的方向和权重根据结构自适应调整——也就是说算法"知道"当前邻域里有没有值得保留的几何特征，而不是盲目地按固定 7/3/5/1 权重往右下倒。

## 效果

在当年的评测中：

- **MSSIM 结构相似度在低对比度区域提升约 25%**；
- 典型案例里蜗牛壳这种细纹理被其他算法糊掉，而这个方法能完整保留；
- 计算开销与基础 error diffusion 同一量级，比当年一些基于优化求解的 halftoning 快好几个数量级。

这让它成为"想要比 Floyd–Steinberg 好、但不想跑到 optimization-based 算法那种成本"的一个务实中间点。相比 Jon Olick 此前试过的 **Structure-Aware Error Diffusion**（效果好但慢），Laplacian 版本以基本相同的速度拿到了接近的质量。

## 和其他 dither 系方法的关系

这属于"把低频可见误差搬到高频不可见频段"思路的结构感知版本，和 [[dither-alpha-clipping|alpha dither]]（解决透明度离散化）、[[color-banding|颜色色带 dither]]（蓝噪声打破条带）共享同一个信号处理直觉，但目标是**二值/调色板输出下的结构保留**，不是连续色彩下的 banding 抑制。

## Sources

- [[sources/jonolick-laplacian-error-diffusion]]
