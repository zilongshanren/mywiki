---
tags: [source, 计算机体系结构, simd, x86]
date: 2026-04-19
sources: 1
---

# Why those particular integer multiplies?（Fabian Giesen / ryg）

[[fabian-giesen|Fabian Giesen]] 2024 年 10 月的文章，回答一个长期被回避的问题：为什么 x86 的 SIMD 整数乘法指令集看起来这么乱？答案是 Intel 25 年来一直围绕一个 16×16 → 32-bit 乘法器数据通路做加法。

## 摘要

Pentium MMX 时代引入 `PMULLW` / `PMULHW` / `PMADDWD` 三条指令都用同一组四路 16×16 乘法器实现——高位、低位、两两 dot product 只在 partial-product reduction tree 的后 10% 分叉。SSE 补 `PMULHUW`。SSE2 的 `PMULUDQ`（32×32→64）看似需要新硬件，其实拆成 `(a1 b1)<<32 + (a1 b0 + a0 b1)<<16 + a0 b0` 就是四个 16×16 + 一个 PMADDWD 结构。SSSE3 的 `PMULHRSW`（rounding）和 `PMADDUBSW`（byte 上的 signed×unsigned + saturate）开始给 reduction tree 加约束。SSE4.1 的 `PMULLD` 需要每 lane 三次 16×16 乘法但只有两路，强制 2 uops、延迟翻倍——这也是 ryg 猜测"Intel 仍然在复用 MMX-era 核心"的最强证据。`VPMULLQ` 需 3 uops，可能借用 FP64 乘法器的 52×52 → 104 尾数通路（IFMA 也是如此）。AMD Zen 和 Intel E-core 后来干脆直接加 32×32 乘法器。

## 关键要点

- **硬件实现视角是理解 ISA 的钥匙**：每条"奇怪"的指令都对应某种 partial-product 路径复用。
- **PMADDWD 是免费午餐**：大 reduce tree 里多塞一个项几乎零成本。
- **PMULLD 的 uop 代价**揭示了"每 32-bit lane 只有 2 个 16×16"约束。
- **IFMA / VPMULLQ** 复用 FP64 尾数——ISA 拼接硬件，不是新设计。

## 链接到的概念

- [[x86-simd-integer-multiplies]]
- [[sse-tricks]]
- [[fabian-giesen]]

## 原文

- 链接：https://fgiesen.wordpress.com/2024/10/26/why-those-particular-integer-multiplies/
- 本地：`raw/articles/fgiesen.wordpress.com/2024-10-26_why-those-particular-integer-multiplies.md`
