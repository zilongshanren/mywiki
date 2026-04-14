---
tags: [source, rendering, webgpu, playcanvas, 引擎]
date: 2026-04-14
sources: 1
---

# Build WebGPU Apps Today with PlayCanvas（Will Eastcott / PlayCanvas Blog）

[[will-eastcott|Will Eastcott]] 2024 年 4 月发表在 PlayCanvas 博客上的产品公告，宣布 WebGPU 支持正式上线 PlayCanvas Editor，并顺便交代了背后的工程节奏与行业态势。

## 摘要

PlayCanvas 自 2011 年起建立在 WebGL 之上，2017 年合作 Mozilla 首发 WebGL 2.0，如今追着 Chrome 113 把 WebGPU 默认打开的节奏，把 WebGPU 支持落地到 Editor。团队的第一优先是**视觉一致性**：切到 WebGPU 后既有 WebGL 项目必须渲染结果完全一致。真正的性能与功能收益来自 WebGPU 的**低驱动开销**与**原生 compute shader**——Engine v1.70.0 已经加入 compute 支持，官方 demo 展示 GPU 上 100 万粒子模拟。文章引用 Web3D Survey 的数据：2024 年 4 月已有 62.19% 终端用户可以跑 WebGPU，Firefox/Safari 的落地预计让这个数字在 2024 年内进一步上升。WebGPU 目前在 Editor 里仍是 beta，需要在项目设置里手动勾选 `Graphics Devices` 的 `WebGPU (beta)`，团队保留默认关闭直到成熟后再切默认。

## 关键要点

- PlayCanvas 的图形栈演进：WebGL → WebGL2 (2017) → WebGPU (2024)。
- 2024-04 Web3D Survey 数据：62.19% 终端用户可跑 WebGPU。
- 视觉一致性优先原则：切换后端不允许产生画面差异。
- Engine v1.70.0 加入 compute shader 支持；官方 100 万粒子 demo。
- 运行时 lightmapper 等功能尚未移植，因此保留 beta 状态。
- 用户需手动在 Project Settings → RENDERING → Graphics Devices 勾选 WebGPU。

## 链接到的概念

- [[webgpu-intro]]
- [[playcanvas-webgpu-editor]]
- [[gaussian-splatting-web]]
- [[will-eastcott]]

## 原文

- 链接：https://blog.playcanvas.com/build-webgpu-apps-today-with-playcanvas
- 本地：`raw/articles/blog.playcanvas.com/2024-04-18_build-webgpu-apps-today-with-playcanvas-playcanvas-blog.md`
