---
tags: [source, 渲染, shader, 纹理, uv, gamemaker]
date: 2026-04-14
sources: 1
---

# Mini: Two Textures（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2022 年 10 月的一篇，讲 **GameMaker 的 texture page 系统**和**在 shader 里同时用两张贴图**的正确姿势。文章从 atlas 的工作机制入手，推出一对 `normalize/unnormalize` UV 转换函数，是后续 ShaderToy 移植教程的前置。

## 摘要

GameMaker 把 sprite 自动打包进 2048×2048 的 texture page，shader 里拿到的 `v_vTexcoord` 是 atlas 全局坐标——单个 sprite 的 UV 并不在 0–1 范围，所以直接写 `fract(uv)` 这类周期操作会采到隔壁 sprite。两种应对：(1) 强制 sprite 独占 texture page（会加 padding、掉 batching）；(2) 手工归一化——把 sprite 的 `[x, y, w, h]` 作为 uniform 传进来，用 `(coord - uvs.xy) / uvs.zw` 从 atlas UV 拿到 sprite-local 的 0–1 坐标，用 `coord * uvs.zw + uvs.xy` 反向转回去。所有非平凡 UV 操作（翻转、扭曲、渐变）都在 local 空间做，最后反归一化去采样。文章末尾把这个思路推广到**两张贴图 blend**：diffuse 归一化成 local 再用 AO 贴图的矩形反归一化，一次 sampler 采到两张贴图对应的像素——normal mapping、splat map、mask 类效果的基础。

## 关键要点

- **Texture page**：GM 的自动 atlas 打包机制，2048² 或按平台配置，2 次幂尺寸。
- **边缘 padding**：GM 在 sprite 边上加复制像素防止滤波串色；但不能阻止 shader 主动采到邻居。
- **Separate texture page** 选项：独占一页、强制 2 次幂、掉 batching——能用但代价大。
- **更好的解法**：通过 `sprite_get_uvs()` 把矩形传入 shader，在 shader 里做 `normalize/unnormalize`。
- **跨 sprite 映射**：normalize(A_uv, A_rect) 得到的 local UV 可以用 B_rect 反归一化——两张贴图就能对齐。
- 前置：GM 的 `v_vTexcoord` 是 atlas 范围；后续 [[sources/xor-mini-shadertoy|ShaderToy 移植]] 依赖本篇。

## 链接到的概念

- [[two-texture-sampling-tricks]]
- [[texel-pixel-conversion]]
- [[shadertoy-basics]]
- [[uv-manipulation-nodes]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/gm-shaders-mini-two-textures-1376349
- 本地：`raw/articles/mini.gmshaders.com/2022-10-01_mini-two-textures.md`
