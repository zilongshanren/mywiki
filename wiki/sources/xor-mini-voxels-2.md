---
tags: [source, 渲染, 体素, shader, gamemaker]
date: 2026-04-19
sources: 1
---

# GM Shaders: Voxels 2（Xor / mini.gmshaders.com）

[[xor-shader-artist|Xor]] 发表于 2024 年 8 月的文章，接续前一篇 DDA voxel raytracing 教程，讲**如何在 GameMaker 这种缺 3D texture / SSBO 的引擎里用 2D 纹理做可编辑的体素地图存储**。

## 摘要

体素地图要想做到「用户可编辑、不每帧重算」，需要一个 GPU 可读写的 3D 数据结构。但 GameMaker（以及许多老版本 OpenGL / WebGL）不支持 3D texture 和 Shader Storage Buffer。Xor 提出的 workaround 是**把 3D 世界按 z 层铺开，每层作为一个子区域拼进同一张 2D 纹理**，构成一个 3D Look-Up Table：8×8 的层布局让 64³ 世界只占 512×512 纹理，最大可支持约 1024×1024×256（受限于 16k 纹理边长）。他给出了 `uv_to_block` 和 `block_to_uv` 两个互逆函数，通过 `mod / floor / dot` 几步代数完成 3D ↔ 2D 地址转换；前者用于 raymarch 采样，后者用于编辑器写 render target。这篇是 Xor voxel 教程系列的第二篇，重点在**持久化与可编辑**，而非渲染本身。

## 关键要点

- 没有 3D texture 时的通用做法：**2D 纹理 + 按 z 层平铺**。
- 布局参数是 4D：`(cell_w, cell_h, cols, rows)`——行优先读法「像读书」。
- `uv_to_block` 和 `block_to_uv` 构成互逆映射，shader 里几条指令搞定。
- 最大世界尺寸受 GPU 最大纹理边长限制（16k → 1024×1024×256）。
- 纹理既是采样源也是 render target，天然支持 runtime 编辑。
- 完整 [GM_Voxels GitHub demo](https://github.com/XorDev/GM_Voxels) 可跑。

## 链接到的概念

- [[voxel-map-lut-2d]]
- [[raymarching-intro]]
- [[greedy-voxel-meshing]]
- [[voxel-ambient-occlusion]]
- [[color-lut]]
- [[texture-swizzle-nested-tiling]]

## 原文

- 链接：<https://mini.gmshaders.com/p/voxels2>
- 本地：`raw/articles/mini.gmshaders.com/2024-08-25_gm-shaders-voxels-2.md`
