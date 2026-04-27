---
tags: [source, computer-systems, arm, cpu, aarch64, server, sbc]
date: 2026-04-27
sources: 1
---

# ARM's Cortex A72: aarch64 for the Masses（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2023 年 11 月的文章，以 AWS Graviton 一代（2.3 GHz Cortex-A72）为测试平台，系统评测 Cortex-A72 微架构，并与高通 Kryo（Snapdragon 821）做横向对比。

## 摘要

Cortex-A72 是 2015 年发布的 ARMv8 3 宽乱序核，虽已被多代架构超越，但在 Raspberry Pi 4、AWS Graviton 一代、网络处理器（Pensando）等设备中仍有广泛部署。文章覆盖了分支预测（A72 识别长 pattern 略优于 Kryo，但 BTB 速度较慢）、前端取指（L2 代码场景双核都不足 1 IPC）、OoO 引擎（128 条目 ROB，分布式调度，FP 寄存器文件为 64-bit 宽，NEON 128-bit 占 5 个寄存器）、store forwarding（7 cycle，支持部分重叠，无内存依赖预测）、以及 Graviton 集群的 L2 共享带宽问题。核心结论：A72 是合格的低功耗乱序核，最大短板是 L2 带宽极有限（16 bytes/cycle 总量，4 核共享），服务器场景受限明显。

## 关键要点

- 3 宽乱序，128 条目 ROB，双 ALU 管道
- 48 KB L1i（比 Kryo 大），BTB 2K–4K 条目但速度慢（2 cycle 起）
- 31 条目返回栈（比 Kryo 的 16 条目深）
- 128-bit NEON 占用 5 个 64-bit FP 寄存器，vector 重命名深度受限
- Graviton 一代：4 核共享 2 MB L2（21 cycle），集群内 L2 带宽 ~16 bytes/cycle，不扩展
- 跨集群 cache coherency 延迟 >200 ns（接近 NUMA）
- DRAM 延迟（4K 页）162 ns，page walk 性能差是主要原因

## 链接到的概念

- [[computer-systems/cortex-a72-microarchitecture]]
- [[computer-systems/neoverse-n1-microarchitecture]]
- [[computer-systems/qualcomm-kryo-microarchitecture]]
- [[computer-systems/branch-predictor-design]]
- [[computer-systems/cache-coherence-cross-cluster]]

## 原文

- 链接：https://chipsandcheese.com/p/arms-cortex-a72-aarch64-for-the-masses
- 本地：`raw/articles/chipsandcheese.com/2023-11-10_arms-cortex-a72-aarch64-for-the-masses.md`
