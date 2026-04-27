---
tags: [cpu, 微架构, intel, alder-lake, gracemont, e-core, atom, x86]
date: 2026-04-19
sources: 1
---

# Gracemont：Atom 的复仇

Gracemont 是 Alder Lake 的 E-Core。别被 "Efficient" 这个标签骗了：它是 5-wide 乱序、reorder window 深、频率接近 4 GHz 的高性能核，只是刻意牺牲向量吞吐与 L3 带宽换面积/功耗。它的血脉上溯 2013 年 Silvermont，但已经长成了与 Cortex-A78 同级的"中核"，绝不是 A55 式的省电背景核。

## 前端：5K 条 BTB + 双解码簇

方向预测器与 [[golden-cove-microarchitecture|Golden Cove]] 几乎一样强，只是 pattern length 超 1K 后有轻微斜率上升（用了 overriding predictor）。BTB 5K 项，zero-bubble 可追 1024 条分支（对齐 Zen 3），L2 BTB 额外 2 周期（AMD 要 3 周期）——降频节省的实现预算用来减 pipeline stage。

Gracemont 不用 uop cache，而是延续 Tremont 开创的 [[clustered-decode-atom|双解码簇]] 方案：两个 3-wide 解码器被分支预测器做分流，对程序而言等效于 6-wide 32 B/cycle 前端。Gracemont 相对 Tremont 的改进是**自动切换**集群（Tremont 只在 taken 分支处切），让长展开循环不再卡在单 cluster。L1i 扩到 **64 KB**（Tremont 32 KB、大核通常 32 KB）——没有 uop cache 的代价就是必须靠大 L1i 保持命中。

## 后端：非调度队列撑起容量

ROB、branch order buffer 都接近 Zen 2/3，但向量寄存器堆只做成 **128-bit 宽**，256-bit AVX 指令拆两条 uop。结果 207 项向量寄存器堆只占 3.3 KB（Golden Cove ≥10 KB、Zen 2/3 5 KB）。在 libx264 里 AVX2 场景平均 47 vector reg/100 inst，Gracemont 够用；Y-Cruncher 那种 >70% 256-bit write 才会撑爆。

整数端配 4 个 ALU，但 [[cpu-scheduler-design|调度器]]是**分布式**的（P6 line 全用统一调度器；Atom 不同）。FP 用 **半统一**：一个三口队列做数学、另一个双口做向量 store。FP 侧塞了大 [[non-scheduling-queue|非调度队列]]——backend 可塞 91 条 FP/vec 未发射 uop 而不 stall rename，这招是跟 AMD 学的。

[[move-elimination-zeroing-idioms|rename 技巧]]接近 Zen 2 水平，比老 Atom 大幅进步，但落后 Golden Cove（后者几乎什么都消得掉）。Gracemont 认得 zeroing idiom 但仍占 ALU 口（Golden Cove 不占）。

## 内存：Atom 式二级缓存 + 桌面 L3

L1D 3 周期（Golden Cove 5 周期，绝对时间还更快）、L2 17 周期 **2 MB 四核共享**——保留 Atom 的共享 L2 思路（代码和常量数据不必跨 L2 复制，省面积）。L3 借的是 Alder Lake 的 ring，所以 Gracemont 通过 ring stop 接上。问题是：**启动任何一个 Gracemont 核，ring clock 从 4.7 GHz 掉到 3.6 GHz**——见 [[intel-hybrid-alder-lake]]。

单核 L3 带宽明显拉胯（Golden Cove 单核 ~100 GB/s，Gracemont 远低于此），L2 接口四核共享 64 B/cycle，按核摊薄到 ~16 B/cycle/core。prefetcher 似乎调得保守以省电。

## 功耗：单核贵，多核省

RAPL 实测 libx264 全八核负载：Gracemont 每核 5.72 W，Golden Cove 每核 21.05 W；IPC 分别 1.72 / 2.25。Gracemont 单核启动时功耗异常高（~5 W），说明 L2/ring stop 这些共享组件吃电，需要多核分摊才能摊平效率。八核全开下 Gracemont 的 perf/W 明显优于 Golden Cove，这才是 Intel 做 hybrid 的根本经济账。

## 战略位置

Chester 的比喻精准：Intel 像 300 AD 的罗马帝国——仍然强，但要同时防 AMD（桌面/服务器）和 ARM（密度/能效）。Gracemont 不只是"桌面背景核"，它是 Intel 进入 hyperscale server（对标 AMD Bergamo、Neoverse N1）的门票。

## 参见

- [[clustered-decode-atom]]
- [[non-scheduling-queue]]
- [[move-elimination-zeroing-idioms]]
- [[littles-law-reorder-buffer]]
- [[golden-cove-microarchitecture]]
- [[intel-hybrid-alder-lake]]
- [[tremont-microarchitecture]]
- [[zen2-microarchitecture]]
- [[neoverse-n1-microarchitecture]]
- [[branch-predictor-design]]

## Sources

- [[sources/chipsandcheese-gracemont]]
- [[sources/chipsandcheese-alder-lake-caching-power]]
