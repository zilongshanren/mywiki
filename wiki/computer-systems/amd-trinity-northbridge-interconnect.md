---
tags: [cpu, amd, APU, 互联, northbridge, trinity, igpu, 缓存一致性, infinity-fabric]
date: 2026-04-27
sources: 1
---

# AMD Trinity Northbridge 互联架构

Trinity 是 AMD 2012 年的 APU 产品，将两个双线程 Piledriver CPU 模块（[[bulldozer-microarchitecture]]）与 Terascale 3 iGPU 集成在同一芯片上。Chester Lam 通过微基准与性能计数器系统性地测量了 Trinity Northbridge 的互联行为，揭示了 Infinity Fabric 诞生前 AMD 在 CPU-iGPU 集成上的设计取舍。

## Northbridge 架构概述

Trinity 的 Northbridge 继承自 Athlon 64 时代的片上北桥，运行在独立电压/频率域（A8-5600K 上为 1.8 GHz）。两级交叉开关（crossbar）结构：

- **SRI（System Request Interface）**：CPU 核心的请求接入点，分别管理内存请求队列（SRQ）与探测（probe）入队。
- **XBAR**：连接 SRI 与内存控制器（MCT）、IO 等设备，XCS 共 40 项调度队列（服务器版 Piledriver 为 64 项）。

MCT（Memory Controller）负责 CPU 侧请求的优先级排序与缓存一致性，含 stride prefetcher；iGPU 则通过独立的 GMC（Graphics Memory Controller）管理带宽。

## 双链路设计："Garlic" 与 "Onion"

AMD 通过两条独立链路解决 CPU/GPU 内存访问路径不同的问题：

| | Garlic（Radeon Memory Bus） | Onion（Fusion Control Link） |
|---|---|---|
| 路径 | GMC → DRAM 直连，绕过 MCT | GPU → XBAR → MCT → CPU 缓存侦听 |
| 带宽 | 可饱和 DRAM（>24 GB/s） | 上限约 10 GB/s |
| 一致性 | 无（GPU 不可见 CPU 缓存） | 完整一致性（可侦听 CPU 缓存） |
| 延迟代价 | 基础路径 | +约 320 ns vs. Garlic |

典型 GPU 图形渲染使用 Garlic，需要与 CPU 共享数据时使用 Onion。无探测过滤器（probe filter），高负载下探测响应超 4500 万次/秒。

## 实测行为

GPU 通过 Garlic 高强度拉取带宽（>24 GB/s）时，CPU 侧 latency 保持在 120 ns 以下，表现良好。CPU 自身带宽争用反而比 GPU 争用更会推高 CPU latency，因为竞争主要发生在 SRI/XBAR 而非 DRAM 控制器。

CPU 访问 GPU 内存（iGPU 映射到 CPU 地址空间时使用写合并 WC 不可缓存）导致 CPU 无法利用内存级并行，读带宽急剧下降，pointer chasing latency 约 93 ns（远高于标准可缓存内存）。

## 与 Infinity Fabric 的对比

Trinity 的设计与 AMD 现代 Infinity Fabric（[[infinity-fabric-loaded-latency]]）形成鲜明对比：

- Infinity Fabric 的 CS（Coherent Slave）对 CPU 和 GPU 的内存访问均可见，含 probe filter，可维护完整一致性而不产生海量探测流量。
- Trinity iGPU 内存映射到 CPU 侧时不可缓存（性能严重退化），而现代 Ryzen APU 上 GPU 内存映射到 CPU 侧仍可缓存（延迟约 100+ ns，但行为一致）。
- Trinity 完全没有 probe filter，跨侧访问会产生大量无效探测。

## 图形工作负载实测

通过 AMD 性能计数器统计 XBAR 与 DRAM 控制器的流量差（即 Garlic 流量），在 Unigine Valley 中峰值 DRAM 带宽达 17.7 GB/s，FF14 Heavensward benchmark 达 22.7 GB/s，绝大多数来自 GPU Garlic 路径。CPU 侧通常保持在 3-5 GB/s。

## 历史意义

Trinity 的 Northbridge 是 AMD 在 APU 路线上的过渡产品。尽管 Garlic/Onion 双链路设计缺乏优雅，在零拷贝和跨侧访问性能上均逊于同期 Intel Sandy/Ivy Bridge 的 ring bus iGPU 方案，但它足以让 iGPU 充分利用 DDR3-1866 带宽用于图形渲染，为 AMD 争得了 APU 时代的立足点，并积累了后来开发 Infinity Fabric 所需的互联经验。

## Sources

- [[sources/chipsandcheese-trinity-northbridge]]
- [[sources/chipsandcheese-magny-cours]]
