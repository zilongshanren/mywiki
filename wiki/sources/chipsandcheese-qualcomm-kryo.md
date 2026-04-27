---
tags: [source, cpu, qualcomm, arm, mobile, microarchitecture]
date: 2026-04-27
sources: 1
---

# Kryo: Qualcomm's Last In-House Mobile Core（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2023 年 7 月的文章，深入解析高通 Kryo 微架构——高通最后一款自研 64 位 ARM 移动处理器核，出现在 Snapdragon 820/821 中。

## 摘要

Kryo 于 2016 年随 Snapdragon 820 亮相，是高通继 Krait 之后的第一款 64 位自研核，也是最后一款。它采用 4-wide 乱序架构，拥有当时移动端最强的 ROB 容量和整数执行资源（4 个 ALU），前端支持零泡沫跳转，向量执行单元吞吐也优于同代 ARM Cortex-A72。文章通过反向工程和微基准测试还原其前端、后端、内存子系统结构，揭示其最大弱点：极慢的 store forwarding（13 周期）、无二级 TLB（仅有 192 entry L1 TLB）、L2 缓存小且延迟高（768 KB，25 周期），以及持续高负载下由热量导致的频率下压。Snapdragon 821 随后被 835 取代，高通此后改用定制化 ARM Cortex 核并沿用 Kryo 品牌名称，掩埋了原版 Kryo 的技术遗产。

## 关键要点

- 4-wide 乱序，Samsung 14nm；前端带宽和整数 ALU 数量媲美同期桌面核
- 零泡沫跳转（Zero bubble taken branch）：小于 8 KB 代码范围内的跳转无流水线清空开销
- Store forwarding 延迟极差（13 周期），几乎等同于 forwarding 失败的代价
- 仅单层 TLB（192 entry L1），超过 768 KB 数据集会触发高达 28 周期的 page walk 惩罚
- L2 小（768 KB / 512 KB）且延迟高（25/23 周期），实际延迟接近 Intel 大容量 L3
- 大小核采用同一微架构（不同 cache 配置），是当时独特的 hybrid 设计理念
- Kryo 之后高通改为定制 ARM 核，直到收购 Nuvia（2021）才重启自研路线

## 链接到的概念

- [[computer-systems/qualcomm-kryo-microarchitecture]]
- [[computer-systems/branch-predictor-design]]
- [[computer-systems/neoverse-n1-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/kryo-qualcomms-last-in-house-mobile-core
- 本地：`raw/articles/chipsandcheese.com/2023-07-13_kryo-qualcomms-last-in-house-mobile-core.md`
