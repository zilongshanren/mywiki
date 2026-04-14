---
tags: [source, 渲染, 阴影, 矩, 体积, 半透明, 论文]
date: 2026-04-14
sources: 1
---

# Improved Moment Shadow Maps for Translucent Occluders, Soft Shadows and Single Scattering（Peters et al.，JCGT 2017）

[[christoph-peters]]、Cedrick Münstermann、Nico Wetzstein、Reinhard Klein 于 *Journal of Computer Graphics Techniques* 6(1) 2017 发表的论文，是 [[sources/peters-beyond-hard-shadows-msm|i3D 2016 "Beyond Hard Shadows" 论文]] 的扩展版。把 [[moment-shadow-mapping|MSM]] 的母系框架推向三个应用，并对底层 MSM 自身做了一系列改进。

## 摘要

像 VSM 一样，MSM 可以直接滤波，但质量显著更高。本文把 MSM 与若干已有方案结合，得到三个新应用：

1. **半透明 occluder 阴影**——对 moment shadow map 启用 alpha blending，无需特殊算法即可处理透明物体（叶子、烟、织物）；
2. **Soft shadows**——按 percentage-closer soft shadows 的精神，对 MSM 的 summed-area table 做两次查询即可得到 contact-hardening 软阴影，称为 **Moment Soft Shadow Mapping（MSSM）**；
3. **参与介质的体积阴影（prefiltered single scattering）**——通过对一张 6 通道 prefiltered moment shadow map 每像素一次 lookup 完成。

作为基础，论文同时对 MSM 自身提出若干改进——这些改进与 [[sources/peters-msm-jcgt2016-demo|2016-09 的 demo 发布]] 中的列表一致：signed depth、稀疏量化变换、最坏情形 bias、新的 [[cubic-equation-solver-hlsl|cubic solver]]、自适应 bias、自适应过/欠估计插值等。所有技术都对高分辨率（4K、VR）扩展性很好，并通过广泛滤波得到正确的反走样。

## 关键要点

- **i3D 2016 的扩展版本**：JCGT 给了篇幅去补全实现细节、对照表与扩展实验。
- **三类应用 + 改进 MSM 自身**：论文一半内容是新应用，一半是底层精细化。
- **半透明 occluder 是最优雅的卖点**：直接 alpha-blend 进 moment shadow map，根本不需要新数学。
- **MSSM 与 PCSS / VSSM 对照**：在漏光与半影质量上都明显改善。
- **6 通道 prefiltered MSM**：是六阶矩在 single scattering 上的应用，依赖 [[cubic-equation-solver-hlsl|新的 HLSL cubic solver]] 才得以稳健。
- **shader 代码 + 可执行 demo 跟随**——论文是 2016-09 demo 的正式书面版本。

## 链接到的概念

- [[moment-shadow-mapping]]
- [[cubic-equation-solver-hlsl]]
- [[christoph-peters]]
- [[shadow-mapping-basics]]
- [[volumetric-fog-froxels]]

## 原文

- 链接：<http://momentsingraphics.de/JCGT2017.html>
- 论文：<http://jcgt.org/published/0006/01/03/>
- 本地：`raw/articles/momentsingraphics.de/2017-01-01_improved-moment-shadow-maps-for-translucent-occluders-soft-s.md`
