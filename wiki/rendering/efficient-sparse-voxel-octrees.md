---
tags: [渲染, 体素, SVO, GPU, 光线追踪, NVIDIA]
date: 2026-04-19
sources: 1
---

# Efficient Sparse Voxel Octrees（Laine 2010）

Samuli Laine 与 Tero Karras 在 NVIDIA Research 发表的论文，把 **Sparse Voxel Octree（SVO，稀疏体素八叉树）** 做到了当时公认最实用的一版——附带完整 CUDA 开源实现，直接推动了"用体素做光线追踪"这条路线的复活。[[sam-lapere|Sam Lapere]] 在 2010 年 3 月第一时间把论文、视频和代码链接转到博客上。

## 核心贡献

- **Contour（轮廓）**：在每个叶节点存一个局部平面或曲面片段，让体素边缘在放大时不再显得块状。这是论文最直观的视觉改进——只增加少量数据就把"体素一放大就像 Minecraft"的观感消掉。
- **Compact encoding**：子节点指针与掩码压到很紧，一个 SVO 节点只占几个字节，显存占用落到可以塞进 GPU 的范围。
- **CUDA ray cast**：附带的 GPU ray cast 代码演示了对百万级体素的交互率遍历，成为后续 voxel GI、voxel cone tracing 等方向的起点。

## 意义

SVO 这个数据结构早在 2000 年代初就被提出，但长期停留在"理论好看、工程难落地"。Laine 的版本第一次让它同时具备：

1. **GPU 友好**——指针压缩、叶节点打包，访存模式适配 CUDA；
2. **无明显块状感**——contour 修正几何走样，使得 SVO 渲染出来的画面逼近连续几何；
3. **开源可复用**——代码放在 code.google.com 上，任何人都可以拿来改。

在这之后的十年里，SVO 被反复引用进：NVIDIA 的 VXGI（voxel GI）、Crassin 的 voxel cone tracing、id Tech 的 SVOGI 实验、以及后来各种 voxel 引擎的场景结构。Hans Krieg 给 Voxelstein 3D 加的 SVO + BIH 路径追踪扩展（Lapere 同篇博客报道）就是早期社区尝试之一。

## 相关

- [[hybrid-voxel-software-raytracing]]
- [[gpu-unbiased-path-tracing]]
- [[path-tracing-basics]]
- [[sam-lapere]]

## Sources

- [[sources/raytracey-svo-path-tracing-update]]
