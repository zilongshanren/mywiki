---
tags: [渲染, pbr, 物理假设, 近似, brdf]
date: 2026-04-27
sources: 1
---

# PBR 近似栈（PBR Approximation Stack）

「物理基础渲染」名字里带着「物理」，但从最顶层的光学框架到最终的像素颜色，整条管线是一个嵌套的**近似栈**（approximation stack）。每一层都在默默接受一些假设，而这些假设在某些条件下会失效。

## 各层近似的盘点

### 第一层：光学框架

- 使用**几何光学**（geometric optics）：光沿直线传播，颜色频率独立
- 已知无法建模的现象：衍射（diffraction）、干涉（interference）、荧光（fluorescence）、磷光
- 这些现象在日常材质中罕见——这是被接受的理由，不是被解决的问题

### 第二层：色彩表示

- 用**三色刺激 / RGB** 代替光谱计算（metamerism 同色异谱效应）
- 已知问题：某些光谱混合在 RGB 下无法区分；[[spectral-rendering]] 在某些材质上结果差异显著
- 假设艺术家能够通过调整灯光和后处理来「修复」色彩偏差——这掩盖了误差，也使误差难以量化

### 第三层：微表面 BRDF

- [[microfacet-brdf]] 把表面视为大量理想镜面小面（microfacet）的统计模型
- 衍射效应被略去（Beckmann-Spizzichino 1963 就已知，照样被忽视）
- Diffuse 项（如 Lambertian、Oren-Nayar）把 microfacet 换成 Lambertian 小面，实为体散射的极度简化代理
- **关键简化：只模拟一次散射**，相邻 microfacet 间的多次弹射被 masking-shadowing 函数吃掉（→ 能量流失，参见 [[ibl-multiple-scattering]] 和 [[ggx-multiscattering-normalization]]）

### 第四层：光源积分

- 像素足迹（pixel footprint）：只考虑法线分布统计，忽略光线方向随像素覆盖区域的变化，以及几何遮蔽
- 不同光源形状（点/线/面/环境）各有独立的近似公式（有时基于 LTC，有时基于多项式拟合），相互间不保证一致
- 面积光 vs 点光近似质量不在同一水平，结果在边界条件下容易出现不连续

### 第五层：全局照明

- 直接光 PBR 的精细化与 GI 所用的粗糙近似（SH、probe、SSAO）之间存在数量级的精度差距
- [[spherical-harmonics]] 只能表示极低频的间接漫反射；高频间接光被完全丢弃
- Participating media（大气、雾、体积云）会让光源的等效大小和方向发生改变，但绝大多数渲染器把直接光和 participating media 分开处理

## 整体性评估的价值

Pesce 的核心论点：不应在近似栈的某一局部无限精化，而忽视其他层的误差。例如，在 BRDF 层面追求一个更精确的 GGX 尾形，但不解决 diffuse 项的物理不一致性，或者不解决面积光积分的粗糙近似，对最终图像的贡献可能微乎其微。

正确的路径是：
1. 采集真实材质数据（如 MERL 数据库），获取地面真值
2. 运行路径追踪，计算端到端的参考结果
3. 用感知误差度量找出最显著的近似误差层
4. 针对性地改进，而非均匀铺开

## 与相关页面的关系

- [[physically-based-shading]] — PBR 整体框架与历史
- [[microfacet-brdf]] — 第三层近似的详细分析
- [[ibl-multiple-scattering]] — 单次散射能量流失的实时补偿方案
- [[ggx-multiscattering-normalization]] — Pesce 提出的「最无知近似法」
- [[spectral-rendering]] — 放弃 RGB 的替代方案

## Sources

- [[sources/c0de517e-whole-pbs-picture]]
