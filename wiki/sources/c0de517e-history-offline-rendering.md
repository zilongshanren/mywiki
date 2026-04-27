---
tags: [source, rendering, 离线渲染, 历史, 光线追踪, 路径追踪]
date: 2026-04-27
sources: 1
---

# Recollecting the History of Offline Rendering（Angelo Pesce / c0de517e）

[[angelo-pesce]] 发表于 2025 年 1 月的文章，对离线渲染技术演进做了个人考古式回顾，聚焦于"路径追踪为何来得这么晚"这一核心谜题。

## 摘要

Pesce 梳理了从 1980 年代的 PovRay 光线追踪时代，到 1990 年代末-2000 年代初由光子映射 + 辐照度缓存主导的"Radiosity 时代"，再到 2000 年代中期公开路径追踪器出现的三个阶段。核心论点是：Kajiya 的路径追踪论文（1986）和 Veach 博士论文（1997）都早于实践，但工业界直到 2004-2006 年前后才开始公开使用无偏路径追踪——比理论成熟晚了至少十年。文章列举了 Arnold、Maxwell Render、PBRT、Indigo、Sunflow 等早期实现的时间线，并指出一些让路径追踪走向实用的工程技巧（firefly 钳制、降噪、重要性采样）长期未被广泛传播。

## 关键要点

- 光线追踪出现得"太早"，路径追踪来得"太晚"，两者均非技术成熟度驱动，而是生态与工程配套的问题
- "Radiosity"和"Unbiased"都曾被严重滥用作营销词汇
- Arnold 约 1999 年已在圈内流传，但直到 2004 年才开始商业化普及
- 现代降噪、时域重投影、路径引导均是早已被理论预见但被推迟实践的技术
- 实时渲染（PBR 革命）与离线渲染（无偏 GI）的去 hack 化趋势高度同步

## 链接到的概念

- [[offline-rendering-history]]
- [[rasterization]]
- [[physically-based-shading]]
- [[quasi-monte-carlo]]

## 原文

- 链接：https://c0de517e.com/018_rthistory.htm
- 本地：`raw/articles/c0de517e.com/2025-01-03_recollecting-the-history-of-offline-rendering-was-ray-tracin.md`
