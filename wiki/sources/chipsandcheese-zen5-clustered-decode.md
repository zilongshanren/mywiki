---
tags: [source, computer-systems, amd, zen5, frontend, op-cache, decoder, microarchitecture]
date: 2026-04-27
sources: 1
---

# Disabling Zen 5's Op Cache and Exploring its Clustered Decoder（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 1 月的实验性文章，通过 MSR 0xC0011021[5] 位强制禁用 Zen 5 的 op cache，暴露底层 2×4-wide 集群式解码器的真实能力与局限。

## 摘要

Zen 5 前端采用两个独立的取指/解码集群，各自服务一个 SMT 线程，外加一个 6K entry 的 op cache 作为主要指令供给源。通过 MSR 禁用 op cache 后，单线程性能在 SPEC CPU2017 整数/浮点上分别下降 20.3% 和 16.8%，高于 Zen 4 的 11.4%/6.6%，体现出更宽执行引擎对前端带宽的更高需求。而 SMT 场景下，双解码集群的优势得以发挥：整数/浮点仅分别下降 4.9% 和 0.82%，远优于 Zen 4（-16%/-10.3%）。文章还分析了游戏负载（IPC < 1）几乎感知不到 op cache 的消失，以及 Cinebench 2024 在单线程高 IPC 段可以观察到 4-wide 解码器的饱和现象。最终结论是：Zen 5 的集群式解码器是专为 SMT 多线程场景设计的安全网，而非主力前端路径。

## 关键要点

- MSR 0xC0011021 第 5 位可禁用 Zen 5 op cache，暴露 2×4-wide 解码器裸跑能力
- 单线程场景下，缺少 op cache 的 Zen 5 性能损失大于 Zen 4（核心更宽、前端压力更大）
- SMT 双线程场景下，两个解码集群几乎能弥补 op cache 缺失，性能损失极小
- 游戏负载（IPC ≈ 1）几乎不依赖 op cache，前端大部分时间空闲
- 507.cactuBSSN 是 SPEC 中唯一 op cache 命中率低于 90% 的测试，SMT 下降至 61.79%
- 与 Steamroller/Excavator 的对比：Zen 5 每个集群拥有独立取指路径，而非共用

## 链接到的概念

- [[computer-systems/op-cache-decoded-uop-cache]]
- [[computer-systems/zen5-microarchitecture]]
- [[computer-systems/clustered-decode-atom]]

## 原文

- 链接：https://chipsandcheese.com/p/disabling-zen-5s-op-cache-and-exploring
- 本地：`raw/articles/chipsandcheese.com/2025-01-23_disabling-zen-5s-op-cache-and-exploring-its-clustered-decode.md`
