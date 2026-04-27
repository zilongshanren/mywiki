---
tags: [渲染, pbr, brdf, 着色]
date: 2026-04-14
sources: 1
---

# 物理基础着色（Physically Based Shading）

**物理基础着色**（PBS，和 PBR 常混用）是 2010 年代游戏和电影渲染的共同基线：要求材质模型满足一组基本物理约束（能量守恒、互易性、菲涅耳规律），艺术家输入的是有物理意义的量（albedo、metallic、roughness、F0），而不是拍脑袋调的「specular color」「gloss」。

这让同一个材质在不同光照下自动表现一致——棚灯、室外、HDR 环境、夕阳——不需要逐场景重调参数。

## 关键支撑结构

- **[[microfacet-brdf|微表面 BRDF]]**：现代 PBR 的通用骨架，$f_r = DFG / (4\,n\cdot l\,n\cdot v)$，其中 $D$ 是法线分布（GGX）、$G$ 是 Smith 型遮蔽-阴影、$F$ 是 Schlick 近似的 Fresnel。
- **能量守恒**：BRDF 在半球上的积分必须 $\leq 1$。单次散射微表面 BRDF 有隐蔽的能量流失，需要 multiscatter 补偿（见 [[microfacet-brdf]] 末尾）。
- **线性空间 / HDR**：所有光强计算在线性空间做，最后 tone-map 回显示空间；见 [[local-tonemapping]]、[[color-space]]。
- **IBL（Image-Based Lighting）**：用 pre-filtered environment map + split-sum 近似把环境光塞进同一个 BRDF 框架。[[spherical-harmonics]] 是低频 diffuse 部分的廉价近似。

## SIGGRAPH「Physically Based Shading in Theory and Practice」

[[stephen-hill|Stephen Hill]] 从 2010 年起组织的 SIGGRAPH 课程，是这个领域的事实标准文献入口。2014 年那届尤其影响深远：

- **Naty Hoffman** — 物理和数学基础入门（每年保留节目）
- **Eric Heitz** — microfacet masking-shadowing 函数的严格理论（对应的 JCGT 论文证明 Smith 模型和暴力模拟非常接近，是 Smith G 被业界普遍采用的决定性依据）
- **Jonathan Dupuy** — LEADR mapping 对预滤波 / 反走样 NDF 的实际处理
- **Sébastien Lagarde & Charles de Rousiers** — Moving Frostbite to PBR，DICE 自家引擎从传统到 PBR 的完整落地笔记
- **Anders Langlands** — alShaders / Arnold 的 PBR 设计决策，把 VFX 侧的实践带进来
- **Pixar Ian Megibben & Farhez Rayani** — 艺术指导视角下 PBR 给 Toy Story *OF TERROR!* 灯光带来的变化
- **Brent Burley（更新版 2012 notes）** — Disney Principled BRDF 的原始论文，游戏业界事实上的 roughness 参数化起点

课程笔记集合在 [blog.selfshadow.com/publications](https://blog.selfshadow.com/publications/) 上，是学 PBR 的必读起点。

## 相关
- [[microfacet-brdf]]
- [[spectral-brdf]]
- [[spherical-harmonics]]
- [[local-tonemapping]]
- [[stephen-hill]]
- [[fast-translucency-wraplight]] — Frostbite 2 的廉价假 SSS：反向光方向 + subsurface distortion
- [[journey-sand-specular]] — 风格化多路 specular 拆分（rim Fresnel + ocean Blinn-Phong）
- [[tiled-light-culling]] —— Brian Karis：用能量守恒和 specular cone 做 tile 级剔除
- [[brian-karis]] —— UE4 Real Shading 的作者
- [[normalised-blinn-phong-shader]] —— 面向美术的 PBR 教学 shader，每个 PBR 组件可切换演示
- [[openpbr]] —— 2023+ 的开放式 uber-shader 标准，Kutz / Portsmouth 主笔
- [[neural-materials]] —— 把离线 shader graph 压进实时推理的神经材质方向
- [[realtime-gi-per-light]] —— Engel 2013：「光源数量优先于 PBR」，per-light bounce GI 的次世代工作流

## Sources
- [[sources/selfshadow-pbs-siggraph-2014]]
- [[sources/selfshadow-pbs-siggraph-2012]]
- [[sources/selfshadow-pbs-siggraph-2025]]
- [[sources/c0de517e-beyond-photorealism]] — Pesce 2016：PBR 之后需要主动构建视觉语言，感知现实 ≠ 物理正确
- [[sources/agraphicsguynotes-pbs-in-games]]
- [[sources/rory-physically-based-shading]] — Driscoll 2013：LBP vs Disney BRDF 的 MERL 对比；「physically-correct」与「physically-based」的区分
- [[sources/humus-pbr-observational-lighting]] —— Engel 2013：「光源数量优先于 PBR 切换」的反直觉优先级论断
