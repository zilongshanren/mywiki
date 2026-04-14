---
tags: [SIMD, SSE, x86, 优化]
date: 2026-04-14
sources: 1
---

# SSE 的「补洞」技巧

SSE 与 SSE2 在每一颗支持 64-bit 的 x86 上都可以用，是工程师能依赖的最低 SIMD 起点。但 SSE2 也是史上**最非正交**的 SIMD 指令集之一：哪些数据类型支持哪些操作，几乎没有规律可循；后续修订（特别是 SSE4.1）才陆续把一部分坑填上。下面这些技巧大多来自 Fabian Giesen 的总结，是与「老 SSE」打交道的工程师必备的常识。

## 无分支 select

SIMD 的标准做法是「两路都算 + 用 mask 合并」。在 SSE2 的世界里，select 永远是

```c
_mm_or_si128(_mm_and_si128(a, cond), _mm_andnot_si128(cond, b));
```

SSE4.1 起多了 `_mm_blendv_epi8 / _ps / _pd`，更短一点。`a ^ ((a ^ b) & cond)` 也可以，但临界路径一样长，少一个寄存器、ILP 略差。**绝对不要**用「`b + (a-b) & cond`」这种 FP 算术「绕过 mask」的写法：它会对 Inf/NaN 出错，并且在小数 + 大数相消时直接丢精度，延迟也比 mask 版本更长。

## 无符号比较

SSE 只提供**等于**和**有符号 greater-than**两种整数比较。无符号比较通常用「先平移到有符号区间再比」：

```
a >  b (unsigned, 32-bit)  ≡  (a - 0x80000000) > (b - 0x80000000) (signed)
```

或者绕个弯用无符号 min/max：`a <= b ⇔ max(a,b) == b`。SSE2 只对 `uint8` 提供 min/max，`uint16/uint32` 的 min/max 要等 SSE4.1。

## 整数乘法的迷宫

- **16×16→32**：SSE2 提供高半部 + 低半部分别取，要用 `unpacklo/hi` 重新拼成 32-bit 结果。
- **32×32→32**：`PMULLD`（`_mm_mullo_epi32`）要 SSE4.1，并且在很多微架构上比其他乘法慢。
- **32×32→64**：SSE2 起就有 `PMULUDQ`（无符号），SSE4.1 加了 `PMULDQ`（有符号）。它们只用偶数 lane，要凑出四路 32 位乘法得手动 shuffle。
- **`PMADDWD` 救场**：当两侧 32-bit lane 的实际值都落在 int16 范围内，可以用 `_mm_madd_epi16` 「一指令完成 32-bit 乘法」——这是 SSE 中最被低估的指令之一。

## 「水平」操作的真相

- 浮点的 `HADDPS` / `DPPS` 从来不是真正的硬件水平加；它们在每一代 Intel 实现里都被解码成多条更基础的指令，**只省代码大小，不省时间**。
- 真正快的「水平」操作在整数侧：`PMADDWD`、`PSADBW`、`PMADDUBSW`。
  - `_mm_sad_epu8(x, _mm_setzero_si128())` 是 x86 上最快的 8 路水平加。
  - `_mm_madd_epi16(x, _mm_set1_epi16(1))` 把相邻 16-bit lane 两两加起来。
- 想要 SIMD 性能，根本之道是 **[[aos-vs-soa|SoA 布局]]** 或 transpose 后批量处理，而不是寄希望于水平指令。

## 32/64-bit load/store 被 intrinsics 命名误导

- `_mm_loadl_epi64` / `_mm_storel_epi64` 真的是 64-bit 不对齐的 load/store，参数被声明成 `__m128i*` 只是 API 混乱。
- 32-bit load 干脆没有专门的 intrinsic，要写 `_mm_cvtsi32_si128(*p)`，编译器会还原成 `MOVD`。

## 教训

SSE 的「非正交」是历史尘埃 + intrinsics 命名灾难叠加的产物。写跨代 SSE 代码时，**记住这些桥洞远比记住每条指令的延迟有价值**——它们决定了你能不能写出可以编译到 SSE2 / SSSE3 / SSE4.1 三个目标都能跑的同一份 SIMD 代码。即便在 AVX2 时代，这些洞里仍然有少数没填上。

## 相关

- [[aos-vs-soa]]
- [[cache-friendliness]]
- [[latency-vs-throughput]]
- [[fabian-giesen]]
- [[fearless-simd]] —— Raph Levien 提出的 Rust 可移植 SIMD 愿景，同样踩到 runtime feature 选档与 inlining 组合的坑
- [[carry-save-adder-pixel-avg]] —— 用 CSA 恒等式在没有硬件 pavgb 的情况下做打包像素的无溢出平均

## Sources

- [[sources/ryg-sse-mind-the-gap]]
