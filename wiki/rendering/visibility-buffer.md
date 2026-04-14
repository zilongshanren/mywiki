---
tags: [渲染, gpu, 延迟渲染, 几何]
date: 2026-04-14
sources: 1
---

# Visibility Buffer

Visibility Buffer 是对传统 [[deferred-rendering|G-Buffer]] 的一种优化替代方案，最早由 Burns & Hunt 提出。**核心思想**：第一遍光栅化只写入极瘦的 thin-gbuffer（通常是 instance id + triangle id 或 primitive id），完全不做材质属性的采样与写入；后续由一个或多个 compute pass 根据像素上的 id，反查顶点缓冲、材质参数与纹理，完成真正的 shading。

## 为什么要这样做

传统 G-Buffer 在高 overdraw、复杂材质场景下开销极大：**每个被后来覆盖的像素都浪费了一次完整的 material shading 写入**（albedo、normal、roughness、metallic……），带宽和着色运算都被白白消耗。Visibility Buffer 则把重负载延后，只对真正可见的像素做一次 shading。

## 工程难点：triangleId 从哪里来

现代图形 API 并不直接给 vertex shader 提供 primitive id。[[people/gameknife|gameknife]] 在 [[gknext-renderer]] 中总结了两种处理方式：

- **最粗暴**：把 mesh 的顶点全部拆开，每三角形独立三顶点，顶点上直接写 triangleId，vs 输出即可。代价是顶点数 ×3。
- **provoking vertex 优化**：对 mesh 的三角形做精心排序，用 zeux 的 `meshoptimizer` 库可以显著减少顶点复制数量，仍保留每三角形的 id 语义。

## 与硬件光追的协同

Visibility Buffer 在混合渲染管线里可以 **完美替代 primary ray**：光栅化一遍 thin gbuffer 的代价远低于从摄像机发射一条射线。gkNextRenderer 的 [[hybrid-raytracing-pipeline|hybrid renderer]] 就是在 VB 之上接短距离硬件光追 + 远距离 cache，达到 2K@120fps。

反方向也能玩：用一遍 primary ray 替代光栅化，直接写出 visibility buffer，后续走"传统" compute shading 流程。这种 reverse-hybrid 管线里，drawcall 优化、裁剪、batching 几乎被整个消掉。

## 相关

- [[deferred-rendering]]
- [[hybrid-raytracing-pipeline]]
- [[bindless-rendering]]
- [[draw-call]]
- [[overdraw]]

## Sources

- [[sources/gameknife-gknextrenderer-yearone]]
