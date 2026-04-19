---
tags: [渲染, gpu, 硬件实现, ieee754, 数值精度]
date: 2026-04-19
sources: 1
---

# UNORM / SNORM 到 float 的硬件级实现

[[unorm-float-conversion]] 页面讲了**软件**上的精确 UNORM8 → float32 构造（几何级数展开、两次乘加即可）。[[fabian-giesen|Fabian Giesen]] 后续文章回答了另一个角度：**硬件里**做这件事要付出什么代价。答案：几乎不需要任何额外面积——一个 LZ 计数 + 一个 16-bit 加法器就够了。

## 关键观察：除法 → 位模式重复

$1 / (2^n - 1)$ 展开为几何级数 $\sum_{k \ge 1} 2^{-kn}$，硬件实现时就是**把 n-bit 整数 $x$ 的位模式沿着分数位不断复制**。由于 $0 \le x \le 2^n - 1$ 且每次复制跳 $n$ 位，**各复制段的 bit 范围互不重叠**——不是真的加法，而是把 bit 拼接/布线。这正是为什么硬件代价这么低。

## 一般情形的硬件数据通路

除去特殊值（UNORM8 的 0x00 → 0.0、0xFF → 1.0；UNORM16 的 0x0000/0xFFFF；SNORM 的 ±1.0 的两个表示），剩下的都要转成规格化 float32：

1. **规格化**：对输入做 **leading-zero count**（16-bit 就够），同时左移得到首位为 1 的 `normalized_x`。LZ 计数和移位可并行，分治实现（先查高 8 位、再高 4 位、再高 2 位、最后 1 位）。
2. **指数**：`exp = 126 - num_lz`（UNORM16 情况下最大非特殊值 0xfffe 落在 [0.5, 1)，biased exp = 126）。
3. **尾数初值**：把规格化后的 15 位（最高位隐含 1）+ 再取 8 位循环（模拟 geometric series 的第二段），拼出 23 bit。
4. **舍入**：round-to-nearest 只需加上 `normalized_x[7]`。由于特殊值已经被上游挑走，进位**永远不会**传到指数——用 15-bit adder 就够，不需要全宽。

全部合计：mux + 16-bit LZ + 16-bit adder + wiring。没有乘法器，没有除法器，没有迭代。

## UNORM8 / UNORM16 / SNORM8 / SNORM16 统一

- UNORM8 → UNORM16 的转换等于**把字节复制两次**：因为 $65535 = 255 \cdot 257$，所以 $x/255 = (x \cdot 257)/65535 = (x \cdot 0x0101)/65535$——直接当 UNORM16 处理。
- SNORM8 / SNORM16 分母 127 / 32767 互无公因子，但**规格化路径可以完全共用**：前端多一个 abs + 符号提取（15-bit adder 就能 abs），LZ 路径把 SNORM 绝对值塞进 16-bit 通路的高位即可。
- SNORM 的循环周期变成 7-bit / 15-bit 而不是 8-bit / 16-bit——尾数提取阶段多一个 mux。

## 启示

这是一个经典案例：**软件里看似要除法的操作，硬件里根本不存在「除法」**。对于 $1/(2^n-1)$ 这种常数，整数位串的重复就是除法结果，硬件只要会布线就够。教科书讲 float → int 要担心舍入传到指数；这里由于特殊值被专门处理，**round 永远不产生跨指数进位**，这是数值上的小幸运，也是硬件小而稳定的理由。

## 相关

- [[fabian-giesen]]
- [[unorm-float-conversion]] — 对应的软件解法
- [[color-space]]

## Sources

- [[sources/ryg-unorm-snorm-hardware-edition]]
