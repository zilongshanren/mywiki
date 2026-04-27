---
tags: [cpu, 微架构, 分支预测, 前端, 流水线]
date: 2026-04-19
sources: 1
---

# 分支预测器设计

分支预测器是 CPU 前端流水线中最关键的结构之一。其职责是在分支指令执行完成之前猜测跳转目标，使流水线得以提前取指，避免等待。如果猜错，CPU 必须冲刷错误路径上已取的指令，并从正确路径重新取指——这一惩罚称为**误预测惩罚（mispredict penalty）**，通常为 12–20 个周期。

## 精度与 MPKI

衡量分支预测器性能最常用的指标有两个：

- **准确率**（Accuracy）：正确预测的分支占所有分支的比例。
- **MPKI**（Mispredicts per Kilo-Instructions）：每 1000 条指令中误预测次数，对指令密集度做了归一化，更能反映实际性能影响。

以 Cinebench R15 单线程为参考：[[zen2-microarchitecture|Zen 2]] 的 MPKI 为 5.15，Skylake 为 6.45，前者少出 25% 的误预测。结合约 16 周期的惩罚，Skylake 每千指令额外损失约 14 个周期。

## 对前端带宽的影响

每次误预测意味着 CPU 同时在正确路径和错误路径上取指，两条路径都消耗前端带宽。Skylake 的前端每条退休指令平均派发 1.63 个微操作，而 Zen 2 为 1.39——Skylake 多浪费约 17% 的前端带宽，这部分额外宽度几乎全部来自误预测冲刷。

更准确的分支预测也直接降低了对 op cache（DSB / Decoded Stream Buffer）的压力，因为错误路径的解码结果在冲刷后无法复用。

## op cache 与分支预测的交互

Skylake 的 op cache 容量为 1536 条目，Zen 2 为 4096 条目，但 CBR15 下 Skylake 的 op cache 命中率（69.1%）反高于 Zen 2（62.7%）。一个可能的原因是：Skylake 误预测时从 op cache 取了更多错误路径指令，人为推高了命中计数；另一个原因是 Skylake 的替换策略在循环容量边缘表现更平缓，而 Zen 2 在超出容量时命中率断崖式下跌。

这一反差提示：op cache 大小与 op cache 命中率并不简单正相关，替换策略对实际命中率的影响不可忽视。

## 参见
- [[zen2-microarchitecture]]
- [[cpu-scheduler-design]]
- [[cpu-performance-formula]]
- [[op-cache-decoded-uop-cache]]
- [[neoverse-n1-microarchitecture]] — N1 走速度优先、精度次之的反向权衡
- [[dispatch-stall-breakdown]] — Zen 3 上误预测在后端的真实代价
- [[via-x86-isaiah-lujiazui]] — Isaiah 2008 年就用 tournament + 4096 BTB，代价是 3-cycle/taken 气泡
- [[cache-size-vs-latency-tradeoff]] — 缓存大小对前端再好也抵不过 miss 率基线差异
- [[golden-cove-microarchitecture]] — 12K 条目 BTB 三级结构，但 zero-bubble 能力回退
- [[gracemont-microarchitecture]] — 5K BTB、1024 zero-bubble，Core class 接近 Golden Cove

## Sources
- [[sources/chipsandcheese-zen2-cinebench-analysis]]
- [[sources/chipsandcheese-zen3-bottlenecks]]
- [[sources/chipsandcheese-neoverse-n1-vs-zen2]]
- [[sources/chipsandcheese-via-isaiah]]
- [[sources/chipsandcheese-zhaoxin-lujiazui]]
- [[sources/chipsandcheese-neoverse-n1-deep-dive]]
- [[sources/chipsandcheese-golden-cove]]
- [[sources/chipsandcheese-gracemont]]
- [[sources/chipsandcheese-tremont]]
- [[sources/chipsandcheese-graviton3-first-impressions]]
- [[sources/chipsandcheese-sunny-cove-intel-lost-gen]]
- [[sources/chipsandcheese-intel-netburst-failure]]
- [[sources/chipsandcheese-tachyum-claims]]
