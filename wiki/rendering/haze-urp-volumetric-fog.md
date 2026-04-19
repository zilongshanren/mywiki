---
tags: [unity, urp, volumetric-fog, froxel, product]
date: 2026-04-19
sources: 1
---

# HAZE：URP 上的 Froxel 体积雾商品

**HAZE** 是 [[harry-alisavakis]] 发售的 Unity URP Renderer Feature，实质上是把 Bart Wronski 2014 年在 Assassin's Creed IV 上推广的 [[volumetric-fog-froxels|froxel 体积雾]] 方案工程化到一个可以直接上架的商品。本页把该产品在实现侧暴露的每个参数对应到已有概念，作为「理论如何落到量产 shader」的映射参考。

## 架构对照

| HAZE 参数 | 对应概念 |
|---|---|
| Froxel Buffer Resolution + Depth | [[volumetric-fog-froxels]] 的 3D 纹理 xy×z slices |
| Buffer Sampling（tricubic/trilinear/point） | [[depth-aware-upsampling]] 的采样模式选择 |
| Interleaved Gradient Noise Strength | IGN jitter，[[temporal-supersampling]] 的配套抖动 |
| Temporal Accumulation Blending | [[taa-history-rectification]] 的混合因子 |
| Main Light Shadow Bias | [[shadow-mapping-basics]] 的自阴影偏移 |
| Global Fog + FogVolume + URP Volume Override | 三层叠加 fog 模型 |
| SSMS Radius / Threshold / Max Iterations | [[bloom-threshold-blur-composite]] 风格的 bloom-as-multiple-scattering 近似 |

## 工程细节

**Froxel 深度切片**通常按对数或指数分布——近处一片 froxel 覆盖 0.5 米，远处覆盖 100 米。HAZE 把这个曲线藏在内部，只暴露 min/max 范围。采样时配合 IGN jitter + tricubic 插值 + 时间累积，压掉 frame-to-frame noise，这正是 Wronski 论文的标准组合。

**SSMS (Screen-Space Multiple Scattering)** 是把 bloom 风格的「高亮区域 threshold → 多次 downsample blur → 合成」借过来当多重散射。物理意义上是廉价近似——Kulla/Conty 的 single-scatter 近似里这是 diffuse 衰减的一种低频补偿。产品体现上它给美术两个旋钮（intensity、radius）让雾看起来「有光泽」。

**Shadow bias 暴露**解决的是 froxel 雾的经典 artifact：薄墙（厚度 < froxel z 跨度）时阴影采样会把对面透光当自光照，导致雾漏光。把 shadow bias 拉大可缓解，代价是阴影断层。

## 为什么单独开页

这一页不是「新技术」，而是把一个**真实量产化的 froxel 体积雾**每个参数都做过归因后，变成 wiki 中理论页与工程实现之间的桥梁。类似 [[custom-srp]] 这种「Jasper Flick 教你把原理走通」和 [[gpu-driven-grass-tiles]] 这种「Marco 的工程实例」的混合层。

## 相关

- [[volumetric-fog-froxels]]
- [[volumetric-fog-raymarch-shadows]]
- [[temporal-supersampling]]
- [[bloom-threshold-blur-composite]]

## Sources

- [[sources/halisavakis-haze-manual]]
