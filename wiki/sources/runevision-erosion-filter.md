---
tags: [source, rendering, terrain, procedural, shader, gpu-friendly, 2026]
date: 2026-04-19
sources: 1
---

# Rune Skovbo Johansen - Fast and Gorgeous Erosion Filter

[[rune-skovbo-johansen]] 于 2026 年 3 月 30 日发布，附带一段 YouTube 视频。文章结构约等于一本"如何从 clayjohn / Fewes 的原型迭代到一个工业可用的山地侵蚀滤波器"的进度日志，里面堆了相当多技术细节。

## 摘要

一种**过程化侵蚀滤波器**——每个点独立求值、GPU 友好、可分 chunk 生成、可叠到任何高度函数之上。技术谱系：2018 年 clayjohn 在 Shadertoy 上做出第一个"eroded terrain noise"，2023 年 Fewes 抛光并重新呈现，作者在 2025-2026 年重写两个版本（Clean Terrain / Advanced Terrain Erosion Filter）。核心链路是：沿梯度方向生成条纹（cos 波做高度、sin 波做斜率）→ 用 cell 内 pivot 防远距失真 → 邻近 cell 条纹 blending → 迭代多个 octave 让每层条纹沿上一层梯度分叉 → 在峰谷（坡度趋零）处用 **fade 方案** 把 gully 淡出到用户提供的 `fadeTarget`（通常按高度归一化）。作者的三个关键增强是 **stacked fading、normalized gullies（由此催生 [[phacelle-noise]]）、straight gullies（用 sign(sin) 代替 sin 让 gully 走直）**，外加 pointy peaks、edge rounding、ridge map / dendritic drainage 线条等附加功能。已开源（MPL v2），社区已有 Unity Burst / ShaderGraph、Unreal Landmass、Godot、Houdini、Hytale 等至少 7 个实现。

## 关键要点

- **与模拟式侵蚀的对立**：模拟每一滴水准确但慢且不可分 chunk；滤波式单 pass 常数复杂度但"只看起来像"而已。
- **frequency vs. fade**：clayjohn/Fewes 用频率随坡度变化让峰顶永远落在白条上（缺陷：谷底也会隆起）；作者用 fade 方案让峰谷都能做到锋利。
- **shaping function**：`1 − (1 − t)²` 代替 `sqrt(t)`，避免峰谷附近的折痕伪像。
- **stacked fading**：下一 octave 的 `fadeTarget` 是上一 octave 的 faded gullies；mask 累乘；`pow_inv(combiMask, detail)` 提供"越小越让高频 gully 只出现在陡坡"的控制。
- **normalized gullies**：把插值后的 (cos, sin) 部分归一化（长度 × 2 再 clamp 到 1），规避完全归一化下的 loopy 尖刺；这段思考独立发表为 [[phacelle-noise]]。
- **straight gullies**：gully 方向用 `sign(sin)` 而非 `sin`，等效于模拟三角波斜率恒定，小 gully 才能干脆分叉而不是粘着大 gully 弯曲。
- **pointy peaks**：归一化后山峰会变钝；gully 权重 × 0.5、侵蚀强度 × 2.0 可恢复尖锐度。
- **ridge map / dendritic drainage**：最终 `fadeTarget` 本身就是"ridge+crease 图"，可直接当作画水系线条的 mask，但因为条纹是插值而来，线条偶尔中途断裂——视觉可接受但不保证拓扑连通。
- **解析导数最终放弃追求精度**——保留仅为可选用途（如树覆盖密度）。
- **fadeTarget 的鲁棒性**：基于高度不鲁棒（高谷可能高于低峰），作者考虑过用二阶导（曲率）但既慢又需额外 wrangle 到 [-1, 1]，最后把决定权交给用户。

## 链接到的概念

- [[erosion-filter-procedural]]
- [[phacelle-noise]]
- [[directional-noise]]
- [[worley-voronoi-noise]]
- [[shaping-functions]]
- [[turbulence-domain-warping]]
- [[layered-grid-noise]]

## 原文

- URL：https://blog.runevision.com/2026/03/fast-and-gorgeous-erosion-filter.html
- 本地：`raw/articles/blog.runevision.com/2026-03-30_fast-and-gorgeous-erosion-filter.md`
- 同期重复抓取 skip：`2026-03-30_runevision-blog.md`（月页，拼接了 erosion + phacelle）
