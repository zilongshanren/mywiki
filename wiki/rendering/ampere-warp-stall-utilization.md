---
tags: [gpu, nvidia, ampere, warp, occupancy, nsight, 延迟]
date: 2026-04-19
sources: 1
---

# Ampere warp stall 与 shader 利用率

GPU 规格表上的 TFLOPS 和带宽数字只是"理论上限"。实际利用率靠的是 SM 上挂着的 warp 数量是否足够——不够就 stall，stall 的根源里最普遍的一条叫 Long Scoreboard，即 warp 在等 cache/VRAM 的数据回来。Chester Lam 用 Nvidia Nsight 跑 Unigine Superposition 8K Optimized，对 Ampere（RTX 3090）和 Pascal（GTX 1080）做了一轮 warp stall 实测，结果颠覆了"堆核心数 = 堆性能"的直觉。

## Speed of Light 框架

Nvidia 的 SOL（Speed of Light）= 某单元实际吞吐 / 理论吞吐。官方指引：top SOL 若 < 60%，整机就没吃满。实测两张卡：

- RTX 3090：VRAM SOL ~30–40%，SM 活跃 79.97%，SM throughput 30.7%
- GTX 1080：VRAM SOL 接近 60%，SM 活跃 85.32%，shader 利用率明显更高

Top stall reason 两张卡都是 Long Scoreboard。再配 `sm__issue_active_per_active_cycle_sol_pct` 判定——Ampere 约 38.3%，Pascal 52%，都远低于 Nvidia 官方的 80% 阈值。结论：即使 8K 工作集对 RTX 3090 也仍然 memory latency bound（参见 [[gpu-memory-hierarchy-latency]]）。

## Pascal 反超 Ampere 的原因

Pascal 每 SM 可追踪 64 warp（64 路 SMT），Ampere 降到 48。在 CPU 类比里相当于 Ampere 的"核心"变宽变多但每核 SMT 线程数变少。当 warp 普遍卡在 long scoreboard 时，谁手上备用 warp 多谁就更可能找到 un-stalled 的来喂执行单元。Pascal 实测总体利用率 56.9%（66.7% occupancy × 85.32% SM active），Ampere 仅 50.1%（62.7% × 79.9%），尽管 Ampere 有 L1 miss 乱序返回、更大 instruction cache、更低执行延迟等微架构改进。

更刺眼的是负载均衡：RTX 3090 的 SM 活跃时间 min/max delta 是 5.61%，GTX 1080 只有 0.71%。Ampere 巨大的 shader array 出现了显著的"早完工者等末位"空转，这是大核心数本身带来的分发与均衡难题（参见 [[gcn-wave-occupancy]] 的类似讨论）。

## 架构含义

Ampere 把 Turing 独立的 integer pipe 合并回 FP/INT 共享 pipe，让每个 SM 的 FP 单元翻倍。理论上限涨了约 30% per SM，但喂饱它们的 warp 数没跟上——和 AMD Vega 当年的"大核心数 + 高功耗 + 低游戏利用率"问题同构。[[samsung-8n-vs-tsmc-n7]] 把这点列为 Ampere 能效问题的架构原因之一，与 GDDR6X 的 PAM4 功耗代价并列。

## 方法论价值

这套 SOL + top stall reason + `sm__issue_active_per_active_cycle_sol_pct` 的判定链路是 Nvidia 官方指导的再现，但作者把它放在"图形 workload 是否 memory latency bound"的宏观问题上验证——比单看 FPS 或 TDP 深入一层。它也为"[[gpu-latency-hiding]] 实际上成不成立"提供了量化抓手：你以为核心多到隐藏延迟，实测发现不是。

## Sources

- [[sources/chipsandcheese-gpu-memory-latency-impact]]
