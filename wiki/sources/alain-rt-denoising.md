---
tags: [source, 渲染, 光线追踪, 去噪, svgf, restir, 机器学习]
date: 2026-04-27
sources: 1
---

# Ray Tracing Denoising（Alain Galvan / alain.xyz）

[[people/alain-galvan]] 发表于 2020 年 10 月的文章，系统梳理实时光追去噪技术全貌，目标是帮助读者构建一个完整的实时光追降噪器。

## 摘要

文章将去噪技术归纳为四类：**滤波**（À-Trous 双边、引导滤波）、**时空重投影**（速度缓冲 + 历史缓冲 + 方差估计）、**采样改进**（SVGF、A-SVGF、ReSTIR）和**近似缓存**（RTXGI 光探针、NeRF）。重点介绍了 SVGF 与 A-SVGF 的区别：SVGF 用历史长度驱动累积系数，A-SVGF 改用动量缓冲区（方差变化量）以减少时域滞后。ReSTIR 被定位为将重投影提前至采样阶段的突破性工作。ML 方向包括 Intel OIDN、NVIDIA Optix 去噪自编码器、DLSS 超分。文章最后给出了分六步的理想降噪管线框架（预通道 → 光追 → 时空积累 → 统计分析 → 滤波 → 历史写回），并附有完整 HLSL 代码示例。

## 关键要点

- À-Trous 滤波重复 3–5 次，stepWidth 每次减半（序列如 4、2、1），引导权重需含法线/深度/物体 ID
- 速度缓冲 = NDC 当前帧坐标 - 前帧坐标，每顶点计算
- A-SVGF 的方差公式：`variance = (1 + 2*(1-histlen)) * max(0, moment.y - moment.x²)`
- ReSTIR 结合了 Resampled Importance Sampling（Talbot 2005）+ 时空复用思想
- 萤火虫剔除：粗糙度偏移（roughnessBias += oldRoughness * 0.75）或方差上界截断
- DLSS 和 OIDN 共同模式：输入噪声图 + 反照率 + 法线 → 输出滤波图

## 链接到的概念

- [[rendering/rt-denoising]]
- [[rendering/svgf]]
- [[rendering/restir-di-math]]
- [[rendering/hybrid-raytracing-pipeline]]

## 原文

- 链接：https://alain.xyz/blog/ray-tracing-denoising
- 本地：`raw/articles/alain.xyz/2020-10-06_ray-tracing-denoising.md`
