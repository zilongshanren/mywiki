---
tags: [source, 渲染, 虚拟纹理, tiled-resources, directx, 流式纹理]
date: 2026-04-27
sources: 1
---

# Tiled Resources / Partially Resident Textures / MegaTextures（Wolfgang Engel）

[[people/wolfgang-engel]] 于 2013 年 7 月发表，一句话主题：对比 DirectX 11.2 / OpenGL 4.4 新引入的硬件 Tiled Resources 特性与软件 MegaTexture 方案，分析艺术家工作量对 MegaTexture 实际可行性的制约。

## 摘要

文章先梳理开放世界游戏解决高分辨率纹理的两条传统路线：持续流式加载（texture streaming）和程序化生成大纹理（依赖 dependent texture read）。MegaTexture 允许存储更多细节，但其最大障碍往往被忽视——有人必须生成这张巨大纹理。"Stamping"（在纹理上多处复用同一图章）在缓解工作量的同时破坏了唯一像素的核心优势。对卫星图像等预存在的高分辨率数据源，MegaTexture 则非常合适。DirectX 11.2 的 Tiled Resources（AMD OpenGL 扩展：AMD_sparse_texture）把 MegaTexture 的核心机制搬进了硬件：可以直接对虚拟大纹理做各向异性过滤，无需 dependent texture read，且 AMD 和 NVIDIA 都在 2013 年左右开始提供支持。Engel 特别期待将 Tiled Resources 用于缓存式阴影贴图（Cached Shadow Maps）。

## 关键要点

- 硬件 Tiled Resources vs 软件 MegaTexture：前者支持硬件各向异性过滤，无 dependent read 开销
- MegaTexture 的实际瓶颈在于美术制作成本，Stamping 与"唯一像素"优势相矛盾
- 卫星/航拍数据等外部高分辨率素材是 MegaTexture 最合适的使用场景
- D3D11.2 Tier1/Tier2 区别在文章中未展开（作者留为后续讨论）
- Cached Shadow Maps 是 Tiled Resources 的另一个高价值应用

## 链接到的概念

- [[megatexture-virtual-texturing]]
- [[cached-shadowmaps]]
- [[mipmap-generation-sampling]]
- [[virtual-memory]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2013/07/tiled-resources-partially-resident.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2013-07-22_tiled-resources-partially-resident-textures-megatextures.md`
