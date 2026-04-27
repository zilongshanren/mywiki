---
tags: [cpu, intel, sandy-bridge, microarchitecture, ring-bus, op-cache, avx]
date: 2026-04-27
sources: 1
---

# Sandy Bridge 微架构

Sandy Bridge（2011 年，Intel 第二代 Core 系列）是 Intel 历史上最重要的架构里程碑之一，奠定了此后十余年 Intel 高性能核的技术基础，也深刻影响了 AMD Zen 系列和 ARM 高性能核的设计思路。

## 历史地位

Sandy Bridge 融合了 P6 家族（Pentium Pro 到 Nehalem）的乱序执行思路与 Netburst 的若干创新（如 micro-op 缓存的理念），形成了全新设计。与之前同为 4-wide 的 Core 2（Merom）和 Nehalem 相比，Sandy Bridge 并未扩宽流水线，而是通过彻底改善各级"供给"效率实现了性能飞跃：更强的分支预测、Micro-op Cache、PRF 乱序引擎、分布式环形总线 L3。

## Micro-op Cache

Sandy Bridge 引入了 1536 entry、8-way 的 micro-op cache（µop cache / decoded instruction cache），虚地址索引，与 32-byte 对齐内存区域一一对应。命中时绕过传统 fetch+decode 路径，以更低功耗和延迟向后端供给 micro-op。

前端因此有四条供给路径：µop cache、L1 指令缓存 decoder、L2 指令预取、BTB 引导。这种复杂但高效的前端设计后来被 AMD（Zen 系列）和 ARM（A77 起）广泛借鉴。Intel、AMD、ARM 在 µop cache 规格（均为约 1536 entry）上的趋同是微架构设计收敛的典型案例。

## 分支预测改进

Sandy Bridge 的分支预测性能相比 Nehalem 有重大提升：

- 使用 1-bit 计数器 + 跨 entry 共享"置信位"，以同等存储面积实现更大的历史表
- BTB 从 2048 扩至 4096 entry，容量翻倍，延迟不增加（2 周期）
- 新增 L0 BTB，可以 1 周期处理最多 8 个 taken branch
- 间接分支预测支持单分支 24 个目标，或 64 个分支各 2 个目标

## PRF 乱序执行引擎

Sandy Bridge 从 P6 的 ROB 存值方案切换到 Physical Register File（PRF）方案：结果存在物理寄存器文件中，ROB 仅持有指向物理寄存器的指针。这避免了在指令 retire 时复制寄存器值，使得实现 256-bit AVX 完整宽度寄存器在功耗和面积上变得可行。ROB 容量因此可以大幅扩展（Sandy Bridge 为 168 entry）。

Sandy Bridge 的执行端口为 6 个（含 1 个专用 store data 端口，实质 5 个通用端口），三个 ALU 端口，两个 AGU 端口。向量和 FP 吞吐在 Port 0/1 上有偏向（乘法/加法分开），多 shuffle 操作会造成 Port 5 拥堵。

## 分布式环形总线 L3

Sandy Bridge 将中央化的 Nehalem Global Queue（GQ）替换为分布式环形总线 + L3 切片架构。每个 L3 切片独立处理本地请求，切片之间通过环形总线互联：

- L3 延迟从 Nehalem 的 ~17.5 ns 降至 ~10.3 ns（6-core 版本）
- 每核 L3 带宽接近翻倍（从约 4.7 bytes/cycle 升至 9+ bytes/cycle）
- core-to-core 延迟因核心与 L3 切片的拓扑距离而略有差异，但最差情况优于 Nehalem 的最好情况

这一分布式 L3 设计后来成为 Intel 所有多核处理器的标准方案，AMD 在 Zen 3 中也引入了类似的环形总线（在 CCD 内部）。

## 影响与延续

Sandy Bridge 是 Intel 自我超越的典范——彼时 Nehalem 已足够击败 AMD 的 Bulldozer，但 Intel 依然推出了在架构上更激进的全新设计。Sandy Bridge 的核心思想：

1. µop cache 解耦 fetch/decode 与 backend
2. 分布式 L3 切片 + 环形总线
3. PRF 乱序执行引擎

至今仍能在 [[computer-systems/golden-cove-microarchitecture]]（Alder Lake P-core）、[[computer-systems/zen4-microarchitecture]]（AMD Zen 4）以及 [[computer-systems/cortex-a710-microarchitecture]]（ARM A710）中找到对应的结构。

## Sources

- [[sources/chipsandcheese-sandy-bridge]]
