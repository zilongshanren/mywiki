---
tags: [SIMD, SSE, x86, little-endian, 调试]
date: 2026-04-19
sources: 1
---

# `_MM_SHUFFLE` 宏的端序约定

从 Altivec/PPC 走到 x86 SSE，最容易崴脚的不是指令集本身，而是 **`_MM_SHUFFLE` 宏的参数顺序**。[[ben-supnik|Supnik]] 2011 年 5 月在把 X-Plane 的 uniform transform 搬到 CPU 侧 SIMD 时，为这条花了 15 分钟才想明白。

## 现象

```c
float le[4] = {0, 1, 2, 3};
__m128 aa = _mm_loadu_ps(le);
__m128 cc = _mm_shuffle_ps(aa, aa, _MM_SHUFFLE(3, 3, 3, 1));
```

直觉以为 `cc = {3, 3, 3, 1}`（把宏参数当作数组下标顺序），但内存/GDB 里看到的是 `{1, 3, 3, 3}`。

## 机制：`_MM_SHUFFLE` 参数从高位到低位写

`_MM_SHUFFLE(a, b, c, d)` 打包成 8-bit 立即数 `aabbccdd`（每个参数 2 bit）。**最左的 `a` 落在最高位，最右的 `d` 落在最低位**。于是：

- `_MM_SHUFFLE(3, 3, 3, 1)` = `0b11111101` = `0xFD`。
- `SHUFPS` 指令按**低位 → 高位**的顺序选通道：低两位 `01` 选进结果的 lane 0 → `aa[1]`。
- Lane 顺序在 x86 里与「数组下标 = 内存低地址 = 低位」对齐，所以 lane 0 就是 `cc[0]`，结果 `{1, 3, 3, 3}` 完全合规。

换言之：**要按「数组下标顺序」读 `_MM_SHUFFLE`，必须从右往左读参数列表**。这是 little-endian 机器上「bit 位值」与「内存顺序」对齐的副产品。

## 画图时的惯例陷阱

Intel 手册里的 SSE 向量图通常把 lane 0 画在**最右边**——因为我们从左到右写十进制数时，个位在右。但 `_mm_srli_epi64`（PSRLQ，逻辑右移）把 bits 朝 lane 0 方向移；`_mm_bsrli_si128`（PSRLDQ）右移字节，把零从 lane 15 补进来。所以**调试注释里把向量写成 `[D C B A]`**（高 lane 在左、低 lane 在右、与数字书写惯例一致）比写成 `[A B C D]` 更少出错。

## 教训

- 树倒了没人看见——只要不 dump 到内存、寄存器里的 lane 顺序在不在「自然顺序」上不会影响程序正确性。
- 出门前要确认的不是每条 SSE 指令的时序，而是「`_MM_SHUFFLE` 参数怎么写、lane 0 在寄存器哪一端、内存里什么样」三件事对齐。
- 文章标题的错别字（*Seriosly*）Supnik 自己没改。

## 相关

- [[sse-tricks]] —— 老 SSE 的其他非正交坑
- [[simd-memory-bandwidth-bound]] —— 同月 Supnik 后续：SSE 加速被内存带宽吃掉
- [[aos-vs-soa]]
- [[ben-supnik]]

## Sources

- [[sources/supnik-sse-shuffle-endianness]]
