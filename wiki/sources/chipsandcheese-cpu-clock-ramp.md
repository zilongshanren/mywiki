---
tags: [source, chipsandcheese, cpu, power-management, clock-speed, benchmark]
date: 2026-04-27
sources: 1
---

# How Quickly do CPUs Change Clock Speeds?（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2022 年 9 月的实验性文章，测量多款 CPU 从空闲到最高 boost 频率所需的时间。

## 摘要

文章设计了一套基于串行整数加法 + RDTSC/CNTVCT_EL0 计时的测试方法，规避了 gettimeofday 等 API 的毫秒级精度限制，实现亚毫秒频率测量。结论是：Intel Speed Shift（Skylake 引入，2015）将 P-state 控制权移交 CPU 硬件，是客户端平台爬升速度的重要里程碑，使桌面 Skylake 在 5.6 ms 内达到最大 boost；AMD Zen 3 移动版更快，约 2 ms；而 Haswell 及以前的老平台需要 60-80 ms。AMD Piledriver 在高待机电压（最低 CPU 状态 100%）下也能实现极速爬升，证明大部分延迟来自电压建立时间。

## 关键要点

- 时钟爬升速度的主要物理瓶颈是 VRM 电压斜率
- Intel Speed Shift（Skylake）将爬升时间压缩 10 倍以上
- Zen 3 移动版爬升最快（测试集中最佳）
- Intel HEDT 平台（Sandy Bridge-E、Haswell-E）刻意慢速爬升，可能为了降低短任务功耗
- CNTVCT_EL0（ARM）时钟精度低于 RDTSC（x86），约每 50 ns 递增一次

## 链接到的概念

- [[cpu-clock-frequency-ramp]]
- [[power-wall]]
- [[dennard-scaling]]

## 原文

- 链接：https://chipsandcheese.com/p/how-quickly-do-cpus-change-clock-speeds
- 本地：`raw/articles/chipsandcheese.com/2022-09-15_how-quickly-do-cpus-change-clock-speeds.md`
