---
tags: [source, computer-systems, cpu, gpu, nvidia, arm, neoverse, hpc, interconnect]
date: 2026-04-27
sources: 1
---

# Grace Hopper, Nvidia's Halfway APU（Chips and Cheese）

[[chester-lam]] 发表于 2024 年 7 月的文章，在 GH200 云实例上实测 Grace CPU（72 核 Neoverse V2）的微架构特性，并与 Graviton 4 的同核实现进行对比，附带 H100 GPU 初步测试。

## 摘要

GH200 将 Grace CPU（72 颗 Neoverse V2，3.44 GHz，114 MB L3，480 GB LPDDR5X）与 H100 SXM 级 GPU（96 GB HBM3）通过 NVLink C2C（900 GB/s 双向）连接。与 Graviton 4 相比，Grace 频率更高但 L2 更小（1 MB vs 2 MB），L3 延迟极差（125 周期，>38 ns）。CPU 访问 HBM3 带宽合理，但延迟高达 800 ns，NVLink C2C 远不如 AMD Infinity Fabric 的延迟表现。实测 libx264 和 7-Zip 均弱于 Graviton 4，STALL_BACKEND_MEM 性能计数器证实 L2 miss 是主要瓶颈。文章总结了 ARM 授权模式的内在挑战：核心设计者无法控制 implementer 的平台决策。

## 关键要点

- Grace Neoverse V2：3.44 GHz，1 MB L2，114 MB L3，L3 延迟 125 周期（vs Graviton 4 的 68 周期）
- NVLink C2C：900 GB/s 双向，CPU→HBM3 延迟 ~800 ns
- LPDDR5X 延迟 >200 ns，远差于 Graviton 4 的 114 ns
- libx264/7-Zip 均弱于 Graviton 4，与频率优势预期相反
- H100 GPU：完整 HBM3 总线，但 NVLink/OpenCL 存在系统稳定性问题
- ARM 授权模式的挑战：implementer 平台决策偏差导致核心性能无法发挥

## 链接到的概念

- [[grace-hopper-cpu-gpu-system]]
- [[neoverse-v2-microarchitecture]]
- [[h100-hopper-architecture]]
- [[cuda-memory-hierarchy]]

## 原文

- 链接：https://chipsandcheese.com/p/grace-hopper-nvidias-halfway-apu
- 本地：`raw/articles/chipsandcheese.com/2024-07-31_grace-hopper-nvidias-halfway-apu.md`
