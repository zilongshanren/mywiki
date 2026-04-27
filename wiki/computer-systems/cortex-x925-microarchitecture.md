---
tags: [cpu, arm, cortex-x925, microarchitecture, high-performance, dsu-120, gb10, spec-cpu2017]
date: 2026-04-27
sources: 1
---

# Cortex-X925 微架构

Cortex-X925 是 Arm 迄今为止最强的自有高性能核，在 Nvidia GB10 中以 3.9–4 GHz 运行，SPEC CPU2017 整数分数与 AMD Zen 5 和 Intel Lion Cove 持平。这是 Arm 首次在高性能桌面/笔记本段真正具备竞争力。X925 是 [[cortex-x2-microarchitecture]] 的后继，相比 [[cortex-a725-microarchitecture]] 在预算上几乎不做妥协。

## 核心规模

10-wide 解码，ROB 容量实测约 525 条指令（据文章，理论 768 有争议，实测含整数+FP+store 的混合最大为 525），高于 AMD Zen 5 的 448，略低于 Intel Lion Cove 的 576。同代 X系列核的唯一重大短板是向量宽度：X925 仅 128-bit，而 Intel/AMD 大核提供 256-bit AVX2 乃至 512-bit AVX-512，FP 浮点 workload 因此需执行更多指令。

## 前端

与 [[cortex-a725-microarchitecture]] 相同，X925 也放弃了 MOP Cache，依赖预解码（76-bit per 2 instructions）+5-wide 原始解码。最高 10 instructions/cycle，使用 2 MB 大页时效果更佳。X925 的 BTB 设计向 AMD Zen 5 靠拢：L1 BTB 最多约 2048 branches（A725 只有 512），支持每周期两个 taken branch；多级 BTB 总容量约 16384 branches。29-entry 返回栈。在 SPEC CPU2017 上分支预测精度与 Zen 5 相当，部分测试（505.mcf、541.leela）甚至略优。

## 乱序执行引擎

**整数侧**：四个调度器各 28 entry，共 8 ALU 端口 + 3 分支单元。madd 被拆成两个 uop 由任意乘法管道处理（不再有专用 madd 管道），换来吞吐提升。Move elimination 支持，但满宽重命名时失效率偏高，且不支持链式 MOV 消除——与 Intel/AMD 大核相比有差距，在 CCC 这类低质量代码下暴露（见 [[sources/chipsandcheese-ccc-april-fools]]）。

**FP/向量侧**：6 管道，每个调度器约 53 entry（三个调度器，极为宽裕）。虽然向量宽度仅 128-bit，但高调度容量和管道数量缓解了很多 throughput 压力。

## 内存子系统

- L1 DTLB：96 entry，全关联
- L2 TLB：2048 entry 8-way，统一指令/数据（6 cycle 额外延迟）
- L1D：64 KB，4 cycle，4×128-bit 读路径，约 64 B/cycle 读带宽
- L2：2 MB 8-way（Nvidia 选配），12 cycle，~32 B/cycle 读；读-改-写模式可达 45 B/cycle
- L2 严格包含 L1D，充当 snoop filter

Store forwarding：整数侧任意包含关系均可转发（优于 X2 只支持半宽）；FP/向量侧仍受对齐限制；不支持零延迟 store forwarding（Zen 5 / Lion Cove 均支持）。

## SPEC CPU2017 表现

整数套件：与 Zen 5 / Lion Cove 误差范围内持平——Arm 靠更高 IPC 弥补 4 GHz vs 竞品 5+ GHz 的时钟差距。浮点套件：明显落后 Zen 5，尤其是 554.roms（X925 需执行 Zen 5 两倍以上的指令数，根本原因是 128-bit 向量宽度不足）。高 IPC 无法抵消更多指令带来的额外延迟暴露。

## 定位与未来展望

X925 证明了 Arm 可以在不依赖高频策略的前提下，用更宽的核、更大的调度容量匹敌 Intel/AMD。但向量短板（128-bit 上限）仍是 FP 密集型 workload 的隐患。Arm 在游戏、软件生态（x86 ISA 壁垒）方面的挑战尚未解决。DSU-120 的 L3 最大只有 32 MB，在游戏等内存延迟敏感场景不及 AMD 3D V-Cache 方案。

## Sources

- [[sources/chipsandcheese-cortex-x925]]
