---
tags: [cpu, 微架构, intel, atom, e-core, skymont, lunar-lake]
date: 2026-04-27
sources: 1
---

# Skymont 微架构

Skymont 是 Intel E-Core 在 Lunar Lake 中的新架构，是 [[crestmont-microarchitecture|Crestmont]] 的后继者，也是 Intel Atom 系列迄今最激进的一次跨代升级。它的目标是使低功耗岛能够承载更广泛的应用负载，包括此前 Atom 历来薄弱的向量计算。

## 三簇前端与 Nanocode

[[clustered-decode-atom|集簇解码]] 模式在 Skymont 扩展为三簇。每簇仍为 3-wide 解码，合计 9 uop/cycle，比 Crestmont 的 6 uop/cycle 提升 50%。三个簇各有 32 条目微操作队列，总容量 96 条目，让前端在后端阻塞时有更大的预执行空间。

Skymont 引入了"Nanocode"机制：将最高频微码指令（如 gather 向量收集）的处理逻辑复制到每个解码簇，允许三簇并行处理不同的微码序列，而不会因共享微码 ROM 访问而互相阻塞。这是 x86 Atom 解码器设计上的一次创新——虽然 Apple Silicon 也有类似思路（每簇带复杂解码器），但实现方式不同。

Intel E-Core 架构师 Stephen Robinson 解释三簇 3-wide 而非两簇 4-wide 的选择：x86 典型代码每 6 条指令含一个分支，3-wide 解码器在这个分支密度下更易填满，且三簇在负载均衡上比两簇更灵活。

## 大幅扩容的后端

- **重命名宽度**：8 uop/cycle
- **退役宽度**：16 uop/cycle（是入队宽度的 2×），通过快速释放后端资源来间接扩大有效 OoO 窗口
- **ROB**：416 条目（Crestmont 256 条目）
- **执行端口**：26 个，其中整数 ALU 8 个，4 个 store 地址 AGU

虽然 4 个 store AGU 超过 L1D 的 2 store/cycle 写带宽，但额外 AGU 有助于更早完成地址计算，加速 load-store 依赖判断。

## 向量执行大升级

Crestmont 及以前的 Atom 核心向量执行能力有限，是主要的"玻璃下巴"（glass jaw）。Skymont 将向量执行扩展至 4×128-bit FP/整数，FMA 延迟从 Crestmont 的 6 cycle 降至 4 cycle，性能接近 Arm Cortex X2（旗舰核定位）。此外，Skymont 为 subnormal 浮点数增加了快速硬件路径——Crestmont 通过微码处理 subnormal 导致超过 280 cycle 的惩罚，Skymont 将其降至可忽略水平。

## 内存与地址转换

L1D 带宽增至 3×128-bit 读/cycle，L2 带宽从 Crestmont 的 64 B/cycle 翻倍至 128 B/cycle。L2 TLB 扩至 4K 条目，超过 Redwood Cove P-Core（2K）和 Zen 4（3K）。Skymont 还在 L2 复合体内处理核间缓存转发，不再依赖片外 fabric（ring bus 或 Scalable Fabric），减少了 Crestmont/Gracemont 中存在的跨核一致性额外延迟。

## 与 Crestmont 及 P-Core 的定位

Intel 声称 Skymont 性能/时钟已接近 Redwood Cove P-Core，标志着 E-Core 与 P-Core 性能差距大幅缩小。游戏负载的 top-down 分析（[[sources/chipsandcheese-skymont-gaming]]）证实 Skymont 以后端内存延迟为主要瓶颈，与同平台 Lion Cove P-Core 的 IPC 差距主要来自前端宽度与 cache hierarchy，而非调度器本身。这与 [[gracemont-microarchitecture|Gracemont]] 接近 Skylake 的历史进程一脉相承。尽管如此，Skymont 的绝对频率依然远低于 P-Core，Intel 的混合核策略仍然成立。AVX-512 缺席仍是 E-Core 系的持续痛点，迫使 Intel 在含 E-Core 的客户端平台上整体禁用 AVX-512。

## Sources

- [[sources/chipsandcheese-skymont]]
- [[sources/chipsandcheese-skymont-detailed]]
- [[sources/chipsandcheese-skymont-gaming]]
