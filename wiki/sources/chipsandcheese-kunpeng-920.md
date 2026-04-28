---
tags: [source, cpu, arm, huawei, kunpeng-920, taishan-v110, 微架构, chiplet]
date: 2026-04-27
sources: 1
---

# Huawei's Kunpeng 920 and TaiShan v110 CPU Architecture（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 7 月的文章，通过微基准系统性地测量了 Kunpeng 920 的系统架构与 TaiShan v110 核心微架构，并与同代 Arm Neoverse N1、AMD Zen 2、Intel Goldmont Plus 进行横向对比。

## 摘要

Kunpeng 920 是华为 HiSilicon 的自研 chiplet 服务器 CPU，采用 TSMC 7nm CoWoS 封装，由 Super CPU Cluster（SCCL）计算 die 与独立 IO die 组成。其独特特性包括：将 L3 tag 放置于 CPU cluster 而非 L3 数据 bank、三种 L3 工作模式（Shared/Private/Partition）以及多 SCCL 之间的 NUMA 拓扑。TaiShan v110 是华为第一代自研 AArch64 核心，4-wide 乱序执行，定位与 ARM Neoverse N1 类似但性能差距明显。测试结论：Kunpeng 920 的 chiplet 策略和动态 L3 分区机制是创新性尝试，但 TSMC 7nm 的工艺优势未能充分发挥，Neoverse N1 在同节点上明显更优，Zen 2 更是遥遥领先。

## 关键要点

- Kunpeng 920 使用 CoWoS 封装，SCCL（7 nm）+ IO Die（16 nm）+ 65 nm 中介层
- L3 tag 放在 CPU cluster，L3 data bank 独立布置，通过 ring bus 互联（21 个 stop/SCCL）
- L3 三模式：Shared（全局共享）、Private（cluster 私有）、Partition（默认，动态调整）
- Partition 模式下单核 L3 延迟约 36 cycle，共享模式下延迟超 90 cycle
- 数据共享时 L3 进入 shared 模式，cluster 内部共享时表现异常（同 cluster 两核也会触发）
- TaiShan v110：4-wide OOO，3 整数 ALU + 1 多周期端口，双端口 FPU，512 KB L2
- 分支预测采用双级动态预测器，准确率与 Goldmont Plus 相当，明显弱于 Zen 2 和 Neoverse N1
- SPEC CPU2017 整数分：领先 Cortex A72 +22.5%、Goldmont Plus +7%，落后 Neoverse N1 -34%
- DRAM 带宽约 63 GB/s（DDR4-2400 双 channel），延迟 96 ns（中等），高负载下延迟急剧上升

## 链接到的概念

- [[computer-systems/kunpeng-920-taishan-architecture]]
- [[computer-systems/xuantie-c910-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/huaweis-kunpeng-920-and-taishan-v110
- 本地：`raw/articles/chipsandcheese.com/2025-07-22_huawei-s-kunpeng-920-and-taishan-v110-cpu-architecture.md`
