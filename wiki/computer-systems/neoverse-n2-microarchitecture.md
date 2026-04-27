---
tags: [cpu, arm, neoverse, server, microarchitecture, cmn700, sve]
date: 2026-04-27
sources: 1
---

# ARM Neoverse N2 微架构

Neoverse N2 是 ARM 服务器核系列的第二代（2022-2023 年商用），基于 [[computer-systems/cortex-a710-microarchitecture|Cortex-A710]] 移动核衍生而来，以更大缓存、更宽 TLB 和 48 位物理地址寻址适配服务器需求。完整商用落地以阿里巴巴倚天 710（Yitian 710，128 核，3.2 GHz）为代表。

## 核心架构

N2 是 5-wide 乱序执行核，最小分支误预测惩罚约 10 个周期（Zen 4 为 11 周期）。相比 Zen 4 的 6-wide，N2 后端规模偏小：ROB 仅 160 条目（Zen 4 为 320），物理整数寄存器约 147 个（Zen 4 为 224）。尽管 ROB 较小，ARM 在调度器容量上投入较多，整数调度器竞争力接近 Zen 4。内存访问调度器与 ALU 调度器分开，实际争抢压力低于 Zen 4 的半统一设计。

向量/FP 侧延续 N1 的两条 128-bit 执行管道，执行端口布局无变化；新增 Non-Scheduling Queue（NSQ）使 FP/向量调度器不满时整数操作也能进入，改善短序列向量代码的 ILP 提取。Neoverse N2 同时引入 SVE 支持，但与 Zen 4 引入 AVX-512 一样，未增加执行单元宽度。

与前代对比，N2 对 [[computer-systems/neoverse-n1-microarchitecture|N1]] 的改进主要在：更大 L1D（三个 128-bit 加载端口）、更大 L2 缓存（可配置至 1 MB）、更宽 TLB、更强的内存级并行性。

## 缓存与互联

所有 N2 核均标配 64 KB L1 缓存（N1 仅 32-48 KB），比 x86 同代产品的 32/48 KB 有明显命中率优势。L2 通常配置为 1 MB，访问延迟 13-14 周期，与 N1 相同。

服务器级 N2 通过 ARM CMN-700 mesh 互联。CMN-700 支持最大 12×12 的 mesh 拓扑，可配合大容量 L3 cache 和高核数（如 Yitian 710 配置了 64 MB L3）。然而 mesh 互联的固有问题是 L3 延迟偏高：Yitian 710 实测 16 MB 工作集下 L3 延迟约 35.5ns，与 Intel Sapphire Rapids（约 33ns）相近，但明显差于 AMD Zen 3 的环形总线方案（约 15ns）。详见 [[computer-systems/cache-size-vs-latency-tradeoff]]。

在 L3 带宽方面，单核 N2 可从 L3 拉取约 36.5 GB/s，与 Sapphire Rapids 接近，但远落后于 Zen 3（单核 80+ GB/s）。核间延迟（core-to-core）在八核实例内约 50-60ns，与 Intel mesh 相近。

## TLB 与物理地址

N2 将 L1 DTLB 从 A710 的 32 条目扩展至 44 条目，L2 TLB 从 1024 条目扩展至 1280 条目（5-way）。但与 Zen 4（L2 DTLB 3072 条目）相比仍有明显差距，且 x86 阵营在持续扩大 TLB 覆盖的趋势中 ARM 跟进偏慢。物理地址从 A710 的 40 位扩展至 48 位（最大 256 TB），仍落后于 x86 服务器的 52 位（4 PB）。

## 设计定位与竞争格局

ARM 的服务器策略与 AMD/Intel 相反：后者从桌面高性能核"降档"做服务器密度版，而 ARM 是从移动低功耗核"升档"增加服务器能力。这带来天然的密度优势（更小的 die area per core），但单核性能天花板较低，尤其向量和 FP 场景差距明显。N2 的定位与 Intel Sapphire Rapids 的 mesh 架构最相似，两者均面临 L3 延迟偏高的共同问题。AMD 的 Bergamo 128 核和 Ampere Siryn 192 核是 N2 的直接高密度竞争者。

## Sources

- [[sources/chipsandcheese-neoverse-n2]]
