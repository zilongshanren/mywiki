---
tags: [source, computer-systems, cpu, loongson, loongarch, mips, china, performance-counters]
date: 2026-04-27
sources: 1
---

# Previewing China's Loongson 3A5000 with Performance Counters（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2023 年 1 月的文章，通过性能计数器对龙芯 3A5000 进行初步基准测试与架构分析。

## 摘要

龙芯 3A5000 搭载四枚 LA464 核心，采用龙芯自研的 LoongArch ISA（基于 MIPS64 语义但使用不同编码，并扩展了 LSX/LASX 128/256-bit 向量指令）。在 7-Zip 压缩测试中，每时钟指令数（IPC）与 Zen 1 相当，但 2.5 GHz 的极低主频导致绝对性能远低于 Zen 1 和 Ampere Altra。视频编码测试（libx264）中，3A5000 需执行 12%–23% 更多指令且同样因主频低而落败。缓存分析显示 L1D 命中率异常偏低（可能是替换策略较差或预取激进），L3（16 MB）大容量在一定程度上弥补了 L2（256 KB）偏小的不足。软件生态是更大的挑战：LoongArch 不兼容 x86 或 ARM，MIPS 软件生态也相当薄弱。文章定性 3A5000 是中国目前最强的自研 CPU 设计，但距国际主流仍有较大差距。

## 关键要点

- LA464 核 @2.5 GHz；IPC 和 Zen 1 相近，但主频差距导致整体性能劣势明显
- LoongArch ISA：MIPS64 语义 + 不兼容编码，加入 LSX（128-bit）和 LASX（256-bit）向量扩展
- L1i：64 KB 4-way；L1D：64 KB 4-way（但命中率低于应有水平）；L2：256 KB；L3：16 MB
- 7-Zip 下指令数差异 <5%，libx264 下 Loongson 需多执行 12–23% 指令（ISA 专用指令不足）
- 分支预测准确率与 Zen 1 / Neoverse N1 接近，但 LoongArch 分支指令比例更高（17.7% vs x86 15.1%）
- 软件生态薄弱：无 x86/ARM 生态支撑，微基准需全部手写 LoongArch 汇编，调试困难

## 链接到的概念

- [[computer-systems/loongson-3a5000-microarchitecture]]
- [[computer-systems/phytium-ftc663-microarchitecture]]
- [[computer-systems/neoverse-n1-microarchitecture]]
- [[computer-systems/zen2-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/previewing-chinas-loongson-3a5000-with-performance-counters
- 本地：`raw/articles/chipsandcheese.com/2023-01-29_previewing-chinas-loongson-3a5000-with-performance-counters.md`
