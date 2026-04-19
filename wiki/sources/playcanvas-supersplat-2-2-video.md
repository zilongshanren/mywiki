---
tags: [source, playcanvas, supersplat, 视频渲染, 嵌入, 社区]
date: 2026-04-19
sources: 1
---

# Render Your Gaussian Splats to Video with SuperSplat 2.2（Will Eastcott / PlayCanvas）

[[will-eastcott]] 在 2025 年 3 月发表，宣布 SuperSplat 2.2，给 [[supersplat-publish-platform|SuperSplat 发布平台]]加上**视频渲染**、**splat 嵌入**和一套社区功能。

## 摘要

SuperSplat 2.2 把 2.0 刚加的 Timeline 相机动画接上了视频输出管线：在新增的 `Render` 菜单里选分辨率、码率，甚至可以直出竖屏比例——适配短视频平台。作者强调视频编码"impressively fast"，暗示走的是浏览器侧的 WebCodecs 或类似硬件加速路径。社区侧同步上线了 **user pages**（每个创作者有自己的展示页）、**评论**、**社交分享**（X / LinkedIn / Slack / email）和 **embed**：点 viewer 里的 Embed 按钮、拷 HTML、贴到自己网站里——出来的是**可交互的 3D splat**而不是 iframe 视频。Viewer 本身也迭代了若干可用性改进：进度条刷场景动画、Orbit / Fly 相机模式切换、重新设计的 Info Panel 覆盖桌面与移动端使用说明。

## 关键要点

- **视频渲染闭环**：Timeline 关键帧 → 视频输出是"splat 生产短视频内容"的完整工作流；对营销、展示、社交平台分发直接可用。
- **竖屏视频预设**：3DGS 工具首次主动适配移动端短视频形态。
- **可交互 embed**：3DGS 从"点开一个链接看"升级为"嵌在任意页面里滚动就能看"，替代 2D 产品图的潜力开始显现。
- **社交 stack**：user page + 评论 + 分享按钮 = 3DGS 版的 Sketchfab 雏形。
- **Orbit vs Fly 相机**对应两种使用场景：Orbit 适合物体展示、Fly 适合空间漫游；在 viewer 层直接一键切换。
- 版本节奏：2.0（2025-02）到 2.2（2025-03）只差一个月，迭代速度相当快。

## 链接到的概念

- [[supersplat-publish-platform]]
- [[supersplat-pwa]]
- [[gaussian-splatting-web]]

## 原文

- 链接：<https://blog.playcanvas.com/render-your-gaussian-splats-to-video-with-supersplat>
- 本地：`raw/articles/blog.playcanvas.com/2025-03-13_render-your-gaussian-splats-to-video-with-supersplat-2-2-pla.md`
