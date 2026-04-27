---
tags: [source, cpu, centaur, numa, 多路, 缓存一致性]
date: 2026-04-27
sources: 1
---

# Centaur CHA's Probably Unfinished Dual Socket Implementation（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2022 年 4 月的文章，测试 Centaur CHA 双路系统的跨路延迟、带宽与 cache coherency 性能，与 Intel Broadwell-E、Westmere-EP 和 AMD Milan-X 对比，揭示 CHA 跨路带宽实现存在明显缺陷。

## 摘要

文章使用 pointer chasing（1 GB，2 MB 大页）和带宽测试（3 GB 测试大小）量化 NUMA 性能。CHA 的跨路延迟增量为 +92 ns，约为本地延迟的等量，远差于 Broadwell 的 +42 ns 和 Westmere 的 +50 ns。更致命的是跨路带宽：仅约 1.3 GB/s，不及十年前 Westmere 的十分之一（11.2 GB/s），也远低于 Broadwell（21 GB/s）和 AMD Milan-X（40+ GB/s）。Chester 判断这是 Centaur 的跨路请求队列尚未完成验证的症状——协议状态机已实现，但实际带宽交付能力是 work in progress。Contested atomic 方面 CHA 表现较好（90–130 ns），但该指标对实用多线程几乎无意义。

## 关键要点

- 跨路延迟增量：CHA +92 ns vs Broadwell +42 ns vs AMD NPS2 同路节点 +14 ns
- 跨路带宽：CHA 仅 1.3 GB/s，低于 NVMe SSD 顺序读；未完成的 request queue 是主因
- Broadwell CoD 模式的教训：同 die 跨 NUMA 节点惩罚大于跨路（directory 查询成本），AMD 目录更快
- Contested atomics：CHA 与 AMD/Intel 持平，但此场景在真实代码中极少
- NUMA-unaware 负载在 CHA 双路上几乎无法有效扩展

## 链接到的概念

- [[numa-multi-socket-design]]
- [[centaur-cns-microarchitecture]]
- [[cache-coherence-cross-cluster]]
- [[core-to-core-latency-lock-test]]

## 原文

- 链接：https://chipsandcheese.com/p/centaur-chas-probably-unfinished-dual-socket-implementation
- 本地：`raw/articles/chipsandcheese.com/2022-04-23_centaur-chas-probably-unfinished-dual-socket-implementation.md`
