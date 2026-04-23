---
tags: [source, cpu, zhaoxin, via, 微架构, benchmark]
date: 2026-04-19
sources: 1
---

# Zhaoxin Part 3: A Sort of Anti-Climax（George Cozma / Chips and Cheese，2021-11）

[[george-cozma]] 发表于 2021 年 11 月的 [[chips-and-cheese]] 三部曲收官篇。前两篇拆了 VIA Isaiah 与 Zhaoxin Lujiazui 的微架构内部，这一篇落到 benchmark 层面，给出 Lujiazui 对比同代架构的真实位置。

## 摘要

文章用 Cinebench R11.5/R20、Geekbench 5 做 clock-normalized 对比：Lujiazui 相对 Isaiah 有 25–30% 的 IPC 提升（对应 Zhaoxin 官方 25% 的 claim），但仍输给 2006 年的 Intel Merom（Core 2）。R20 里对 AVX 加速的支持使 Lujiazui 相对 Isaiah 翻倍，AES 子测试因硬件加密加速一骑绝尘，但整数子测试面对 15 年前的老架构仍全面败退，仅 Navigation 子测试能扳回一局。2021 年 11 月 Centaur 被 Intel 收购的新闻让 Zhaoxin 的未来路线图突然充满不确定性——作者推测：若 Centaur 在被收购前把 CNS 架构 IP 交给 Zhaoxin，Lujiazui 的下一代有望达到 Sandy Bridge 级 IPC（仍比当下 Intel/AMD 落后一代）；若没交，Zhaoxin 只能按 Jaguar 对 Bobcat 的 +50% 套路继续死磕 Lujiazui。

## 关键要点

- Clock-normalized 后 Lujiazui 对 Isaiah 约 +25% IPC，对应官方 claim
- R20/Geekbench 5 整数仍输 Merom，仅 AES（硬件加密）与少数子测试胜出
- 双通道 DDR4 几乎没帮助：cores 用不上多出的带宽，暴露 L2 瓶颈或 prefetcher 不够进取
- Centaur 被 Intel 收购给 Zhaoxin 未来路线带来重大不确定性
- 建议 Zhaoxin 参照 Jaguar→Bobcat 的 +50% 改进套路：扩大结构、改 BTB、降数学延迟、FPU 宽度 128→256 bit

## 链接到的概念

- [[via-x86-isaiah-lujiazui]]
- [[branch-predictor-design]]

## 原文

- 链接：<https://chipsandcheese.com/p/zhaoxin-part-3-a-sort-of-anti-climax>
- 本地：`raw/articles/chipsandcheese.com/2021-11-16_zhaoxin-part-3-a-sort-of-anti-climax.md`
