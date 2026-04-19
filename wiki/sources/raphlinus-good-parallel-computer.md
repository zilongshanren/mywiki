---
tags: [source, gpu, parallel, architecture, opinion]
date: 2026-04-19
sources: 1
---

# I Want a Good Parallel Computer（Raph Levien）

[[raph-linus]] 发表于 2025 年 3 月的宣言式长文，来自他在 UCSC CSE 同名 colloquium 的博客版，系统阐述他对现代 GPU 执行模型的不满和对"一台好的并行计算机"的想象。

## 摘要

Raph 的核心论点：GPU 比 CPU 快 10–100×，但没有成为通用并行计算机，原因是执行模型太贫瘠（处理大块规则数据很行，动态工作负载困难）和语言工具不到位。文章先以他自己的 Vello 2D renderer 为痛点来源——每个 stage 的中间 buffer 大小依赖输入且不可预测，CPU 端预分配要么浪费要么失败，根本原因是缺乏 [[gpu-queues-vs-dispatch-execution|stage 间队列]]。然后回顾三个历史的"正确方向"：Connection Machine（1985，64k 处理器、推动了 prefix sum 研究）、Cell（PS3 2006，8 核 SIMD + 全局 job queue，"基本满足好并行计算机的定义"，死于编程模型太粗糙）、Larrabee（2008，x86 + 宽 SIMD + 最少硬件固化，Xeon Phi / AVX10 / ISPC 延续了它的遗产）。然后给出四条前进路径：Cell reborn（Tenstorrent / Esperanto）、GPU 上运行 Vulkan 命令（CUDA 12 device graph launch 是雏形）、work graphs（当前版本有 join / ordering / 变长元素三大 blocker）、CPU 演化（E-cores 汇合 GPU，但 perf-per-watt 差一个数量级）。他最后的判断是"也许硬件已经在那里了"——GPU 里那个被藏起来的 command processor 如果对用户代码开放，也许就是答案。

## 关键要点

- Vello 的痛点是 dispatch + barrier 模型逼着 CPU 预估最大中间 buffer——根本原因是缺队列语义。
- **Latency 才是动态工作创建的主 blocker**——不是 throughput，不是并行度；100µs 级 RPC latency 导致 GPU 不能细粒度调度自己。
- Cell 和 Larrabee 都曾"接近好并行计算机"但都失败了——Cell 死于编程模型，Larrabee 死于驱动/软件生态 + 部分是 Intel 的执行力。
- [[d3d12-work-graphs|Work graphs]] 是 2024 年 GRAMPS 思想的现代复活，但 Raph 指出三个 blocker：无 join、无 ordering、无变长元素，所以 Vello 无法直接迁移上去。
- 传统 3D pipeline 保留 ordering（胡须画在脸上，Z-fighting 防止）——这是 work graphs 至今做不到的基本能力。
- CPU E-cores 的持续增加可能渐近逼近 GPU，但 perf-per-watt 差一个数量级，很难真正竞争。
- Compute 在游戏里的占比越来越大：Starfield 约一半时间在 compute，Nanite 用 compute 做小三角形的 raster——未来只会更多。

## 链接到的概念

- [[good-parallel-computer]]
- [[gpu-queues-vs-dispatch-execution]]
- [[d3d12-work-graphs]]
- [[vello-gpu-2d-renderer]]
- [[gpgpu-string-unescaping]]
- [[gpgpu-json-parsing]]

## 原文

- 链接：https://raphlinus.github.io/gpu/2025/03/21/good-parallel-computer.html
- 本地：`raw/articles/raphlinus.github.io/2025-03-21_i-want-a-good-parallel-computer.md`
