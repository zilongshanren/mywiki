---
tags: [人物, 作者, playcanvas, 引擎, webgpu]
date: 2026-04-14
sources: 14
---

# Will Eastcott

**Will Eastcott** 是 [PlayCanvas](https://playcanvas.com) 的联合创始人兼 CEO，也是该公司博客上技术公告的主要作者。PlayCanvas 是一款面向 web 的 3D 引擎，自 2011 年起与 Mozilla 等浏览器厂商紧密合作推动 WebGL / WebGL2 / [[webgpu-intro|WebGPU]] 等新一代图形 API 的落地。Eastcott 的文章通常以产品发布公告的形式出现，但在"产品动机"一节里会给出相当诚实的工程细节——比如 WebGPU 切换时"视觉一致性优先于性能"、比如 compute shader 如何让 splat 处理 2 倍提速——是了解一个**商业 web 引擎如何推进 API 迁移**的第一手视角。

## 主要贡献

- 2024 年主导把 WebGPU 支持落地到 PlayCanvas Editor（[[playcanvas-webgpu-editor]]）。
- 推动 PlayCanvas 在 3D Gaussian Splatting 领域的工具链建设：开源 [[supersplat-pwa|SuperSplat]] 编辑器、Editor 原生集成 3DGS（[[gaussian-splatting-web]]）、设计 compressed PLY 格式。
- 在 blog.playcanvas.com 上持续输出产品与工程公告，是观察 web 3D 行业节奏的重要信号源。
- 2024 年 8 月推动 PlayCanvas Engine 从 1.x 跨到 **2.0.0**（[[playcanvas-engine-2-breaking-changes]]），借 major bump 砍掉 WebGL 1 / Scripts 1.0 / AudioSourceComponent 等长期 cruft，为 [[webgpu-intro|WebGPU]] 后端腾出接口预算。
- 2025 年主导 [[supersplat-publish-platform|SuperSplat]] 从编辑器扩张为编辑-发布-托管-社区一体化平台（2.0 发布 + 2.2 视频渲染与 embed + viewer 开源），并把整条链路全部 MIT 开源。
- 2025 年发布 [[sog-compression-format|SOGS → SOG]] 压缩格式，把 3DGS 数据压到 1GB → 42MB（~95%），格式规范和参考实现全部 MIT 开源。
- 2025-07 开源 [[splat-transform-cli|SplatTransform]] CLI，把 SuperSplat 的批处理能力变成命令行工具：格式互转、空间变换、多文件合并、过滤、CSV 导出。
- 2026-02 发布 SuperSplat Studio（annotations + post effects + tonemapping），2026-03 发布 Walk Mode（voxel collision 驱动的第一人称探索）+ Streamed LOD（基于 SOG 切片）+ Easy Upload。

## 相关
- [[webgpu-intro]]
- [[playcanvas-webgpu-editor]]
- [[gaussian-splatting-web]]
- [[supersplat-pwa]]
- [[playcanvas-engine-2-breaking-changes]]
- [[supersplat-publish-platform]]
- [[mark-lundin]]
- [[dave-evans]]

## Sources

- [[sources/playcanvas-webgpu-editor]]
- [[sources/playcanvas-supersplat-pwa]]
- [[sources/playcanvas-editor-gaussian-splat]]
- [[sources/playcanvas-engine-2-release]]
- [[sources/playcanvas-supersplat-2-0-publish]]
- [[sources/playcanvas-supersplat-2-2-video]]
- [[sources/playcanvas-supersplat-viewer-oss]]
- [[sources/playcanvas-sogs-20x-compression]]
- [[sources/playcanvas-splat-transform-cli]]
- [[sources/playcanvas-sog-opensource]]
- [[sources/playcanvas-reflct-spotlight]]
- [[sources/playcanvas-voxelo-spotlight]]
- [[sources/playcanvas-supersplat-studio]]
- [[sources/playcanvas-supersplat-walk-lod]]
