---
tags: [SIMD, 位运算, 像素格式]
date: 2026-04-14
sources: 1
---

# Carry-Save Adder 与打包像素的无溢出平均

[[fabian-giesen|Fabian "ryg" Giesen]] 2010 年的一篇 bit-twiddling 短文，系统记录了一个很少有地方讲全的技巧：**用 carry-save adder 的简化公式对打包格式的像素做无溢出的平均**。在硬件里这是整数乘法器的标准建造块，在软件里它的价值完全不同——当你手上的 SIMD 指令集没有 add-with-carry、没有更宽的中间累加器时，它让你一条指令算出平均值。

## 两输入 CSA 的恒等式

任意两个无符号整数满足：

```
a + b = (a ^ b) + ((a & b) << 1)
```

分别命名为和位 `S = a ^ b` 与进位位 `C = a & b`。硬件里这叫 _2-input carry-save adder reduction_，它把两路加法拆成两路完全不进位的输出（一路 XOR，一路 AND-左移），唯一一次真正带进位的加法可以延到最后做。软件 ALU 反正都一样快，这条式子本身没什么用，但它的**除以二变体**非常有用：

```
(a + b) / 2 = (a ^ b) / 2 + (a & b)
```

左式可能在 `a + b` 这一步溢出——比如 8 位里 `200 + 200 = 400` 要先扩宽再除。右式永远安全：`(a ^ b)` 和 `(a & b)` 都在 `a | b` 范围内。这就是为什么很多 SIMD 码里能看到它——SSE2 的 8-bit/16-bit 加法没有进位位可取，这条恒等式省掉了 unpack / repack 的往返。

## 三输入 CSA 与带 rounding bias 的变体

三输入版本的 CSA 公式是：

```
a + b + c = S + (C << 1)
S = a ^ b ^ c
C = (a & b) | (a & c) | (b & c)
```

把它套在 `(a + b + 1) / 2`（向上取整的两数平均）上，可以推出：

```
(a + b + 1) / 2 = (a ^ b) / 2 + ((a & b) | ((a | b) & 1))
```

也能用，但不如原文评论区 Charles 给出的写法漂亮：

```
(a + b + 1) / 2 = (a | b) - ((a ^ b) >> 1)
```

推导一行就行：`a + b = (a | b) + (a & b)`（XOR/OR 互补恒等），代进去即可。这种写法和 round-down 版本一样便宜，而且两种 masking 套路都可以无缝加上。

## 和打包像素的结合

真正 cool 的地方是：**这个技巧对位打包格式天然可组合**——A8R8G8B8、R5G6B5、R11G11B10 全都可以。唯一要做的是在 `>> 1` 那步用 mask 阻断相邻通道之间的进位串扰：

```
avg_a8r8g8b8(a, b) = ((a ^ b) >> 1) & 0x7F7F7F7F) + (a & b)
```

`0x7F7F7F7F` 的作用是把每通道最低位的 bit 扫掉，避免上一个通道的低位被移位「漏」到下一个通道的高位。对 64-bit 寄存器里两个 32-bit 像素一起做，mask 换成 `0x7F7F7F7F7F7F7F7F`；对 R5G6B5 这样不均等的字段，mask 对应调整。换句话说，**SWAR**（SIMD within a register）平均值一条指令管到底，不需要 unpack。

加 rounding bias 的版本也可以和 masking 正交组合；把 Charles 的 `(a | b) - ((a ^ b) >> 1)` 套上 `& 0x7F7F7F7F` 后得到：

```
avg_round_up_a8r8g8b8(a, b) = (a | b) - (((a ^ b) >> 1) & 0x7F7F7F7F)
```

## 为什么值得记住

这条 trick 解的是一个小问题，但它是那种「每隔几年就会在 SIMD 内层循环里救你一命」的工具。现代 AVX2/NEON 虽然有 `pavgb` 这样的硬件平均指令，但一旦通道宽度不标准（R5G6B5、R11G11B10、甚至非字节对齐字段），你还是要回到这条手推的公式上来。[[sse-tricks|SSE tricks]] 的补洞精神在这里表现为：**整数 ALU 没有的东西，用 bit identity 合成出来**。

## 相关

- [[sse-tricks]]
- [[fabian-giesen]]
- [[compact-vertex-format]]

## Sources

- [[sources/ryg-carry-save-adders]]
