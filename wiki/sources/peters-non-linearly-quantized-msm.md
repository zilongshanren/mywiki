---
tags: [source, 渲染, 阴影, 矩, 量化, compute-shader, 论文]
date: 2026-04-14
sources: 1
---

# Non-linearly Quantized Moment Shadow Maps（Peters，HPG 2017）

[[christoph-peters]] 2017 年 7 月在 *High Performance Graphics* 发表的论文，把 [[moment-shadow-mapping|MSM]] 的存储压缩进一步推到极限，并配套提出一个把 MSAA resolve 与 9² Gaussian blur 全部锁在 shared memory 里的 compute shader。

## 摘要

原版 MSM 在每个 texel 存四个深度幂 `(z, z², z³, z⁴)`，64 或 128 bits/texel；64-bit 量化引入的舍入误差需要 bias 来补偿，bias 一加，漏光（light leaking）就被加重。本文提出一个**非线性变换**，把这四个矩映射成「更直接描述深度分布」的四个量，再将之量化到 32 或 64 bits。

- **64 bits/texel 非线性版本**与原版 128 bits/texel 几乎不可区分；
- **32 bits/texel 极限版本**漏光几乎不增加，但可能出现 banding，需要 [[blue-noise-dithering|蓝噪声 dithering]] 缓解。

同时，重建步骤的算术量也减少了——非线性参数化保存的本来就更接近解码中间状态。

非线性量化的代价是**与硬件 bilinear 不兼容**。Peters 配套写了一个 compute shader：把整个 tile 拉进 shared memory，在 LDS 里做完 MSAA resolve 与两遍 9-tap 高斯模糊，**只在最后一次**把量化后的小 footprint 写回 device memory。这个 "on-chip filtering" 让端到端帧时间和 32 bits/texel 的 VSM 相当。在采样阶段用 nearest + 蓝噪声 dithering 替代硬件 bilinear，把视觉上的瑕疵从锯齿化为均匀噪声。

## 关键要点

- **核心洞察**：四个原始幂矩之间存在强相关性，独立线性量化是浪费比特预算；非线性变换贴着信号流形重新选坐标。
- **三赢**：质量（漏光更少）、带宽（仍是 64 bit、可降至 32 bit）、ALU（解码更便宜）同时改善。
- **32 位是 VR / 移动端友好的极限**：banding + dithering 是已知折中。
- **on-chip filtering**：MSAA resolve + 9² Gaussian + 量化全部在 LDS 完成，device memory 只写一次。
- **采样端用 blue noise dithering**：补偿失去的硬件 bilinear。
- **与"32-bit VSM 同 cost 而质量接近 128-bit MSM"** 是论文最有吸引力的工程结论。

## 链接到的概念

- [[non-linearly-quantized-msm]]
- [[moment-shadow-mapping]]
- [[christoph-peters]]
- [[shadow-mapping-basics]]
- [[blue-noise-dithering]]

## 原文

- 链接：<http://momentsingraphics.de/HPG2017.html>
- DOI：<https://doi.org/10.1145/3105762.3105775>
- 本地：`raw/articles/momentsingraphics.de/2017-01-01_non-linearly-quantized-moment-shadow-maps.md`
