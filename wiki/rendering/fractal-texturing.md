---
tags: [渲染, shader, 纹理, lod, mipmap, 3d]
date: 2026-04-14
sources: 1
---

# Fractal Texturing：深度无关的一致细节

一张棋盘纹理贴在一条延伸到远方的地面上会遇到两个相反方向的问题。**拉远**时 texel 密度超过屏幕像素，出现 moiré、闪烁、重复图案明显的「地毯感」——这是 [[msaa-ssaa|欠采样]]，标准解法是 mipmap。**拉近**时 texel 被放大成一个个色块，细节彻底消失——这是所有 raster 纹理的老问题，mipmap 解决不了。[[xor-shader-artist|Xor]] 在做一个两周 game jam 项目时遇到了这两个问题的双重打击，给出了一个简单漂亮的解法：**根据深度动态缩放 UV，并在相邻的两个缩放层级之间 blend**。他把这个技巧叫 **fractal texturing**——因为它本质上把同一张纹理**以不同尺度递归地叠加**，很像程序化分形噪声的 fBm 结构。

## 问题的对称性

Xor 观察到两种 artefact 其实是同一个东西的两端：

- **远处**：一张小纹理在世界空间里占一米，屏幕上远看可能覆盖 1 个像素——相当于 texel 尺寸 ≪ 像素尺寸，重复感和 aliasing 双重出现。
- **近处**：同一张纹理走到眼前可能覆盖 1000 个像素——texel ≫ 像素，细节不够分，出现块状马赛克。

两边的根源都是**texel 和 pixel 的尺寸不匹配**。mipmap 只对第一种情况有效——它通过预过滤降低欠采样带来的 aliasing，但不能无中生有补出第二种情况的细节。

## 核心想法：把 UV 按深度缩放

理想情况下，如果能让 texel 始终保持屏幕像素级的尺寸，两种 artefact 就都消失了。达成这点的办法是 **UV 除以深度**：

```glsl
vec2 scaled_uv = uv / depth;
```

深度越大，UV 越被压缩，纹理看起来越大——**补偿了**透视投影让远处东西变小的效应。1 米远时看到的是「原尺寸的纹理」，100 米远时看到的是「被放大 100 倍的纹理」。从任何距离看，texel 在屏幕上的大小都近似一致。

但这样直接做会炸：**每个像素都用它自己的深度算 UV**，相邻像素（哪怕相差 1）的 UV 尺度就不同，图案完全对不上，出现连续的可见 swim。

## 离散化到「缩放层级」

Xor 的解法是让尺度**分级**——相邻像素只要还在同一级就用完全相同的 UV scale，图案不再游动。自然的分级方式是**按对数取整**：

```glsl
float LOD = log(depth);
float LOD_floor = floor(LOD);
vec2 scaled_uv = uv / exp(LOD_floor);
```

`log` 把「缩放倍率」转成了线性空间，`floor` 量化到整数级别，`exp` 转回倍率。效果是每当深度翻倍（或按任意倍数扩展——取决于 `log` 的底），LOD 级数加 1，UV scale 翻倍。这就保证了**每个 LOD 层内部 scale 恒定**——相邻像素在同一层里看到同一个缩放的棋盘，不再 swim。

但层与层之间会出现**可见的接缝**：LOD = 2 的区域和 LOD = 3 的区域纹理尺度骤变，产生条带。

## Fractal blend：在两层之间插值

干净的解法是**同时采样三层，然后在它们之间 blend**：

```glsl
vec4 fractal_texture(sampler2D tex, vec2 uv, float depth) {
    float LOD = log(depth);
    float LOD_floor = floor(LOD);
    float LOD_fract = LOD - LOD_floor;

    vec2 uv1 = uv / exp(LOD_floor - 1.0);   // 下一级（更密）
    vec2 uv2 = uv / exp(LOD_floor + 0.0);   // 当前级
    vec2 uv3 = uv / exp(LOD_floor + 1.0);   // 上一级（更疏）

    vec4 tex0 = texture2D(tex, uv1);
    vec4 tex1 = texture2D(tex, uv2);
    vec4 tex2 = texture2D(tex, uv3);

    return (tex1 + mix(tex0, tex2, LOD_fract)) * 0.5;
}
```

三次采样对应三个连续的尺度。固定「当前级」`tex1` 作为主频，`mix(tex0, tex2, LOD_fract)` 在上下两级之间按小数部分线性插值——平均下来得到一个随深度平滑过渡的结果。视觉上：

- **层与层接缝消失**——每次 LOD 跳变时，两边的三次采样里有两次是完全相同的，只有第三次换了一档，权重变化是连续的。
- **不同尺度的 texel 叠加在同一个像素上**——这就是「fractal」的来历，结构上非常像 fBm 噪声（几个倍频段叠加），只不过叠加的对象是贴图采样而不是噪声函数。
- **省掉了 mipmap**——因为 fractal blend 本身就保证了 texel-per-pixel 的一致性，没有欠采样问题，直接用没有 mipmap 的纹理也不会 alias。这对 GameMaker 这种 mipmap 支持不够理想的引擎很有意义。

## 局限

Xor 自己点名了一个重要的适用边界：**fractal texturing 只对「天然可以任意缩放仍然合理」的纹理有效**——噪声、砂砾、草地、水面波纹、岩石表面。对**有固定比例尺**的纹理（砖墙、瓷砖、木地板）这一招就废了，因为它会把砖块放大到奇怪的尺寸，还会把两个尺度的砖块叠在一起形成视觉噪声。

本质上这是一个**尺度不变性**的约束：只有具有分形 / 自相似特征的纹理才能在任意尺度下保持合理。地形里的泥土、草、石头符合这个假设；人工结构不符合。

## 和 mipmap、triplanar 的位置

这个技巧和传统的纹理 LOD 是正交而互补的：

- **[[msaa-ssaa|Mipmap]]**：解决远距离 aliasing，用预过滤的小尺寸版本替代高频原图。
- **[[triplanar-mapping|Triplanar mapping]]**：解决**方向**问题——陡坡上 UV stretch，换成多轴采样 blend。
- **Fractal texturing**：解决**尺度**问题——同一个方向上、同一张纹理，距离跨度极大时保持一致的屏幕细节。

真实的 terrain shader 经常把三者叠起来：先 triplanar，再在每一路里做 fractal blend，必要时 mipmap 补上远距离的反 aliasing——三重组合能覆盖几乎任何复杂地形的视觉需求。

## 和 Shadertoy demo

Xor 的[原文 demo](https://www.shadertoy.com/view/mds3R4) 同屏对比了三种版本：无缩放、fractal、fractal + mipmap。从静态图里已经能看出 fractal 把重复感彻底消除了，mipmap 再进一步把最远处的闪烁压平——两者叠加效果最好。

## 相关
- [[fragment-shader]]
- [[msaa-ssaa]] —— aliasing 的更一般背景
- [[sampling-theorem-sinc]] —— 采样/过滤的理论基础
- [[triplanar-mapping]] —— 另一条 terrain 纹理路线
- [[sampler-filter-wrap-modes]]
- [[layered-grid-noise]] —— Xor 的另一个「多尺度叠加」技巧
- [[turbulence-domain-warping]] — 同一多尺度思路的 domain warping 变体
- [[xor-shader-artist]]
- [[planet-terrain-dem-pipeline]] —— Outerra 的行星尺度 DEM + fractal resample 管线

## Sources

- [[sources/xor-mini-fractal-texturing]]
