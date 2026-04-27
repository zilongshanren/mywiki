---
tags: [source, cpu, arm, cortex-a710, mobile, microarchitecture]
date: 2026-04-27
sources: 1
---

# ARM's Cortex A710: Winning by Default（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2023 年 8 月的文章，测试运行在 Snapdragon 8+ Gen 1（Asus Zenfone 9）上的 Cortex-A710，系统分析其相比 A77/A78 的演进与权衡，以及与 Sandy Bridge 等经典桌面核的对比。

## 摘要

Cortex A710 是 ARM 在 A78 基础上的效率优先迭代，削减了一部分前端宽度（6→5-wide rename，6→5-wide op cache 出口）以换取更好的每瓦性能，但大幅扩充了乱序缓冲区容量（接近 A76 的两倍 ROB）和 scheduler 规模（integer cluster scheduler 超过 Zen 2）。其 micro-op cache 与 Sandy Bridge 的设计高度相似（均为 1536 entry 虚地址索引），L2 代码预取能力强于老一代 ARM 核。DSU-110 互联采用双环形总线，行为类似 Sandy Bridge 的环形总线：延迟因 cacheline 所在 L3 切片距离不同而变化。主要短板包括：较小 DTLB（32 entry L1）、1024 entry L2 TLB（远落后于 Zen 4 的 3072 entry）、store forwarding 仅支持上下半 store 转发、以及 LPDDR 导致的高内存延迟。

## 关键要点

- 5-wide 乱序核，10 级流水线，效率优先于极致性能
- 1536 entry 虚地址 micro-op cache，与 Sandy Bridge 方案一致；5 µop/cycle 出口（A77/A78 为 6）
- 大型分布式 scheduler：integer cluster scheduler 容量超过 Zen 2
- 2048 entry L1 BTB（有效约 512–1024），10K entry L2 BTB，64 target 间接预测能力
- TLB 容量保守：32 entry L1 DTLB，1024 entry L2 TLB；Zen 4 为 72 + 3072 entry
- DSU-110 环形总线，行为类似 Sandy Bridge ring bus，L3 延迟 ~20-21 ns（6 MB Snapdragon 版）
- LPDDR 内存延迟极高，但 A710 的大 transaction queue（48–62 entry）可部分掩盖
- ARM 市场垄断带来了"不出错即胜利"的保守产品策略

## 链接到的概念

- [[computer-systems/cortex-a710-microarchitecture]]
- [[computer-systems/op-cache-decoded-uop-cache]]
- [[computer-systems/branch-predictor-design]]
- [[computer-systems/neoverse-n1-microarchitecture]]
- [[computer-systems/sandy-bridge-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/arms-cortex-a710-winning-by-default
- 本地：`raw/articles/chipsandcheese.com/2023-08-11_arms-cortex-a710-winning-by-default.md`
