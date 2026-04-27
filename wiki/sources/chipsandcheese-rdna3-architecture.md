---
tags: [source, rendering, gpu, amd, rdna3, memory-hierarchy, compute, microbenchmark]
date: 2026-04-27
sources: 1
---

# Microbenchmarking AMD's RDNA 3 Graphics Architecture（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2023 年 1 月的文章，对 AMD Radeon 7900 XTX（RDNA 3）进行全面微基准测试，与 RDNA 2（6900 XT）及 Nvidia Ada Lovelace（RTX 4090）进行对比。

## 摘要

RDNA 3 在 RDNA 2 基础上全面扩展：缓存容量在各层级几乎翻倍，同时引入 VOPD（双发射）指令以提升每 WGP 计算吞吐。文章系统测量了标量/向量两路径的缓存延迟与带宽，以及全 GPU 占用下的带宽扩展性。主要发现：L0 向量缓存翻倍至 32 KB/CU；L1 翻倍至 256 KB；L2 从 4 MB 扩至 6 MB；Infinity Cache 从 128 MB 缩减至 96 MB（移至独立 memory controller die），延迟有所上升。LDS 延迟大幅改善，可能对光线追踪 BVH 栈访问有益。VOPD 双发射在 FP32 加法上有效，但 FMA（TFLOPs 的计算基础）几乎未能双发射——编译器能力不足是主要限制。总体上 7900 XTX 性能与 RTX 4080 相当，但设计哲学不同：AMD 用 chiplet+高带宽存储层次，Nvidia 用大型单芯片+更大 L2。

## 关键要点

- L0 标量缓存延迟：RDNA 3 15.4 ns vs RDNA 2 17.4 ns（16 KB，4-way）
- L1（256 KB，16-way）和 L2（6 MB，16-way）均有延迟改善，尽管容量翻倍
- Infinity Cache（96 MB，on-chiplet）延迟上升，但 L2 命中率更高，减少对其依赖
- LDS 延迟大幅改善：超越 Nvidia，单 WGP LDS 延迟优于 RDNA 2；利好 RT BVH 栈操作
- VOPD（双发射）：FP32 加法场景有效；FMA 几乎无双发射（编译器无法识别机会）
- FP64 吞吐量较 RDNA 2 下降一半（每 WGP 每周期 4 vs 8 次 FP64 操作）
- VRAM 带宽：7900 XTX 384-bit GDDR6，接近 GA102 水准
- 7900 XTX vs RTX 4080：性能基本持平（1440p 慢 1%，4K 快 1%）

## 链接到的概念

- [[rendering/rdna3-architecture]]
- [[rendering/ada-lovelace-architecture]]
- [[computer-systems/gpu-memory-hierarchy-latency]]
- [[computer-systems/gpu-latency-hiding]]

## 原文

- 链接：https://chipsandcheese.com/p/microbenchmarking-amds-rdna-3-graphics-architecture
- 本地：`raw/articles/chipsandcheese.com/2023-01-07_microbenchmarking-amds-rdna-3-graphics-architecture.md`
