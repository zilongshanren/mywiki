---
tags: [source, 渲染, tessellation, reyes, displacement]
date: 2026-04-19
sources: 1
---

# Possible approaches for tessellation（Brian Karis / Graphic Rants）

[[brian-karis|Karis]] 2026-02-01 的第二篇，把 UE5.4 Nanite Tessellation 选型过程摊开：**为什么光靠 Nanite 扩展不够、为什么 tracing 类方案不够、最后为什么滑向 Reyes**。

## 摘要

位移是艺术家面向的功能，tessellation 只是实现。Karis 先逐个否掉 tracing 路线——Shell mapping / DMM / Thonat 都假定棱柱浅或位移是纹理，不适配"基础 mesh 是任意密度 Nanite mesh + 位移是任意 shader"的真实条件。转而扩展 Nanite 簇层级（做 amplification 而不仅是 simplification）是最优雅的，但实际工程里发现：Nanite build 过程本身就复杂、做反向更复杂，且**不可能**保留 Nanite 的 quadric adaptive 优势；更根本的是，位移场是 user shader，本身不可预知，误差只能按采样率估。这里会出现**真正的 micropoly**（Nanite 本身是 1 像素误差不是 1 像素三角形），失去 content-adaptive 后三角形数必然更多。因此跳出 Nanite 框架、每帧动态 tessellate，自然回到 [[nanite-reyes-comparison|Reyes]]——Bound/Split/Dice/Shade/Rasterize，电影业干了几十年。Nanite Tessellation 是 Karis 所知**第一个 shipping 游戏**的实时 Reyes（Fortnite 地面）。

## 关键要点

- **Tracing 方案全军覆没**：Shell mapping / DMM 没有位移方向加速结构，假设棱柱浅；Thonat 限定单贴图位移。
- **Nanite 簇内 amplification 不现实**：同时需要 simplification + amplification；位移下的误差需要重建 mesh；失去 quadric adaptive；**真正的 micropoly** 成本不可避免。
- **Reyes 是天然答案**：同样的 split 层级结构和 Nanite cluster 遍历同构；dice 后 shade 只做位移，其余 shading 走像素空间 deferred material。
- **Object-space shading 是遗迹**：现代 production path tracer（Manuka / PRMan）也都转 hit 上 shade 或 BxDF lobe 缓存。

## 链接到的概念

- [[tessellation-approaches-overview]]
- [[nanite-reyes-comparison]]
- [[nanite-virtualized-geometry]]
- [[visibility-buffer]]

## 原文

- 链接：<http://graphicrants.blogspot.com/2026/02/possible-approaches-for-tessellation.html>
- 本地：`raw/articles/graphicrants.blogspot.com/2026-02-01_possible-approaches-for-tessellation.md`
