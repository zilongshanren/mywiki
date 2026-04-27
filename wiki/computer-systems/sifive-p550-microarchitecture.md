---
tags: [risc-v, sifive, p550, microarchitecture, out-of-order, cpu, low-power]
date: 2026-04-27
sources: 1
---

# SiFive P550 微架构

P550 是 SiFive 面向中低功耗应用场景的 3-wide 乱序（Out-of-Order）RISC-V 核心，目标是在严格的功耗和面积约束下实现相对竞争性的性能。SiFive 将 P550 定位为"最高单位面积性能"，并声称比同级 Arm Cortex A75 拥有超 30% 的性能提升，占用不足一半面积。

## 总体概览

P550 是 13 级流水线的乱序核心，实测于 Eswin EIC7700X SoC（TSMC 12nm FFC，1.4 GHz），搭配 4 MB 共享 L3 和 16 GB LPDDR5-6400 内存。其乱序执行窗口与 Intel Core 2 或 [[goldmont-plus-microarchitecture]] 相当，远小于现代 AMD/Intel 大核。

## 前端

- 32 KB 4-way L1i，提供约 12 byte/cycle 取指带宽
- 单线程可维持 3 IPC（代码在 L1i 内）；L2 命中约 2 IPC，L3 命中约 1 IPC
- 9.1 KiB 分支历史表（BHT），模式识别能力合理但远弱于高性能核心
- 32 entry BTB（单级），超出后由 L1i 直接计算目标地址（约 3 周期 L1i 延迟）
- 16 entry 返回栈，溢出时处理不优雅，导致大量 mispredict（A75 返回栈约 42 entry）

## 后端执行引擎

整数侧有灵活的多端口调度器（比 A75 更灵活），浮点侧有两个 FP 端口，支持 add/mul/FMA 统一由 FMA 单元处理（4 周期延迟）。P550 没有向量扩展（RISC-V V 扩展），是当前最明显的功能缺口。

存储访问采用 load AGU 与 store AGU 分离设计（不可互换），与 Intel Pentium Pro 的权衡相同：实测性能损失不到 1%。不支持非对齐访问硬件处理——触发 OS trap 软件模拟，单次非对齐 load 耗费约 1062 周期（A75 最差情况仅 15 周期），是 P550 最严重的工程缺陷。

## 缓存层次

| 级别 | 大小 | 相联度 | 延迟 | 带宽 |
|------|------|--------|------|------|
| L1D  | 32 KB | 4-way | 3 周期 | 16 B/cycle |
| L2   | 256 KB | 8-way | 13 周期 | 8 B/cycle |
| L3   | 4 MB（共享）| — | ~38 周期 | 8 B/cycle/核 |
| DRAM | — | — | ~194 ns | ~16.74 GB/s |

L2 的 8 B/cycle 带宽偏窄，但对于无向量能力的核心尚可接受。DRAM 延迟 194 ns 显著高于同类 LPDDR5 平台（如 Meteor Lake、Van Gogh），说明 EIC7700X 的片上网络或内存控制器实现有待优化。

## 一致性与核间通信

使用目录式（directory-based）缓存一致性，适合多核/多集群扩展。核间传输延迟测试结果偏高，说明互连设计仍有完善空间。

## 定位与意义

P550 代表 SiFive 从微控制器领域向中性能应用处理器跨越的关键一步。类比来看，P550 更接近 Arm Cortex A57 的成熟度水平，而非已经打磨良久的 A75。SiFive 已公布更激进的 P870 设计，P550 是这一系列的技术基础。对于 RISC-V 生态，P550 的价值在于验证了乱序执行在该 ISA 下的可行性，尽管与 x86/Arm 主流高性能核心仍有相当差距。

## Sources

- [[sources/chipsandcheese-sifive-p550]]
