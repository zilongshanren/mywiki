---
tags: [source, 渲染, unity, urp, 后处理, world-space, 扫描]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders Pro - World Scan（Daniel Ilett）

[[daniel-ilett]] 发布的 *Snapshot Shaders Pro* 产品内参考文档，介绍 World Scan 后处理——从某个世界空间原点向外扩散的扫描条带。

## 摘要

World Scan 把一条扫描带叠加在原始场景之上，向外从某个世界空间原点扩张——开放世界游戏常见的"按 R 扫描一下周围"视觉。参数五个：`Scan Origin`（世界空间起点，一般由 C# 脚本从玩家位置或射线交点设置）、`Scan Distance`（扫描已走过的距离，在 `Update` 里累加）、`Scan Width`（扫描带的厚度，世界空间单位）、`Overlay Ramp Tex`（一张 `x-by-1` 的 ramp 纹理，把扫描距离映射成颜色，必须设置）、`Overlay Color`（HDR 加色，最终色 = ramp × Overlay Color）。与 [[world-scan-shader-effect]] 条目里描述的 `inner * outer` 双 step 逻辑一致——把 `distance(worldPos, origin)` 落在 `[ScanDistance, ScanDistance + ScanWidth]` 之间的片元画成发光条带。这里 Pro 版相比 Shader Graph 教程版多了一个 ramp 纹理作为颜色过渡——可以做出扫描带内"中心最亮、边缘淡出"的梯度感。

## 关键要点

- `Scan Origin` 是世界空间坐标——不是屏幕 UV；适合"从玩家脚下"或"从射线点击处"扩散
- `Scan Distance` 需要 C# 脚本每帧累加（`scanDistance += Time.deltaTime * speed`），Pro 版没有内置动画驱动
- `Overlay Ramp Tex` 是横条纹理，x 轴代表"条带内从内到外的位置"，y 是单像素——可以做软边（黑→白→黑）、尖锐条（中央亮）或多段梯度
- HDR `Overlay Color` 配合 URP Bloom 产生发光扩散感
- 与 [[world-scan-shader-effect]] 的 Shader Graph 版 emissive 实现是同一个核——Pro 版是把它做成了屏幕空间 Volume override（作用于整个场景而非单个材质）

## 链接到的概念

- [[world-scan-shader-effect]]
- [[urp-volume-post-processing]]
- [[bloom-threshold-blur-composite]]

## 原文

- 链接：<https://danielilett.com/snapshot-shaders-pro/world-scan/>
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-pro-world-scan.md`
