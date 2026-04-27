---
tags: [cpu, 兆芯, x86, 微架构, 国产芯片, 乱序执行, avx2]
date: 2026-04-27
sources: 1
---

# 兆芯世纪大道（Century Avenue）微架构

世纪大道是兆芯（Zhaoxin）为 KX-7000 处理器开发的新一代 x86-64 微架构，也是其对前代 LuJiaZui（[[via-x86-isaiah-lujiazui]]）的全面升级。Chester Lam 在 Chips and Cheese 对 KX-7000 进行了详细的微基准测试分析。

## 背景

兆芯是上海市政府与 VIA Technologies 的合资企业，继承了 VIA 的 x86-64 授权。前代 LuJiaZui 是 2-wide 核心，ROB 仅 48 项，性能大约与 1997 年 Pentium II 相当，明显不足以服务现代应用软件生态。世纪大道的目标是在国产化背景下，达到能替代西方芯片的最低性能门槛。

## 核心概览

世纪大道是 4-wide、支持 AVX2 的乱序核心，192 项 ROB 容量与 Intel Haswell、AMD Zen 及 Centaur CNS 相当（[[centaur-cns-microarchitecture]]）。KX-7000 包含 8 个核心，采用类单 CCD Ryzen 的 chiplet 结构——8 核 CCD 共享 32 MB L3，加上独立 IO Die。工艺节点未官方披露，社区证据指向 6nm（TSMC 或 SMIC 7nm）。

## 前端

64 KB 16-way 指令缓存，16 bytes/cycle 取指带宽，4-wide 解码器，无 loop buffer 或 op cache。分支预测方向准确性较 LuJiaZui 大幅改善，能处理复杂规律模式；但分支目标缓存（BTB，4096 项）与 L1i 耦合，taken branch 延迟 3 周期，在 2024 年后设计中属于偏慢。缺乏 branch fusion（`cmp+jz` 须各占资源），不支持跨 L1i miss 的长距离预取。

## 重命名与乱序执行

从 LuJiaZui 的 ROB-based 改为基于物理寄存器文件（PRF）的方案，可显著分离 ROB 扩展与寄存器文件扩展。3 条 ALU 流水线 + 2 条 AGU；FP/向量侧有 4 条流水线，支持每周期 2 次 FP 运算，256-bit AVX2 FMA 吞吐与 Haswell 持平——但 256-bit 指令在内部被拆为 2 条 128-bit micro-op，ROB、调度器与寄存器文件占用均翻倍。

## 存储子系统

L1D 32 KB，8-way，4 周期 load-to-use，两个 128-bit 端口（仅一端口写）。L2 延迟 15 周期，容量较小（未披露）。L3 32 MB，延迟超 80 核心周期（27 ns），带宽约 8 bytes/cycle，明显弱于 Zen 2 及 Skylake-X。DRAM 内存控制器仅能训练到 1600 MT/s，读带宽实测不足 12 GB/s，八核共享队列导致 2 核以上读带宽不再提升，高并发下 latency 可飙至 1 μs。

## SPEC CPU2017 性能

整数套件单线程约与 AMD Bulldozer FX-8150 相当（Bulldozer 领先约 13.6%），浮点套件反超 Bulldozer 约 10.4%。多线程 libx264 和 7-Zip 测试中 KX-7000 甚至不及 Bulldozer（2011 年设计），根因在于低 L3 带宽、AVX2 的内部拆分代价以及前端瓶颈。

## 评价

世纪大道是兆芯向高性能进军的重要一步，从宏观架构设计看具有合理性。但从整体平衡性看，其前端延迟、AVX2 内部处理方式、L2 容量与 L3 延迟之间存在明显不协调，呈现出"把所有部件都做大，但没有系统性地保证整体均衡"的特征。这更像是一款以兼容为优先的最低成本 AVX2 实现，而非为性能最优化设计的现代核心。

## Sources

- [[sources/chipsandcheese-zhaoxin-kx7000]]
