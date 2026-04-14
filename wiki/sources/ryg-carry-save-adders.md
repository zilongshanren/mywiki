---
tags: [source, SIMD, 位运算]
date: 2026-04-14
sources: 1
---

# Carry-save adders and averaging bit-packed values（Fabian Giesen）

[[fabian-giesen|ryg]] 2010 年 8 月的短文，把一个他说「很少见有人完整写过」的 SIMD/SWAR bit trick 正式归档——如何在**没有硬件平均指令**的情况下对打包像素做无溢出平均，并且带可选的 rounding bias。

## 摘要

两输入 carry-save adder 的恒等式 `a + b = (a ^ b) + ((a & b) << 1)` 在硬件里作为整数乘法器的基本单元有意义，但在软件里没什么直接用途。它的变体 `(a + b) / 2 = (a ^ b) / 2 + (a & b)` 却是绕过溢出的老 SIMD 技巧——两路加法的中间值永远在 `a | b` 的范围内，不需要先扩宽到更宽类型。三输入版本 `a + b + c = S + (C << 1)` 能推出 `(a + b + 1) / 2` 的变体，但评论区的 Charles 给出了更漂亮的 `(a | b) - ((a ^ b) >> 1)`——一行推导 `a + b = (a | b) + (a & b)` 即可。

真正的亮点是和**位打包像素格式**的组合：只要在 `>> 1` 那步用掩码阻断相邻通道的串扰，这套公式对 A8R8G8B8（`& 0x7F7F7F7F`）、R5G6B5、R11G11B10、甚至 64-bit 里两个 32-bit 像素并排都一视同仁，不需要任何 unpack。ryg 自己评价 `not terribly useful in practice, but it's come in handy for me a couple times over the past few years, and I think it's just fundamentally too cool not to have it properly documented`。

## 关键要点

- **round-down**：`(a + b) / 2 = ((a ^ b) >> 1) + (a & b)`。
- **round-up（Charles 版）**：`(a + b + 1) / 2 = (a | b) - ((a ^ b) >> 1)`。
- **A8R8G8B8 平均一条表达式**：`(((a ^ b) >> 1) & 0x7F7F7F7F) + (a & b)`。对 64-bit 里两个像素并排，mask 扩成 `0x7F7F7F7F7F7F7F7F`。对 R5G6B5 等不对称字段，mask 对应调整。
- **rounding bias 和 bit-packing 正交**：两种 mask 技巧可以任意组合。
- **背景动机**：SSE2 时代整数加法没有输出进位位，很多 SIMD 指令集对操作数宽度有硬限制；这套公式让 SWAR 平均值不需要 unpack→widen→repack 往返。

## 链接到的概念

- [[carry-save-adder-pixel-avg]]
- [[sse-tricks]]
- [[fabian-giesen]]
- [[compact-vertex-format]]

## 原文

- 链接：https://fgiesen.wordpress.com/2010/08/23/carry-save-adders-and-averaging-bit-packed-values/
- 本地：`raw/articles/fgiesen.wordpress.com/2010-08-23_carry-save-adders-and-averaging-bit-packed-values.md`
