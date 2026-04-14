---
tags: [source, rendering, gaussian-splatting, playcanvas, 编辑器]
date: 2026-04-14
sources: 1
---

# Create 3D Gaussian Splat Apps with the PlayCanvas Editor（Will Eastcott / PlayCanvas Blog）

[[will-eastcott|Will Eastcott]] 2024 年 6 月发表的文章，宣布 PlayCanvas Editor 对 3D Gaussian Splatting 的原生支持，并给出一个从手机扫描到发布应用的完整工作流示范。

## 摘要

文章以一个"虚拟雕像展厅"为例展开整条 web 3DGS 工作流：**Step 1**，在 SuperSplat 里清洗扫描得到的 PLY，裁掉背景、对齐原点、导出成 PlayCanvas 的**压缩 PLY 格式**——示例里 V&A 博物馆的雕像压缩后只有 **1.56MB**。**Step 2**，把压缩 PLY 拖进 Editor 的 Asset Panel，再拖进视口加入场景，配合 cube map 加出背景；同时从 Asset Store 拉 Orbit Camera 脚本，配 UI、音效、物理、VR/AR 等常规 Editor 功能。**Step 3**，动画与后处理：Editor 允许**自定义 splat 的渲染 shader 代码**，示例里用 shader 逐 splat 做位置变换与重着色做出淡入淡出的过渡，再叠一层全屏 bloom。作者把这条工作流定位为面向产品可视化、汽车、教育、旅游等多个垂直行业的通用方案，并推荐读者 fork 示例项目体验。

## 关键要点

- 工作流：手机扫描 → SuperSplat 清洗 → 压缩 PLY 导入 Editor → 动画/后处理 → 发布。
- V&A 雕像压缩 PLY 只有 1.56MB，显示压缩 PLY 对 web 场景可行。
- Editor 支持 Splat 作为一等资产拖拽导入、脚本化、配合 Orbit Camera / UI / 物理 / VR-AR。
- **Editor 允许定制 splat 的渲染 shader**：示例用它做淡入淡出过渡与逐 splat 变换/变色。
- 目标垂直：产品可视化（家具、服饰、电子产品）、汽车、教育、旅游等。
- 提供示例项目 "3D Gaussian Splat Statues" 供 fork 学习。

## 链接到的概念

- [[gaussian-splatting-web]]
- [[supersplat-pwa]]
- [[playcanvas-webgpu-editor]]
- [[will-eastcott]]

## 原文

- 链接：https://blog.playcanvas.com/create-3d-gaussian-splat-apps-with-the-playcanvas-editor
- 本地：`raw/articles/blog.playcanvas.com/2024-06-05_create-3d-gaussian-splat-apps-with-the-playcanvas-editor-pla.md`
