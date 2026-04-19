---
tags: [source, 渲染, 路径追踪, 教学, 蒙特卡洛]
date: 2026-04-19
sources: 1
---

# Path tracing workshop（Christoph Peters）

[[christoph-peters|Christoph Peters]] 为 Intel 准备、随后公开发布的 path tracing 入门 workshop：76 分钟视频 + ShaderToy 习题，从零写到一个功能正确的 Cornell Box path tracer。

## 摘要

Workshop 分两部分。**Part 1 ray tracing**（视频 + ShaderToy 习题）：学 GLSL + ShaderToy 工作流，手写相机 ray、ray-triangle intersection、ray-mesh intersection；结果是没有任何 acceleration structure、慢但正确的 Cornell Box 线框（无 shading）。**Part 2 path tracing**：引入 radiance、rendering equation、Monte Carlo integration；均匀半球方向采样、递归 ray 追踪；结果是有全局光照的 Cornell Box——sample 多才收敛。原计划的 Part 3 （importance sampling：BRDF 重要性采样、light sampling、MIS）从未完成，取而代之的是 Peters 给 TU Delft 准备的 [[sources/peters-path-tracing-lectures|path tracing lectures]]。Workshop 选择**极端简化**路径——不做 BVH、不做重要性采样、不做 denoiser——让初学者看见每部分代码对应什么物理量。

## 关键要点

- 两阶段：先写功能正确（但慢）的 path tracer，再用 lectures 学如何降方差。
- 主张**简单到极致**——砍掉 BVH / 重要性采样，换取概念可见性。
- ShaderToy-based exercises 降低入门门槛。
- 目标人群：已有基础编程和数学功底的工程师（Intel 内部广泛受众）。

## 链接到的概念

- [[path-tracing-basics]]
- [[radiometry-integral-view]]
- [[christoph-peters]]

## 原文

- 链接：http://momentsingraphics.de/PathTracingWorkshop.html
- 本地：`raw/articles/momentsingraphics.de/2024-11-05_path-tracing-workshop.md`
