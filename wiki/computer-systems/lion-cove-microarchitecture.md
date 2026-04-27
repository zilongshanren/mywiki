---
tags: [cpu, 微架构, intel, p-core, lion-cove, lunar-lake]
date: 2026-04-27
sources: 1
---

# Lion Cove 微架构

Lion Cove 是 Intel P-Core 在 Lunar Lake 中的新一代微架构，是 [[golden-cove-microarchitecture|Golden Cove]] 系列的后继者（Golden Cove → Redwood Cove → Lion Cove）。它延续了 P6 血统，但在调度器设计上做出了 P6 系历史上最大的结构性变化。

## 拆分调度器

Lion Cove 最核心的创新是将 Golden Cove 以来的统一数学调度器（Unified Math Scheduler，五端口）拆分为两个独立部分：一个 6 端口整数调度器和一个 4 端口向量调度器。拆分的设计理由有二。

第一，功耗效率：向量调度器可在无向量代码时独立进行时钟门控，降低功耗或将节省的功率预算转移至核心其他部分以支持更高频率。

第二，设计复杂度下降：原本五端口统一调度器每端口需处理三操作数指令（含 AVX 掩码），意味着 15 路读端口加掩码逻辑，扩展代价极高。拆分后，向量侧仅需 4 端口×3 操作数=12 路读；整数侧 6 端口×2 操作数=12 路读，且无需掩码，整体复杂度与前代相当，同时端口数量更多。

总调度器槽位约为 Golden Cove 的 2×。

## 新增缓存层级

Lion Cove 对缓存层次做了重构，引入了三级私有缓存：

- **L0**（原 L1）：48 KB，延迟 4 cycle（恢复至 Skylake 水准，Redwood Cove 为 5 cycle）
- **L1**（新增）：192 KB，延迟 9 cycle，作为 L0 与 L2 之间的缓冲
- **L2**：3 MB（前代 2 MB），延迟 17 cycle（仅比 Redwood Cove 多 1 cycle）

Lunar Lake 工程权衡：L1 到 L2 的实际带宽被限制为 64 B/cycle（理论上限约 110 B/cycle），以节省功耗和面积。

## 其他升级

- 核心宽度从 Redwood Cove 的 6-wide 扩至 8-wide
- ROB 从 512 增至 576 条目
- 整数 ALU 6 个；整数乘法器首次增至 3 个（x86 P-Core 历史首次支持 >1/cycle 整数乘）
- 向量 SIMD ALU 从 3 增至 4 个，新增第二个 FP 除法器
- 前端 fetch 带宽 48 B/cycle，uop cache 扩容
- L1 DTLB 增至 128 条目；新增第三个可处理 store 地址的 AGU
- 整体 IPC 提升约 14%

## 超线程与产品定制化

Lunar Lake 版 Lion Cove 移除了超线程，不仅是软件禁用，而是在芯片上直接去掉了相关电路。这简化了 Thread Director 的调度（只需面对 P-Core 和 E-Core，无需处理 P-Core Thread）并减小了芯片面积。

Intel 引入"Sea of Cells"设计方法论，使单一架构可按产品需求定制是否包含超线程等功能。未来面向 Arrow Lake 或服务器的 Lion Cove 变体可重新引入超线程。

## 在 Intel P-Core 路线中的意义

Lion Cove 是 P6 系首次在调度器拓扑上做结构性重构，标志着 Intel P-Core 向更灵活、可定制化的设计哲学演进。与 [[golden-cove-microarchitecture|Golden Cove]] 时代在大核面积和功耗上的激进扩展相比，Lion Cove 的哲学是在保持竞争力的同时追求更优的 PPA（Performance/Power/Area）权衡。

## Sources

- [[sources/chipsandcheese-lion-cove]]
- [[sources/chipsandcheese-lion-cove-arrow-lake]]
- [[sources/chipsandcheese-lion-cove-gaming]]
