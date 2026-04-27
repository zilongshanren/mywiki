---
tags: [cpu, arm, server, microarchitecture, neoverse, graviton]
date: 2026-04-27
sources: 2
---

# ARM Neoverse V2 微架构

Neoverse V2 是 ARM 服务器核 Neoverse V 系列的第二代（2023 年），对应客户端的 Cortex-X3。它代表了 ARM 在高性能服务器核上的阶段性成熟：乱序深度已与 [[zen4-microarchitecture|Zen 4]] 持平，但时钟频率明显偏低，二者形成了鲜明的 IPC 与频率的取舍对比。落地于 AWS Graviton 4（96 核）和 Nvidia GH200 Grace（72 核）。

## 核心规格

| 结构 | Neoverse V2 | Zen 4（参考）|
|------|-------------|-------------|
| 解码宽度 | 6 宽（8 宽 rename，实测 6） | 6 宽 |
| ROB | ~320 项 | ~320 项 |
| 整数 ALU 调度队列 | ~60 项（Graviton 4 禁用 2 条额外 ALU）| ~96 项 |
| FP/向量管道 | 4×128 位 | 4×256 位 |
| 典型频率 | 2.8 GHz（Graviton 4）/ 3.44 GHz（Grace）| 3.7 GHz（Genoa-X 全核）|

## 分支预测

使用 8 分量 TAGE 预测器，与 [[golden-cove-microarchitecture|Golden Cove]] 能力相近，但弱于 Zen 4 对超长历史的处理能力。Zen 4 为支持 SMT 而过度建设了分支预测器，在实际 workload 中优势有限。

BTB 采用三级方案：nano-BTB 处理小循环（256 项，每周期两个 taken branch）；中层约 8K 项，单周期延迟；L2 BTB 约 14K 项，2–3 周期延迟。总体覆盖范围在同代核中领先，有助于应对分支密集的服务器代码。

返回栈约 31 项，Call+Return 延迟与 Zen 4 持平。

## Micro-op Cache

1536 项 Micro-op Cache（MOC），较前代 Cortex X2 的 3072 项缩减，因为 V2 时钟较低时 MOC 主要作用是降功耗而非提频率，过大反而浪费面积。MOC 虚拟索引虚拟标签，命中可跳过 TLB 查询。

## 整数执行

在 Graviton 4 的实现中，Arm 规格书所列的 6 条 ALU（较 V1 的 4 条增加）有 2 条被 AWS 删去，实际可用 4 条主 ALU + 独立 Branch 端口。Branch 仍走独立端口，有利于分支早执行。Zen 4 在整数端口上存在 AGU 与 ALU 共享调度队列的设计，V2 此处略有差异。

## FP/向量执行

四条 128 位管道，全部支持 FMA，可与 Zen 4 对齐 FP 吞吐量（在不使用 256 位向量的情况下）。标量 FP 加法 2 周期延迟，向量整数加法也是 2 周期（疑似 FP 寄存器堆双周期读取）。Non-scheduling Queue 延迟调度器溢出时的停顿。

## 内存子系统

- **L1D**：64 KB，4 周期延迟，RRIP 替换策略（优于伪 LRU）。
- **L2**：AWS 选 2 MB，Grace 选 1 MB；2 MB 版延迟约 11 周期，远低于 Zen 4 的 14 周期（绝对 ns 值则因 V2 低频而更接近）。
- **L3/Mesh**：V2 依赖大 L2 缓冲低性能 L3。Graviton 4 仅 36 MB L3，延迟约 25 ns；Grace 配 114 MB L3，但延迟高达 125 周期（>38 ns），是整个系统的主要性能短板。
- **Store forwarding**：仅支持 64 位 store 的前半/后半向 32 位 load 转发，比 Intel/AMD "任意包含子集均可转发"的能力弱；快路径 5 周期，转发失败 10–11 周期（优于 Zen 4 的 19 周期）。

## 实现差异：Graviton 4 vs Grace

两者使用相同的 Neoverse V2 核，但实现策略截然不同：

- **Graviton 4（AWS）**：降频至 2.8 GHz，2 MB L2，36 MB L3，低时钟+大 L2 减少 noisy neighbor 影响，稳定性优先。
- **Grace（Nvidia GH200）**：提频至 3.44 GHz，1 MB L2，114 MB L3，追求高并行吞吐量；但 L3 延迟极高（125 周期），加之 LPDDR5X 内存延迟 >200 ns，反而造成 libx264 等 workload 低于 Graviton 4。

这一案例说明了 ARM IP 授权模式的内在张力：Arm 必须支持多元 implementer，无法像 AMD/Intel 那样针对固定平台精细调优 — 详见 [[sources/chipsandcheese-grace-hopper]]。

## 竞争定位

Neoverse V2 并非面向极限单线程性能的核（不像 [[golden-cove-microarchitecture|Golden Cove]] 或 [[oryon-microarchitecture|Oryon]]），而是面向服务器高密度与功耗受限场景。在 7-Zip 等分支密集任务中竞争力不错；在 libx264 等需要高带宽向量运算的场景，Zen 4 凭借 AVX2/频率优势领先。后续 Cortex X4/Neoverse V3 在多个子系统上进行了针对性加强。

## Sources

- [[sources/chipsandcheese-neoverse-v2]]
- [[sources/chipsandcheese-grace-hopper]]
