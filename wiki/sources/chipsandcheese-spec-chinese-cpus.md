---
tags: [source, computer-systems, spec-cpu2017, loongson, zhaoxin, benchmark, chinese-cpu]
date: 2026-04-27
sources: 1
---

# Running SPEC CPU2017 on Chinese CPUs, and More（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2024 年 10 月的文章，在龙芯、兆芯等国产 CPU 上运行 SPEC CPU2017，与 Intel/AMD 各代参照物进行系统对比。

## 摘要

文章使用 GCC 14.2.0、`-O3 -march=native -mtune=native` 标志，在裸机 Linux 上运行 SPEC CPU2017 Rate-1 单线程测试，覆盖龙芯 3A6000（LA664 架构）、龙芯 3A5000（LA464 架构）、兆芯 KX-6640MA（Lujiazui 架构）及多个参照 CPU。

**龙芯 3A6000**：单线程性能低于 Intel Crestmont（Atom E-Core），SMT 增益约 20%（与 Zen 5 相近），但双线程仍不及单线程 Zen 4/5。LA664 在若干浮点子测试（imagick、wrf、fotonik3d）能超过 Crestmont，但整体分数落后。分支预测精度比 Skylake（2015）更好，是对 3A5000 的显著改进。IPC 指标在部分测试中相当有竞争力，但时钟频率（2.5 GHz）严重拖累绝对性能。Loongarch64 平均比 x86-64 多执行约 10.6% 的指令（部分 FP 测试多出 77%），编译器代码质量是另一短板。

**龙芯 3A5000**：性能介于 Celeron J4125 与 Bulldozer FX-8150 之间，与 Skylake 相比差距悬殊，被宣传的"接近初代 Ryzen"更接近营销夸大。

**兆芯 KX-6640MA**：2-wide 乱序核 2.6 GHz，性能略低于 Intel Goldmont Plus，与 Arm Cortex A73 接近，属低功耗 CPU 档位。x86-64 ISA 保持兼容性优势，但执行宽度和乱序窗口太小。

跨 ISA 指令数对比显示 x86-64 与 aarch64 执行指令数几乎相当（x86-64 仅多 1.17%），Loongarch64 多约 10.6%，说明 ISA 设计的差距已非主要瓶颈，频率和架构宽度才是核心问题。

## 关键要点

- 3A6000 单核性能低于 2019 年上市的 Intel Crestmont E-Core
- 3A5000 约等于 2012 年的 Bulldozer；"接近 Ryzen 1"的说法不实
- 兆芯 KX-6640MA 约等于 Goldmont Plus / Cortex A73，属于低功耗平台档
- Loongarch64 比 x86-64 多执行约 10.6% 指令，个别 FP 测试多达 77%
- 3A6000 分支预测精度优于 Skylake，是 3A5000 的重大进步
- 龙芯需同时提升 IPC 和时钟频率，才有望与 Intel/AMD 竞争

## 链接到的概念

- [[loongson-3a6000-microarchitecture]]
- [[loongson-3a5000-microarchitecture]]
- [[via-x86-isaiah-lujiazui]]
- [[spec-cpu2017-methodology]]
- [[branch-predictor-design]]
- [[crestmont-microarchitecture]]
- [[skylake-microarchitecture]]
- [[bulldozer-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/running-spec-cpu2017-on-chinese-cpus
- 本地：`raw/articles/chipsandcheese.com/2024-10-19_running-spec-cpu2017-on-chinese-cpus-and-more.md`
