---
tags: [渲染, 环境探针, 视差映射, 重投影, 反射, 全局光照]
date: 2026-04-27
sources: 1
---

# 探针 Warp 重投影（Probe Warping）

**探针 Warp 重投影**是指利用在位置 A 烘焙的深度感知探针（每方向存储场景深度），近似在位置 B 所见内容的技术——无需在 B 处重新烘焙或做昂贵的散射/raymarching。

该问题与[[rendering/parallax-corrected-cubemap|视差修正 Cubemap]]密切相关，但后者依赖解析型代理形体（AABB/OBB）；探针 Warp 则直接利用探针中存储的深度，通过迭代几何算法近似光线交点。

## 算法描述

Angelo Pesce 在 GeoGebra 上独立推导出如下单步 warp 算法（事后发现是视差映射的球面推广）：

1. 沿查询方向 `Dir` 在探针 A 中采样，得到交点 S1（位置 = A + t·Dir，t 由深度导出）
2. 在 S1 处构造**垂直于 Dir 的平面** P
3. 从位置 B 出发沿 Dir 方向与平面 P 求交，得到点 I
4. 在探针 A 中沿方向 `normalize(I - A)` 采样，得到 S2
5. 将 S2 投影到从 B 出发的 Dir 射线上，作为近似交点

此步骤可迭代：用上一步结果再次构造平面并重复，类似 steep parallax mapping 的多步行进。实践中单步效果通常更优，两步有时因过度扭曲而变差。

## 与视差映射的关系

| 方法 | 对应关系 |
|------|---------|
| 单步探针 warp | offset mapping / 偏移映射 |
| 多步探针 warp | steep parallax mapping |
| 深度存储于探针各方向 | 高度图贴图 |
| 球面方向采样 | 2D uv 采样 |

该算法还可追溯至 Szirmay-Kalos 等人的论文 *"Approximate Ray-Tracing on the GPU with Distance Impostors"*，是一个多次独立发现的经典案例。

## 与视差修正 Cubemap 的比较

[[rendering/parallax-corrected-cubemap|视差修正 Cubemap]] 假设场景可用 AABB 包围盒近似，在 shader 中解析求交，简单但对复杂场景精度差。探针 Warp 直接利用烘焙的真实深度，理论上精度更高，且"比传统视差修正更少数学"；代价是需要存储深度通道，且不适合预卷积的 specular 探针（Jacobian 变化在高光中明显）。

## 适用场景与局限

- 适合 diffuse irradiance 探针从一点到另一点的近似——对精度要求相对低
- 预卷积 specular 探针应谨慎：高粗糙度时可 fade out 修正，或使用软代理形体
- 深度图宜平滑（低分辨率 + mip 模糊），硬边深度不连续会导致扭曲伪影
- 场景高度凹陷（如室内角落）是最坏情况，室外/开阔环境效果更好

## 相关

- [[rendering/parallax-corrected-cubemap]] — 同类问题的代理形体解析方案
- [[rendering/environment-probe-placement]] — 探针放置策略
- [[rendering/hbao-interleaved-sampling]] — 另一个 Pesce 关注的屏幕空间采样技术
- [[people/angelo-pesce]]

## Sources

- [[sources/c0de517e-probe-warping-half-baked]]
