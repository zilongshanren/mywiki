---
tags: [source, playcanvas, gaussian-splatting, sogs, 压缩, webp, 球谐]
date: 2026-04-19
sources: 1
---

# PlayCanvas Adopts SOGS for 20x 3DGS Compression（Eastcott / PlayCanvas Blog）

[[will-eastcott|Will Eastcott]] 2025-05-15 发布于 blog.playcanvas.com 的工程公告：PlayCanvas Engine 2.7.5 引入了 **SOGS（Self-Organizing Gaussians）** 这个由 Fraunhofer HHI 的 Wieland Morgenstern 开发的压缩格式，把 3DGS 数据体积砍到 1/20。

## 摘要

3DGS 的典型文件体积是 web 分发的核心障碍——每个 Gaussian 要存位置/尺度/四元数旋转/opacity/基础色/45+ 个球谐系数，原始 PLY 动辄几百 MB 到 1GB。SOGS 借鉴图像压缩的做法：把所有 Gaussian 的每个属性摊成 2D "属性图"（59+ 张），用 **PLAS（Parallel Linear Assignment Sorting）** 算法重排 Gaussian 在 2D 网格上的位置，让邻居的主属性（位置、尺度、色）尽量相近，顺便让次要属性（opacity、旋转、SH）也跟着平滑——"co-sorting"。然后对每张已经平滑的属性图用 **WebP** 编码。PlayCanvas 的 church 示范场景从 1GB PLY 压到 55MB（~20×），浏览器侧用标准 WebP 解码即可。

## 关键要点

- **核心洞见**：压缩有序数据远比压缩噪声高效（排过序的图 vs 随机图，JPEG 下差 9×）。
- **三步流水线**：属性图摊平 → PLAS 排序 → WebP 编码。
- **排序键**：位置 + 尺度 + 基础色（主属性）；相似主属性的 Gaussian 次要属性大概率也相近。
- **解码代价极低**：浏览器原生 WebP 解码，不需要自研解码器。
- **Next step**：Editor 一等公民、SuperSplat 导出集成、性能优化提帧率。
- **开源谱系**：SOGS（Fraunhofer HHI）、PLAS（同团队）、PlayCanvas Engine（MIT）。

## 链接到的概念

- [[sog-compression-format]]
- [[gaussian-splatting-web]]
- [[supersplat-publish-platform]]

## 原文

- 链接：<https://blog.playcanvas.com/playcanvas-adopts-sogs-for-20x-3dgs-compression>
- 本地：`raw/articles/blog.playcanvas.com/2025-05-15_playcanvas-adopts-sogs-for-20x-3dgs-compression-playcanvas-b.md`
