---
tags: [source, chipsandcheese, cpu, 微架构, arm, neoverse-n1, zen2, 缓存]
date: 2026-04-19
sources: 1
---

# Deep Diving Neoverse N1（Chester Lam / Chips and Cheese）

[[chester-lam]] 2021 年 10 月发表于 [[chips-and-cheese]] 的 Neoverse N1 深度续篇。承接之前 [[sources/chipsandcheese-neoverse-n1-vs-zen2|Neoverse N1 vs Zen 2]] 一文，把 Ampere Altra 与 3950X 从 workload 比较扩到**微架构结构尺寸 + 宏观 benchmark 重测**，并纠正了前一篇中 WSL1 vs Linux VM 引入的偏差。

## 摘要

**缓存 / 带宽**：单线程下 Altra 的 L2 给出 19.28 字节/周期（略高于 16，暗示 L2 接口 32 字节宽），Zen 2 L3 带宽就已超过 Altra L2；Altra L3 延迟超过 Zen 2 两倍。作者据此判断 AMD 不该往 IOD 里塞 L4/system cache——高延迟小容量的非核缓存没用。多核扩展上 Altra 80 核的总带宽优势明显，但仍要真的用满 80 核。**TLB / pagewalk**：Zen 2 L1 DTLB 64 项对 N1 48 项，L2 TLB 2048 对 1280；N1 L2 TLB 延迟更低（5 vs 7 cycle）但整体命中率不如 Zen 2。**分支预测 2D**：Zen 2 的 TAGE 第二级 override 第一级会产生递增气泡（对应"L2 BTB Overrides"PMU 事件）；N1 indirect 预测反而更大（可 track 4096 indirect targets），但在 direct + indirect 混合测试中容量降得快。**Return stack**：N1 是两级（11 + 31 项），第二级比 Zhaoxin 慢得多的栈友好得多；Zen 2 单级 31 项但更快。**Rename 优化**：Zen 2 可零延迟消除任意 reg-to-reg MOV，N1 只折叠依赖但不消除，且仅识别"mov imm 0"这一种零习语。**Load/Store queue**：N1 测量 44 store / 56 load（不是 Wikichip 数字）；Zen 2 load queue 44 项（等数据）/ 116 项（等 retire）——口径不同。**宏观 benchmark**（Linux VM 重测）：Gem5 编译 N1 同频落后 Zen 2 40.3%（WSL 前一篇数字是"同频略胜"，修正后差距扩大）；7z、OpenSSL、Blender、libx264/x265 全面 Zen 2 领先；仅 ChampSim 场景 N1 凭 99.7% L1i 命中率与 98.86% 分支预测反杀。PMU 分析：N1 的 rename 阶段大量时间 backend-bound，是后端容量不足而非前端瓶颈——这解释为什么 ARM 在 A77/A78 加宽 OOO 后端。

## 关键要点

- Altra L3 带宽不如 Zen 2 L3，延迟是其两倍 —— IOD L4 不划算
- N1 indirect BTB 容量比 Zen 2 大（4096 vs 1024）但 direct+indirect 混合塌陷
- N1 L1 return stack 11 项 + L2 31 项是两级设计
- Zen 2 MOV 零延迟消除 vs N1 只折叠依赖
- N1 L/S 队列实测：44 store / 56 load
- 修正 WSL1 偏差后，Gem5 编译 N1 同频落后 Zen 2 40%（而非持平）
- ChampSim 场景 N1 反杀：99.7% L1i 命中 + 2.65 MPKI 分支
- N1 瓶颈是 backend-bound，对应 A77/A78 加宽 OOO 后端的路线

## 链接到的概念

- [[neoverse-n1-microarchitecture]]
- [[branch-predictor-design]]
- [[zen2-microarchitecture]]
- [[isa-implementation-not-architecture]]
- [[cache-size-vs-latency-tradeoff]]

## 原文

- 链接：https://chipsandcheese.com/p/deep-diving-neoverse-n1
- 本地：`raw/articles/chipsandcheese.com/2021-10-22_deep-diving-neoverse-n1.md`
