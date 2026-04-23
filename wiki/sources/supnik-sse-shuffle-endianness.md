---
tags: [source, SIMD, SSE, x86, X-Plane]
date: 2026-04-19
sources: 1
---

# Seriosly Strange Execution?（Ben Supnik / The Hacks of Life）

[[ben-supnik|Supnik]] 2011 年 5 月 17 日的 debug 小记（标题的 *Seriosly* 错别字原文保留），从 PPC/Altivec 换到 x86 SSE 后第一次被 `_MM_SHUFFLE` 的参数顺序绊倒。

## 摘要

`_mm_shuffle_ps` 吃一个 8-bit 立即数，`_MM_SHUFFLE(3,3,3,1)` 打包成 `0xFD`。Supnik 本以为结果应该是 `{3,3,3,1}`，实际是 `{1,3,3,3}`。拆开看：宏参数**从高位到低位**写，最右的 `1` 落在最低两位 `01`，这两位选进 lane 0，于是 lane 0 = `aa[1]` = 1。整套约定是 little-endian 下「bit 值位」与「内存 / 数组下标」对齐的副作用——读宏时要从右往左读才能得到「数组下标顺序」。Supnik 随后把 `%xmm0` 的 128-bit 值与 `cc` 在内存里的字节顺序都 dump 出来做了 15 分钟心理斗争，结论是：**只要不 dump 到内存，寄存器内部 lane 顺序对程序正确性是透明的**——写代码把 `__m128` 当 `float[4]` 即可，调试注释里把向量写成 `[D C B A]`（高 lane 在左）比 `[A B C D]` 少出错。顺带一提：`_mm_srli_epi64`（逻辑右移）与 `_mm_bsrli_si128`（字节右移）印证了 lane 0 就是「低位」。

## 关键要点

- `_MM_SHUFFLE(a,b,c,d)` 打包成 `aabbccdd`（a 在最高 2 位）
- Lane 0 ≡ 低位 ≡ 内存低地址 ≡ 数组下标 0
- 要按「数组下标顺序」读宏，必须从右往左读参数
- Intel 手册把 lane 0 画在右边是「数字书写习惯」的工件
- 调试注释用 `[D C B A]` 格式与移位语义更一致
- 实用结论：不用 dump 内存 → lane 顺序不影响正确性

## 链接到的概念

- [[sse-shuffle-endianness]]
- [[sse-tricks]]
- [[simd-memory-bandwidth-bound]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/05/seriosly-strange-execution.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-05-17_seriosly-strange-execution.md`
