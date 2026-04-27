---
tags: [source, chipsandcheese, cpu, intel, redwood-cove, meteor-lake, microarchitecture, p-core]
date: 2026-04-27
sources: 1
---

# Intel's Redwood Cove: Baby Steps are Still Steps（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2024 年 9 月的文章，对 Meteor Lake 的 P-Core 架构 Redwood Cove 进行系统解析，重点覆盖前端改进、新增预取器、SMT 资源分配策略，并与 Golden Cove 和 Zen 4 做比较。

## 摘要

Redwood Cove 是 Golden Cove 的第二代演进（经由 Raptor Cove），主要结构容量基本未变，但在前端做了一批精确的小改进：L1i 翻倍至 64 KB、IDQ 扩容至 192 项（单线程）、新增 Branch Hint 0x3E 支持、扩充宏融合（MOV+OP、LD+OP）。预取器方面增加了 LLC 页预取器（提前拉取后续 8 KB 至 L3）和 Array-of-Pointers 预取器。后端与 Golden Cove 完全一致，仅 FP 乘法延迟从 4 周期降至 3 周期。文章最后将 Redwood Cove 定性为 Intel 的 "tick"：Meteor Lake 系统级的巨变（chiplet 化）决定了 P-Core 必须保守，以控制整体风险。与 AMD 同期 Zen 4→Zen 5 的激进演进相比，Redwood Cove 的改动幅度明显偏小。

## 关键要点

- L1i 从 32 KB 翻倍至 64 KB；IDQ 从 144 项增至 192 项（单线程），双 SMT 各 96 项
- BTB 容量沿用 12K 项，但 L2 BTB 延迟从 3 周期降至 2 周期；单线程只能访问约 6K BTB 项
- 恢复 Pentium 4 时代的 0x3E taken branch hint 前缀，仅在预测器无信息时生效
- LLC 页预取器：预判 page 末尾访问，将后续 8 KB 预取至 L3；通过 IDI 机会性发包避免资源竞争
- AOP 预取器：识别 array-of-pointers 间接访问模式（Apple M1 早已采用）
- L3 延迟约 75+ 周期，高于 Zen 4 移动版的约 50 周期；DRAM 延迟约 148 ns

## 链接到的概念

- [[computer-systems/redwood-cove-microarchitecture]]
- [[computer-systems/golden-cove-microarchitecture]]
- [[computer-systems/lion-cove-microarchitecture]]
- [[computer-systems/meteor-lake-chiplet-architecture]]
- [[computer-systems/zen4-microarchitecture]]
- [[people/chester-lam]]

## 原文

- 链接：https://chipsandcheese.com/p/intels-redwood-cove-baby-steps-are-still-steps
- 本地：`raw/articles/chipsandcheese.com/2024-09-22_intels-redwood-cove-baby-steps-are-still-steps.md`
