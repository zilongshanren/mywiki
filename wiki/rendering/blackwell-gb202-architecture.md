---
tags: [gpu, nvidia, blackwell, gb202, 微架构, 渲染]
date: 2026-04-27
sources: 1
---

# Blackwell GB202 架构

GB202 是 Nvidia Blackwell 显卡架构中规模最大的 die，面积 750 mm²，搭载 921 亿晶体管，共 192 个 Streaming Multiprocessor（SM）。RTX PRO 6000 Blackwell 是目前启用 SM 最多（188 个）的 GB202 产品，功耗上限 600 W。

## 工作分发

Blackwell 保持了 Ada Lovelace 之前的两级分发层次：GPC（Graphics Processing Cluster）负责光栅化与工作分发，SM 是基本计算单元。GB202 将 GPC:SM 比率从 Ada 的 1:12 扩至 1:16，以更低的 GPC 复制代价换来更高的 SM 总数。

这一比率与十年前 AMD GCN Fury X 相同（SE:CU = 1:16）。代价是短 wave 场景下分发成为瓶颈，GPC 分配速率而非 SM 计算速率决定吞吐。Blackwell 相比老 GCN 有更高的每 SM wave 发射率，因此影响较小，但 GB202 仍比小 GPU 更难喂饱。

Blackwell 新增支持同一队列中不同类型工作负载（图形 + compute）的重叠执行，消除了此前需要 subchannel switch 和 wait-for-idle 的强制序列化，提升混合工作负载下的 SM 阵列利用率。

## SM 前端

Blackwell 沿用 post-Turing 的固定长 128-bit（16 字节）指令格式，采用两级指令缓存：每个 SM partition 私有的 32 KB L0i，以及全 SM 共享的 128 KB L1i。

L1i 大约可容纳 8K 条指令，L0i 容量与 Ada 持平（均为 32 KB，较 Turing 的 16 KB 翻倍）。L1i 单 partition 带宽足够，但若两个 partition 同时走不同代码路径且均 spill 出 L1i，每 partition 吞吐降至 1 指令/2 周期。

AMD 的可变长指令（4–12 字节）在相同容量下能容纳更多条目，RDNA4 WGP 有 32 KB 共享 L1i，理论上每 SIMD 可供 32 字节/周期，且两 wave 走不同路径时不掉速。

## 执行单元

每 SM partition 最多追踪 12 条 wave（RDNA4 每 SIMD 为 16 条），寄存器堆维持 Ampere 以来的 64 KB/partition，若以 8 寄存器为分配粒度，最大占用率下每 wave 不超过 40 个寄存器（RDNA3/4 高端 SIMD 为 192 KB，可维持最大占用的同时支持 96 寄存器/wave）。

Blackwell FP32/INT32 主执行管道重组为单路 32-wide pipe，与 AMD RDNA 及 Nvidia Pascal 类似，避免了单一类型指令连续流造成停顿。每 partition 每周期可完成 16 次 INT32 乘法（Pascal 和 RDNA 约为 1/4 速率，即 8 次）。

Blackwell 在 uniform datapath（类 AMD 标量单元）中新增浮点指令，包括 add、multiply、FMA、min/max 及整数/浮点转换，与 AMD 在 RDNA 3.5/4 中新增 FP 标量指令的趋势呼应。

## SM 内存子系统

Blackwell 沿用 128 KB L1 Cache/Shared Memory 共用块，布局与 Ada Lovelace 和 Ampere 相同。与数据中心版不同，消费级 Blackwell 未扩容该模块。

RTX PRO 6000 的 188 SM 合计拥有超过 24 MB L1/Shared Memory 及 60 TB/s 的 L1 聚合带宽。AMD RX 9070 的 28 WGP 共约 6 MB 第一级数据存储，但每 WGP 的向量 L0（128 B/cycle 每个）和 LDS（256 B/cycle）单位带宽更高。

Blackwell 的地址生成优势：依赖数组访问只需一条 IMAD.WIDE 即可完成索引到地址的转换；AMD 向量单元原生仅支持 32-bit 整数，生成 64-bit 地址需要 add-with-carry，略慢于 Nvidia。若编译器能将地址计算路由到标量单元，AMD 可反超。

## GPU 级内存子系统

Blackwell 延续 Ada Lovelace 策略，以更大的 L2 代替 AMD 的 Infinity Cache 层级。GB202 有 64 个 L2 bank，L2 带宽约 8.7 TB/s。但 L2 延迟相比 Ada 有所回退，达到约 130 ns（Ada 约 107 ns），现在更接近 AMD Infinity Cache 延迟而非 L2 延迟。

VRAM 延迟约 329 ns，高于 AMD RDNA4（254 ns）。Ada 和 Ampere 的 VRAM 延迟与 RDNA2/4 相当；Blackwell 的延迟回退可能部分源于 die 规模扩大带来的片上网络延迟增加。

GB202 配备 512-bit GDDR7 总线，在大工作集场景下 VRAM 带宽大幅领先 AMD 的 256-bit GDDR6 方案。

## 规模优势

Blackwell 的主要竞争力来自规模而非单核效率：188 SM 对比 AMD RX 9070 的 28 WGP，在算力、L1 总量和 VRAM 带宽上全面领先。Chester 指出 GB202 的光线三角形相交测试速率是 Ada 的两倍；支持 Opacity Micromaps；FluidX3D 等计算负载中，RTX PRO 6000 显著领先 RX 9070。

## 竞争格局

2025 年消费级顶端缺乏有效竞争。Intel Battlemage 和 AMD RDNA4 止步于中端，均未挑战 Nvidia GB202 的顶端地位。RTX PRO 6000 的 FP32 向量算力接近 AMD MI300X 数据中心 GPU，远超 Nvidia 自家 B200 数据中心 GPU——后者设计侧重 FP64 和 Tensor Core 而非纯 FP32 算力。

## 相关

- [[rdna4-architecture]]
- [[gb10-gpu-blackwell-igpu]]
- [[ada-lovelace-architecture]]
- [[h100-hopper-architecture]]
- [[gpu-register-file-occupancy]]
- [[gpu-latency-hiding]]

## Sources

- [[sources/chipsandcheese-blackwell-gb202]]
- [[sources/chipsandcheese-b200-blackwell]]
