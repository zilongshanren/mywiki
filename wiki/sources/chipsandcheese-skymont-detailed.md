---
tags: [source, cpu, intel, skymont, e-core, lunar-lake, microarchitecture]
date: 2026-04-27
sources: 1
---

# Skymont: Intel's E-Cores Reach for the Sky（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2024 年 10 月的详尽微架构测评，通过实测微基准对 Lunar Lake 中的 Skymont E-Core 进行深入剖析。

## 摘要

Skymont 以 TSMC N3B 工艺为基础，对 Crestmont 进行了全面大幅升级：8-wide OoO 核心，ROB 从 256 扩至 416 条目，三簇解码前端（9 uop/cycle），四管 FPU，7 个 AGU，L2 从 2 MB 翻倍至 4 MB 且带宽加倍。Chester 的测试揭示了 Skymont 架构改进与 Lunar Lake 缓存层次之间的微妙博弈：在计算密集、缓存友好的工作负载（如 Y-Cruncher）上 Skymont 大幅领先 Crestmont，但在 libx264 等内存密集型任务中却因缺乏等效的大 L3 而落后。文章还测量了分支预测器细节（48 entry 随机模式 vs Crestmont 16 entry）、L1 BTB（8K vs Crestmont 6K）、store 转发行为、TLB 层次（48 entry L1 DTLB，4096 entry L2 TLB）及 subnormal 浮点快速路径新特性。

## 关键要点

- Skymont ROB 416 条目，接近 Golden Cove 的 512 条目，远超 Crestmont 256 条目
- 4 管 FPU：延迟从 5 cycle 降至 4 cycle，FP 除法平均延迟从 5 降至 2.5 cycle
- L1 DTLB 仅 48 条目（仍较小），但 L2 TLB 扩至 4096 条目（超越 Lion Cove 的 2048）
- Subnormal 浮点新增硬件快速路径，消除原来 >100 cycle 惩罚；反观 Lion Cove P-Core 尚未跟进
- Lunar Lake 的 8 MB memory side cache 延迟约 59.5 ns，接近旧 DDR 主内存，对 CPU 帮助有限
- 对比低功耗 Crestmont 性能提升 78-84%，但对比 Meteor Lake 标准 Crestmont 几乎持平（仅 ~0.7% INT SPEC 提升），核心架构提升被缓存劣势所抵消

## 链接到的概念

- [[computer-systems/skymont-microarchitecture]]
- [[computer-systems/crestmont-microarchitecture]]
- [[computer-systems/golden-cove-microarchitecture]]
- [[computer-systems/gracemont-microarchitecture]]
- [[computer-systems/lion-cove-microarchitecture]]
- [[computer-systems/cache-size-vs-latency-tradeoff]]
- [[computer-systems/branch-predictor-design]]

## 原文

- 链接：https://chipsandcheese.com/p/skymont-intels-e-cores-reach-for-the-sky
- 本地：`raw/articles/chipsandcheese.com/2024-10-03_skymont-intels-e-cores-reach-for-the-sky.md`
