---
tags: [source, playcanvas, supersplat, 开源, viewer, 3dgs]
date: 2026-04-19
sources: 1
---

# SuperSplat 3DGS Viewer is now Open Source（Will Eastcott / PlayCanvas）

[[will-eastcott]] 在 2025 年 4 月发表，宣布 **SuperSplat Viewer** 从闭源转为 MIT 开源，补齐了 SuperSplat 全链路的开源版图。

## 摘要

自 2023 年 11 月首次发布以来，SuperSplat 编辑器本身一直是开源的；但**把 splat 放上线让人看**的那个 viewer——即用户 `Publish` 之后跳转的网页播放器，或点 `Download Viewer` 自托管时拿到的那一坨前端代码——此前一直闭源。2025 年 4 月 9 日，团队把 `playcanvas/supersplat-viewer` 仓库以 MIT 协议开放到 GitHub，意味着现在"编辑 → 发布 → 观看"三段全部开源可复用。Eastcott 列出了 viewer 的卖点：基于 [[playcanvas-webgpu-editor|PlayCanvas Engine]] 的高帧率、先进的 3DGS shader 带来的视觉质量、AR / VR WebXR 支持、Timeline 相机动画播放、全屏、Orbit / Fly 双相机模式；并预告了下一个大功能**annotations**——在 splat 场景里放置信息面板，像 Matterport 的 tag 但嵌在 3DGS 里。

## 关键要点

- **开源补齐最后一块**：从编辑器、到引擎、到现在的 viewer，SuperSplat 的完整链路都是 MIT——用户既可以用托管版本，也可以 fork 自己魔改。
- **viewer 统一**：`superspl.at` 托管版和自托管 `Download Viewer` 本质是同一份代码，保证体验一致。
- 卖点清单映射出 3DGS viewer 的**标准功能集**：高性能 + WebXR + 相机动画 + 全屏 + 多相机模式。
- **annotations 预告**：3DGS 走向"可交互沉浸内容"（导览、教学、产品说明）的下一步。
- 开源动机的表达：感谢 3DGS 社区 18 个月的集体推进，团队以"开源回馈"作为立场。

## 链接到的概念

- [[supersplat-publish-platform]]
- [[supersplat-pwa]]
- [[gaussian-splatting-web]]
- [[playcanvas-webgpu-editor]]

## 原文

- 链接：<https://blog.playcanvas.com/supersplat-3dgs-viewer-is-now-open-source>
- 本地：`raw/articles/blog.playcanvas.com/2025-04-09_supersplat-3dgs-viewer-is-now-open-source-playcanvas-blog.md`
