---
tags: [source, 渲染, shader, 纹理, lod]
date: 2026-04-14
sources: 1
---

# Fractal Texturing（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2022 年 10 月的一篇，给出一个叫 **fractal texturing** 的技巧：**按深度动态缩放 UV 并在相邻缩放层级间 blend**，让同一张纹理在任意距离都保持一致的屏幕空间细节。来源于他当时做两周 game jam 项目遇到的 terrain 纹理问题。

## 摘要

拉远时纹理重复、拉近时 texel 马赛克——这两个 artefact 其实是同一个问题的两端：texel 和 pixel 尺寸不匹配。mipmap 只能解决欠采样（远处 aliasing），不能补出过采样（近处块感）。Xor 的解法是让 UV 随深度缩放 `uv / depth`——但如果每像素用自己的深度会连续 swim，所以**先取 log 再 floor 离散化**：`LOD = log(depth)`、`LOD_floor = floor(LOD)`、`uv / exp(LOD_floor)`。这样每当深度翻倍，scale 才翻一倍，相邻像素绝大多数在同一个 LOD 层内、scale 恒定。层与层之间的接缝用**同时采三个尺度、按 LOD 小数部分 blend** 的做法抹平：`(tex_current + mix(tex_finer, tex_coarser, LOD_fract)) * 0.5`。这个三次采样也就是「fractal」的来历——同一张贴图以不同频率叠加。该技巧还顺带绕过 mipmap，对 GameMaker 这类 mipmap 支持一般的引擎很友好。**前提是纹理本身尺度无关**——噪声、砂砾、草地 OK，砖墙、瓷砖这类固定比例的不行。

## 关键要点

- **问题对称性**：远处欠采样 + 近处过采样，两端都是 texel/pixel 比例不对。
- **核心变换**：`scaled_uv = uv / exp(floor(log(depth)))`——按 2 的幂离散化的深度缩放。
- **Blend 公式**：`(tex1 + mix(tex0, tex2, LOD_fract)) * 0.5`，其中 `tex0/1/2` 来自三个连续缩放的 UV，权重按 `LOD_fract` 平滑过渡。
- **省掉 mipmap**：fractal blend 本身保证屏幕细节一致性，无 aliasing。
- **depth 缩放系数**需要按场景调：Xor 用 `depth *= 1e3 / iResolution.y;`——跟纹理尺度、深度单位、屏幕分辨率都有关。
- **适用边界**：只对尺度不变的纹理（自然纹理）生效；砖墙 / 瓷砖这类固定比例纹理会出问题。
- 结构上很像 [[layered-grid-noise|分层网格噪声]] 或 fBm——同一函数在多个频段叠加，只是叠加对象是 texture sample。
- [原文 demo on Shadertoy](https://www.shadertoy.com/view/mds3R4) 同屏对比三种方案。

## 链接到的概念

- [[fractal-texturing]]
- [[msaa-ssaa]]
- [[sampler-filter-wrap-modes]]
- [[triplanar-mapping]]
- [[layered-grid-noise]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/gm-shaders-mini-fractal-texturing-1408552
- 本地：`raw/articles/mini.gmshaders.com/2022-10-15_fractal-texturing.md`
