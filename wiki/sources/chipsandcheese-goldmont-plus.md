---
tags: [source, computer-systems, intel, atom, goldmont-plus, gemini-lake]
date: 2026-04-27
sources: 1
---

# Intel Atom 旅程：Goldmont Plus（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2024 年 6 月的历史回顾文章，测试平台为 Celeron J4125（Gemini Lake），梳理 Goldmont Plus 在 Intel Atom 演化路线上的定位。

## 摘要

Goldmont Plus（GLP）是 2017 年以 14 nm 发布的 Atom 架构，介于手机时代的 Silvermont 与混合核时代的 Tremont 之间。它是 3-wide 超标量乱序设计，比 Silvermont 大幅扩展了执行资源（93 条目 ROB vs Silvermont 的 32 条目），分支预测能力接近 Skylake。文章覆盖前端预解码缓存、分布式调度器、内存依赖处理（仅支持精确地址匹配的快速转发）、双级缓存（24 KB L1D + 4 MB 共享 L2）等要点。GLP 存在几个明显缺陷：L1D 为 write-through 设计（配合 4 KB 写合并缓冲），没有 AVX 支持，DRAM 延迟超过 180 ns 等。作者将 Goldmont Plus 定位为 Atom 的"过渡相"——面积效率优先但尚未达到 Tremont 后的成熟混合核水准。

## 关键要点

- 3-wide OoO，ROB 93 条目，对比 Silvermont 32 条目是巨大进步
- 分支预测器能力接近 Skylake，但 BTB 只有 2048 条目，3 cycle 延迟较慢
- L1D 为 write-through + 4 KB 写合并缓冲（类似 Bulldozer 策略）
- 512 条目 L2 TLB 覆盖指令和数据（改进自 Goldmont 仅覆盖数据侧）
- 不支持 AVX；缺失微操作缓存；无快速聚集（gather）硬件
- DRAM 延迟 >180 ns，约为同期低端 Core i7 的 2-3 倍
- 是 [[clustered-decode-atom]] 集簇解码模式的早期准备阶段

## 链接到的概念

- [[goldmont-plus-microarchitecture]]
- [[tremont-microarchitecture]]
- [[clustered-decode-atom]]
- [[gracemont-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/tracing-intels-atom-journey-goldmont-plus
- 本地：`raw/articles/chipsandcheese.com/2024-06-10_tracing-intels-atom-journey-goldmont-plus.md`
