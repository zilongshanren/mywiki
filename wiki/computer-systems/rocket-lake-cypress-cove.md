---
tags: [cpu, intel, rocket-lake, cypress-cove, 14nm, power-efficiency, backport]
date: 2026-04-27
sources: 1
---

# Rocket Lake / Cypress Cove 微架构

Rocket Lake 是 Intel 第 11 代桌面处理器（2021 年），核心代号 Cypress Cove。它将 [[computer-systems/sunny-cove-microarchitecture|Sunny Cove]]（原本为 10nm 设计）反移植（backport）到 Intel 14nm 工艺。这是 Intel 在 10nm 量产良率不足时的临时应对方案，直接导致 Cypress Cove 成为 14nm 上面积和功耗代价最大的核心之一。

## 效率特性

Rocket Lake 的功耗恶名大多来自全速（stock）运行下的糟糕效率，但更细致的分析揭示了不同故事：

- **30W 以上**：在 14nm 产品中效率最高，超越 Skylake 和 Kaby Lake。高 IPC（Sunny Cove 级别）可以通过低频实现相同性能，使每焦耳计算量改善
- **2.5–3 GHz 甜点区间**：效率与 Kaby Lake 相近，也与 [[computer-systems/golden-cove-microarchitecture|Golden Cove]] 在 4.2–4.5 GHz 的效率区间重叠
- **30W 以下**：效率急剧下降。Rocket Lake 无法像 Atom 核心那样缩减至极低功耗，形成明显的"低功耗盲区"
- **全速时**：比同频 Skylake 快 71.5%（libx264），但完成同等任务的总耗能接近 Skylake 的 2 倍

## 背景：为何 Backport？

Intel 原计划用 Cannon Lake（10nm 初代）替换 Kaby Lake，但 Cannon Lake 良率问题导致仅极少量出货，且禁用了 AVX-512。随后 Ice Lake（10nm+）也受限于产能，难以撑起桌面线。Rocket Lake 是将已验证的 Sunny Cove 核心逆向到成熟 14nm 的"兜底"方案。

## 混合架构假设

文章探讨了假设性的"Rocket Lake + Goldmont Plus"组合：Goldmont Plus 的功耗/性能曲线正好覆盖 Cypress Cove 的低功耗盲区，构成逻辑自洽的 big.LITTLE 配对。真正实现这一思路的是 [[computer-systems/intel-hybrid-alder-lake|Alder Lake]]（Golden Cove + Gracemont），但彼时的 ISA 对齐问题（Atom 不支持 AVX-512）阻止了 Rocket Lake 时代的混合方案落地。

## 延伸阅读

- [[computer-systems/sunny-cove-microarchitecture]] — Sunny Cove 原始 10nm 设计
- [[computer-systems/golden-cove-microarchitecture]] — Rocket Lake 的继任架构
- [[computer-systems/intel-hybrid-alder-lake]] — 真正的混合架构方案

## Sources

- [[sources/chipsandcheese-rocket-lake-efficiency]]
