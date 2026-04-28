---
tags: [source, cpu, risc-v, condor, cuzco, andes, ooo, hot-chips-2025, 微架构]
date: 2026-04-27
sources: 1
---

# Condor's Cuzco RISC-V Core at Hot Chips 2025（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2025 年 8 月的文章，深入分析 Condor Computing（Andes Technology 子公司）在 Hot Chips 2025 上展示的 Cuzco RISC-V 高性能核心，着重解析其"基于时间的调度"（time-based scheduling）这一核心创新。

## 摘要

Cuzco 是一款面向高端许可市场的 RISC-V 乱序核，与 SiFive P870 和 Veyron V1 同属高性能 RISC-V 设计梯队。其最大创新在于将调度逻辑从后端分布式调度器（issue queues）前移至重命名/分配阶段，由一个时间资源矩阵（TRM）对未来 256 个周期内的执行资源进行预测性规划，从而大幅简化后端调度器的复杂度。这种"时间调度"在功耗和面积上有潜在优势，代价是对指令延迟的预测出错时需要通过指令重放（replay）来修复。实测重放率约 70.07 次/千指令，Chester 认为尚在可接受范围。

## 关键要点

- 8-wide 乱序核，256 条目 ROB，12 级流水线，10 cycle 误预测惩罚
- 前端：TAGE-SC-L 分支预测器（基础 TAGE 表 16K bimodal 条目），8K 两级 BTB，32 条目 return stack
- **时间资源矩阵（TRM）**：重命名级维护，追踪未来 256 个周期内各执行资源使用情况；每个指令最多搜索 8 cycle 窗口寻找空闲资源槽位
- 后端调度器（XEQ）仅需按时间计数下发指令，无需动态检查依赖，从而降低功耗和面积
- 使用"毒化位（poison bit）"机制处理误调度：将错误执行结果标记为 poison，后继指令被迫重新执行
- 负载变延迟统一以 L1D 命中假设入表，L1D miss 通过重放处理；L3 命中导致某指令被重放三次（L1D miss → L2 miss → L3 hit）
- 向量支持 256/512-bit VLEN（多 µop），4 slices 时峰值 FP32 吞吐 8 FMA/cycle；FP add 延迟 2 cycle，FP MUL/FMA 延迟 4 cycle
- 2 MB L2 在 TSMC 5nm 上占约 1.04 mm²；通过 CHI 总线与片外 NoC 连接，支持多集群高核数配置

## 链接到的概念

- [[computer-systems/cuzco-riscv-core]]
- [[computer-systems/branch-predictor-design]]
- [[computer-systems/out-of-order-execution]]

## 原文

- 链接：https://chipsandcheese.com/p/condors-cuzco-risc-v-core-at-hot
- 本地：`raw/articles/chipsandcheese.com/2025-08-29_condors-cuzco-risc-v-core-at-hot-chips-2025.md`
