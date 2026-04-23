---
tags: [source, cpu, intel, tremont, atom, 微架构, jasper-lake]
date: 2026-04-19
sources: 1
---

# Intel's Tremont: Atom Changes Course（Chester Lam / Chips and Cheese，2022-01-02）

[[chester-lam]] 把 Alder Lake 下 Gracemont 的前辈 Tremont 拉出来与 Skylake、Gracemont 一起横测，为 Gracemont 的设计抉择做溯源。

## 摘要

Tremont（Jasper Lake 的 Celeron N5095）引入几乎所有被 Gracemont 放大复用的招数：[[clustered-decode-atom|双 3-wide 解码簇]]、[[non-scheduling-queue|NSQ]]、"Core class branch prediction"（4096 BTB、zero-bubble 512 条）。ROB 接近 Haswell/Skylake，因为没 AVX、没 SMT 把寄存器配额都让给了 rename capacity。短板是**整数调度器只有 45 项（可用 31 项）**，严重小于 Zen 2 / Skylake；libx264 backend stall 主因是调度器填满而非 ROB。**没有 AVX** 是致命伤：Lakefield 就因此在 P/E 迁移上受限，Gracemont 补齐 AVX 才让 hybrid 可行。Store forwarding 只接受按 load 大小对齐的子集，其它情况 12–13 周期，比 Skylake 的"load 完全包含"规则弱得多（Neoverse N1 做类似保守转发但能跨 cache line）。L2 只 1.5 MB、每核 16 B/cycle，L3 带宽低于移动 SoC SLC，是所有 Atom 线里最弱环节——Gracemont 把 L2 口加倍正是针对此。功耗极低：4 核全开 2 W/core、非核 2–3 W；**半速但 1/4 功耗**，perf/W 优于 Skylake 但绝对性能仍落后一代。Tremont 的意义是 Intel 把 Atom 从手机撤出、押"hybrid + 边缘/云"的转型起点。

## 关键要点

- Clustered decode 首发，Gracemont 改为自动切换解决退化
- NSQ 首发，Gracemont 放大到 91 条 FP 容量
- BTB 4096 + zero-bubble 512，方向预测接近 Skylake
- 没 AVX + 小整数调度器 + 差 L2/L3 = "Atom 式低功耗税"
- Store forwarding 按 load 大小对齐才成功，失败代价高
- 转型意味：Total Memory Encryption、cache QoS、accelerator interfacing 指令暗示云/边缘野心

## 链接到的概念

- [[tremont-microarchitecture]]
- [[clustered-decode-atom]]
- [[non-scheduling-queue]]
- [[move-elimination-zeroing-idioms]]
- [[gracemont-microarchitecture]]
- [[intel-hybrid-alder-lake]]
- [[branch-predictor-design]]
- [[cpu-scheduler-design]]
- [[neoverse-n1-microarchitecture]]

## 原文

- 链接：<https://chipsandcheese.com/p/intels-tremont-atom-changes-course>
- 本地：`raw/articles/chipsandcheese.com/2022-01-02_intels-tremont-atom-changes-course.md`
