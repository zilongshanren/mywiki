---
tags: [arm, cpu, microarchitecture, mobile, little-core, in-order]
date: 2026-04-27
sources: 1
---

# Cortex-A510 微架构

Arm Cortex-A510 是 2021 年发布的 ARMv9 小核（"5 系列"），搭档 [[cortex-a710-microarchitecture]] 和 Cortex-X2 构成 DynamIQ 三层集群。与前代 A55 相比，A510 最核心的变化是从 2 宽增加到 **3 宽顺序执行**，并引入了两核共享资源的"合并核（merged core）"配置。

## 前端与分支预测

A510 维持 8 级流水线，但解码阶段扩展为 3 个周期（前代 A55 仅 1 个周期），以容纳更宽的解码器。分支预测采用两级 BTB：64 条目的 L1 BTB 提供单周期延迟，约 512 条目的 L2 BTB 延迟 2 个周期；返回栈仅 8 条目，深度调用栈场景性能有限。

L1i 可配置 32 KB 或 64 KB，4 路组相联，伪随机替换策略（省去 LRU 位但可能降低命中率）。

## 执行引擎

执行端接近顺序，但 A510 相较 A53 改进了非阻塞 load 能力：可在两次缓存缺失之间 overlap 最多 12 条指令（A53 为 8 条）。整数加法/逻辑/比较可 3 发射，但分支与乘法不能同时发射。

浮点/向量部分是 A510 的独特设计点：在合并核配置下，两颗核共享一个 FPU（Snapdragon 8+ Gen 1 选择 2×64-bit 共享 FPU），每核每周期最高获得 128-bit 向量吞吐。这以降低峰值 FP 性能为代价换取面积效率。

## 共享资源设计

A510 的合并核策略借鉴了 [[bulldozer-microarchitecture]] 的"模块化"思路，但目标完全不同：

- **共享 FPU**：A53/A55 的 FPU 在实际负载中利用率低，共享设计合理。
- **共享 L2 缓存**：128 KB（Snapdragon 8+ Gen 1），8 路，可选 ECC。两核同时压 L2 时带宽不成线性扩展。
- **共享 L2 TLB**：2048 条目（4 路），较 A55 翻倍；但顺序执行核对 TLB 缺失延迟极敏感，共享有潜在的多线程性能代价。

实际测试（Snapdragon 8+ Gen 1）显示 A510 时钟上限约 1.8 GHz，远低于标称的 2.016 GHz。

## 缓存与内存

- L1d：32 KB 或 64 KB，4 路，VIPT，伪随机替换
- L2（可选）：128–512 KB，8 路，与两核共享
- L1 DTLB：16 条目全相联；L2 TLB：2048 条目，两核共享
- DRAM 延迟（Snapdragon 8+ Gen 1）：超过 300 ns，属移动平台典型水准

## 定位

A510 不与大核竞争性能，而是以最小面积和功耗承载后台任务与轻负载。共享资源的成功验证了 Arm "5 系列"的演进方向，且已在 Snapdragon 8+ Gen 1 的量产 SoC 中部署。

## Sources

- [[sources/chipsandcheese-cortex-a510]]
