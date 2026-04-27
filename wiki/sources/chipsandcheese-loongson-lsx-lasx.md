---
tags: [source, cpu, loongson, loongarch, simd, vector, lsx, lasx]
date: 2026-04-27
sources: 1
---

# Loongson's LSX and LASX Vector Extensions（Chester Lam / Chips and Cheese）

[[people/chester-lam]] 发表于 2023 年 2 月的文章，通过逆向工程与实测揭露龙芯 LoongArch 的 128-bit（LSX）和 256-bit（LASX）向量扩展的指令集语义、编码规则与执行性能。

## 摘要

文章针对龙芯未公开文档的 LSX/LASX 扩展，通过 Loongnix 工具链生成并反汇编指令来推断编码规律。主要发现包括：LSX/LASX 的寄存器别名设计与 x86 SSE/AVX 类似（XR0-XR31 覆盖 VR0-VR31 覆盖 F0-F31），但部分访问语义存在未定义行为——128-bit 操作会污染整个 256-bit 寄存器，与 x86 保留高位的策略截然不同。从性能角度，3A5000 的 LASX 实现为原生 256-bit 执行（非 128-bit 拆分），两个执行端口支持整数/逻辑操作双发射，但浮点端仅共享一个 FMA 单元，FP 延迟（5 周期）高于 Zen 1（3 周期），整体向量吞吐不及 Zen 1，与 Skylake 差距更大。

## 关键要点

- LASX 指令编码使用变长 opcode 以支持最多 4 个寄存器字段（类比 FMA4，非破坏性三操作数）
- 128-bit LSX 数学指令会作用于整个 256-bit 寄存器——上半部分不保留，违反 x86 惯例
- 跨页边界的部分寄存器加载会产生极不可预测的行为（随机读取相邻 cache line 或其他内存位置）
- 标量 FP 与向量混用时，3A5000 的 FP/向量重命名容量下降约 32 条目
- 3A5000 的 256-bit 向量 RF 容量为 4 KB（96 条重命名寄存器），Zen 1 为 128-bit 宽但有 160 条
- libx264 测试中 3A5000 落后 Zen 1，主因是低主频（2.5 GHz）和部分专用指令缺失

## 链接到的概念

- [[computer-systems/loongson-3a5000-microarchitecture]]
- [[computer-systems/simd-memory-bandwidth-bound]]
- [[computer-systems/fearless-simd]]

## 原文

- 链接：https://chipsandcheese.com/p/loongsons-lsx-and-lasx-vector-extensions
- 本地：`raw/articles/chipsandcheese.com/2023-02-26_loongsons-lsx-and-lasx-vector-extensions.md`
