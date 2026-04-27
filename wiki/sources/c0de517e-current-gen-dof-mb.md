---
tags: [source, 渲染, 后处理, 景深, 运动模糊]
date: 2026-04-27
sources: 1
---

# Current-gen DOF and MB（C0DE517E）

[[angelo-pesce]] 发表于 2012 年 1 月的文章，介绍一种把景深（Depth of Field）与运动模糊（Motion Blur）融合到同一个可分离滤波器的后处理方案，并附关键 shader 伪代码。

## 摘要

Pesce 从"正确"的渲染积分视角出发——DOF 和 MB 都是在时间维度和胶片平面维度多采样同一积分——推导出两者本质上都是散射（scattering）滤波。将 DOF 的圆形核心沿运动方向倾斜，自然得到 DOF+MB 联合的椭圆基，与 Crytek 在 SIGGRAPH 2011 公开的方案相似。Pesce 的变体改用**可分离滤波**（沿两条对角轴）替代 Crytek 的圆形多采样，并对纯运动模糊（无 DOF）场景下的零长度轴做了特殊处理。

## 关键要点

- **DOF 和 MB 是同类滤波**：两者都相当于在额外维度对渲染积分采样，后处理中都表现为 scattering 滤波；唯一难点是丢失的可见性（occluded / moving background）。
- **gather-as-scatter 策略**：以被采样点的散射核半径为权重决定是否贡献给当前像素，比纯 gather（只看当前像素的核大小）更物理正确，能处理大散焦区域向焦内区域扩散的情形。
- **可分离滤波**：Pesce 沿两条斜对角轴做两次 1D gather 替代圆形多采样。纯 MB 无 DOF 时两轴退化为同一方向但非零，避免了 Crytek 方案中零向量的特殊情形；纯 DOF 无 MB 时插值到圆形。
- **scattering 预 pass**：在正式 blur 之前先做一个小半径 gathering-as-scattering pass，把散射核大小写入一个辅助 buffer，用于后续可分离 blur 的 scatter 判定，类似 PCSS 的思路。
- **权重公式**：采样权重 = `saturate(maxLengthAtSample - currentLength) * filterWeight[i]`，即只有散射半径大到"能覆盖当前距离"的样本才参与贡献。

## 链接到的概念

- [[circular-separable-dof]]
- [[gather-bokeh-dof]]
- [[scatter-bokeh-dof]]
- [[variable-size-gather-dof]]
- [[motion-vectors]]

## 原文

- 链接：https://c0de517e.blogspot.com/2012/01/current-gen-dof-and-mb.html
- 本地：`raw/articles/c0de517e.blogspot.com/2012-01-04_current-gen-dof-and-mb.md`
