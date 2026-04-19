---
tags: [source, unity, urp, shader-graph, subgraph]
date: 2026-04-19
sources: 1
---

# Shader Toolbox for URP - Subgraph Library（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 为 *Shader Toolbox for URP* 编写的 **subgraph 节点速查表**——pack 里可以直接拖到用户 Shader Graph 中的通用子图清单。

## 摘要

Shader Toolbox 除了提供 11 个成品效果 shader 以外，还附带了一套**通用 subgraph 节点库**，可在用户自己的 Shader Graph 里复用。清单分几类：**色彩空间转换**（HCL↔RGB 双向），**光照数据获取**（Get Main Light 返回方向/颜色/shadow & distance attenuation、Get Ambient Light 返回球谐光照），**贴图与向量工具**（Apply Normal Map 将切线空间法线叠加到世界法线、Find Perpendicular Vectors 给任意向量返回两正交向量并对零向量做保护、Sample Texture 2D Grad 让用户手动供应梯度向量以避免 divergent sampling），**Lit 组合积木**（Lit Default 打包 PBR 属性、Lit Stochastic 在 Default 基础上追加 [[stochastic-texture-sampling|stochastic sampling]] 抑制平铺），以及两个关键增强：**Better Voronoi** 把 [[worley-voronoi-noise|Voronoi]] 节点升级为同时输出「到最近 cell 中心距离」和「到 cell 间边界距离」——原生 Voronoi 只有前者，后者才是构建 [[voronoi-lava-shader|Voronoi Lava]] 分层的关键；以及 **Sample Transparent Texture** 读取 pack 引入的 `_CameraTransparentTexture`（若未配置 pipeline 则 fallback 到灰色默认纹理）。

## 关键要点

- Pack 的双层价值：**成品 shader** + **可重组的 subgraph 原子库**——后者是更长期的资产
- **Better Voronoi** 的「到边距离」输出是 Lava / 裂纹 / 干涸河床等效果能 work 的前提，原生 Voronoi 节点不足
- Lit Default / Lit Stochastic 是让用户自定义 shader 也能继承 URP Lit 的 PBR 光照管线的入口
- Apply Normal Map 暴露的是「tangent-space 法线如何组装回 world-space」这条样板——避免用户在每张图里重写
- Find Perpendicular Vectors 对 zero vector 的保护是细节但决定健壮性——向量场中偶尔会采到零梯度区
- Sample Texture 2D Grad 用户自控梯度，与 [[divergent-gradient-in-branches|分支内采样的梯度丢失问题]] 相关——在 `if` 分支里手动喂梯度是规避之一

## 链接到的概念

- [[shader-graph-custom-function-hlsl]]
- [[worley-voronoi-noise]]
- [[stochastic-texture-sampling]]
- [[tangent-space-normal-mapping]]
- [[divergent-gradient-in-branches]]
- [[urp-volume-post-processing]]

## 原文

- 链接：https://danielilett.com/shader-toolbox/subgraph-library/
- 本地：`raw/articles/danielilett.com/2026-01-01_shader-toolbox-for-urp-subgraph-library.md`
