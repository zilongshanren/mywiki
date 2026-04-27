---
tags: [cpu, intel, raptor-lake, cache, l2, alder-lake, e-core, p-core]
date: 2026-04-27
sources: 1
---

# Raptor Lake 的 L2 缓存改进

Raptor Lake（Intel 第 13 代酷睿，2022 年）在 [[intel-hybrid-alder-lake|Alder Lake]] 架构基础上做了缓存层次的针对性强化，其中最显著的变化是 P-Core 和 E-Core 的 L2 容量大幅提升。Chester Lam 在量产前的工程样品上对这一变化进行了测量验证。

## P-Core L2：1.25 MB → 2 MB

[[golden-cove-microarchitecture|Golden Cove]] P-Core 的 L2 从 Alder Lake 的 1.25 MB 增加到 2 MB，延迟仅增加 1 个周期。考虑到 Golden Cove 拥有深度乱序执行缓冲区（512 项 ROB），1 个周期的延迟增量基本可以被吸收。这是 Intel 在 P-Core L2 上持续迭代的结果：相比 Comet Lake 时代的 256 KB L2，Raptor Lake 的 2 MB 是巨大的跨越。

## E-Core L2：2 MB → 4 MB（集群共享）

[[gracemont-microarchitecture|Gracemont]] E-Core 的 L2 容量从 2 MB 加倍到 4 MB，且延迟维持不变（20 周期）。对 E-Core 而言，这一改进的意义甚至超过 P-Core。原因在于：

- Gracemont 的乱序执行缓冲区更浅，对高延迟 L3 的容忍度更低
- Alder Lake 的 E-Core 访问 L3 需要超过 60 个周期，Raptor Lake 略有改善（约 16.64 ns）但仍高
- 更大的 L2 意味着大量访问可在 L2 命中，大幅减少跨环形总线的 L3 流量

4 MB 的 E-Core L2 容量已与移动端 Zen 2 芯片的整个 L3 容量持平。

## 量化分析：IPC vs 功耗

Chester Lam 用 ChampSim 模拟器评估了 L2 扩容的影响：

- P-Core L2 miss 率下降 14.55%，E-Core 下降 16.05%
- 固定频率下的 IPC 提升不足 1%（模拟器可能低估实际收益）
- 但功耗收益显著：更少的 L3 流量减少了环形总线的数据搬运能耗；节省的功耗预算可转化为更高的频率余量

高性能 CPU 经常处于功耗受限状态——在功耗上限不变的前提下，更高的缓存命中率等价于可用于提频的功耗预算。此外，Intel 的环形总线在高频下往往跟不上核心频率，更高的 L2 命中率可以减轻这一瓶颈。

## 历史背景

E-Core 的 L2 角色随 Intel Atom 演化而变化：在 Goldmont Plus 时代，L2 是最后一级缓存（类似主流 Intel 芯片的 L3）；加入混合架构后，E-Core 并入环形总线，L2 不再是末级缓存，容量因此可以缩小。Raptor Lake 将 E-Core L2 重新扩大，是对 Alder Lake 设计中 E-Core 过度依赖高延迟 L3 这一缺陷的直接响应。

## Sources

- [[sources/chipsandcheese-raptor-lake-l2]]
