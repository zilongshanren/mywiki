---
tags: [source, graphics, unity, urp, volumetric-fog, product-manual]
date: 2026-04-19
sources: 1
---

# HAZE — How to Use（Harry Alisavakis）

[[harry-alisavakis]] 2025 年 10 月发布的用户手册，对应他自己在 Unity Asset Store 发售的 URP 体积雾渲染器 **HAZE**。是一篇产品文档，但技术含量足够让它记为一个**现实中的 froxel 体积雾落地实现**的参考。

## 摘要

HAZE 作为 URP Renderer Feature 加入流水线。核心参数集围绕 **froxel buffer**（3D 纹理，xy 屏幕空间 + z 视距 slice）：分辨率、aspect 比例、最远距离、sampling 模式（tricubic / trilinear / point）、interleaved gradient noise 强度、时间累积 blend、主光阴影偏差。HAZE 额外集成 **Screen-Space Multiple Scattering**——用 bloom 风格的 threshold + blur 近似多重散射，带来粗糙光晕感。全局雾 + Volume 内 fog override + 局部 FogVolume 三层叠加，每层都有自己的密度、颜色、噪声贴图。多附加光源可选加入贡献（shadow cost 线性叠加）。文档也给了常见 troubleshoot：TAA 合作、透明物体支持、性能调优。

这篇本身不是新方法，但是把 [[volumetric-fog-froxels]] 的标准架构（temporal accumulation + tricubic upsample + noise jitter）落到一个**可上架商品**的完整表达——特别适合对照 Bart Wronski 的 Assassin's Creed IV volumetric fog 论文来看工程细节。

## 关键要点

- **Froxel buffer** 分 xy 与 depth 两个分辨率轴，depth 方向是 log 分布——近处细、远处粗；
- **tricubic sampling** 抗闪烁但贵，point sampling 留给 lo-fi 风格；
- **temporal accumulation** 的 blend 值暴露为参数——移动光源时调低可减 trailing ghost；
- **SSMS** 是 bloom-like 技巧，作者直接把 pre-filter threshold 和 radius 开放给美术；
- **FogVolume local density** + 全局 fog + URP Volume override 的三层叠加模型，是移动端常见的 fog 分层；
- **主光 shadow bias** 特意开放，解决「雾漏过薄墙」这个 froxel 阴影的经典问题。

## 链接到的概念

- [[haze-urp-volumetric-fog]]
- [[volumetric-fog-froxels]]
- [[temporal-supersampling]]

## 原文

- 链接：https://halisavakis.com/haze-manual/
- 本地：`raw/articles/halisavakis.com/2025-10-01_haze-how-to-use.md`
