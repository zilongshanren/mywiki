---
tags: [source, computer-systems, intel, skylake, microarchitecture]
date: 2026-04-27
sources: 1
---

# Skylake: Intel's Longest Serving Architecture（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2022 年 10 月的深度分析，系统性地解剖了 Intel Skylake 架构的设计决策、竞争历史及其六年服役生涯的始末。

## 摘要

文章以微测试为基础，逐层分析 Skylake 相对 Haswell 的前端（指令缓冲、微操作缓存、分支预测器）、后端（调度器拆分、寄存器文件重组、执行单元）和内存层次的变化。作者指出，Skylake 对客户端性能的提升相当有限（约 5.7% IPC），因为它将大量工程投入用于支持服务端 AVX-512 和不同核心配置——这在 2015 年 AMD 毫无竞争力的背景下是合理决策，却在 Zen 系列崛起后暴露出隐患。文章还追溯了 Skylake 如何在 Zen 1/2/3 的步步紧逼下依赖频率和核心数增加勉强维持竞争力，直到 Zen 3 在几乎所有方面将其超越。

## 关键要点

- Skylake 的主要工程投入是为服务端 AVX-512 铺路，客户端仅受益于副产品（x87/MMX 寄存器文件等）
- 调度器从统一结构拆分为两个分布式调度器（58+39 项），移除了最后一块 P6 遗产
- 微操作缓存带宽 6/cycle，但受 4-wide 重命名级限制，瓶颈在重命名
- L2 TLB 扩大至 1536 项，L2↔L3 队列从 16 扩至 32 项
- L3 延迟随核心数增加（4→10 核）上升约 11 cycle，但绝对延迟仍在 10 ns 左右
- AMD Zen 2 最终在几乎所有可测指标上持平或超越 Skylake（向量、缓存带宽、分支预测）
- Zen 3 最终在取跳转分支处理上也赶上，完成对 Skylake 的全面超越

## 链接到的概念

- [[computer-systems/skylake-microarchitecture]]
- [[computer-systems/golden-cove-microarchitecture]]
- [[computer-systems/sunny-cove-microarchitecture]]
- [[computer-systems/zen2-microarchitecture]]
- [[computer-systems/netburst-microarchitecture]]
- [[computer-systems/op-cache-decoded-uop-cache]]
- [[computer-systems/branch-predictor-design]]

## 原文

- 链接：https://chipsandcheese.com/p/skylake-intels-longest-serving-architecture
- 本地：`raw/articles/chipsandcheese.com/2022-10-14_skylake-intels-longest-serving-architecture.md`
