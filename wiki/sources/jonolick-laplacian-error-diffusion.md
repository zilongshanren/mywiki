---
tags: [source, 图像处理, 误差扩散, halftone, dither]
date: 2026-04-14
sources: 1
---

# Laplacian Based Structure-Aware Error Diffusion（Jon Olick）

[[jon-olick|Jon Olick]] 2024 年 8 月的文章，介绍 2010 年的一篇 halftoning 论文《Laplacian Based Structure-Aware Error Diffusion》，他在为某个内部二值 mask 用途挑选算法时重新发现了它。

## 摘要

经典 [[floyd-steinberg-dithering|Floyd–Steinberg]] 误差扩散只看量化误差做固定方向扩散，对低对比度纹理容易糊掉。该算法在扩散前用 **Laplacian 算子提取局部结构信息**，让误差的扩散方向与权重根据边缘/纹理结构自适应，从而在二值化输出下更好地保留细节。论文评测显示，它在低对比度区域的 **MSSIM 提升约 25%**，计算开销与基础误差扩散同数量级，比当年基于优化求解的 halftoning 快几个数量级；视觉对比上，像蜗牛壳细纹这种其他算法会糊掉的结构能被完整保留。对 Jon Olick 来说，它是"比 Floyd–Steinberg 好、但不想付 optimization-based 成本"的合适中间点；相比更早试过的 Structure-Aware Error Diffusion（效果好但慢），Laplacian 版本在基本同速下接近同等质量。

## 关键要点

- Halftoning 问题：把灰度图转成二值/调色板图的同时尽量保留结构细节；
- Floyd–Steinberg 的局限：固定 7/3/5/1 权重，扩散方向不随局部几何调整；
- 关键改动：用 Laplacian 提取边缘/纹理，按结构自适应误差扩散的方向与权重；
- 实测：低对比度区 MSSIM +25%，速度与 FS 同级；
- 典型案例：蜗牛壳纹理保留良好，其他方法糊掉；
- Jon Olick 的用途：内部某个二值 mask 生成。

## 链接到的概念

- [[laplacian-structure-aware-error-diffusion]]
- [[floyd-steinberg-dithering]]
- [[jon-olick]]

## 原文

- 链接：https://www.jonolick.com/home/laplacian-based-structure-aware-error-diffusion
- 本地：`raw/articles/jonolick.com/2024-08-30_laplacian-based-structure-aware-error-diffusion.md`
