---
tags: [source, rendering, computer-systems, intel, igpu, xe-lpg]
date: 2026-04-27
sources: 1
---

# Intel's Ambitious Meteor Lake iGPU（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2024 年 4 月的文章，对 Meteor Lake（Core Ultra 7 155H）集成 GPU 进行架构分析与微基准测试，与 AMD Phoenix（Radeon 780M）对比。

## 摘要

Meteor Lake iGPU 采用 Xe-LPG 架构，等同于 Arc A770 的 1/4 规模：8 个 Xe Core，2 个 Render Slice，运行频率最高 2.25 GHz，峰值 4.5 TFLOPS FP32。系统层面，Intel 放弃了 Sandy Bridge 以来共享 CPU L3 的设计，改为通过 Scalable Fabric 连接独立 iGPU tile（TSMC 5nm），代价是跨 die 延迟约 10 ns。Xe-LPG 每个 Xe Core 有 192 KB L1（实测可用 160 KB）+ 独立 Texture Cache；全 GPU 共享 4 MB L2。寄存器分配采用静态方式（每线程固定 128 寄存器），占用率不受寄存器文件容量限制，与 AMD/NV 动态分配策略不同。并行 XVE 对锁步执行导致即便连续对齐的 SIMD16 组也可能出现分支发散惩罚。整体而言，Radeon 780M 计算吞吐和缓存带宽略胜，但 Meteor Lake 缓存容量更大，为光追加速提供关键支撑。

## 关键要点

- Xe-LPG = Xe-HPG 的 iGPU 版本（去除矩阵乘单元 XMX）
- 8 Xe Core × 16 XVE × 8 FP32 = 1024 FP32 lane，2.25 GHz → 4.5 TFLOPS
- 静态寄存器分配：每线程 128 寄存器，占用率不受寄存器数量约束
- L1 192 KB（实用 160 KB）+ Texture Cache（32 KB）；L2 4 MB 全局共享
- Scalable Fabric 替代 ring bus，跨 die 延迟 ~10 ns
- 成对 XVE 锁步导致 SIMD16 层面可能出现分支发散损耗
- 与 Phoenix 780M 总体持平；缺少 XMX 单元是明显短板

## 链接到的概念

- [[rendering/xe-hpg-architecture]]
- [[computer-systems/meteor-lake-chiplet-architecture]]
- [[computer-systems/intel-gen7-igpu]]
- [[computer-systems/xe-lpg-igpu-architecture]]
- [[computer-systems/amd-phoenix-soc]]
- [[computer-systems/van-gogh-steam-deck-apu]]

## 原文

- 链接：https://chipsandcheese.com/p/intels-ambitious-meteor-lake-igpu
- 本地：`raw/articles/chipsandcheese.com/2024-04-08_intels-ambitious-meteor-lake-igpu.md`
