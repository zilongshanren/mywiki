---
tags: [source, SIMD, x86, 优化]
date: 2026-04-14
sources: 1
---

# SSE: mind the gap!（Fabian Giesen）

[[fabian-giesen|Fabian "ryg" Giesen]] 2016 年 4 月的长帖，集中归纳了在 SSE/SSE2 这两个「最低公约数」SIMD 指令集上写代码必须知道的几十个 trick。这是一篇典型的 ryg 风格——既讲指令本身的非正交性，也顺手澄清了一堆 microarchitecture 谣言。

## 摘要

SSE2 是史上**最非正交**的 SIMD 指令集之一：很多操作只有部分数据类型支持，毫无规律可言。SSE4.1 之后慢慢补齐，但跨代代码仍不得不绕。文章按主题给出技巧：
- **branchless select**：`and / andnot / or` 三件套（SSE4.1 起 `_mm_blendv_*` 更短）。
- **无符号比较**：用 `0x80000000` XOR 偏移到有符号区间，或用 unsigned min/max 转化。
- **整数 min/max**：SSE2 只有 uint8 / int16，其余要 SSE4.1 或自己合成。
- **整数乘法迷宫**：`PMULLD` 慢且要 SSE4.1，`PMULUDQ` 只用偶数 lane，`PMADDWD` 在数值落入 int16 时是隐藏的 «32-bit 乘法» 神器。
- **「水平」操作的真相**：浮点 `HADDPS` / `DPPS` 永远是宏指令，速度并不比手动展开快；真正快的水平加在整数侧的 `PSADBW`。
- **load/store intrinsic 的命名陷阱**：`_mm_loadl_epi64` 实际是 64-bit 不对齐 load，`_mm_cvtsi32_si128(*p)` 才是 32-bit load。

文末和评论区有一段精彩的「不要把 select 写成 `b + (a-b)·cond`」的辩论：那种 FP 算术 trick 既不正确（小数 + 大数相消时丢精度、Inf/NaN 出错），延迟也比 mask 版本更长。ryg 顺带普及了 Intel 自 Core 2 之后「执行端口」「bypass cluster」的真实模型——bypass 延迟是延迟而非吞吐惩罚，throughput-bound 的 SIMD 代码根本观察不到。

## 关键要点

- **「想做 SIMD 性能就别指望水平指令」**——用 [[aos-vs-soa|SoA]] 或 transpose 后整批处理。
- **`PMADDWD` 是 SSE 中最被低估的指令**：当 32-bit lane 实际值在 int16 范围内，一指令完成 4 路乘法。`PSADBW` 是最快的 8 路水平加。
- **常量构造的迷信要小心**：用 `pcmpeqd reg,reg` 造 all-ones 看起来省一次 load，但在所有现代 x86 上 load-op 形式的常量比指令构造更便宜，编译器还会把它 hoist 出循环。
- **关于 bypass 延迟的真相**：ANDPS vs PAND 的差别只在跨 cluster 时才有 1 cycle 的 bypass，且只算在依赖路径上、不影响 throughput——和大量教程里的说法不一样。
- **延迟 ≠ 卡顿**：很多人对延迟过度焦虑，乱序执行会自然把多次迭代重叠起来；只有非常长的串行依赖链才真正暴露延迟。

## 链接到的概念

- [[sse-tricks]]
- [[fabian-giesen]]
- [[aos-vs-soa]]
- [[latency-vs-throughput]]

## 原文

- 链接：https://fgiesen.wordpress.com/2016/04/03/sse-mind-the-gap/
- 本地：`raw/articles/fgiesen.wordpress.com/2016-04-03_sse-mind-the-gap.md`
