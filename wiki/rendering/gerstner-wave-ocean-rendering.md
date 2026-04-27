---
tags: [渲染, ocean, water, gerstner-wave, trochoidal, planet-engine, shore-wave, procedural]
date: 2026-04-27
sources: 1
---

# Gerstner 波与行星尺度海洋渲染

实时海洋渲染通常将**开阔海域波**与**海岸破碎浪**作为两套独立系统分别生成，再在视觉上叠合。Outerra 的实现给出了一套在行星引擎约束下（球面坐标、超大视距、地形 tile 驱动的 mesh）可行的端到端方案。

## Gerstner（Trochoidal）波

Gerstner 波（又称 trochoidal wave）是一种解析波形：水面上的质点沿圆形轨道运动，水平与垂直分量均为正弦，叠加后形成略尖的波峰与扁平的波谷。相比简单正弦波更接近真实深水波形。

多个 Gerstner 波叠加后写入一张 2D 可无缝 tile 的贴图覆盖海面。**可 tile 的约束**要求每个波分量在 $(u, v)$ 方向各有整数个波峰，由此反推可用频率集。振幅须 < 波长/20，否则波顶会"翻转"（质点轨迹相交）。深水波速公式：

$$v = \sqrt{\frac{g\lambda}{2\pi}}$$

**风向偏置**：通过为各分量赋予不等振幅权重，使靠近主风方向的分量幅度更大；逆向分量振幅可压为零，适用于河流单向流动场景。

## 海岸破碎浪

当水下地形抬升，波速下降而振幅升高，波峰倾斜并最终破碎。Outerra 用**岸线距离图**驱动这一过程：

1. 对含水陆边界的地形 tile，shader 搜索最近异类点（水找陆、陆找水），输出距离；
2. 对距离图做 **Sobel 滤波**得到梯度向量，用作海岸波的法向/传播方向；
3. 以距离为自变量查询波形函数贴图（precomputed skewed trochoidal shapes），参数 γ 控制倾斜度——γ=1 为标准 Gerstner，γ↑ 波峰前倾；
4. 时变掩码贴图让破浪在岸边断续出现，而非全周期连续。

## 水色参数化

水的颜色由 **RGB 分量的吸收深度**决定（默认约 7/30/70 m）：光在到达该深度时衰减到原始强度的 1/e。在纯水中散射贡献可忽略，主导因素是**溶解有机物**（腐殖质等），因此不同水体颜色差异主要通过调整有机物散射系数实现。

## 实现细节

- 地形与海面共用同一套 patch mesh 系统，顶点在 GPU 端根据波形公式做位移动画；
- 泡沫纹理以独立掩码通道叠加，当前版本仅为静态占位，动态泡沫列为 TODO；
- 波频谱目前为"平坦"分布（等振幅），与 JONSWAP 等真实谱有出入，自适应谱生成列为改进项。

## 相关

- [[planet-terrain-dem-pipeline]] — 地形 tile 系统，海面 mesh 与地形共享
- [[procedural-grass-rendering]] — 同引擎的程序化植被，展示 Outerra 覆盖层设计思路
- [[sphere-mapped-terrain-culling]] — 行星尺度 tile 剔除
- [[terrain-vector-overlay-crater]] — 同一向量覆盖层系统上实现的弹坑
- [[outerra-team]]

## Sources

- [[sources/outerra-ocean-rendering]]
