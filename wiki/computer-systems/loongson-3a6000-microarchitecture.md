---
tags: [cpu, loongson, chinese-cpu, microarchitecture, la664]
date: 2026-04-27
sources: 1
---

# 龙芯 3A6000 微架构（LA664）

龙芯 3A6000 是目前中国自研 CPU 中性能最强的产品之一，搭载 LA664 核心，运行频率 2.5 GHz，四核心配置，首次引入 SMT。在单线程、每核对比中达到 AMD Zen 1 水平。

## 架构概览

LA664 在 LA464（3A5000，参见 [[loongson-3a5000-microarchitecture]]）基础上进行了系统性升级：

| 维度 | LA464（3A5000） | LA664（3A6000） |
|------|----------------|----------------|
| 发射宽度 | 4 宽 | 6 宽 |
| SMT | 无 | 2-way |
| ROB 容量 | 中等 | 接近 Zen 3 |
| L1D 延迟 | 4 周期 | 3 周期 |
| L2 延迟 | 14 周期 | 12 周期 |
| DRAM 延迟 | 144 ns（DDR4 控制器极差） | 104 ns（大幅改善） |
| L3 带宽（多核） | 明显竞争争用 | 基本线性扩展 |

## 前端与分支预测

LA664 的分支预测器是相对于 3A5000 最引人注目的升级之一。3A5000 的分支预测器接近 2000 年代初期水平；LA664 的准确率提升至与 Zen 2 相当，与近代 x86 CPU 处于同一量级，仅落后于 Zen 3 的双级覆盖预测器方案。参见 [[branch-predictor-design]]。

BTB 设计上，LA664 使用 64 KB 大型 L1i 缓存承担 BTB miss 时的指令供给，而非引入独立的大容量解耦 L2 BTB（Intel 和 AMD 的做法）。这一选择类似 Tachyum Prodigy（[[tachyum-prodigy-architecture]]），降低了时钟频率的复杂度，但代价是当指令流溢出 L1i 时 IPC 下降较明显。

## 乱序执行引擎

LA664 将 ROB 容量扩展至接近 Zen 3，是 3A5000 的显著升级。整数调度器为统一设计（相比 Zen 2 分布式调度器）；浮点/向量调度器使用水位线（watermarked）共享。SMT 实现保守，ROB、寄存器堆、load/store 队列均静态对半分配——对于首代 SMT 实现是合理选择，避免了更激进共享策略（如 Zen 2 整数调度器的竞争共享）所带来的验证风险。

## 浮点与向量执行

LA664 最亮眼的改动之一是向量 FP 加法从 2 管道扩展至 4 管道（256-bit），超过 AMD Zen 2/3 和 Intel Golden Cove 的 2 管道 256-bit 加法能力。然而 FMA 吞吐量维持不变（1 FMA/cycle），仍是 Zen 2 的一半。此外标量 FP 运算仅有 2 管道处理，且标量 FP 乘和向量乘使用不同端口，存在设计不一致。

L1D 写带宽达 512 B/cycle，与 Intel Golden Cove 并列，是目前消费级核心中罕见的水平。

## 内存子系统

3A5000 的 DDR4 控制器极差（144 ns），3A6000 大幅改善至 104 ns，但对于 DDR4-2666 双通道单芯片设计而言仍不算出色。实际 DRAM 读带宽仅与 Intel Core i5-6600K（DDR4-2133）相当，远低于同频率的 Zen 2 平台。

## 定位与局限

LA664 的单核性能约等于 Zen 1，代表中国自研 CPU 的重大突破，但距离现代主流 CPU（Golden Cove、Zen 4）仍有显著差距：
- 仅为四核配置，缺乏 Zen 1 当年靠多核数取胜的路线
- 主频 2.5 GHz，绝对延迟因此偏高，即便 IPC 有竞争力
- 软件生态仍是更大挑战

## Sources

- [[sources/chipsandcheese-loongson-3a6000]]
