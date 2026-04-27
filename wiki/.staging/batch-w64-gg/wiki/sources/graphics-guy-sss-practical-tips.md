---
tags: [source, 渲染, subsurface-scattering, bssrdf, 离线渲染]
date: 2026-04-19
sources: 1
---

# Practical Tips for Implementing Subsurface Scattering in a Ray Tracer（A Graphics Guy's Note）

[[graphics-guy-notes]] 2020 年 11 月的文章，详细记录 SORT 集成 PBRT 3rd SSS 实现并参考 Cycles 迭代的工程过程。

## 摘要

文章定位于 SSS 「工程层」的实战笔记——理论网上一大堆，但「真正接进 path tracer 且不冒 fireflies」的经验极少。作者从集成 PBRT 3rd ed. separable BSSRDF 开始（diffusion profile + disk 投影采样），碰到三组核心问题：fireflies 严重、SSS 与 Lambert 过渡有接缝、两个同材质 mesh 互相干扰。核心 trick 三则：(1) 前一次 bounce 是 SSS 时，本次把 SSS 当 Lambert 算，消除 SSS 体内反复弹跳；(2) 多交点不 uniform pick 而是全部评估，依赖 (1) 的路径不膨胀；(3) 去掉 BSSRDF 两侧 Fresnel 并整体除 $\pi$，让 mean-free-path → 0 时解析退化到 Lambert。工程上还做了：材质系统重构引入 `ScatteringUnit` 基类让 BXDF+多 BSSRDF 可混合、K-nearest intersection 接口、SSS 专用 skip MIS、mesh 实例化独立材质副本避免相互交。未解决的问题：薄几何（龙头偏暗）、BDPT 下的 SSS、random walk SSS。

## 关键要点

- PBRT 3rd 的 separable BSSRDF = $S_w^{out} \cdot S_p \cdot S_w^{in}$；$S_p$ 只看距离，Disney profile 有解析 pdf。
- 位置采样：法线垂直的 disk 上采 $(r, \theta)$，投射短射线找 mesh 交点。
- Fireflies 根源 A：SSS 体内反复散射——换 Lambert 解决 90%。
- Fireflies 根源 B：多交点 uniform pick 让 pdf 塌方——改为全部评估。
- Fresnel 去掉后，mean-free-path → 0 时 BSSRDF 精确退化成 $f_{lambert}$，消除接缝。
- 同材质多 mesh 用 instance unique id 隔离。
- `ScatteringUnit` / `ScatteringEvent` 替代 BSDF，支持多 BSSRDF + BXDF 混合（做皮肤）。
- 性能：K-nearest intersection 接口避免重复遍历，整体 +11.5%。

## 链接到的概念

- [[sss-practical-implementation]]
- [[volume-rendering-offline]]
- [[microfacet-brdf]]
- [[path-tracing-basics]]
- [[fast-translucency-wraplight]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/practical_tips_for_implementing_subsurface_scattering_in_a_ray_tracer/
- 本地：`raw/articles/agraphicsguynotes.com/2020-11-13_practical-tips-for-implementing-subsurface-scattering-in-a-r.md`
