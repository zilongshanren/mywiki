---
tags: [source, 渲染, 光线追踪, 发散, SER, ada-lovelace, nvidia, gpu-profiling]
date: 2026-04-27
sources: 1
---

# Shader Execution Reordering: Nvidia Tackles Divergence（Chips and Cheese）

[[people/chester-lam|Chester Lam]] 于 2023 年 5 月发表的分析文章，深入剖析 Nvidia Ada Lovelace 的 Shader Execution Reordering（SER）机制及其在 Cyberpunk 2077 Overdrive 模式中的实测效果，并尝试推断 SER 的硬件实现原理。

## 摘要

文章首先回顾 SIMD 发散问题的两种形式：控制流发散（条件分支导致部分 lane 被 mask 掉）和内存访问发散（散乱地址导致单条指令膨胀为多次 cache 访问）。光追比光栅化更容易触发发散，因为射线碰撞的几何和材质各不相同，条件分支大量增加。SER 让 shader 调用 `NvReorderThread()` 并传入"coherence hint"（排序键），将具有相似执行路径的线程重新聚合成 warp，从而减少发散。实测（RTX 4070 Ti，Cyberpunk Overdrive）：启用 SER 后 DispatchRays 耗时缩短 24%，active lanes/warp 提升 46%。文章推测 SER 仅在 SM 内部重排（而非跨 GPC），利用 shared memory 暂存排序键，向量寄存器状态 spill 到 L2，Ada 的大 L2 在此发挥关键作用。

## 关键要点

- SER 是显式 API：需开发者在 shader 中调用 `NvReorderThread()`，非透明硬件优化
- coherence hint 仅需少量 bit 即可完成高效 radix sort（O(m·n)，m 极小）
- 排序粒度推测为 SM 内部（48 warp/SM，1536 threads），不跨 SM 同步以降低开销
- SER 会将活跃变量 spill 到内存，Ada 大 L2 是实现低 overhead 的关键
- 与 RDNA 3 的 BVH 遍历栈 LDS 指令不同，SER 是波前级调度重组，适用范围更广
- SER 有 overhead，开发者需谨慎选择调用时机

## 链接到的概念

- [[rendering/shader-execution-reordering]]
- [[rendering/ada-lovelace-architecture]]
- [[rendering/path-tracing-basics]]
- [[rendering/bvh-traversal-hardware]]
- [[rendering/gpu-latency-hiding]]

## 原文

- 链接：https://chipsandcheese.com/p/shader-execution-reordering-nvidia-tackles-divergence
- 本地：`raw/articles/chipsandcheese.com/2023-05-17_shader-execution-reordering-nvidia-tackles-divergence.md`
