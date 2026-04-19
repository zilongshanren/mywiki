---
tags: [source, playcanvas, gaussian-splatting, supersplat, annotations, 后处理, tonemapping, 3dgs]
date: 2026-04-19
sources: 1
---

# Build Gaussian Splat Experiences with SuperSplat Studio（Eastcott / PlayCanvas Blog）

[[will-eastcott|Will Eastcott]] 2026-02-11 发布于 blog.playcanvas.com 的产品公告：**SuperSplat Studio** 作为 [[supersplat-publish-platform|SuperSplat]] 平台之上的二级应用发布——把已发布的 splat 升级成带 annotations、post effects、tonemapping 控制的**交互式讲述体验**。

## 摘要

SuperSplat Studio 的三块功能：**Annotations / Hotspots**——在 splat 上放信息热点，每个含标题、描述、相机视点；点击后相机平滑过渡到保存的视点并展开内容。每场景上限 25 个，支持排序。Viewer 新增 annotation 导航条让观众顺序浏览。典型用途是教育 walkthrough、产品展示、导览。**Post Effects**——一整套由 PlayCanvas Engine 驱动的后处理：Bloom（高光晕）、Sharpen、Vignette、Color Grading（亮度/对比度/饱和度/色调）、Chromatic Fringing。所有参数实时预览。**Tonemapping + 背景色**：在 Linear / Filmic / ACES / ACES 2.0 / Hejl / Neutral 之间选；Bloom 等 HDR 相关效果需要打开 Scene 设置里的 High Precision Rendering。入口：在 SuperSplat Editor 发布 splat → 去 Manage 页 → 点 Edit 就进入 Studio。

## 关键要点

- **annotations 的落地**：这正是 [[supersplat-publish-platform|SuperSplat Viewer 开源公告]] 里预告的功能——把 Matterport 风格的信息热点搬到 3DGS。
- **post-processing 作为一等公民**：之前 SuperSplat 的侧重点在清洗和发布，Studio 把"视觉风格化"显性化为一层工具。
- **tonemapping 自选**：ACES / ACES 2.0 / Hejl / Neutral 等主流 operator 都在；对 splat 场景的偏色和高光处理有直接影响。
- **HDR 开关依赖**：Bloom 这类 HDR 特效需要 High Precision Rendering，文章明确提示——避免用户踩坑。
- **产品分层**：Editor = 清洗与发布；Studio = 叙事打磨；两者复用同一平台。

## 链接到的概念

- [[supersplat-publish-platform]]
- [[sog-compression-format]]

## 原文

- 链接：<https://blog.playcanvas.com/build-gaussian-splat-experiences-with-supersplat-studio>
- 本地：`raw/articles/blog.playcanvas.com/2026-02-11_build-gaussian-splat-experiences-with-supersplat-studio-play.md`
