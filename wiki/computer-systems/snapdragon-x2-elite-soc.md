---
tags: [cpu, qualcomm, snapdragon, oryon, soc, laptop, arm, windows-on-arm]
date: 2026-04-27
sources: 2
---

# Snapdragon X2 Elite SoC

Snapdragon X2 Elite（SDX2E）是高通面向 Windows on ARM 生态的新一代旗舰 SoC，预计 2026 年上半年上市。相较前代 Snapdragon X Elite（SDXE），SDX2E 在 CPU、GPU、NPU 三个维度均有显著升级。

## CPU 架构

SDX2E 共 18 个 CPU 核心，分三个集群：两个 Prime 集群（各 6 核，最高 5.0 GHz）和一个 Performance 集群（6 核，低功耗变种，低于 2W）。Prime 核心采用 [[oryon-microarchitecture]] Gen 3，每集群共享 16 MB L2（Performance 集群 12 MB）。

值得注意的命名惯例：高通的"Performance 核"对应业界的效率核，"Prime 核"对应业界的性能核——与其他厂商相反。

**Oryon Gen 3 相对 Gen 1 的主要变化：**
- 解码/重命名/退休宽度：8-wide → **9-wide**
- Branch Unit 数量：2 → **4**（翻倍）
- 新增 **SVE 和 SVE2** 指令集支持
- L1-miss 到 L2-hit 延迟：17 → **21 cycles**（L2 变大的代价）
- 每集群新增 **SME 兼容 Matrix Engine**（4096 位宽，独立时钟域）
- ROB 650+ 条目、物理寄存器文件 400+ 条目，与 Gen 1 相近

## Matrix Engine

每个集群（含 Performance 集群）各配一个矩阵引擎，运算单元为 64×64-bit MLA 阵列，支持：
- 128 FP32/INT32 ops/cycle
- 256 FP16/BF16/INT16 ops/cycle
- 512 INT8 ops/cycle

矩阵引擎运行于独立时钟域，便于功耗和热管理。

## GPU

集成 [[adreno-x2-igpu-architecture]]，2048 FP32 ALU，最高 1.85 GHz，是高通迄今最大 GPU。

## NPU

Hexagon NPU 6：INT8 算力 80 TOPS（前代 45 TOPS），新增 FP8/BF16 支持，矩阵引擎增加 INT2 反量化，DMA 升级至 64 位虚拟寻址（可访问 4 GB 以上内存）。

## 功耗

高通引入 INPP（Idle Normalized Platform Power）指标，从总平台功耗中扣除空闲功耗，以近似纯 SoC+DRAM+转换损耗。集群级 Turbo Boost 算法（独立于各集群，与 Intel 的 SoC 级策略不同）根据活跃核心数调整频率。

## Sources

- [[sources/chipsandcheese-snapdragon-x2]]
- [[sources/chipsandcheese-adreno-x2]]
