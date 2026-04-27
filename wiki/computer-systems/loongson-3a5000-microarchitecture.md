---
tags: [cpu, 微架构, loongson, loongarch, mips, 中国芯片, 国产处理器]
date: 2026-04-27
sources: 1
---

# 龙芯 3A5000：中国最强自研 CPU 的一次快照

龙芯 3A5000（2021 年）搭载四枚 LA464 核心，是龙芯迄今最强的自研通用处理器。它也是龙芯从 MIPS64 兼容 ISA 迁移到自研 LoongArch ISA 后的第一代主力产品。

## ISA：LoongArch

龙芯在 3A5000 上放弃了对 MIPS64 编码的兼容，改用自研的 **LoongArch**（龙架构）：
- 语义与 MIPS64 高度相近（整数和浮点指令集），便于移植
- 使用全新、不兼容的指令编码
- 新增 **LSX**（128-bit 向量）和 **LASX**（256-bit 向量）扩展

从软件生态角度看，这是一次颇为冒险的决策：MIPS 软件生态本就不及 x86 和 ARM，重新定义编码意味着所有汇编优化代码需重写，而兼容层方案也难以提供高性能。

## 核心架构特征

LA464 是一款乱序执行核。整体 OoO 窗口大小与 [[phytium-ftc663-microarchitecture|Phytium D2000]] 相近（较小），但其他 OoO 缓冲区尺寸更合理。主频极低（约 **2.5 GHz**），这是 3A5000 性能最大的限制因素。

| 指标 | 3A5000 | Zen 1 | Neoverse N1 |
|------|--------|-------|-------------|
| 主频 | ~2.5 GHz | ~3.6 GHz | ~3.0 GHz |
| L1i  | 64 KB 4-way | 64 KB 4-way | 64 KB 4-way |
| L1D  | 64 KB 4-way | 32 KB 8-way | 64 KB 4-way |
| L2   | 256 KB | 512 KB | 1 MB |
| L3   | 16 MB（片级共享） | 8 MB | 32 MB（80 核共享）|

L1D 命中率低于预期——考虑到 64 KB 容量，其 miss 率显著高于使用类似几何的 Neoverse N1，推测替换策略或预取逻辑存在问题。

## 性能分析

**整数压缩（7-Zip）**：每周期指令数（IPC）与 Zen 1 相近，指令数差异 <5%，但 2.5 GHz 主频导致绝对性能远低于 Zen 1（约达到无 SMT 的 4 核 Ampere Altra 水平）。

**视频编码（libx264）**：3A5000 需执行 12–23% 更多指令才能完成同等工作，推测 LASX 缺少某些 AVX2/NEON 中已有的专用指令（如某些置换/洗牌指令）。性能明显落后 Zen 1 和 Altra。

分支预测准确率与竞品接近，但 LoongArch 程序中分支指令比例略高（17.7% vs x86 15.1%），且 IPC 相当时意味着绝对误预测次数更多。

## 与其他中国芯片的比较

Chips and Cheese 此前评测的 [[phytium-ftc663-microarchitecture|Phytium D2000]] 和 Zhaoxin KX-6640MA 在单核性能上弱于 3A5000。3A5000 有大缓存、合理的 OoO 设计，代表了中国自研 CPU 的阶段性高水位。但三者共同的问题是主频低且软件生态有限——一款 CPU 的性能再好，如果跑不起主流软件，价值也大打折扣。

## 参见

- [[phytium-ftc663-microarchitecture]] — 同期对比的另一款国产 ARM CPU
- [[neoverse-n1-microarchitecture]] — 性能参照点
- [[zen2-microarchitecture]] — 性能参照点

## Sources

- [[sources/chipsandcheese-loongson-3a5000]]
