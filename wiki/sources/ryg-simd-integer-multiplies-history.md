---
tags: [source, 计算机体系结构, SIMD, x86, 硬件乘法器]
date: 2026-04-19
sources: 1
---

# Why those particular integer multiplies?（Fabian Giesen / ryg）

[[fabian-giesen|Fabian Giesen]] 2024 年 10 月的文章，追溯 x86 SIMD 整数乘法指令集从 MMX 到 AVX-512 的演化，并给出了一套「所有这些指令几乎都能用一组 16×16 → 32 位乘法器硬件实现」的猜测性解读。

## 摘要

Pentium MMX 时代的 PMULLW / PMULHW / PMADDWD 三条指令用同一组四路 16×16 → 32 位乘法器硬件就能全覆盖：低 16 位、高 16 位、两两求和成 32 位。SSE 时代补了 PMULHUW（unsigned 高位）。SSE2 引入的 PMULUDQ 看起来是 32×32 → 64，但 ryg 指出它可以通过 `a = a1·2^16 + a0, b = b1·2^16 + b0` 的拆分变成四路 16×16 再拼接，依然复用 MMX 的硬件。SSSE3 的 PMADDUBSW 把字节做 unsigned×signed 然后 saturating 累加，硬件代价开始上升。到 SSE4.1 的 PMULLD（双字乘低位）情况就变得诡异——Intel 大核上是 2 uops、延迟翻倍，ryg 的推测是因为每 32-bit lane 需要三次 16×16 乘法但硬件只有两路，被迫两拍完成。VPMULLQ 在 Intel 大核要 3 uops，很可能把 double-precision 浮点乘法器的 52×52 → 104 尾数路径复用进来（IFMA 也是如此）。

## 关键要点

- **PMADDWD 是 MMX 设计的一块隐藏的美玉**：硬件里 16×16 乘法本来就是分 partial product 算的，最后把两条 32-bit 结果合并只需要在已有 reduction tree 上多加一级——几乎白送。
- **PMULUDQ 的 4-subproduct 拆分**是理解后续所有 doubleword 乘法的钥匙——`a1·b1 << 32 + (a1·b0 + a0·b1) << 16 + a0·b0`，每一项都是 16×16。
- **PMULLD 为何贵**：每 32-bit lane 需要 3 个 16×16（忽略顶部不需要算的那块），但每 32-bit lane 只能分到 2 个 16×16 乘法器。于是分两拍，Intel 大核上是 2 uops、延迟翻倍、吞吐减半。
- **AMD / Intel E-core 的另一条路**：干脆给 32×32 → 32 乘法器单独添加，不再纠结能不能复用 16-bit 硬件。
- **IFMA 的身世**：「用 double 浮点乘法器的尾数路径来做 52-bit 整数乘」，这也是 VPMULLQ 能用 3 uops 做 64×64 的合理猜测。
- **评论区补充**：候选理论「每隔一 lane 才有一个 32×32 乘法器」可以同时解释 PMULUDQ (1 uop) / PMULLD (2 uop) / VPMULLQ (3 uop) 的阶梯；但 Karatsuba 在这里行不通，因为它要求 adder topology 不一样。

## 链接到的概念

- [[x86-simd-integer-multiplies]]
- [[sse-tricks]]
- [[faster-math-functions]]
- [[fabian-giesen]]

## 原文

- 链接：https://fgiesen.wordpress.com/2024/10/26/why-those-particular-integer-multiplies/
- 本地：`raw/articles/fgiesen.wordpress.com/2024-10-26_why-those-particular-integer-multiplies.md`
