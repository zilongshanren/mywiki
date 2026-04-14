---
tags: [source, rendering, gaussian-splatting, supersplat, pwa, playcanvas]
date: 2026-04-14
sources: 1
---

# A Faster SuperSplat with PWA Support（Will Eastcott / PlayCanvas Blog）

[[will-eastcott|Will Eastcott]] 2024 年 5 月 22 日发表的 SuperSplat v0.17.1 发布说明，聚焦两项改动：**2× GPU 性能**与 **PWA 化**。

## 摘要

SuperSplat 是 PlayCanvas 开源的 3D Gaussian Splatting 编辑/优化工具，这次更新带来两个层面的跃迁。性能侧，底层 PlayCanvas Engine v1.71.0 借 [[webgpu-intro|WebGPU compute shader]] 重写了 splat 的 GPU 处理路径，bike 场景的 GPU 耗时从 32ms 降到 13.5ms，整体性能提升超过 2 倍；这让 SuperSplat 能流畅处理百万级 splat。交付侧，SuperSplat 新增 **Progressive Web App** 支持：用户从地址栏 "Install SuperSplat" 就可以把它装到桌面、任务栏（Windows）、Dock（macOS）；安装后 PWA 向操作系统注册了 PLY 文件关联，右键 PLY 可以直接选 SuperSplat 打开，甚至设为默认工具后双击 PLY 就直接进编辑器。两条改动合起来让 SuperSplat 从"在线 demo"变成"本地工具链的一环"。

## 关键要点

- bike 场景 GPU 耗时 32ms → 13.5ms，2× 加速。
- 加速来自 PlayCanvas Engine v1.71.0 对 splat 处理的 compute shader 重写（PR #6357）。
- PWA 安装：地址栏 "Install SuperSplat"，支持钉到 Taskbar/Dock。
- PLY 文件关联：右键 → 选 SuperSplat，或设为默认工具双击打开。
- 目标是让百万级 splat 的编辑也能保持流畅帧率。

## 链接到的概念

- [[supersplat-pwa]]
- [[gaussian-splatting-web]]
- [[playcanvas-webgpu-editor]]
- [[webgpu-intro]]
- [[will-eastcott]]

## 原文

- 链接：https://blog.playcanvas.com/a-faster-supersplat-with-pwa-support
- 本地：`raw/articles/blog.playcanvas.com/2024-05-22_a-faster-supersplat-with-pwa-support-playcanvas-blog.md`
