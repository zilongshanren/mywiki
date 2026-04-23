---
tags: [source, cpu, intel, alder-lake, hybrid, ring-bus]
date: 2026-04-19
sources: 1
---

# Alder Lake – E-Cores, Ring Clock, and Hybrid Teething Troubles（Chester Lam / Chips and Cheese，2021-12-16）

[[chester-lam]] 发在 Alder Lake 推出约两个月后的短文，披露 Alder Lake hybrid 设计里一个硬件侧的首代毛病。

## 摘要

Alder Lake 的 ring bus 在 P-Core 独享时跑 4.7 GHz。**只要有一个 Gracemont E-Core 被调度，ring 立刻降到 3.6 GHz**——哪怕那个 E-Core 只跑 NOP loop 只读 L1i、根本不碰 L3。测到的影响：L3 延迟 +11.7%（+1.78 ns、+9–10 周期），L3 带宽 −20%；内存延迟 +3.4 ns（+3.7%），内存带宽几乎无影响。实际 P-Core 压缩性能 −2.9%、编码 −5.8%——用秒表能测到，体感无感。但这揭示了 Intel 首代 x86 桌面 hybrid 的一类硬件层面 teething troubles：ring clock gating 策略不够细，未能在 E-Core 只做轻活时保持高 ring 频率。Chester 期待 Raptor Lake 在这方面有改进（泄漏路线图里确实提到）。

## 关键要点

- Ring clock 因任一 E-Core 激活即从 4.7 → 3.6 GHz
- 对 P-Core L3 的代价：+11.7% 延迟、−20% 带宽、+9–10 周期
- 真实 benchmark 损失 3–6%，Gracemont 贡献的额外吞吐远补偿这点损失
- 与 Windows 11 Thread Director 软件侧 teething 并列，是首代 hybrid 的硬件侧教训
- 这是 [[golden-cove-microarchitecture|Golden Cove]] 大 ROB 的隐藏用途之一：吸收 hybrid tax 引入的额外 L3 延迟

## 链接到的概念

- [[intel-hybrid-alder-lake]]
- [[golden-cove-microarchitecture]]
- [[gracemont-microarchitecture]]
- [[littles-law-reorder-buffer]]

## 原文

- 链接：<https://chipsandcheese.com/p/alder-lake-e-cores-ring-clock-and-hybrid-teething-troubles>
- 本地：`raw/articles/chipsandcheese.com/2021-12-16_alder-lake-e-cores-ring-clock-and-hybrid-teething-troubles.md`
