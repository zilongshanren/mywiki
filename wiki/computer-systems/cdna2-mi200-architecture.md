---
tags: [gpu, amd, hpc, cdna, mi200, instinct, infinity-fabric, chiplet]
date: 2026-04-27
sources: 1
---

# AMD CDNA2 / MI200 架构

AMD Instinct MI200 系列（MI250、MI250X）是 CDNA（Compute DNA）的第二代，专门面向 HPC 与 AI 计算，与消费级 RDNA 架构彻底分道扬镳。MI200 的核心突破在于：**全速 FP64**、**双 GCD chiplet 设计**、以及通过 Infinity Fabric 实现的 CPU-GPU 统一内存。

## 架构概览

MI200 延续了"Compute Unit（CU）→ Shader Engine → Compute Engine"的 GCN 血统，但大幅重组了数值精度优先级：

- **4x SIMD16 + 4x Matrix Core** 的 CU 基础结构继承自 MI100
- ALU 升级为原生 64 位宽，实现 **全速 FP64**（MI100 只有半速 FP64），相当于 FP64 FLOPS 翻倍
- 引入 **Packed FP32** 支持：两个相邻对齐的 FP32 操作合并执行，理论 2x FP32 吞吐量，但需要编译器辅助代码修改
- Matrix Core 单元的 FP64 矩阵吞吐量相比 MI100 提升 **4x**

## 寄存器文件统一

MI100 将向量寄存器（VGPR）和矩阵累积寄存器（Accumulator）分开存储（各 256 项）。MI200 合并为 **512 项统一寄存器文件**，消除了矩阵操作时在两个 RF 之间移数据的开销，同时也提高了非矩阵代码的 occupancy。

## 内存层次

每个 GCD 配备：
- **8 MB L2 缓存**，分 32 个 slice，总带宽 4096 B/clk（MI100 的 2 倍）
- **4 栈 HBM2E**，共 64 GB，带宽 1.6 TB/s/GCD

与 RDNA2 相比，CDNA2 选择了简单的两级缓存 + 超高带宽路线，而非 RDNA2 的复杂多级缓存 + 便宜 GDDR6 组合。

## 双 GCD Chiplet 设计

MI250/MI250X 每块加速卡内含两个 GCD，通过 **4 条 Infinity Fabric 片内链路** 互联，双向总带宽 400 GB/s。但这仍远低于 HBM2E 的内存带宽，因此 AMD 选择将 MI250X 暴露为**两个独立 GPU**，而非一个统一的 GPU——因为无法在 die 间提供与 HBM 等效的带宽来支持统一内存模式。

对比之下，Intel Ponte Vecchio 和 Biren BR100 在同一代可以将多 die 呈现为单一 GPU，但依赖软件感知拓扑才能达到最佳性能。

## CPU-GPU 统一内存（Infinity Architecture 3）

每个 GCD 拥有三条跨封装 IF 链路，可连接其他 MI250X 卡或主机 CPU：

- 连接 AMD Trento（优化版 EPYC）时，IF 链路工作在完整 GPU-CPU 硬件缓存一致性模式，CPU 可以直接缓存 GPU 的 HBM 内存
- 连接其他 x86 CPU 时，退化为 PCIe x16 接口

此外，MI200 新增了下行 PCIe 4.0 ESM 接口，让 GPU 可以直接驱动 NIC 等 IO 设备，将网络流量的内存带宽压力转移到高带宽 HBM 上——支持 4x 200 Gbps NIC 接入而不耗尽 CPU 侧 DDR4 带宽。

## HPC 成果

MI250X 成功进入 Frontier（世界第一超算）和 LUMI（世界第三超算），标志着 AMD 在 HPC 领域取得重大突破。相对弱点是低精度矩阵性能（AI 训练）仍落后于 NVIDIA A100/H100，这一问题由继任的 CDNA3（MI300）通过 FP8 支持和更强矩阵单元解决。

## 相关

- [[mcm-gpu-design]]
- [[gcn-wave-occupancy]]
- [[gpu-memory-hierarchy-latency]]
- [[gpu-latency-hiding]]
- [[amd-k8-microarchitecture]]

## Sources

- [[sources/chipsandcheese-mi200-architecture]]
