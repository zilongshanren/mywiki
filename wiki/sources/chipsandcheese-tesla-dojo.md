---
tags: [source, chipsandcheese, cpu, ai, tesla, dojo, accelerator, sram, hot-chips]
date: 2026-04-27
sources: 1
---

# Hot Chips 34 – Tesla's Dojo Microarchitecture（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2022 年 9 月的文章，基于 Tesla 在 Hot Chips 34 大会上的公开演讲，详细解析 Tesla Dojo 超算专用处理器的微架构设计与权衡。

## 摘要

Dojo 是 Tesla 为 ML 训练自研的专用处理器，采用 8-wide、4-way SMT、2 GHz 的保守设计，配备 512-bit 向量单元和 8×8×4 矩阵乘法单元。核心以 1.25 MB 的软件管理 SRAM 替代传统缓存层次，通过 DMA 与系统 HBM 通信。为最大化计算密度，Dojo 放弃了精确异常、虚拟内存和缓存一致性，类似于 IBM Cell SPE 的设计理念。单个 D1 die 面积 645 mm²，354 核，峰值 362 BF16 TFLOPS@2 GHz。25 个 D1 die 构成一个 tile，通过 interface processor 卡连接 160 GB HBM。

## 关键要点

- 不实现精确异常（有 debug mode 替代），节省 ROB 面积与功耗
- 无虚拟内存、无 TLB，4-way SMT 主要用于同一任务内的计算/DMA 重叠
- SRAM 直接寻址（21-bit 地址），避免 cache tag lookup 降低延迟
- D1 die 仅用 28.9% 面积于非 SRAM/核逻辑（vs AMD Zeppelin 44%）
- 指令缓存不具备一致性，加载新代码需手动 flush

## 链接到的概念

- [[tesla-dojo-microarchitecture]]
- [[memory-hierarchy]]
- [[gpu-latency-hiding]]

## 原文

- 链接：https://chipsandcheese.com/p/hot-chips-34-teslas-dojo-microarchitecture
- 本地：`raw/articles/chipsandcheese.com/2022-09-01_hot-chips-34-teslas-dojo-microarchitecture.md`
