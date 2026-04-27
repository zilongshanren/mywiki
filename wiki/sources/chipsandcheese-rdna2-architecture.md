---
tags: [source, gpu, amd, rdna2, cache, raytracing, compute]
date: 2026-04-27
sources: 1
---

# AMD's RDNA 2: Shooting For the Top（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2023 年 2 月的深度测评文章，从游戏工作负载的实测角度系统解剖 RDNA 2 架构的缓存体系、光追实现与计算性能。

## 摘要

文章以 RX 6900 XT 为测试对象，通过 AMD Radeon GPU Profiler 和 Microsoft PIX 对多款游戏（《赛博朋克 2077》、《Titanic Honor and Glory》、《Gunner HEAT PC》）进行帧级分析。核心论点有三：第一，RDNA 2 的四级缓存体系（16 KB L0 → 128 KB L1 → 4 MB L2 → 128 MB Infinity Cache）在大工作集下相比 Nvidia Ampere 具有明显延迟与带宽优势，但 L1 命中率普遍低下，RDNA 3 将其翻倍是正确决策；第二，RDNA 2 的光追加速是"最低成本可用"方案——直接借用纹理单元做 BVH 相交检测，每 CU 每周期 4 次 box test 或 1 次 triangle test，由常规 compute shader 负责 BVH 遍历，比 Nvidia 的专用硬件更节约面积但也更依赖寄存器与缓存；第三，游戏工作负载中 compute shader 占比持续提升，RDNA 2 在 compute-heavy 场景表现出色。

## 关键要点

- WGP 内每 SIMD 可追踪 16 个 wavefront（较 RDNA 1 从 20 缩减），配合 128 KB 向量寄存器文件，旨在以更低功耗跑更高频率
- Infinity Cache 运行在独立时钟域以省电，延迟约为 RTX 3090 L2（140 ns）的一半
- 《赛博朋克 2077》中 BVH 构建消耗约 9 ms，接近 BVH 遍历时间——优化 BVH 构建与优化遍历同等重要
- 光追 kernel 中 L0 命中率仅 55%，L2 扛起 95% 的累积命中；Infinity Cache 无法通过 AMD 工具直接观察
- RDNA 2 在低占用率（few wavefronts）场景的带宽表现优于 Ampere，有助于处理大量短时光追 dispatch
- 游戏 compute shader 越来越依赖 scalar 数据路径，RDNA 2 的 scalar cache 命中率超 90%，有效卸载 vector 路径压力

## 链接到的概念

- [[rendering/rdna2-architecture]]
- [[rendering/rdna3-architecture]]
- [[computer-systems/gpu-latency-hiding]]
- [[rendering/hybrid-raytracing-pipeline]]
- [[computer-systems/gpu-memory-hierarchy-latency]]

## 原文

- 链接：https://chipsandcheese.com/p/amds-rdna-2-shooting-for-the-top
- 本地：`raw/articles/chipsandcheese.com/2023-02-20_amds-rdna-2-shooting-for-the-top.md`
