---
tags: [arm, cpu, microarchitecture, mobile, out-of-order, cortex-x]
date: 2026-04-27
sources: 1
---

# Cortex-X2 微架构

Cortex-X2 是 Arm Cortex-X 系列第二代旗舰大核，2021 年发布，ARMv9，与 [[cortex-a710-microarchitecture]] 共享基本流水线框架，但在面积和功耗预算上大幅扩展。典型实现见于高通 Snapdragon 8+ Gen 1（单 X2 核，主频 2.8 GHz）。

## 核心定位

Cortex-X2 是 A710 的"拉满版本"：相同的 10 级流水线，但乱序结构更大、前端更宽、执行单元更多。它与 [[neoverse-n2-microarchitecture]] 是表兄弟架构，但 X2 分支预测更强、结构容量更大。

## 前端

- **微操作缓存（MOC）**：3072 条目，大于 Intel Sunny Cove，可提供 8 ops/cycle，轻松喂饱 6 宽重命名器
- **指令缓存**：强制 64 KB（A710 允许 32 KB），有利于大代码占用场景
- **5 宽解码器**：优于 Zen 4 和 A710 的 4 宽；L2 代码运行时仍可超过 4 IPC
- **BTB**：微 BTB 64 条目，~10K 条目主 BTB，14 条目返回栈

## 乱序引擎

ROB 扩展至 288 条目，配套整数/浮点调度队列均按比例增大。整数调度与 Zen 4 相近（4 × 24 条目），AGU 独立于整数调度队列。

FP/向量端从 A710 的双管道升级为**四管道**，是 X2 相比 A710 最显著的变化。四管道均支持 128-bit FMA，常见 FP 吞吐与 Zen 4 的两条 256-bit FMA/cycle 相当。FP 非调度队列（NSQ）29 条目，可跟踪 75 个 in-flight FP 操作（Zen 4 为 128）。

## 内存子系统

三 AGU，支持每周期 3 load + 2 store。store forwarding 行为与 [[neoverse-n1-microarchitecture]] 以来的 Arm 大核一致：快路径 5 cycle，慢路径 10–11 cycle，不支持跨 64-bit 边界的复杂转发情形。

TLB：48 条目 L1 DTLB，2048 条目 L2 TLB（是 A710 的 2 倍）。

缓存层次（Snapdragon 8+ Gen 1）：
- L1d：64 KB，4 cycle
- L2：1 MB，11 cycle（~4 ns），ECC 强制
- L3：6 MB（12 路），~51 cycle（18 ns），由 DSU-110 提供

## 瓶颈与局限

Snapdragon 8+ Gen 1 的 6 MB L3 和极高 DRAM 延迟（202 ns）是限制 X2 发挥的主要外因。Apple M1 的 12 MB 共享 L2（兼做系统缓存）延迟更低，导致 X2 在内存敏感场景落后。写流式（write streaming）优化使 DRAM 写带宽达 41.2 GB/s，优于读带宽（32.5 GB/s）。

## 与 x86 的对比

X2 与 Zen 4 的整数调度容量接近；FP in-flight 数量不及 Zen 4，但 128-bit 向量吞吐理论值相当。Zen 4 的优势在于 256-bit AVX、更好的 store forwarding 和更高的时钟。

## Sources

- [[sources/chipsandcheese-cortex-x2]]
