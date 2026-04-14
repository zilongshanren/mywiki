---
tags: [人物, 作者, shader教程]
date: 2026-04-14
sources: 12
---

# Linden Reid

独立游戏开发者与 shader 教程作者（博客 lindenreid.wordpress.com / lindenreidblog.com，Twitter `@so_good_lin`）。定位是面向初学者的 Unity shader 与程序化几何教程，写作风格偏口语、重配图、重"为什么"——典型读者是刚从 gameplay/美术跨入图形编程的人。

她自己的叙述里反复强调"视觉化数学"：把线性代数从抽象符号翻译成可以画在纸上的几何，这也决定了她教程的行文结构（先画图 → 再给公式 → 再落到 shader 代码）。

## 主要教程线

- **Basic Math for Shaders**（2018）—— 面向"自认数学差"的读者的 shader 向量数学速成，见 [[shader-vector-math-primer]]。
- **Intro to Procedural Geometry**（2018 系列）—— 用 Unity Mesh API 从零构造 plane、cube、法线与 UV，见 [[unity-procedural-mesh]]。
- **Foggy Window Shader**（2018）—— 用 GrabPass + 可分 Gaussian blur + 纹理编码时间做可交互雾气窗户，见 [[unity-grabpass-blur]] 与 [[texture-encoded-state]]。
- **Limit Theory Procedural Geometry**（2017）—— 早期为 Procedural Reality 的 Limit Theory 写的一组 CPU 侧程序化几何教程，覆盖参数化基元（torus、sphere、ellipsoid）与 per-face 变形/细分（stellation、extrusion、fan/centroid/triforce triangulation），见 [[procedural-mesh-primitives]] 与 [[mesh-warps-and-tessellation]]。
- **2017-12 Unity Shader 系列** —— 2017 年 12 月的四连发：[[procedural-greeble]]（n 边形 extrusion + 随机 length 做科幻细节）、[[stylized-water-shader]]（camera depth texture + 顶点噪声的卡通水面）、[[texture-dissolve]]（多层 `_ColorThreshold` 的演出用 dissolve）、[[cel-shader-outline]]（ramp lighting + stencil 描边）。

## 相关

- [[shader-vector-math-primer]]
- [[unity-procedural-mesh]]
- [[unity-grabpass-blur]]
- [[texture-encoded-state]]
- [[ronja-bohm]] —— 同赛道的另一位 Unity shader 教程作者
- [[harry-alisavakis]] —— 同赛道
- [[procedural-mesh-primitives]]
- [[mesh-warps-and-tessellation]]

## Sources

- [[sources/lindenreid-basic-math-for-shaders]]
- [[sources/lindenreid-procedural-geometry-part2]]
- [[sources/lindenreid-foggy-window-shader]]
- [[sources/lindenreid-procedural-stellation]]
- [[sources/lindenreid-procedural-extrusion]]
- [[sources/lindenreid-procedural-torus]]
- [[sources/lindenreid-procedural-sphere-ellipsoid]]
- [[sources/lindenreid-mesh-tessellation-triangulation]]
- [[sources/lindenreid-procedural-greeble]]
- [[sources/lindenreid-stylized-water-shader]]
- [[sources/lindenreid-dissolve-shader]]
- [[sources/lindenreid-cel-shader-outline]]
