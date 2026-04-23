---
tags: [source, raytracey, SVO, 体素, 路径追踪]
date: 2026-04-19
sources: 1
---

# SVO and path tracing update（Sam Lapere, 2010-03）

[[sam-lapere|Sam Lapere]] 发表于 2010 年 3 月的短博，一篇是两个消息的合订：Voxelstein 3D 给引擎加 SVO 路径追踪扩展，以及 NVIDIA Research 的 Samuli Laine 公开了 [[efficient-sparse-voxel-octrees|Efficient Sparse Voxel Octrees]] 论文、视频和 CUDA 代码。

## 摘要

Voxelstein 3D 的作者（Hans Krieg）给引擎加了一条路径追踪扩展，用 **SVO + BIH（bounding interval hierarchy）** 组织体素，CUDA 与 CPU 双实现。初期出图偏糙，但自带柔和的全局光照。紧接着 Laine 的论文放出——Lapere 称它是"到目前为止 SVO 最实用、最 efficient 的实现"，并附开源 CUDA 代码。两条消息放一起，说明 2010 年初 SVO 作为一种 ray-traceable 场景结构正在从学术走向社区可用。

## 关键要点

- Voxelstein 3D 社区尝试：SVO + BIH 组合，CPU + CUDA 双路径
- Laine 的 SVO 贡献在于 **contour**（消除体素放大后的块状感）与紧凑编码
- Lapere 预判 SVO 很快会被"graphics engineers 滥用"——事实上后来 voxel GI、voxel cone tracing、VXGI 都走了这条线

## 链接到的概念

- [[efficient-sparse-voxel-octrees]]
- [[hybrid-voxel-software-raytracing]]
- [[gpu-unbiased-path-tracing]]

## 原文

- 链接：http://raytracey.blogspot.com/2010/03/svo-and-path-tracing-update.html
- 本地：`raw/articles/raytracey.blogspot.com/2010-03-11_svo-and-path-tracing-update.md`
