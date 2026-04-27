---
tags: [source, rendering, z-buffer, depth-buffer, early-z, x-plane]
date: 2026-04-27
sources: 1
---

# You Can Never Have a Custom Z Buffer Distribution and Early Z at the Same Time（Ben Supnik / The Hacks of Life）

[[people/ben-supnik]] 发表于 2016 年 9 月的文章，论证自定义深度编码与 Early-Z 硬件优化之间存在无法调和的根本矛盾。

## 摘要

标准 GPU 深度精度按 1/z 分布，近裁剪面附近精度浪费严重。自定义方案（对数 Z、眼空间线性浮点深度）可以改善分布，但它们产生非线性的裁剪空间 Z 值，必须在 fragment shader 里逐像素计算，这直接关闭了 Early-Z 优化。不仅写 Z 的 pass 受影响，所有做 Z 测试的物体（粒子、云层等填充率密集效果）都要在 fragment shader 里重新计算深度，带来双倍甚至更高的代价。唯一不破坏 Early-Z 的"更好分布"方案是 [[reversed-z]]（配合 ARB_clip_control），X-Plane 由于该扩展普及率不足，暂时维持两段 Z pass 的方案保留 Early-Z。

## 关键要点

- 自定义 Z 编码（log-Z、eye-space linear）在顶点阶段写入时会产生三角形内部非线性插值误差，必须移到 fragment shader
- Fragment shader 修改深度值 → GPU 丢弃 Early-Z → 被遮挡像素的 shader 照常执行
- 代价不止一次：所有 Z 测试物体均需在 fragment shader 计算自定义深度
- Reversed-Z + 浮点深度缓冲是唯一同时拥有好精度分布和 Early-Z 的路径
- X-Plane 的两段 Z pass：只改 near/far，复用 shadow map 和 G-Buffer，将分帧代价降到最低

## 链接到的概念

- [[rendering/z-buffer-custom-encoding-early-z-tradeoff]]
- [[rendering/z-buffer]]
- [[rendering/reversed-z]]
- [[rendering/early-z-late-z]]
- [[rendering/depth-texture-silhouette]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2016/09/you-can-never-have-custom-z-buffer.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2016-09-08_you-can-never-have-a-custom-z-buffer-distribution-and-early.md`
