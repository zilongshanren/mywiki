---
tags: [cpu, 微架构, intel, alder-lake, golden-cove, p-core, x86]
date: 2026-04-19
sources: 2
---

# Golden Cove：Alder Lake 的 P-Core

Golden Cove 是 Intel 2021 年随 Alder Lake 发布的「性能核」，是自 Skylake 以来第一个在桌面端对 AMD 具备竞争力的 P-Core 设计。Chester Lam 的拆解把它定位成 Sunny Cove 的大幅加宽：**流水线更宽、reorder window 更深**，但也背着几个被 AMD 压着打的弱点。

## 前端：更大的 uop cache 与更强的 BTB

L1 指令缓存向 decoder 的带宽翻倍到 32 B/cycle，解码器从 4-wide 扩到 6-wide。uop cache 从 2.25K 扩到 **4K 条目**，uop 端带宽 8/cycle 追平 Zen。最引人注目的是 **12K 条目的 BTB**——分三级，miss 一级进下一级仅 1 周期惩罚（AMD L2 BTB miss 要 3 周期）。uop queue 还能像微缩 trace cache 一样对小循环 unroll，小循环里 taken 分支可做到 2/cycle。但代价是"zero bubble"可追踪分支数退回 128 条（Haswell 水准，Sunny Cove 的回退），为的是在 5 GHz+ 把大 BTB 实现出来。[[branch-predictor-design|方向预测]]抓长 pattern 能力明显强于 Skylake，但仍略逊 Zen 3。

## 后端：ROB +45%，但整数寄存器堆没跟上

重排序缓冲扩到 **512 项**（Sunny Cove 352），FP 寄存器堆、load/store queue、superqueue 都同比例放大。Golden Cove 配 **五个 ALU 端口**（x86 史上最多）、**3 个 load AGU + 2 个 store AGU**、FP 三端口。FP add 延迟压到 **2 周期**@5 GHz+（仅 VIA Nano 做过但时钟低），vector register file 推测有 8 read + 3 write 口。

但 **integer register file 居然没扩**——实测甚至略小于 Sunny Cove。Chester 的推断是：为喂五条 ALU、要 10 个读口再加 AGU 的 5 个，再扩寄存器堆代价太高。结果在纯整数负载里，ROB 还没填满整数寄存器就先耗尽，512 项 ROB 的头条数字用不出来。对 FP/vector 则无碍，因为整数结果占比低得多。

## 内存子系统：带宽怪兽、延迟高

L1D 每周期 3 条 256-bit 向量 load（Zen 3 是 3 load 但只 2 个能向量）、L2 每周期 64 B（AMD 32 B）、L1D 可做 2×512-bit load/cycle（AVX-512）。L3 AMD 仍领先，但差距被 Intel 的 DDR5 控制器抹平（96.6 GB/s vs Zen 3 DDR4 的 ~50 GB/s）。代价是**所有层级的延迟都高于 Zen 3**。靠应用 [[littles-law-reorder-buffer|Little's Law]]：ROB 大到足以吸收这个延迟差，正是 Intel 给 Golden Cove 塞大 ROB 的本质动机。

## 渲染式的权衡结论

Golden Cove 的整数性能被 Chester 评为"没把管线喂饱就堆 ALU"——他猜是因为这颗核要同时进 Alder Lake 和 Sapphire Rapids 服务器平台，整数侧做了妥协。FP/vector 侧则堪称 Intel 近年最好的设计：五个 ALU 端口有三个面向 FP/vector，vector 寄存器堆大到吓人，1.25 MB L2 让 cache blocking 更好做。[[intel-hybrid-alder-lake|Alder Lake 的 hybrid]] 布局配上 [[gracemont-microarchitecture|Gracemont]] E-Core 才是完整故事。

## 参见

- [[cache-size-vs-latency-tradeoff]] — ChampSim 仿真对 L1D/L2/L3 参数变体的系统分析
- [[branch-predictor-design]]
- [[op-cache-decoded-uop-cache]]
- [[move-elimination-zeroing-idioms]]
- [[littles-law-reorder-buffer]]
- [[gracemont-microarchitecture]]
- [[intel-hybrid-alder-lake]]
- [[zen2-microarchitecture]]
- [[neoverse-n1-microarchitecture]]
- [[via-x86-isaiah-lujiazui]] — Nano 也做过 2 周期 FP add，但频率远低

## Sources

- [[sources/chipsandcheese-golden-cove]]
- [[sources/chipsandcheese-golden-cove-cache-analysis]]
- [[sources/chipsandcheese-graviton3-first-impressions]]
- [[sources/chipsandcheese-alder-lake-caching-power]]
- [[sources/chipsandcheese-raptor-lake-l2]]
- [[sources/chipsandcheese-skylake-architecture]]
- [[sources/chipsandcheese-zen4-part1]]
- [[sources/chipsandcheese-zen4-part2]]
