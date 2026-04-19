---
tags: [source, 渲染, tessellation, remesh, 算法]
date: 2026-04-19
sources: 1
---

# How to tessellate（Brian Karis / Graphic Rants）

[[brian-karis|Karis]] 2026-02-01 的第三篇，解决"**给定一个要 dice 的三角形 patch，怎么切才能得到密度均匀（而不仅拓扑均匀）的 micropoly**"这个单点问题。核心产物是 UE 使用的 **Tessellation Table**。

## 摘要

先沿用 [Moreton / D3D 硬件 tessellator] 的 TessFactor 范式——每条边独立决定切几段、共享边自动匹配。TessFactor 的计算绕开 Diagsplit（要采样位移函数，不切合 shader 驱动）和 artist hint（material graph 不可见），**用未位移世界空间边长投影到屏幕像素 / DiceRate 得到**；UE 默认 DiceRate = 2 像素。然后主贡献在 dice 算法：D3D 的"拓扑均匀"方案会多出 ~45% 冗余三角形，Karis 要的是**密度均匀**——所有边 ≤ 目标长度的最少三角形网格。这等价于 [Botsch-Kobbelt 2004] 等 isotropic remesh，offline 跑不起，于是枚举 TessFactor 组合预计算成 **Tessellation Table**。通过"TessFactor 排序大到小"作为唯一索引把表从 N³ 压到 N(N+1)(N+2)/6；barycentric 量化到 16 bit 时把 1.0 映射到 65534（偶数）才能让边界 0.5 精确对齐，否则 patch 间出现裂缝。同一张表也用于 split——更宽 branching 比二分好。实测：均匀 dice 只产 D3D 拓扑均匀的 **69%** 三角形；均匀 split 只产二分的 **68%** 子 patch。

## 关键要点

- **TessFactor = 未位移边长在屏幕上的投影 / DiceRate**。DiceRate > 1 像素通常无视觉差异。
- **Remeshing 离线预计算成 Tessellation Table**；"TessFactor 大到小排序"作为唯一索引。
- **barycentric 数学纯 intrinsic**：$\|PQ\|^2 = -a^2 vw - b^2 wu - c^2 uv$，允许 TessFactor 构成 non-Euclidean 三角形（a > b+c）时平滑降级。
- **量化**：1.0 → 65534（偶数），median barycentric 量化 + 其它重算归一化，保边界对称避裂缝。
- **Split 同理**：`SplitFactor = min(TessFactor / MaxDiceFactor, MaxSplitFactor)`，让 dice 阶段尽量吃满 MaxDiceFactor。
- **复用**：UE 的 Tessellation Table 已授权给 `nvpro-samples/vk_tessellated_clusters` 使用。

## 链接到的概念

- [[tessellation-approaches-overview]]
- [[nanite-tessellation-approach]]
- [[hull-domain-tessellation-urp]] —— 传统 D3D11 tessellator 对照

## 原文

- 链接：<http://graphicrants.blogspot.com/2026/02/how-to-tessellate.html>
- 本地：`raw/articles/graphicrants.blogspot.com/2026-02-01_how-to-tessellate.md`
