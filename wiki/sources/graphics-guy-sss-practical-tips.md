---
tags: [source, rendering, subsurface-scattering, offline-rendering, path-tracing]
date: 2026-04-27
sources: 1
---

# Practical Tips for Implementing Subsurface Scattering in a Ray Tracer（A Graphics Guy's Note）

[[people/graphics-guy-notes]] 发表于 2020 年 11 月的文章，记录了在自研离线渲染器 SORT 中实现 BSSRDF（次表面散射）的多轮迭代过程，着重讨论萤火虫噪点的消除、多交叉点处理优化、以及如何将 SSS 与普通 BRDF 平滑混合。

## 摘要

文章从 PBRT 3 的可分离 BSSRDF 模型出发，介绍了基于 Disney 扩散剖面（diffusion profile）的重要性采样方法，即在着色点上方随机采样圆盘上的点并通过短光线找到表面交叉点。PBRT 在多交叉点时随机均匀选一个，但作者发现这导致严重萤火虫——几何体内部复杂时，少数成功逃出的路径获得极低 PDF 导致权重爆炸。文章提出三项关键改进：（1）相邻 SSS 材质退化为 Lambert，避免多次 BSSRDF 弹射；（2）评估所有交叉点而非随机选一个；（3）移除 SSS 内置 Fresnel，改由材质系统层统一处理，确保 mean free path → 0 时 BSSRDF 平滑退化为 Lambert。此外还扩展了材质系统，将 BXDF 与 BSSRDF 统一为"散射单元（scattering unit）"，支持多层 SSS 混合。

## 关键要点

- BSSRDF 比 BRDF 多两个积分维度（位置域），精确重要性采样远比方向采样困难
- Disney 扩散剖面有解析 PDF，但多交叉点时的条件概率 `P_uniform(X|R)` 使总 PDF 效率大幅下降
- 评估所有交叉点（而非随机选一）在前一优化基础上几乎消除萤火虫，渲染时间大致相同
- SSS 内置 Fresnel 会在 mean free path = 0 时与 Lambert 产生不连续边界，去掉后用 `S ≈ Sp/π` 保证平滑过渡
- 为 K 近邻交叉点实现专用空间加速接口（vs 朴素重复 raycast），在纯 SSS 场景性能提升约 14%
- SSS 后不需要 MIS（Lambert BRDF 无尖峰，只需对光源采样），可省去一条 shadow ray

## 链接到的概念

- [[rendering/path-tracing-basics]]
- [[rendering/monte-carlo-integration]]
- [[rendering/skin-rendering-practice]]
- [[rendering/preintegrated-skin-shading]]
- [[rendering/importance-sampling-pdf-cancellation]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/practical_tips_for_implementing_subsurface_scattering_in_a_ray_tracer/
- 本地：`raw/articles/agraphicsguynotes.com/2020-11-13_practical-tips-for-implementing-subsurface-scattering-in-a-r.md`
