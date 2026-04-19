---
tags: [x86, simd, mmx, sse, 指令集, 硬件乘法器]
date: 2026-04-19
sources: 1
---

# x86 SIMD 整数乘法指令的历史

x86 的 SIMD 整数乘法指令看起来一堆奇形怪状：`PMULLW` / `PMULHW` / `PMADDWD` / `PMULHUW` / `PMULUDQ` / `PMULHRSW` / `PMADDUBSW` / `PMULDQ` / `PMULLD` …… 为什么偏偏是这几条、而不是更整齐划一？[[fabian-giesen|Fabian Giesen]] 2024 年的文章用一条主线把这套乱麻串起来：**Intel 主流核心 25 年来一直围绕一个 16×16 → 32-bit 整数乘法器的数据通路做加法**，所有后来指令都是尽量少改这个核心。

## 核心不变量：16×16 乘法器

MMX（Pentium MMX）初代的三条指令本质上都是「四路 16×16 乘法，每路产出 32 bit 部分积」：

- `PMULLW`：取低 16 bit（signed/unsigned 等价）。
- `PMULHW`：取高 16 bit（signed）。高字取低字要算全 32 bit，硬件就顺手写成完整 16×16→32 单元。
- `PMADDWD`：两两相加成 32-bit dot product。从乘法器角度看，前 90% 的 partial product 合并完全一样，只在最后 10% 决定「是送低 16 还是做 32-bit 加」。

SSE 补上了 `PMULHUW`（unsigned 高字）——一个"加三角形到组合逻辑"的小改动。

## SSE2 如何不改乘法器搞定 64-bit 输出

`PMULUDQ` 做两路 32×32→64 bit 乘法。朴素想法是引入一个全新的 32-bit 乘法器，但其实不用：

$$a \cdot b = (a_1 b_1) \ll 32 + (a_1 b_0 + a_0 b_1) \ll 16 + a_0 b_0$$

这正是**四个 16×16 乘法 + 一个类 PMADDWD 的结构**，恰好匹配 64-bit 输出空间里的四个 16-bit lane。只是前后端多了一些 mux 把字节路由到合适的乘法器、末尾加法器做 64-bit 加。没有新乘法器。

## SSSE3 的两个变奏

- `PMULHRSW`：signed 16×16，带 rounding 的 `(a*b + 0x4000) >> 15`——在 reduction tree 里多挤进一个项的事。
- `PMADDUBSW`：8-bit unsigned × signed 乘法并两两相加成 saturated 16-bit。把 16×16 切成 byte 片更复杂，开始给内部实现加约束。

## SSE4.1 的 PMULLD：代价显形

`PMULLD`（32×32 取低 32）在只有 16×16 乘法器时需要**三个** 16-bit partial product（略去最高的 $a_1 b_1$），但每 32-bit lane 只分到两个乘法器。结果是 Intel big core 上 `PMULLD`：**2 uops、latency 2×**、throughput 1/2。Giesen 的猜测：第一条 uop 做 PMADDWD 样式的中段项、第二条做低位项并合并。一致的证据是 `PMULUDQ` 8 年间都只占 1 uop，直到 PMULLD 出现才突破约束。

AMD Zen 和 Intel E-core 终于配了真正的 32×32 乘法器；`PMULLD` 在它们上面回归 1 uop。

## AVX-512 的 `VPMULLQ`、IFMA、VNNI

- `VPMULLQ`：3 uops。如果用 double 浮点乘法器的 52×52→104 bit 尾数通路复用，三次 52-bit 乘法组合出 64×64→64 也合理。
- **IFMA**：显式借用 FP64 乘法器的尾数路——完全不同的设计约束。
- **VNNI**：PMADDWD 风格加一次累加，AVX2 之后本就是 3-operand 数据通路，把加法再挤一项几乎免费。

## 启示

这套历史对系统程序员有两个现实意义：一是**选指令要看 uop 数和 port，不是看"名字像 32-bit 就是一条 32-bit 乘法"**；二是 x86 的"为什么不统一"经常背后是一条沿用 25 年的硬件数据通路——改 ISA 容易，改芯片难。

## 相关

- [[fabian-giesen]]
- [[sse-tricks]]
- [[carry-save-adder-pixel-avg]]
- [[fearless-simd]]

## Sources

- [[sources/ryg-why-those-particular-integer-multiplies]]
