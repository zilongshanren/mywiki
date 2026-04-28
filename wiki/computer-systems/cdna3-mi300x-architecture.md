---
tags: [gpu, amd, cdna3, mi300x, hpc, ai, chiplet, infinity-cache, coherence]
date: 2026-04-27
sources: 1
---

# AMD CDNA 3 / MI300X 架构

CDNA 3 是 AMD 第三代计算 GPU 架构，以 MI300X 和 MI300A（APU 版）为代表。它在 [[cdna2-mi200-architecture]] 的基础上做出了三大飞跃：统一大 GPU 呈现、Infinity Cache 引入、以及 CU 执行单元改良。

## Chiplet 布局

MI300X 由三种 die 组成：

- **XCD（Accelerator Complex Die）**：TSMC 5 nm，每片含 40 个 CDNA 3 CU（MI300X 启用 38 个）和 4 MB L2 缓存。MI300X 共 8 枚 XCD，合计 304 CU。
- **IO Die**：TSMC 6 nm，每片含 Infinity Cache 切片、HBM3 内存控制器，以及跨 die Infinity Fabric 互联。MI300X 共 4 枚 IO Die。
- **Base Die**：被动中介层，通过 Foveros/CoWoS 封装连接所有 die。

与 [[cdna2-mi200-architecture]] 的 MI250X（两片 GCD，编程模型是双 GPU）不同，MI300X 通过大幅提升 die-to-die 带宽（东西向 2.4 TB/s/方向、南北向 3.0 TB/s/方向，较 MI250X 提升 12×），使 8 片 XCD 以单一统一 GPU 呈现。

## Infinity Cache：带宽优先设计

MI300X 从 RDNA 消费 GPU 借入了 Infinity Cache（AMD 内部称 MALL，Memory Attached Last Level）。其设计思路是**带宽优先，而非容量优先**：

- 128 切片，每切片 2 MB、64 B/cycle 读带宽
- 总理论带宽 **17.2 TB/s**（@2.1 GHz），对比 HBM3 的 5.3 TB/s
- 16 路组相联，作为内存侧缓存（memory-side cache）置于内存控制器旁

roofline 模型分析：利用 Infinity Cache 时，仅需 4.75 FLOP/byte 即可跑满 FP64 峰值算力；纯靠 DRAM 则需 14.6~15 FLOP/byte。

### 跨 die 带宽瓶颈

当 MI300X 以统一模式运行时，若内存访问平均条带化到所有 IO die，每片 IO die 的 2.7 TB/s ingress 带宽不足以满足两片 XCD 所需的 4.2 TB/s Infinity Cache 带宽（其中 3/4 需跨 die 获取），形成潜在瓶颈。高 L2 命中率或 NUMA 分割模式可缓解此问题。

## 跨 XCD 一致性

CDNA 3 通过 Coherent Master（CM，位于 XCD-IO 边界）和 Coherent Slave（CS，位于每个内存控制器旁）实现跨 XCD 缓存一致性，机制与 Zen 系列 Infinity Fabric 类似。CS 含探测过滤器（snoop filter）覆盖所有 XCD 的 L2 缓存状态，避免广播探测。普通写操作仍需显式 `buffer_wbl2` / `buffer_inv` 指令完成 L2 写回和失效，与 CPU 的硬件自动维护有所不同。

## CU 执行单元改进

### FP32 双发射

CDNA 2 提供原生 FP64，FP32 通过 packed 执行（编译器将两个 FP32 打包进相邻寄存器）实现 double-rate，但编译器难以自动完成。CDNA 3 改为**运行时双发射**：每周期调度器为一个 SIMD 扫描可执行线程，若找到两个均有 FP32 指令就绪的线程则同时发射。每 SIMD 可追踪线程数从 8 扩至 24，以提升找到双发射机会的概率。

这一策略依赖高 occupancy——简单 kernel 使用少量寄存器，可维持更多活跃线程。

### 其他改进

- L1 缓存：容量 16 → 32 KB，带宽 64 → 128 B/cycle
- 指令缓存：32 → 64 KB，4-way → 8-way（对应更复杂的计算 kernel）
- 矩阵吞吐：每 CU 矩阵运算吞吐相比 CDNA 2 翻倍

## MI300A：CPU-GPU 统一内存 APU

MI300A 将 6 枚 XCD + 24 个 Zen 4 核心集成在同一封装中，CPU 与 GPU 共享同一内存地址空间，彻底消除 PCIe 数据搬运开销。

详细内存子系统分析、延迟数据与 CPU-GPU 协调机制见 [[computer-systems/mi300a-apu-memory-subsystem]]。GPU 算力横评（对比 MI300X）见该页面附录。

## Sources

- [[sources/chipsandcheese-cdna3]]
- [[sources/chipsandcheese-mi300x-testing]]
- [[sources/chipsandcheese-mi300a-memory]]
- [[sources/chipsandcheese-mi300a-gpu]]
- [[sources/chipsandcheese-cdna4]]
