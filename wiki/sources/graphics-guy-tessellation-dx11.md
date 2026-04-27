---
tags: [source, 渲染, tessellation, dx11, hull-shader, domain-shader]
date: 2026-04-27
sources: 1
---

# Tessellation on DX11（Jiayin Cao / A Graphics Guy's Note）

[[graphics-guy-notes|Jiayin Cao]] 发表于 2015 年 6 月的文章，系统介绍 DX11 Tessellation 管线三阶段的工作原理与实践细节。

## 摘要

文章以工程师视角梳理 DX11 新增的 Hull Shader、Tessellator（固定功能）、Domain Shader 三级管线。核心论点：tessellation 的真正价值在于**动态 LOD**和配合**位移贴图**产生真实凹凸效果，而 Hull Shader 的 `partitioning` 参数（equal / fractional_even / fractional_odd / pow2）直接决定 tess factor 变化时几何是否平滑过渡。文章还讨论了 PN 与 Phong 两种曲面光顺策略、Hull Shader 中的 patch 级提前剔除逻辑，以及裂缝（crack）问题的成因——两个法线或 UV 不同的顶点共享同一 world-space 位置时，Hull/Domain 的细分走向不同方向从而产生缝隙。

## 关键要点

- Tessellator 输出的是 barycentric 坐标，Domain Shader 负责用控制点插值出实际 clip-space 位置。
- Hull Shader 的 constant function 里将 tess factor 置 0 可跳过整个 patch，但位移后依然可见的 patch 若提前剔除会出错。
- `partitioning("equal")` 会导致 factor 连续变化时几何跳变；`fractional_even/odd` 才能平滑过渡。
- Phong tessellation 比 PN triangle 计算量更低，效果相近：线性插值 → 投影到各顶点切平面 → 再次插值。
- 裂缝的通用修复原则：保证同一 world-space 位置的所有属性一致，或用 Dominate Data Algorithm / AEN 等算法运行时统一。

## 链接到的概念

- [[hull-domain-tessellation-urp]]
- [[tessellation-approaches-overview]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/tessellation_on_d3d11/
- 本地：`raw/articles/agraphicsguynotes.com/2015-06-16_tessellation-on-dx11.md`
