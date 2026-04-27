---
tags: [source, rendering, pbr, brdf, ggx, 多次散射, 能量守恒]
date: 2026-04-27
sources: 1
---

# Misunderstanding Multiscattering（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2019 年 8 月的文章，以「尽量少学物理」的思路推导出一个实用的 GGX 多次散射近似，并论证为什么这个更简单的参数化在实际生产中反而优于 Kulla/Conty 的「更正确」解法。

## 摘要

粗糙金属的 GGX BRDF 在高 roughness 下会变暗——这是单次散射模型遗漏多次弹射能量的结果（炉子测试可验证）。Kulla/Conty 2017（SIGGRAPH）给出了数学上更完整的解法，但 Pesce 提出：对生产来说，更简单的归一化方案同样能量守恒，且得到的参数化（f0 的含义）对艺术家更直观、更正交。

核心做法：用现有引擎 split-sum LUT 中已经存储的 directional albedo（bias + scale 两项之和）反过来归一化 BRDF，使 f0=1 的材质在任意 roughness 下炉子测试都输出白色。

## 关键要点

- **为什么要修**：标准 GGX 在高粗糙度下变暗，roughness 和亮度不正交，艺术家需要手动补偿
- **炉子测试**：均匀白光环境 + f0=1 → 理想 BRDF 应输出纯白；标准 GGX 不是，说明能量流失
- **最简近似**：用 split-sum LUT 的 `1/(bias(roughness, ndotv) + scale(roughness, ndotv))` 直接归一化 BRDF；无需新纹理（引擎里已有这张表）
- **与 Kulla/Conty 的区别**：Kulla 方案额外加了多次弹射积累的**色彩饱和度**（每多弹射一次就染一次颜色）；Pesce 的方案不这么做，理由是：对艺术家来说，roughness 影响亮度已经够麻烦，如果 roughness 还影响饱和度，参数空间更混乱
- **参数化语义差异**：两种方案都能量守恒，但 f0 代表不同的 albedo；Pesce 认为自己的版本「物理上不那么正确但工程上更合理」
- **解析近似**：LUT 归一化函数可进一步近似为 `1 + 2*α²*NdotV`（α = roughness²），甚至 `1 + α²`（去掉 NdotV 依赖），视精度需求选择
- **不满足互易性**：Pesce 的方案不满足 BRDF 互易性，对离线路径追踪可能有问题，实时渲染无影响

## 链接到的概念

- [[ggx-multiscattering-normalization]]
- [[microfacet-brdf]]
- [[ibl-multiple-scattering]]
- [[split-sum-approximation]]
- [[physically-based-shading]]

## 原文

- 链接：https://c0de517e.blogspot.com/2019/08/misunderstanding-multiscattering.html
- 本地：`raw/articles/c0de517e.blogspot.com/2019-08-12_misunderstanding-multiscattering.md`
