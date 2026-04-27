---
tags: [source, cpu, amd, zen5, avx512, frequency, ipc-throttling]
date: 2026-04-27
sources: 1
---

# Zen 5's AVX-512 Frequency Behavior（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 3 月的文章，通过微基准测试深入剖析 Zen 5 在遭遇重载 AVX-512 指令时的频率与 IPC 动态行为。

## 摘要

Zen 5 是 AMD 首款全宽 AVX-512 数据通路的核心，支持每周期两条 512-bit 载入。作者通过依赖整数加法测量 IPC 的方法，观察到 Zen 5 在遭遇 512-bit 寄存器操作时几乎无过渡期（不足 1.3 微秒），但引入 512-bit 内存操作数后出现约 22 ms 的过渡期，表现为 IPC 节流（而非降频）。性能计数器数据揭示：Zen 5 并非降低时钟，而是通过减少每周期派发微操作数来"软降速"，直至频率稳定在可持续的水平。这与 Skylake-X 的固定 25% 指令派发率节流机制截然不同。Zen 5 还有意延长 AVX-512 负载消失后的恢复时间（超过 100 ms），以避免频繁的过渡惩罚。

## 关键要点

- 纯 512-bit 寄存器到寄存器 FMA：无频率损失，无过渡期
- 512-bit 内存操作数：触发约 22 ms 的 IPC 节流过渡；更高 FPU 负载使过渡期延长至 ~32 ms
- IPC 节流机制：Zen 5 FP Non-Scheduling Queue（NSQ）检测背压，调度器阶段控制派发速率
- 每个 Zen 5 核心拥有独立传感器，过渡行为因核心而异
- 频率恢复时间 > 100 ms，且非线性（越接近峰值越保守）
- Ryzen 9 9900X 的慢 CCD（5.4 GHz 上限）从不触发过渡，因为其起始频率不高

## 链接到的概念

- [[computer-systems/zen5-avx512-frequency]]
- [[computer-systems/zen5-microarchitecture]]
- [[computer-systems/non-scheduling-queue]]

## 原文

- 链接：https://chipsandcheese.com/p/zen-5s-avx-512-frequency-behavior
- 本地：`raw/articles/chipsandcheese.com/2025-03-01_zen-5-s-avx-512-frequency-behavior.md`
