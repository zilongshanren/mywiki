---
tags: [source, computer-systems, cpu, ampere, arm, server, density, cloud, hot-chips]
date: 2026-04-27
sources: 1
---

# AmpereOne at Hot Chips 2024: Maximizing Density（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2024 年 8 月的文章，结合 Hot Chips 2024 演讲与 Oracle 云实例实测，深度解析 Ampere Computing 自研服务器核心 AmpereOne 的微架构设计理念。

## 摘要

AmpereOne 是 Ampere Computing 首款完全自研服务器 CPU（此前 Altra 授权自 Arm Neoverse），目标是在不依赖工艺节点缩放的前提下，通过架构设计最大化单芯片可服务的用户密度与性能一致性，为此牺牲了 SMT 和动态频率调整。核心以 3.7 GHz 运行，芯片采用 TSMC 5nm + 7nm 混合 chiplet 设计（计算/PCIe/内存控制器分离）。

前端设计有意押注低延迟：16 KB L1i 缓存（相对细小）+ 低延迟 L2 直通路径，实现 10 周期分支预测失误恢复（Zen 4 约 11-18 周期）。分支预测器使用 8 表 TAGE，8K 项 BTB；支持最高 5 指令/周期扫描以利用指令融合，宣称融合激进度为业界最高。后端有 8 组调度器（192 项总容量）供给 12 条执行管道，整数调度器每个约 20 项，FP/向量调度器约 2×24 项（相对其性能定位偏浅）。L1D 64 KB 写直达（write-through）设计，有高带宽 L2 写通路支撑。私有 2 MB L2 是密度优化策略的核心：提供 11 周期延迟与充足容量，隔离核心与高延迟 mesh 系统。系统级采用基于 Arm CMN 网格（自定义扩展）的 8×9 mesh，配合"自适应流量管理"使各核对下游压力进行背压反应。实测综合 IPC 接近 Intel Skylake，FP/向量侧弱于 Crestmont，符合其密度而非性能定位。

## 关键要点

- 设计目标：密度、一致性、安全隔离（no SMT，no 动态频率），非 peak 性能
- 前端：16 KB L1i（有意缩小以降低 mispredict 恢复延迟），8 表 TAGE 分支预测器，10 周期恢复
- 指令融合：5 指令/周期扫描，4 微操作/周期发射，自称融合最为激进
- 后端：8 组调度器、192 总项；FP/向量 2×24 项（偏浅）；整数每组约 20 项
- L1D：64 KB 写直达；L2：2 MB，11 周期延迟，高带宽设计
- Chiplet：计算 die（5nm）+ PCIe/内存 die（7nm）；最高 8/12 通道 DDR5
- 内存标记（MTE）：首个数据中心级实现，无带宽/容量开销
- 自适应流量管理：下游压力反馈给核心，延迟敏感与带宽密集型工作负载差异化响应
- 综合 IPC：接近 Skylake；FP/向量侧弱于 Crestmont；非峰值性能追求

## 链接到的概念

- [[computer-systems/ampereone-microarchitecture]]
- [[computer-systems/branch-predictor-design]]
- [[computer-systems/neoverse-v2-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/ampereone-at-hot-chips-2024-maximizing-density
- 本地：`raw/articles/chipsandcheese.com/2024-08-29_ampereone-at-hot-chips-2024-maximizing-density.md`
