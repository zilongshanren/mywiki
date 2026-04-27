---
tags: [cpu, amd, epyc, turin, zen5, server, memory-bandwidth, gmi, numa]
date: 2026-04-27
sources: 1
---

# Zen 5 EPYC 服务器平台（Turin）

Turin 是 AMD 第五代 EPYC 处理器，基于 [[zen5-microarchitecture|Zen 5]] 核心，于 2024 年 10 月发布。相比桌面端 Zen 5，Turin 在内存互联和插槽配置上有显著差异，是数据中心高核密度与高频率并行路线的集大成者。

## 内存互联：GMI3-W

Turin 引入 **GMI3-W**（Coherent Interconnect，Wide 变体），与桌面/移动 Zen 5 的关键区别在于：

- **双 GMI 链路**：每个 CCD 通过两条 GMI 连接到 IO Die（桌面 Zen 5 / Genoa 仅单链路）
- **写链路加宽**：32 B/link（桌面版仅 16 B/link）

这使得单 CCD 可获得的内存带宽约为桌面版的两倍，全插槽（8 CCD）理论峰值读带宽约 576 GB/s，实测可达约 99%（~570 GB/s）。相比之下，[Bergamo](https://chipsandcheese.com/p/testing-amds-bergamo-zen-4c-spam) 等 Zen 4c EPYC 使用相同 3 条 socket-to-socket GMI 链路，延迟行为相似。

## 时钟与核心配置

EPYC 9575F 为 64 核/128 线程，属于低核数高频率 F-SKU：

- 单线程最高可达 **5 GHz**（all-core CCD 级别也可维持 5 GHz）
- 全 128 线程跑 Cinebench 2024 时稳定在约 4.3 GHz
- 轻载（如 TLS 业务）全核约 4.9 GHz

这是历史上首批服务器 CPU 实现全核 5 GHz，标志着 Zen 5 频率墙的突破，也使 Turin 成为对延迟敏感的传统企业应用（数据库、交易系统）的有力竞争者。

## 内存延迟

Turin 的内存延迟特性：

| 层级 | 延迟 |
|------|------|
| Intra-CCD（同 CCD 核间） | ~45 ns |
| Inter-CCD（跨 CCD） | ~150 ns |
| Socket-to-Socket | ~260 ns |

较 Genoa 略有增加，尤其是 intra-CCD 延迟。加载下测试（7 核带宽压力 + 1 核延迟探针）显示 CCD 满载时延迟增加约 39 ns，全 socket 满载时增加约 31 ns，行为稳定。

## 市场定位

Turin 覆盖了 EPYC 生态的两端：
- **高核数 SKU**（9755、9965 等）：面向超大规模数据中心，依赖 Zen 5c 密度优化核心
- **低核数高频 F-SKU**（9575F 等）：面向传统企业，低延迟、高单线程性能

总体上 Turin 是稳步演进（类比 Milan→Genoa）：核心架构升级（Zen 4→Zen 5）+ 内存带宽增加（GMI3-W）+ 核数扩展，而非代际飞跃。

## 与其他平台对比

[[computer-systems/neoverse-n2-microarchitecture|Arm Neoverse]] 平台在 AmpereOne 等实现中以密度和能效见长，Turin 的优势在于向后兼容 x86 生态和高单线程性能。Intel Granite Rapids（Xeon 6）则在 AVX-512 密集工作负载上有对应竞争力。

## Sources

- [[sources/chipsandcheese-turin-epyc]]
