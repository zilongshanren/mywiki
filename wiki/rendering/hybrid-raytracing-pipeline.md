---
tags: [渲染, 光线追踪, gpu, 管线]
date: 2026-04-14
sources: 1
---

# 混合光追管线（Hybrid Ray Tracing Pipeline）

纯路径追踪（path tracing）在实时预算下最大的问题是"射线又多又长"：每像素动辄数十次弹射，且每条射线都要穿越整个加速结构求交。**混合管线的核心思路是用更便宜的手段替代那些最贵的射线**，同时尽量保留路径追踪的视觉结果。

## 结构

以 [[gknext-renderer|gkNextRenderer]] 的 hybrid renderer 为例（作者 [[people/gameknife|gameknife]]）：

1. **Primary Ray 被光栅化替代**：用 [[visibility-buffer|Visibility Buffer]] 一遍写出像素归属的 instance+triangle，获得 hit 信息。性能比真正的 primary ray 便宜得多。
2. **Secondary Ray 走硬件光追**：但刻意 **缩短射线距离**，只处理近距离的遮蔽、接触阴影与反射。短射线对 BVH 的命中更集中、缓存命中也更好。
3. **后续弹射使用 cache**：远距离 GI、间接光等走 ambient cube / probe / SDF 等 cached 数据结构，而不是再发射新射线。

最终：**每像素只有 1–4 条短距离硬件 tracing**，但视觉上已经逼近完整 path tracing。gkNextRenderer 在 city 场景可以跑到 2K@120fps。

## 反向混合（Reverse-Hybrid）

作者还做了一条反方向：用 primary ray 直接写出 [[visibility-buffer]]，后面全部走光栅化管线里的 compute shading。"**传统光栅化的各种裁剪、drawcall 优化技术都不复存在了**"——因为光栅化本身没了。

## 材质分支

在 slang 统一 shader codebase 之后，可以按 material type 分支：primary ray 命中玻璃这类材质时，切回真正的完整 path tracing；命中漫反射材质时走 hybrid 路径。这在工程上是很自然的 SIMD 分支组织。

## 相关

- [[visibility-buffer]]
- [[bindless-rendering]]
- [[deferred-rendering]]
- [[gknext-renderer]]

## Sources

- [[sources/gameknife-gknextrenderer-yearone]]
