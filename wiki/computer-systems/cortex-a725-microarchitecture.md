---
tags: [cpu, arm, cortex-a725, microarchitecture, efficiency-core, dsu-120, gb10]
date: 2026-04-27
sources: 1
---

# Cortex-A725 微架构

Cortex-A725 是 Arm 7 系列效率核的最新代，随 Nvidia GB10 进入桌面/开发者场景。A725 核设计宗旨是密度优先——以数量取胜，而非单核性能。GB10 中每个 cluster 各配 5 颗 A725（主频 2.8 GHz）和 5 颗 [[cortex-x925-microarchitecture|X925]]。

## 核心定位：密度优化的效率核

与 Intel Skymont E-Core 或 AMD 低电压核走的是同一条路：以更小的面积和更低的功耗提供有竞争力的多线程性能，换取单核吞吐的让步。A725 相对于 [[cortex-a710-microarchitecture]] 的升级是保守且精准的——只在最关键的乱序结构上扩容，其余要么持平要么缩减。

## 前端变化：去掉 MOP Cache

A725 放弃了 A710 引入的 MOP Cache，改回纯解码路径，吞吐维持 5 MOP/cycle。理由是 Arm 已通过**预解码（predecode）sideband bits**降低了解码成本，MOP Cache 与预解码叠加属于过度设计。A725 的 L1I 在每条 32-bit AArch64 指令旁存储 5-bit sideband，覆盖 valid opcode 标识及解码辅助信息。实测表明对 NOP 流 A725 只能到 5 IPC，而 A710 借 MOP Cache 中的 NOP 融合可达 10 IPC——但那是人工构造的极限场景，对真实 workload 意义不大。

## 乱序执行引擎

ROB 从 A710 的 160 条目扩大至 **224 条目**，与 Intel Skylake/AMD Zen 2 量级相近。整数寄存器文件扩大，内存序列队列加深。FP/向量寄存器文件调整为 64-bit 条目（A710 为 128-bit），可用的 128-bit 向量重命名 entry 反而减少——这是刻意的面积/功耗权衡，向量执行单元在效率核上本就不是重点。

整数侧四管道全部升级为可处理单周期操作，A710 中有一管仅能做多周期运算的限制被消除。整数乘法保持两周期延迟、两发射的强表现。

## 内存子系统

**L1 DTLB** 从 A710 的 32 entry 增至 **48 entry**，覆盖 192 KB；L1 ITLB 反向从 48 缩至 32——数据侧脚印通常比代码大，因此这是合理的资源调配。L2 TLB 升级到 **1536 entry 6-way**，覆盖远超 A710。A725 还支持**页面聚合（"8×32" 模式）**，类似 AMD Zen 5 的 page smashing：将 8 个连续 4 KB 页合并为 32 KB 单条目，变相拓展 TLB 覆盖。

三 AGU（两可做 store），store forwarding 快路径 5 cycle，其他对齐 11 cycle。A725 对 store 对齐更敏感，32B 边界即会降低吞吐（A710 只在 64B 边界有惩罚）。

## SPEC CPU2017 表现

A725 在 GB10 中主频 2.8 GHz，在计算密集、cache 命中率高的 workload（如 548.exchange2）上吃亏于时钟——Neoverse N2（3.4 GHz）领先约 17%，Crestmont（3.8 GHz）领先约 14.5%。但 IPC 层面 A725 有约 10.9% 的优势。在内存延迟主导的 workload（如 520.omnetpp）中，A725 不受时钟速率影响，可以与更高频的 Neoverse N2 持平，甚至接近 Skymont。

## 竞争格局

Intel Skymont 倾向于将 E-Core 做成功率缩水版的 P-Core；AMD 则将高性能架构降频使用取得密度。Arm 的策略是真正从面积/功耗约束出发设计：去掉冗余结构（MOP Cache）、重新分配 TLB（数据侧加、指令侧减）、FP 资源向量缩减换整数扩容。在同等时钟下，A725 对 A710 应全面占优；实际上 GB10 的低主频使其未能超越老设计。

## Sources

- [[sources/chipsandcheese-cortex-a725]]
