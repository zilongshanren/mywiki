---
tags: [source, computer-systems, amd, mi300a, infinity-fabric, hbm3, memory-subsystem, apu, numa]
date: 2026-04-27
sources: 1
---

# Inside the AMD Instinct MI300A's Giant Memory Subsystem（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 1 月的文章，深入剖析 AMD Instinct MI300A 的 Infinity Fabric 内存子系统，重点测量其各级延迟、跨节点带宽以及 CPU-GPU 协调机制。

## 摘要

MI300A 是一块将 24 颗 Zen 4 核心与 228 个 CDNA 3 CU 整合于同一封装的巨型 APU，通过四块 IO Die 作为主动中介层统一连接，并配备 256 MB Infinity Cache 与 5.3 TB/s HBM3。这种架构中 CPU 与 GPU 共享同一 Infinity Fabric 网络，带来了高带宽的同时也引入了远高于桌面 Zen 4 的内存访问延迟。Infinity Cache 命中延迟超过 140 ns，HBM3 Miss 后更达 227 ns；在四插槽 NUMA 配置中，跨节点 DRAM 延迟高达 477~559 ns。CPU 侧 DRAM 带宽约 212 GB/s，远不能耗尽 HBM3 容量——后者实为 GPU 专用。文章还测试了 OpenCL Shared Virtual Memory（SVM）的零拷贝行为，结果 MI300A 表现出色，CPU-GPU 原子交换延迟约 222 ns，接近 Zen 4 跨 CCD 延迟，体现了深度硬件缓存一致性支持。

## 关键要点

- Infinity Cache 命中延迟 >140 ns，Miss 后 227 ns；均远高于桌面 Zen 4 DDR5 系统
- 四插槽 NUMA 配置下，跨节点 DRAM 延迟 477 ns（近节点）～559 ns（远节点）
- Infinity Cache 是 memory-side cache，与各自 CS 绑定，无法缓存其他节点地址——简化设计但牺牲部分 NUMA 性能
- CPU 侧三块 CCD 可实现约 212 GB/s 读带宽，远低于 5.3 TB/s HBM3 总带宽
- 跨节点 CPU 读带宽仅约 25 GB/s，疑似延迟瓶颈；非临时写可达 45 GB/s
- MI300A 支持 OpenCL Fine-Grained SVM 零拷贝，CPU-GPU 同步开销低于 Intel Meteor Lake
- GPU-side atomic 通过 L2 专用 ALU 处理，CPU-GPU 原子交换约 222 ns，跨插槽表现依然出色

## 链接到的概念

- [[computer-systems/mi300a-apu-memory-subsystem]]
- [[computer-systems/cdna3-mi300x-architecture]]
- [[computer-systems/infinity-fabric-loaded-latency]]
- [[computer-systems/cuda-memory-hierarchy]]

## 原文

- 链接：https://chipsandcheese.com/p/inside-the-amd-radeon-instinct-mi300as
- 本地：`raw/articles/chipsandcheese.com/2025-01-18_inside-the-amd-instinct-mi300a-s-giant-memory-subsystem.md`
