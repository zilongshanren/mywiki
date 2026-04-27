---
tags: [source, cpu, 微架构, loongson, loongarch, 中国芯片]
date: 2026-04-27
sources: 1
---

# Loongson's 3A5000: China's Best Shot?（Chips and Cheese）

[[people/chester-lam|Chester Lam]] 与 George Cozma 于 2023 年 4 月发表的深度微架构评测，通过大量 microbenchmark 汇编测试，全面考察龙芯 3A5000（LA464 核心）的前端、执行单元、内存子系统。

## 摘要

文章从龙芯的历史脉络（863 计划、ICT、GS464 系列）切入，对 LA464 核心进行全面微架构剖析并与 Zen 1、Neoverse N1、Skylake 等横向对比。结论是：3A5000 是中国目前最强自研 CPU，在分支预测、BTB 大小、OoO 窗口、内存控制器等多个维度均与西方对手存在数代差距；时钟频率仅 2.5 GHz 是最大短板；DDR4 内存控制器性能极为低下（144 ns 延迟，仅 14 GB/s 带宽）。软件生态方面，LoongArch 的"旧世界 / 新世界"ABI 分裂问题进一步削弱实用性。

## 关键要点

- LA464 为 4-wide 乱序核，128 entry ROB，与 GS464E 结构相近，但调度队列有所扩大
- 分支预测器疑似 tournament 风格，与 Bulldozer 同代水平，远落后于 TAGE/感知器
- BTB 仅 64 entry，超出后跳转延迟约等于 L1i 延迟（3 cycle）
- 整数乘法吞吐优秀（2 乘/周期），但 4 cycle 延迟与十余年前 x86 持平
- L1D 4 cycle 延迟 + LoongArch 缺少 scaled-index 寻址，实测数组访问延迟高达 8 cycle
- L2 256 KB，victim cache，14 cycle 延迟，慢于同代 Intel/AMD
- DDR4 内存控制器是最大弱点：单核 7 GB/s，4 核合计不足 14 GB/s（相当于 DDR3-1066 水准）
- LoongArch "旧世界 / 新世界"ABI 不兼容导致软件生态高度碎片化

## 链接到的概念

- [[computer-systems/loongson-3a5000-microarchitecture]]
- [[computer-systems/branch-predictor-design]]
- [[computer-systems/memory-hierarchy]]
- [[computer-systems/zen4-microarchitecture]]
- [[computer-systems/neoverse-n1-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/loongsons-3a5000-chinas-best-shot
- 本地：`raw/articles/chipsandcheese.com/2023-04-09_loongsons-3a5000-chinas-best-shot.md`
