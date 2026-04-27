---
tags: [source, cpu, amd, APU, northbridge, trinity, igpu, 互联, 缓存一致性]
date: 2026-04-27
sources: 1
---

# AMD's Pre-Zen Interconnect: Testing Trinity's Northbridge（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2025 年 6 月 14 日的文章，通过微基准测试与 AMD 性能计数器对 Trinity APU（A8-5600K）的 Northbridge 互联架构进行了系统性分析，并与现代 Infinity Fabric 进行了横向比较。

## 摘要

文章首先介绍了 Trinity Northbridge 的双级 crossbar 结构（SRI + XBAR）和 CPU/GPU 双内存路径设计：高带宽"Garlic"链路（GMC → DRAM 直连）与低带宽但支持缓存一致性的"Onion"链路（GPU → MCT → CPU 缓存侦听）。通过 GPU 带宽压力测试验证了 Garlic 在不影响 CPU latency 的情况下可拉取超过 24 GB/s；通过 OpenCL 内存访问测试揭示了 Onion 的 10 GB/s 上限与+320 ns 额外延迟。对比 Infinity Fabric 指出：Trinity 缺乏 probe filter，跨侧访问性能退化明显，而现代 APU 在统一互联下 CPU/GPU 均可访问对方内存且保持可缓存性。最后通过 Unigine Valley、FF14 Heavensward、ESO 等游戏工作负载的性能计数器数据，展示了 Trinity 实际运行时 DRAM 流量的分布（Garlic 为主，CPU 侧约 3-5 GB/s）。

## 关键要点

- Northbridge：SRI + XBAR 双级 crossbar，1.8 GHz 独立域
- Garlic（Radeon Memory Bus）：GPU 直连 DRAM，绕过 MCT，无缓存一致性，可满速
- Onion（Fusion Control Link）：走 XBAR + MCT，完整一致性，上限 10 GB/s，+320 ns
- 无 probe filter，高负载下探测响应超 4500 万次/秒
- CPU 访问 iGPU 内存须用 WC（写合并不可缓存），读带宽急剧退化
- FF14 Heavensward 峰值 DRAM 带宽 22.7 GB/s，绝大多数来自 Garlic
- 与 Infinity Fabric CS 相比：Trinity 缺乏 probe filter，跨侧访问均有性能代价

## 链接到的概念

- [[amd-trinity-northbridge-interconnect]]
- [[bulldozer-microarchitecture]]
- [[infinity-fabric-loaded-latency]]

## 原文

- 链接：https://chipsandcheese.com/p/amds-pre-zen-interconnect-testing
- 本地：`raw/articles/chipsandcheese.com/2025-06-14_amds-pre-zen-interconnect-testing-trinitys-northbridge.md`
