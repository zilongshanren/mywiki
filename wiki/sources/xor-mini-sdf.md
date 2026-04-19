---
tags: [source, 渲染, shader, sdf, raymarching]
date: 2026-04-19
sources: 1
---

# Signed Distance Fields（mini.gmshaders.com / Xor）

[[xor-shader-artist]] 2025 年 2 月 mini 教程：Signed Distance Field 的用途与常见修改操作大全。

## 摘要

SDF 是"到形状边界的有符号距离"函数——边界内负、外正。它一份数据支持：碰撞检测、描边、阴影、AA、raymarching。操作组合：布尔并（min）、交（max）、差（`max(a, -b)`）、smooth min（混合边界）；onion（`abs(d) - thickness`）、hollow（减薄）；空间变换 mirror（`abs(p)`）、tile / repeat（`mod(p, L) - L/2`）、扭曲（在采样前 rotate / twist p）。拼出复杂形状不需要任何几何数据。

## 关键要点

- SDF 一份数据支持多种下游（碰撞 / 描边 / AA / raymarching）
- min / max / smooth min 是形状布尔的基本操作
- 空间变换（mirror / tile / twist）在采样前预处理 p

## 链接到的概念

- [[sdf-operations-shader]]
- [[sdf-2d-primitives]]

## 原文

- 链接：<https://mini.gmshaders.com/p/signed-distance-fields>
- 本地：`raw/articles/mini.gmshaders.com/2025-02-19_signed-distance-fields.md`
