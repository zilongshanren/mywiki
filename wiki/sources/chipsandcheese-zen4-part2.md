---
tags: [source, computer-systems, amd, zen4, memory-subsystem, cache, ddr5]
date: 2026-04-27
sources: 1
---

# AMD's Zen 4 Part 2: Memory Subsystem and Conclusion（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2022 年 11 月，Zen 4 深度解析的第二部分，聚焦 load/store 执行、缓存层次延迟与带宽、TLB 改进，以及对 DDR5 内存的迁移。

## 摘要

文章测量了 Zen 4 的存储转发特性（无延迟前提下 2 IPC，精确地址匹配）、缓存延迟（L1 ~0.7 ns、L2 ~2.44 ns、L3 ~8-9 ns，均因高频受益）、TLB 改进（L1 DTLB 64→72 项，L2 TLB 2048→3072 项）以及带宽（L3 单核 27 bytes/cycle，多核受益于高频）。DDR5-6000 实测约 72.85 GB/s（理论值 76%），较 DDR4 提升约 43% 但效率略有下降。文章结论认为 Zen 4 的性能提升更多来自频率而非 IPC 增益，但频率提升带来的收益是线性的，总体性能表现与前几代 Zen 的提升幅度相当。

## 关键要点

- L2 容量翻倍至 1 MB，延迟仅增加 2 cycle（绝对延迟略优于 Zen 3）
- L3 延迟恢复到 Zen 2 水平（~8-9 ns）但容量更大（32 MB），优于 Zen 3 V-Cache 的延迟
- Golden Cove L3 延迟比 Zen 4 高约 20 cycle，需要更大乱序窗口弥补
- L2 TLB 3072 项（vs Golden Cove 的 2048 项），大工作集场景优势显著
- 单核 DRAM 带宽超 57 GB/s，暗示 L2 miss 追踪队列极深（通过 Little's Law 估算）
- Intel Golden Cove 在 L1/L2 带宽上有优势（尤其 AVX-512），L3 带宽则急剧下降
- 写带宽受 CCD→IO die 链路（2×16 bytes/cycle @2000 MHz = 64 GB/s）限制，可用 non-temporal write 验证
- 整体结论：执行单元容量不是瓶颈，喂饱执行单元（更好的前端、更深的队列、DDR5）才是关键

## 链接到的概念

- [[computer-systems/zen4-microarchitecture]]
- [[computer-systems/golden-cove-microarchitecture]]
- [[computer-systems/memory-hierarchy]]
- [[computer-systems/littles-law-reorder-buffer]]
- [[computer-systems/raptor-lake-l2-cache]]
- [[computer-systems/numa-multi-socket-design]]

## 原文

- 链接：https://chipsandcheese.com/p/amds-zen-4-part-2-memory-subsystem-and-conclusion
- 本地：`raw/articles/chipsandcheese.com/2022-11-08_amds-zen-4-part-2-memory-subsystem-and-conclusion.md`
