---
tags: [source, computer-systems, risc-v, sifive, p550, microarchitecture, out-of-order]
date: 2026-04-27
sources: 1
---

# Inside SiFive's P550 Microarchitecture（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 1 月的文章，对运行在 Eswin EIC7700X SoC 上的 SiFive P550 进行完整微架构剖析，横向对比 Arm Cortex A75。

## 摘要

P550 是 SiFive 面向中等性能目标的 3-wide 乱序核心，13 级流水线，运行于 TSMC 12nm FFC 工艺、1.4 GHz。文章逐层测量分支预测器（9.1 KiB BHT、32 entry BTB、16 entry 返回栈）、前端（32 KB L1i、12 B/cycle 取指带宽）、乱序后端（寄存器文件、调度器、两个 AGU 分别专用于 load 和 store）、以及缓存层次（32 KB L1D、256 KB L2、4 MB 共享 L3）。P550 最严重的缺陷是非对齐访问：没有硬件支持，触发 OS trap 软件模拟，一次非对齐 load 耗费约 1062 核心周期。核心到核心延迟也偏高。整体性能与 Intel Core 2 或 Goldmont Plus 相当，明显弱于现代 Arm 大核，但对于 SiFive 而言代表着乱序设计能力的重要里程碑。

## 关键要点

- 3-wide OoO，13 级流水线，1.4 GHz / TSMC 12nm FFC
- 单纯 load/store 分离的双 AGU，与 Pentium Pro 权衡一致：性能损失不足 1%
- 非对齐访问无硬件支持，依赖 OS trap 软件模拟（~1062 周期），远落后于 A75 的 15 周期
- 32 entry BTB，16 entry 返回栈（A75 约 42 entry），返回栈溢出处理不够优雅
- 无向量扩展（V 扩展），FP 执行单元支持 add/mul/FMA（统一 FMA 路径，4 周期延迟）
- L3 38 cycle 延迟，DRAM 实测 194 ns，低于其他 LPDDR5 平台（Meteor Lake / Van Gogh）
- 目录式 cache 一致性，核心间传输延迟较高

## 链接到的概念

- [[computer-systems/sifive-p550-microarchitecture]]
- [[computer-systems/cortex-a72-microarchitecture]]
- [[computer-systems/branch-predictor-design]]
- [[computer-systems/memory-hierarchy]]

## 原文

- 链接：https://chipsandcheese.com/p/inside-sifives-p550-microarchitecture
- 本地：`raw/articles/chipsandcheese.com/2025-01-26_inside-sifives-p550-microarchitecture.md`
