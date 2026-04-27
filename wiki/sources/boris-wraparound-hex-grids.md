---
tags: [source, game-development, hex-grid, math, procedural-generation]
date: 2026-04-27
sources: 1
---

# Wraparound Hex Grids（Boris The Brave）

[[people/boris-the-brave]] 发表于 2025 年 2 月的短文，记录在 Sylves 库中实现六边形绕回网格（六边形集合本身也是六边形状）的数学推导过程。

## 摘要

绕回六边形网格（Toroidal Hex Grid）是一种六边形集合，其整体形状也是六边形，且从任意一侧越界会从对侧重新进入——类似环面拓扑在六边形格坐标上的实现。实现思路是：将无限六边形平面按 Sander Evers 的六边形分块方法切割成等尺寸的六边形"大块"（chunk），计算每个大块回到中心块的平移量，从而将任意坐标映射到中心块内等价坐标。关键参数是半径 r，推导出 `shift = 3r+2`、`area = r*(3r+2)+r+1`。文章附完整 Python 实现（20 行）。RedBlobGames 的六边形参考文档尚未覆盖此主题。

## 关键要点

- 绕回六边形网格的等价映射依赖对无限平面的六边形分块（Sander Evers 方案）
- 核心公式：计算坐标所在大块 (xh, yh, zh)，再推算 (i, j) 偏移量，平移回中心块
- 半径为 r 的绕回网格面积 = r·(3r+2) + r + 1 个单元格
- Sylves（Boris 的 .NET 几何/网格库）已集成此实现
- RedBlobGames 是六边形网格的权威参考，但此具体主题未覆盖

## 链接到的概念

- [[game-development/wraparound-hex-grids]]
- [[game-development/triangle-grid]]

## 原文

- 链接：https://www.boristhebrave.com/2025/02/17/wraparound-hex-grids/
- 本地：`raw/articles/boristhebrave.com/2025-02-17_wraparound-hex-grids.md`
