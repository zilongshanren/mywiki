---
tags: [source, computer-systems, cpu, arm, microarchitecture, efficiency]
date: 2026-04-27
sources: 1
---

# Arm's Cortex A73: Resource Limits, What are Those?（Chips and Cheese）

[[chester-lam]] 发表于 2024 年 7 月的文章，在 Amlogic S922X（Odroid N2+）上对 Cortex-A73 进行了详细的微基准测试，并与 A57（Nintendo Switch）和 A72（AWS Graviton 1）进行对比。

## 摘要

Cortex-A73（2016 年）是 ARM 在 A57/A72 热节流问题后的效率优先重设计：2 宽乱序核，以"无限乱序容量"（slot 机制，ROB 不可测）为特色，通过削减宽度和调度器规模换取稳定频率。前端 BTB 能力有限（L1 仅 48 项，2 周期），整数调度 6 项，FP FMA 延迟 7 周期。L1D 切换为 VIPT（3 周期），伪随机替换。实测显示在 Amlogic 平台上 L2 性能偏弱（Amlogic 仅配 1 MB），DRAM 带宽为 32 位 DDR4-2640 所限。A73 最终说服高通回归 Cortex 授权（骁龙 835），为 ARM 重拾大厂信任奠定基础。

## 关键要点

- 2 宽前端，slot 机制使 ROB 理论无上限
- L1 BTB 48 项，2 周期；主 BTB ~3072 项，与 L1i 绑定
- 整数 ALU 调度队列仅 6 项，专用 Branch 端口
- L1D：VIPT，3 周期，8 路，伪随机替换
- Store forwarding 快路径 4–5 周期
- L2 实测带宽远低于规格（Amlogic 实现限制）
- DRAM：32 位 DDR4-2640，实测 ~8 GB/s

## 链接到的概念

- [[cortex-a73-microarchitecture]]
- [[branch-predictor-design]]
- [[qualcomm-kryo-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/arms-cortex-a73-resource-limits-what-are-those
- 本地：`raw/articles/chipsandcheese.com/2024-07-18_arms-cortex-a73-resource-limits-what-are-those.md`
