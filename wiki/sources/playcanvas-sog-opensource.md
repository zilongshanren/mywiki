---
tags: [source, playcanvas, gaussian-splatting, sog, 压缩, morton-order, webp, 3dgs]
date: 2026-04-19
sources: 1
---

# PlayCanvas Open Sources SOG: The WebP of Gaussian Splatting（Eastcott / PlayCanvas Blog）

[[will-eastcott|Will Eastcott]] 2025-09-17 发布于 blog.playcanvas.com 的正式格式公告：**SOGS 升级为 SOG（Spatially Ordered Gaussians）**，格式规范、参考写入（SplatTransform）、参考渲染（PlayCanvas Engine）全部开源。标题自诩是 "WebP of Gaussian Splatting"。

## 摘要

SOG 延续 SOGS 的路子（`meta.json` + 多张 `.webp` 图），但在四处改进：**Morton order** 存储让 splat 在空间上按 Z-order 曲线排列，加载时不需要预处理、"GPU-ready"；**单 `.sog` 打包**（ZIP 壳）使分发变成一个文件（散包 `.json`+`.webp` 仍可用但 Editor 不支持）；压缩端从 **CUDA 换到 WebGPU**，打破原先 SOGS 对 NVIDIA 卡的依赖；同等比特下精度更高，伪影更少。数字：4M Gaussian 的 skate park 从 1GB PLY 压到 42MB（~95%）；比 Compressed PLY 进一步缩 2-3×。工具链集成：PlayCanvas Engine 2.11.0+ 原生支持、[[playcanvas-react-declarative|PlayCanvas React]] 和 Web Components 同步、Editor 把 `.sog` 作为一等资产（拖进来自动建 GSplatComponent）、SuperSplat 默认用 SOG 压缩。规范和参考实现（SplatTransform 写入、Engine 读取/渲染）一并开源，鼓励其他引擎接入成为事实标准。致谢 Wieland Morgenstern（SOGS 作者）和 Vincent Woo（SOGS → PlayCanvas 集成）。

## 关键要点

- **四项改进**：Morton order（GPU-ready）、单文件 `.sog`、WebGPU 压缩（跨平台）、更高精度。
- **压缩能力**：~95% 缩减（比 SOGS 的 ~20× 更进一步），相对 Compressed PLY 2-3×。
- **单文件 vs 散包**：`.sog` 是 ZIP 打包，便于分发；散包 Editor 不认。
- **WebGPU compute 解锁压缩端可移植性**：SOGS 需要 CUDA，SOG 只要 WebGPU——从 NV-only 打开到任何 GPU。
- **全栈集成**：Engine / React / Web Components / Editor / SuperSplat 同步支持。
- **规范开源**：不仅开源实现，连格式规范也开源，鼓励成为跨引擎标准。

## 链接到的概念

- [[sog-compression-format]]
- [[splat-transform-cli]]
- [[supersplat-publish-platform]]
- [[gaussian-splatting-web]]
- [[webgpu-intro]]

## 原文

- 链接：<https://blog.playcanvas.com/playcanvas-open-sources-sog-format-for-gaussian-splatting>
- 本地：`raw/articles/blog.playcanvas.com/2025-09-17_playcanvas-open-sources-sog-the-webp-of-gaussian-splatting-p.md`
