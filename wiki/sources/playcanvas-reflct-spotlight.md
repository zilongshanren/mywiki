---
tags: [source, playcanvas, gaussian-splatting, 电商, three-js, 迁移, 3dgs]
date: 2026-04-19
sources: 1
---

# Gaussian Splatting for E-Commerce - Developer Spotlight on Reflct（Eastcott / PlayCanvas Blog）

[[will-eastcott|Will Eastcott]] 2025-08-21 发布于 blog.playcanvas.com 的 Developer Spotlight 第五期：采访 Reflct（新西兰团队）的 In Ha 和 Willie，他们把 3DGS 做成可配置"镜头点 + 轨道边界"的电商 viewer，并把底层从 three.js 迁到了 PlayCanvas。

## 摘要

Reflct 的核心产品是给**非技术用户**看 3DGS 的 viewer：底部三个大按钮（左右箭头 + 播放），拖屏幕只能绕一个点做 orbit。看起来简单是因为复杂度全压到了创作者侧——他们在 Reflct dashboard 里放若干"views"，每个 view 存相机位姿 + 焦点 + orbit 限制 + 过渡动画 + 可选 product metadata，被按钮切换时平滑过渡。**orbit 限制**是关键设计：避免观众看到 3DGS 场景的"rough edges"（扫描盲区、飞点）。与 Shopify 集成后 view metadata 可以挂 `productHandle`，自动拉产品详情——"shoppable 3DGS"。技术面上他们从 Mark Kellogg 的 `GaussianSplats3D` three.js 插件切到 PlayCanvas：相同 PLY 下帧率近乎翻倍、内存降 80%；切 [[sog-compression-format|SOG]] 后同场景 3SH 版本比他们之前"最优格式"2SH 的包体还小一半，关键资源显存降 95%+。迁移方法论：先把 UI 和事件监听从三维层里剥出去，再替换核心渲染器，剩下的自动对齐——"他们都是提供 3D 空间、相机、3D 对象，本质相通"。

## 关键要点

- **UX 设计**：三按钮 + 创作者侧约束，典型"把复杂度后移给专业人"的分工。
- **orbit 限制作为产品特性**：不只是 UX 润色，也是"隐藏 3DGS artifacts"的工程手段——3DGS 扫描在某些角度暴露飞点和空洞，约束相机可以让用户只见好处。
- **Shopify / React 集成库**：Reflct 不把自己当纯 viewer，而是提供 React 组件和 Shopify app 让第三方网站挂进去。
- **three.js → PlayCanvas 迁移**：帧率 ~2×、内存 -80%、3SH vs 2SH 包体还小一半。
- **SOG 推动迁移**：是压垮 three.js 插件生态的"最后一根稻草"——SOGs demo 出来后 Reflct 决定重构。
- **迁移方法**：剥离 UI 层 → 换 renderer → 剩下自然对齐（因为 API 概念同构）。

## 链接到的概念

- [[sog-compression-format]]
- [[gaussian-splatting-web]]
- [[supersplat-publish-platform]]

## 原文

- 链接：<https://blog.playcanvas.com/gaussian-splatting-for-e-commerce-developer-spotlight-on-reflct>
- 本地：`raw/articles/blog.playcanvas.com/2025-08-21_gaussian-splatting-for-e-commerce-developer-spotlight-on-ref.md`
