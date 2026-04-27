---
tags: [cpu, amd, 缓存, 3d堆叠, vcache, tsv, 封装技术]
date: 2026-04-27
sources: 2
---

# 3D V-Cache：通过 Die 堆叠大幅扩充末级缓存

3D V-Cache 是 AMD 从 Zen 3（5800X3D，2022 年）开始引入的缓存堆叠技术，通过在 CPU die 上方直接键合一枚 SRAM die，将每个 L3 slice 的容量翻倍乃至三倍，而不改变核心架构本身。Zen 4 的 7950X3D 等 SKU 进一步沿用并完善了这一方案。

## 技术原理

传统片外 DRAM 缓存（如 Intel 的 EDRAM L4）受限于封装走线带宽，只能作为独立的第四级缓存，延迟高（>30 ns）、带宽低（~50 GB/s）。3D V-Cache 采用**TSV（Through-Silicon Via）** 键合，使堆叠 die 上的 SRAM 直接延伸成为每个 L3 slice 的额外容量，配备独立的 tag 和 LRU 阵列。L3 控制器在物理上只有一级缓存协议逻辑，跨 die 访问通过 TSV 完成，成本远低于 on-package 走线。

这种设计的核心结果是：
- **延迟惩罚极小**：Zen 4 上额外约 4 cycle / 1.6 ns，相比 EDRAM 的 30+ ns 几乎可忽略
- **带宽保持一致**：on-CCD 的 ring bus 未改变，带宽差异仅来自时钟差异
- **容量大幅提升**：Zen 4 CCD 从 32 MB 跃升到 96 MB L3

## 性能特性与取舍

VCache 的唯一代价是**时钟频率受限**：堆叠 SRAM die 对高电压耐受性差，Zen 4 VCache CCD 最高 boost 约 5.2 GHz，低于普通 CCD 的 5.5 GHz+（约 7% 差距）。因此：

- 缓存 miss 率高的场景（部分游戏、文件压缩等）VCache 收益显著，可超出频率差补偿后仍有净提升
- 缓存 miss 率本就低的场景（如 DCS），频率劣势可能导致净亏

AMD 的 7950X3D 双 CCD 设计（一枚 VCache、一枚普通）提供了罕见的对照实验机会。L3 命中率典型提升范围在 16%（libx264）到 47%（COD Black Ops Cold War）之间，IPC 提升 5%–20%。

## 与历史方案对比

| 方案 | 延迟 | 带宽 | 定位 |
|------|------|------|------|
| Intel EDRAM L4（Haswell/Skylake） | >30 ns | ~50 GB/s | 独立 L4 |
| AMD VCache（Zen 3/4） | L3+约 1.6 ns | 与 L3 一致 | L3 延伸 |

EDRAM 因延迟过高只能作 L4，且带宽不足，实用价值有限。TSV 堆叠 SRAM 从根本上解决了这一问题。Intel 的 Meteor Lake 曾计划引入 L4 堆叠缓存，但依然以 L4 形式存在，预计延迟/带宽仍与 VCache 有差距。

## Sources

- [[sources/chipsandcheese-7950x3d-vcache]]
- [[sources/chipsandcheese-ibm-l3-v-cache-future]]
- [[sources/chipsandcheese-broadwell-edram]]
- [[sources/chipsandcheese-9800x3d-vcache]]
