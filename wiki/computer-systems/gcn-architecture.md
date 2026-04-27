---
tags: [gpu, amd, gcn, compute-unit, architecture-history, simd, scheduling]
date: 2026-04-27
sources: 1
---

# AMD GCN 架构

GCN（Graphics Core Next）是 AMD 于 2011 年随 Tahiti（HD 7950）推出的 GPU 架构，彻底取代 Terascale/VLIW 路线。GCN 以可预测的通用计算性能为核心设计目标，其基本结构延续到 2021 年的 Cezanne，并在 [[cdna2-mi200-architecture]] 与 CDNA 3（[[cdna3-mi300x-architecture]]）中以计算变体形式延续。

## 设计转向

Terascale 使用 VLIW 宽指令束和编译器驱动的 ILP，运算单元利用率高度依赖编译器质量。Nvidia 的 Fermi/Kepler 则已转向硬件调度。GCN 的解法是：

- 放弃 VLIW，改为每线程 scalar 执行
- 将调度责任从编译器转移到硬件（线程级并行驱动多发射）
- 缓存体系现代化，从只读纹理缓存升级为支持写回的通用层次

## Compute Unit 结构

一个 CU 包含：

- 4 个 16-wide SIMD，每个 SIMD 有独立的 64 KB 向量寄存器文件和 10 槽线程缓冲区（每个 SIMD 可追踪 10 个 wavefront，全 CU 共 40 个）
- 每周期调度器选择一个 SIMD，扫描可就绪的线程，最多可五路多发射（跨不同功能单元类型）
- 单线程以每 4 周期发射一条指令的节奏推进（16-wide × 4 cycle = 64-wide wavefront）
- 8 KB 标量寄存器文件 + 标量 ALU（处理控制流与地址计算，卸载向量 ALU）

CU 之间共享 32 KB 指令缓存（4 CU 共用）和 16 KB 标量缓存（4 CU 共用，~50 ns 命中延迟）。

## 缓存层次

GCN 将 GPU 缓存体系现代化：

- **L1 向量缓存**：16 KB，4-way，写通/写分配，64 B/cycle，虚拟地址（避免 TLB miss）
- **LDS（本地数据共享）**：64 KB 软件管理 scratchpad，32 banks × 32-bit = 128 B/cycle，支持 LDS 原子操作（优于 Kepler 的 Shared Memory）
- **L2 缓存**：写回设计，按内存控制器分片，每片 64 KB / 64 B/cycle；支持原子操作（Terascale L2 是只读纹理缓存）

相比 Kepler 的多条独立缓存路径（纹理缓存、L1/scratchpad 共享、常量缓存），GCN 结构更简洁，面积更紧凑（CU 私有存储 ~80 KB vs. Kepler SMX 的 146 KB）。

## 调度策略对比

| 架构 | 策略 | 依赖 |
|------|------|------|
| Terascale | 编译器 VLIW 打包 | 编译器质量 |
| GCN | 硬件多线程多发射 | 高 occupancy |
| Kepler | 编译器标记 dual-issue（cherry on top） | 稀疏触发 |

GCN 的高 occupancy 要求意味着：大 kernel、长执行、高并行度的工作负载表现出色；小三角形、短 draw call、低并行度场景则被 Kepler 追上甚至超越（Kepler 单线程 IPC 更强）。

## 图形性能瓶颈

GCN 的光栅化前端与计算后端比例失衡。Tahiti 仅有 2 个光栅器面对 32 个 CU，达到最低 occupancy 需 256 cycle，全满 occupancy 需 2560 cycle。Hawaii 升到 4 个光栅器，有所改善。这一问题推动了后续 RDNA 对 Compute Unit 利用率和前端吞吐的重新设计。

## 历史地位

GCN 的设计预见了 GPU 向通用计算的演进方向，尽管 AMD 在 CUDA 生态下未能从中获得商业回报。其标量数据路径被 Turing 借鉴，CDNA 系列保留了其 CU 基本结构（去除了图形硬件），成为 Frontier 超算的核心组件。

## Sources

- [[sources/chipsandcheese-gcn-modernization]]
