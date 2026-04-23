---
tags: [source, 渲染, 裁剪, simd, 多线程, stingray, bitsquid]
date: 2026-04-19
sources: 1
---

# The Implementation of Frustum Culling in Stingray（Andreas Asplund / bitsquid 博客）

[[andreas-asplund]] 发表于 2016-10-04 的博客，承接 9 月 state reflection 那篇，详细讲 Stingray 视锥剔除的**SIMD 实现、两级 sphere→OOBB、多线程**。

## 摘要

Stingray 不用空间分割树，坦言当前 culling 没成瓶颈，因此走暴力路线：sphere 测试先、OOBB 测试后。可剔除对象在 [[main-render-thread-state-reflection|state reflection]] 的 `create_object` 里按 flag 进三套 `ObjectSet`（普通、投射阴影、遮挡体），每个 `ObjectSet` 是 SoA 结构（`min_x` / `max_x` / 16 路 world matrix 分量 / `ws_pos_*` / `radius` / `visibility_flag` / `type` / `id`），pad 到 SIMD lane 数。

球级剔除：对每个 frustum plane 把 normal + d splat 成 `float4`，4 球一把做 dot+radius+compare，6 个 plane 全 `vector_and`，结果写 `visibility_flag`（0 或 `0xffffffff`）。中间 `remove_not_visible` 线性扫 flag 压成 compact 的 `indirection[]`。OOBB 级走 Fabian Giesen 的 "Method 2b：将 8 顶点变到 clip 空间，测试是否全落在某一裁剪面外侧"，引入 `SIMDVector` / `SIMDMatrix` 的 struct-of-SIMD 写法，`simd_min_max_transform` 共享 min/max 角点的乘加节省一半乘法。

多线程：`ThreadPool` 提供 `add_tasks / do_work / wait_atomic`，`work_size = 512` 对象一块拆成 N 个 task，每个 `CullingWorkItem` 自带 atomic signal，等待方 `wait_atomic` 会在 signal 未设前主动帮忙跑 task（help-if-idle）。末尾还提了 contribution culling（屏幕 extent 阈值剔除，近平面后方的 OOBB 角点直接放弃优化）和 cascaded shadow 的 enclosure 优化（对象完全在 cascade N 内则跳过后续 cascade）。

## 关键要点

- SoA `ObjectSet` 让每个 SIMD kernel 只 load 自己需要的几条数组，cache 友好。
- OOBB 方法直接引用 [[fabian-giesen]] https://fgiesen.wordpress.com/2010/10/17/view-frustum-culling/ 与 Arseny Kapoulkine http://zeuxcg.org/2009/01/31/view-frustum-culling-optimization-introduction/，这两篇是业界 frustum culling SIMD 化的主要参考。
- 放弃 BVH/OCtree 是有意识的 KISS：暴力 SIMD + 多线程在当前负载足够。
- `simd_multiply(SIMDVector, SIMDMatrix)` 的代码几乎和标量矩阵乘一样，但一步算 4 对象。
- 这套 culling 在主场景和 shadow pass 里复用；灯光也走同一套。

## 链接到的概念

- [[stingray-simd-sphere-oobb-culling]]
- [[culling]]
- [[view-frustum-culling-ryg]]
- [[obb-frustum-sat]]
- [[main-render-thread-state-reflection]]

## 原文

- 链接：https://bitsquid.blogspot.com/2016/10/the-implementation-of-frustum-culling.html
- 本地：`raw/articles/bitsquid.blogspot.com/2016-10-04_the-implementation-of-frustum-culling-in-stingray.md`
