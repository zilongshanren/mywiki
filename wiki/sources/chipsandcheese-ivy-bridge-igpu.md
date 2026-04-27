---
tags: [source, gpu, intel, igpu, gen7, ivy-bridge, history]
date: 2026-04-27
sources: 1
---

# Ivy Bridge's Gen7 Graphics: Intel's Modern iGPU Push（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2023 年 8 月的文章，以微基准测试补充 Real World Tech 的 Ivy Bridge GPU 分析，重点考察 Gen 7 EU 结构、缓存层次、本地内存与原子操作。

## 摘要

Ivy Bridge（2012）Gen 7 iGPU 标志着 Intel 集成显卡走向可编程的转折点。Gen 7 将 EU 组织为 subslice，引入 DirectX 11 支持和较强的 INT8/INT16 吞吐，但 INT32 吞吐只有 FP32 的一半。与 AMD/Nvidia 不同，Gen 7 EU 使用 send 消息指令访问内存与采样器，而不是直接内存访问指令，这种解耦使 Intel 能以 EU 粒度调节 GPU 规模。EU 寄存器文件不随占用率动态分配——每线程固定 128 寄存器，最多 8 活跃 wave，这种设计一直延续至今。本地内存从 GPU 级 L3 缓存中分配，而非 CU 内专用 SRAM，导致延迟远差于 Nvidia 同代产品。采样器 L1 缓存延迟高达 141ns，L3 延迟约 87ns，总体性能接近 Nvidia Fermi 低端产品。文章指出 Gen 7 奠定了 Intel GPU 的设计语言，Xe 架构的 subslice、固定 128 寄存器、send 指令等特征均可追溯至此。

## 关键要点

- EU 使用 send 消息指令而非直接内存访问，解耦使 GPU 可以 EU 粒度缩放
- 寄存器文件不动态分配：128 寄存器/线程，8 线程/EU，使用较少寄存器不增加占用率
- 本地内存映射到 GPU L3 cache，而非私有 SRAM，导致延迟高于竞争对手
- 采样器 L1/L2 延迟分别约 141ns/145ns；全局内存经 L3 获得约 87ns 延迟
- INT32 吞吐是 FP32 的一半（只用 FPU pipe，不用 EM pipe）
- 设计语言延续到 Xe：subslice→Xe Core，EU→Vector Engine，固定占用率模型不变

## 链接到的概念

- [[computer-systems/intel-gen7-igpu]]
- [[rendering/xe-hpg-architecture]]
- [[rendering/gpu-latency-hiding]]
- [[rendering/gpu-memory-hierarchy-latency]]

## 原文

- 链接：https://chipsandcheese.com/p/ivy-bridges-gen7-graphics-intels-modern-igpu-push
- 本地：`raw/articles/chipsandcheese.com/2023-08-25_ivy-bridges-gen7-graphics-intels-modern-igpu-push.md`
