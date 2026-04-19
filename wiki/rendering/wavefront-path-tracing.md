---
tags: [渲染, 路径追踪, 离线渲染, 架构, hyperion]
date: 2026-04-19
sources: 2
---

# Wavefront Path Tracing

**Wavefront path tracing** 是把路径追踪从「每条 ray 顺着从头跑到尾」改成「按 bounce 同步推进大批 ray」的渲染器架构，目的是让同一 bounce 的工作在 shader 执行、纹理读取、BVH 遍历等各个维度上尽量同质，借此提升 SIMD 占用与缓存命中。

## Disney Hyperion 的实现

[[hyperion-renderer]] 以此架构出名（Eisenacher et al. 2013 *Sorted Deferred Shading for Production Path Tracing*）。典型做法是：

- 当前 bounce 生成的所有命中点按材质 / shader 排序再 shade。
- 缓存友好的 Ptex 读取顺序从 sort 中获益，但并非 Ptex 的本质属性——[[ptex-gpu-streaming]] 在完全非相干访问模式下仍然能做到零停顿。
- 然而「只保留当前 bounce 的路径状态」会让依赖完整路径历史的算法难做；[[path-guiding-production]] 就必须为此在 Hyperion 里重新设计 path guiding 的数据流。

RenderMan XPU（Christensen et al. 2025）同样是 wavefront 架构，Disney Animation 与 Pixar 在 path guiding 项目里面对的挑战是相似的。

## 与传统 megakernel / recursive PT 的区别

- **Megakernel**：一条 ray 的整个生命周期在同一个 kernel 里跑完，实现简单但 divergence 高、shader 表越大越慢。
- **Wavefront**：每个 bounce 切成独立阶段，阶段间可以排序、可以调度，代价是必须把路径状态「外存」在 buffer 里。

## 相关
- [[hyperion-renderer]]
- [[path-guiding-production]]
- [[ptex-gpu-streaming]]
- [[ray-differentials]] — Hyperion 的 wavefront 架构和 ray differentials 的简化方案

## Sources

- [[sources/yiningkarlli-moana-2]]
- [[sources/yiningkarlli-path-guiding-siggraph2025]]
