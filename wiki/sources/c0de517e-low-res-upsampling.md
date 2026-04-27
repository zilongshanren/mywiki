---
tags: [source, rendering, upsampling, depth-aware, black-ops-3]
date: 2026-04-27
sources: 1
---

# Low-Resolution Effects with Depth-Aware Upsampling（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2016 年 2 月的文章，介绍其在 Call of Duty: Black Ops 3 开发过程中解决低分辨率效果升采样边缘伪影问题的实战方案。

## 摘要

Pesce 回顾了自己在多个项目（Fight Night Champion、Space Marines、COD:BO3）上尝试 depth-aware upsampling 的经历——前几次均因边缘 artifact 以"够用"的 hack 勉强出货。BO3 的体积光效果必须在 1/4 分辨率以内计算，迫使他认真研究这个问题。

他提出了两个关键改进：**一**，传统 bilateral 加权（bilinear 权重 × 深度权重相乘）本质上有缺陷——极端情况下 bilinear 会强选一个完全不属于目标表面的样本，正确做法是基于深度不连续性在 bilinear 和 nearest-depth 两种策略之间切换，而非两者加权混合；**二**，低分辨率深度 buffer 的降采样应采用棋盘格式的 min/max 交替采样，确保 2×2 邻域内同时保留近/远两个表面的代表，最大化后续升采样时找到正确深度代表的概率。

## 关键要点

- 直接对深度 buffer 做平均降采样会生成"不属于任何表面"的幽灵深度，产生边缘 bleeding
- bilateral 权重相乘方案的根本缺陷：bilinear 权重强选了错误样本，再乘以深度权重也无法纠正
- 正确方案：检测深度不连续后硬切换到"仅保留最相似深度的样本"，而非渐变混合
- 棋盘格 min/max 降采样是确保多表面代表共存的简洁方案，比纯 min 或纯 max 更鲁棒
- 未来方向：compute shader 深度聚类、利用法线/G-buffer 属性做更准确的表面判断、更宽的滤波核

## 链接到的概念

- [[depth-aware-upsampling]]
- [[deferred-rendering]]
- [[volumetric-fog-froxels]]

## 原文

- 链接：https://c0de517e.blogspot.com/2016/02/downsampled-effects-with-depth-aware.html
- 本地：`raw/articles/c0de517e.blogspot.com/2016-02-06_low-resolution-effects-with-depth-aware-upsampling.md`
