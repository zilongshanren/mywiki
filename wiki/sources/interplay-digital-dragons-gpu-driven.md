---
tags: [source, 渲染, gpu-driven, 剔除, profiling, 演讲]
date: 2026-04-14
sources: 1
---

# GPU Driven rendering experiments at the Digital Dragons conference（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 2018 年 5 月在波兰 *Digital Dragons* 大会上做了一个小时的 GPU-driven rendering 演讲，本文是会后的短记。虽然是公告性质，但夹带了一次**把实例数从 2K 推到 20K 的 profiling 实验结果**——这是整条 GPU-driven 系列里唯一一次在有代表性的规模上量化性能的节点，因此值得单独留档。

## 摘要

和 [[multidraw-indirect-occlusion-culling|Part 2]] 相比，这次的主要改动有三个：

1. **实例数从 2K 推到 20K**——只有在这个量级上 profiling 数据才有意义。
2. **Scan 算法改写**以支持更多 thread group——Part 2 的 prefix scan 在 1 thread group × 1024 线程下只能处理 2K instance，20K 必须跨多个 group 并合并。
3. **按 stream 拆分 instance data**——原来塞在一个 struct 里的所有 per-instance 数据按「位置 / 4×3 矩阵 / drawcall ID / …」拆成多个 typed buffer；能 pack 的都 pack。用 4×3 矩阵代替 4×4 矩阵（最后一行是 `(0,0,0,1)` 可省）。

结果：**GTX 970 上 20K instance 的完整 occlusion pass 跑到 0.25ms**；HD4000 集显上约 1ms——作者称比 Part 2 的同一代码快了 **约 10 倍**（在 HD4000 上）。同时也再次吐槽 Intel 对 MultiDrawIndirect 扩展的缺席在大规模 drawcall 时明显拖性能。

## 关键要点

- 20K instance / 0.25ms 是整条系列唯一可以拿去对比的工业相关数字（GTX 970, 2018）。
- **Prefix scan 跨多 thread group** 是扩展到 >2K instance 的必经之路——参考 [[stream-compaction]] 的讨论。
- Instance data **split streams + packing** 是最大的 bandwidth 优化来源，与 [[compact-vertex-format]] 思路一致。
- 4×3 transform matrix 是 GPU-driven 管线里的常见压缩——工程上总值得做。
- Intel HD4000 10× 提速表明**瓶颈主要在 CPU → GPU draw call 数量**而非计算——在弱 GPU 上 MultiDraw 的缺席尤其痛。
- 演讲有附 PDF/PPTX slides + 完整源代码（NVAPI 依赖），但**不是单纯 slide dump**——博客正文里已经讲清了主要改动。

## 链接到的概念

- [[gpu-based-occlusion-culling]]
- [[multidraw-indirect-occlusion-culling]]
- [[stream-compaction]]
- [[compact-vertex-format]]
- [[batching]]
- [[kostas-anagnostou]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2018/05/25/gpu-driven-rendering-experiments-at-the-digital-dragons-conference/
- 本地：`raw/articles/interplayoflight.wordpress.com/2018-05-25_gpu-driven-rendering-experiments-at-the-digital-dragons-conf.md`
