---
tags: [gpu, amd, infinity-cache, 内存子系统, 缓存, strix-halo]
date: 2026-04-27
sources: 1
---

# Infinity Cache 实效分析（Strix Halo）

Infinity Cache（AMD 官方也称 MALL，Memory Attached Last Level）是 AMD 自 RDNA2 以来在消费级 GPU 中持续使用的内存侧缓存，旨在以较低的 DRAM 带宽实现高 GPU 性能。由于 AMD 的开发工具在 L2 层面就停止提供可见性，其实际效果长期难以直接测量。Strix Halo 是目前最好的观测窗口：该 SoC 拥有完整的 Infinity Fabric 性能计数器，包括 CS（Coherent Station）和 UMC（Unified Memory Controller）两端可编程计数器。

## 测量方法

Chester 的方法基于 CS 与 UMC 流量差异：CS 观察到的所有 Infinity Fabric 请求中，未传播到 UMC 的部分可作为 Infinity Cache 命中的代理指标。

主要误差来源：
- Strix Halo 仅有 8 个 IF 性能计数器，每个端点需两个（读/写各一），只能同时监控 4 个 CS；Chester 通过乘以 4 估算总带宽，存在几个百分点的误差
- CPU 侧内存流量会被计入 miss（Infinity Cache 仅对 GPU 写入填充），轻微高估 miss 率
- 采样粒度为每秒一次（而非毫秒级），可能低估短时带宽峰值

尽管如此，该方法足以回答关键问题：Infinity Cache 是否有效防止 DRAM 带宽成为瓶颈。

## 主要结论

**带宽放大有效**：Strix Halo 配备 256-bit LPDDR5X-8000，理论带宽约 256 GB/s。在测试的全部工作负载中，实测 DRAM 带宽均明显低于理论上限：
- 3DMark Time Spy Extreme：若无 Infinity Cache，CS 侧观察到的流量需要约 335 GB/s DRAM 带宽，实测 DRAM 流量仅为该值的一半左右
- GHPC 和 Unigine Valley 等重载场景中，CS 侧流量接近但未超过 256 GB/s 上限

**命中率随分辨率下降**：更高分辨率的渲染目标尺寸更大，工作集超出 32 MB 缓存，命中率随之下降。1080P 下命中率最高，8K 时缓存依然能发挥作用但效果有限。Wild Life Extreme 8K 下，Strix Halo iGPU 仅约 10 FPS，此时带宽需求反而低于 30 FPS 场景。

**1080P 流量最高**：尽管高分辨率更容易命中 DRAM 带宽上限，但 1080P 实测的 Infinity Fabric 侧峰值流量最高，原因是该分辨率下 GPU 帧率最高，单位时间内产生的流量最多。

**PS5 对比**：PS5 使用 256-bit 14 GT/s GDDR6（约 448 GB/s），无内存侧缓存。Digital Foundry 数据显示 Strix Halo iGPU 性能与 PS5 接近，说明 32 MB Infinity Cache + 256 GB/s LPDDR5X 在效果上大体等同于 PS5 的高带宽方案。

## 与 Infinity Cache 历史对比

AMD 在 Hot Chips 2021 发布的幻灯片中展示了不同分辨率和不同缓存容量的命中率曲线，理论上较大的缓存在高分辨率下命中率更高。Strix Halo 的实测数据与 AMD 的理论模型一致。

从大 iGPU 历史来看：
- 十年前 Intel 在 Haswell 上用 128 MB eDRAM（Iris Pro）配合 128-bit 内存总线
- PS5 等主机芯片依赖超高带宽 DRAM
- Strix Halo 折中两者：适量缓存 + 高于普通客户端但低于主机的 DRAM 带宽

## 工具局限与期望

Chester 指出，AMD 的现有工具（如 Radeon GPU Profiler）在 L2 以下不提供 Infinity Cache 命中率可见性，这对开发者调优和研究人员都是障碍。鉴于 Infinity Cache 已历经多代并进入移动平台，AMD 有理由在下一代工具中开放这一数据。

## 相关

- [[rdna4-architecture]]
- [[strix-halo-soc]]
- [[gpu-memory-hierarchy-latency]]
- [[memory-hierarchy]]
- [[gpu-latency-hiding]]

## Sources

- [[sources/chipsandcheese-strix-halo-infinity-cache]]
