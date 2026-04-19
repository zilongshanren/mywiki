---
tags: [source, 渲染, frame-analysis, fox-engine, mgs-v, deferred-rendering, 2017]
date: 2026-04-19
sources: 1
---

# Metal Gear Solid V - Graphics Study（Adrian Courrèges / 2017）

[[adrian-courreges]] 2017 年 12 月的长篇帧解剖，对象是 Kojima Productions Fox Engine 驱动的《Metal Gear Solid V: The Phantom Pain》PC 版。因为 Fox Engine 检测 DLL 注入会直接自杀，Courrèges 自己 fork 了 [ReShade](https://reshade.me/)，加了一套 hook 能导出中间 buffer、纹理、DXBC 着色器字节码——这套工具后来开源在 [acourreges/reshade/tree/mgsv_tpp](https://github.com/acourreges/reshade/tree/mgsv_tpp)。这是全文最长、最细节的一篇 graphics study，也是 [[mgs-v-fox-engine-frame|Fox Engine 一帧的全流程]] 这一 wiki 页的唯一来源。

## 摘要

帧选在医院序章——Snake 躺地、两名士兵前站、"Man on Fire"在走廊尽头。总计 **2331 draw call / 623 纹理 / 73 RT**。整条管线：depth pre-pass（地形从 heightmap）→ 3-RT G-Buffer（B8G8R8A8 + reverse-Z depth）→ velocity map（动态 mesh + reprojected static）→ **双 SSAO**（LISSAO 低频 + Scalable Ambient Obscurance 高频，compute 合成）→ 每区域的 SH 球面 irradiance（16×16 atlas）→ 半分辨率 diffuse GI + bilateral upscale →非阴影光 → shadow map（4k×4k per spot）+ 阴影光 → **早 tonemap 到 LDR**（非常 signature 的选择，bloom 用预存在 alpha 里的 pre-tonemap luminance 做 bright-pass）→ emissive/transparent + reflection probe（256×256 HDR cubemap，天气 × 时刻 × 地点的海量 permutation）→ SSR（raymarch 4 tap）→ heat distortion（多次 copy RT）→ decal + particle → bloom（Kawase × 4）→ sprite-scatter DoF（多级分辨率 buffer 按 CoC 分流）→ lens dirt + 多边形 anamorphic lens flare → motion blur（MHBO 2012）→ 256×16 3D LUT color grading → FXAA → 美工 final touch sprite。

"Bonus Notes"里演示了用定制 hook blacklist bandage 的 draw call、让 Ishmael 的真面孔显形（原模型下有隐藏几何），并警示 Psycho Mantis 的 gas mask 下**根本没有脸**——美工为省顶点没建。

## 关键要点

- **反调试**：Fox Engine 主动杀 DLL-injector 类的 debugger；Courrèges 靠 fork ReShade 自建 hook 绕过。
- **Small G-Buffer**：只 3 张 B8G8R8A8 + 32-bit float depth（reverse-Z）——specular RT 把 roughness / specular / material-ID / SSS 压在四通道里。
- **双 SSAO**：LISSAO（Toy Story 3 技术，5 tap）+ SAO 变体（11 tap），各自 half-res + depth-aware blur，compute 合成。
- **SH irradiance atlas**：关卡按区域烘 SH，每帧重建 small spherical maps 到 16×16 tile 的 HDR atlas。
- **早 tonemap**：Fox Engine 选择在 emissive/transparent/SSR/DoF 之前就 tonemap 到 LDR——和 Frostbite / UE 相反。靠 alpha 通道保 pre-tonemap HDR luminance 给后续 bloom bright-pass 用。
- **Reflection probe**：baked 256×256 HDR cubemap，需要 sunny/cloudy/rainy/stormy × 各时刻的**多个版本**。
- **DoF**：sprite scatter，但为控 overdraw，用 1/4 / 1/8 / 1/16 多级 buffer，vertex shader 按 CoC 决定 sprite 去哪一级，不合格的顶点推到视锥外丢掉。
- **Bloom**：Kawase blur × 4 替代 Gaussian；程序化 lens flare + chromatic aberration 也融在 bloom 里。
- **Color grading**：256×16 2D LUT（16 slice 横排）→ 3D texture trilinear。美工工作流是"截图里嵌 neutral LUT → PS 调 → 提取修改后 LUT 喂回"。

## 链接到的概念

- [[mgs-v-fox-engine-frame]]
- [[adrian-courreges]]
- [[deferred-rendering]]
- [[spherical-harmonics]]
- [[scatter-bokeh-dof]]
- [[kawase-blur]]
- [[bloom-threshold-blur-composite]]
- [[color-lut]]
- [[chromatic-aberration-post]]
- [[shadow-mapping-basics]]

## 原文

- 链接：<http://www.adriancourreges.com/blog/2017/12/15/mgs-v-graphics-study/>
- 本地：`raw/articles/adriancourreges.com/2017-12-15_metal-gear-solid-v-graphics-study-adrian-courreges.md`
