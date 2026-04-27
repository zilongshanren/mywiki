---
tags: [source, computer-systems, x86, isa, risc-cisc, arm, loongarch, compatibility]
date: 2026-04-27
sources: 1
---

# Why x86 Doesn't Need to Die（Chester Lam / Chips and Cheese）

[[chester-lam]] 发表于 2024 年 3 月的文章，回应 Hackaday 一篇"x86 应该消亡"的文章，系统性反驳 RISC vs CISC 论战中的常见误解。

## 摘要

文章的核心论点与 [[isa-implementation-not-architecture]] 高度呼应：现代高性能 CPU（无论 x86 还是 ARM）都采用超标量、推测执行、乱序执行、寄存器重命名与多级缓存，这些设计与 ISA 无关。文章逐一驳斥 Hackaday 的具体指控：（1）x86 解码复杂——ARM 同样昂贵，均使用 micro-op cache 缓解，Arm 核心更有 predecode L1I；（2）复杂指令（如 mpsadbw）增加重命名开销——恰恰相反，等价的 RISC 指令序列需要更多重命名与调度条目；（3）ISA 扩展是 x86 特有——ARM 同样有 ASIMD/SVE/SVE2，LoongArch 有 LSX/LASX。文章还肯定了 x86 的软件生态兼容性价值：同一个 OS 安装盘可以在 Zen 4 和 15 年前的 Phenom 上运行；相比之下 ARM 手机软件生态高度碎片化，OS 支持生命期短暂。最后文章指出 Itanium 的失败（128 架构寄存器、静态调度、固定长度指令）恰恰说明 RISC 哲学在晶体管预算充足时并无优势。

## 关键要点

- RISC/CISC 哲学区别在 1990 年代初已基本失效；现代 CPU 同时具备复杂与简单指令
- 解码成本 ARM/x86 无本质差异：均使用 decoded µop cache；Cortex X2 有 predecode L1I
- 复杂指令（mpsadbw）实际**降低**重命名/调度压力，等价 RISC 序列更重
- 向量扩展跨 ISA 普遍存在：x86（AVX-512） ↔ ARM（SVE2） ↔ LoongArch（LASX）
- x86 兼容性优势：real mode 保留使同一 OS 跨越 15 年硬件；ARM 手机碎片化严重
- Itanium 失败验证：显式并行 + 静态调度 + 大寄存器堆的 RISC 极致路线被硬件 OoO 击败
- aarch64 今天在云端（Graviton、Ampere Altra）与 x86 竞争靠的是微架构与生态，而非 ISA 简洁性

## 链接到的概念

- [[computer-systems/isa-implementation-not-architecture]]
- [[computer-systems/loongson-3a5000-microarchitecture]]

## 原文

- 链接：https://chipsandcheese.com/p/why-x86-doesnt-need-to-die
- 本地：`raw/articles/chipsandcheese.com/2024-03-27_why-x86-doesnt-need-to-die.md`
