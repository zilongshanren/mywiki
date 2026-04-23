---
tags: [人物, 作者, 引擎架构, 渲染, bitsquid, stingray]
date: 2026-04-19
sources: 2
---

# Andreas Asplund

Bitsquid → Autodesk Stingray 的渲染工程师，2016 年在 Bitsquid Blog 上写了两篇把**Stingray 渲染底层机制讲透**的文章——正好是 [[tobias-persson|Tobias Persson]] 2017 年 Renderer Walkthrough 系列在开篇时主动让出来的"已有专题文"。

## 主要贡献（公开）

- **"State reflection"（2016-09）** —— 参见 [[main-render-thread-state-reflection]]。讲清楚 Stingray 怎么用 `StateStream` + `render_handle` + 双表示（`MeshObject` vs `RenderMeshObject`）把主线程状态单向镜像到渲染线程。同样的 pattern 在资源 streaming、[[stingray-render-resource-context|RRC]]、网络状态同步等处反复复用。
- **"The Implementation of Frustum Culling in Stingray"（2016-10）** —— 参见 [[stingray-simd-sphere-oobb-culling]]。全链路贴代码：SoA `ObjectSet`、SIMD 球测试、SIMD OOBB clip-space 测试、`ThreadPool::wait_atomic` 的 help-if-idle 多线程拆分，以及 contribution culling + cascaded shadow enclosure 两个小优化。

## 相关

- [[niklas-frykholm]]
- [[tobias-persson]]
- [[main-render-thread-state-reflection]]
- [[stingray-simd-sphere-oobb-culling]]
- [[stingray-renderer-three-stage-pipeline]]

## Sources

- [[sources/bitsquid-state-reflection]]
- [[sources/bitsquid-frustum-culling-stingray]]
