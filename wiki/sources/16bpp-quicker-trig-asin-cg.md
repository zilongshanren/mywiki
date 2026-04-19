---
tags: [source, math, trigonometric, approximation, benchmark, cpp]
date: 2026-04-19
sources: 2
---

# Quicker Trig + Gotta Go Fast（16BPP.net）

[[16bpp]] 2026 年 3 月的两篇连载（`2026-03-11` *Quicker Trig* 与 `2026-03-16` *Gotta Go Fast*），都是 PSRayTracing 里把 `std::asin()` 换成近似版的性能实验。第二篇是第一篇发布后 5 天内的 follow-up，把同一个近似用 **Estrin's Scheme** 再压榨一轮。为避免切碎，这里合并为一篇 source summary。

## 摘要（Part 1：Quicker Trig）

作者原本用 4 阶 Taylor 级数做 `asin` 近似，在 $|x| > 0.8$ fallback 到 `std::asin()`，在 PSRayTracing 上 +5%。他听说了 [Padé Approximants](https://en.wikipedia.org/wiki/Pad%C3%A9_approximant)，推出 [3/4]、[5/4] Padé；配合 **half-angle transform** 把 $|x| > 0.85$ 的区间传送到原点附近，再用 [1/2] Padé 算内层，精度大幅提升，但 PSRayTracing 端到端和 Taylor 版本几乎一样快。

然后他问 Gemini「C++ 里 `asin` 有什么快近似」，拿到了 Nvidia Cg Toolkit 里 2012 前就有的 **Abramowitz & Stegun 公式 4.4.45** 实现——3 阶 Minimax 多项式 + `sqrt(1-|x|)` + `copysign`，branchless、全区间精度几乎完美。PSRayTracing 渲染从 111 秒降到 101.5 秒，microbench 上 **1.47×~1.90×** 加速。作者在 README 里把 Taylor 版当作成就摆了几年，**C++ 和图形圈没人来指正**。

## 摘要（Part 2：Gotta Go Fast）

Reddit / HN / Lobste.rs 的评论启发作者继续看这个 Cg 实现。他意识到 Horner 展开写法：

```cpp
double p = a3 * abs_x + a2;
p = p * abs_x + a1;
p = p * abs_x + a0;
```

有一条长度 3 的依赖链。用 **Estrin's Scheme** 代数重排：

```cpp
const double x2 = abs_x * abs_x;
const double p = (a3 * abs_x + a2) * x2 + (a1 * abs_x + a0);
```

依赖链降为 2，乱序 CPU 可以并行 `(a3*x+a2)` 和 `(a1*x+a0)`。跨 3 CPU × 3 OS × 3 编译器 × 1000 万次 × 250 runs 测下来，**Intel i7 再加 17~20%**（总相对 `std::asin` 1.80×~1.88×），AMD Ryzen 9 几乎无额外增益（OoO 窗口已充分利用 Horner 的并行），Apple M4 + Clang +11%。端到端 PSRayTracing Intel 上 +3%（M4 上变化在噪声内）。

## 关键要点

- **Nvidia Cg 的 asin 实现基于 Abramowitz & Stegun 4.4.45**（1964 年的 Minimax 系数），是图形应用里全区间最优的 3 阶近似；
- **Taylor 不是逼近工具**——Robin Green 在 [[faster-math-functions]] 强调过，这篇实操上又踩了一次；
- **Padé 好于 Taylor，但还不是最优**——参见 [[pade-approximants]]；
- **Horner → Estrin** 是低成本的 ILP 优化，参见 [[estrin-scheme]]；
- 收益强依赖 CPU 微架构：Intel 老 i7 > AMD ≈ Apple M4；
- 「**先搜搜有没有人解决过你的问题**」是作者最痛的教训——这段代码在 Cg 文档里躺了 13 年；
- 作者也试了 LUT 但更慢且精度更差，印证「在现代 CPU 上数学公式常胜过查表」；
- 用 SIMD 会更快，但 PSRayTracing 的架构不允许（基于原书的结构，非向量化）。

## 链接到的概念

- [[asin-cg-approximation]]
- [[estrin-scheme]]
- [[pade-approximants]]
- [[faster-math-functions]]
- [[benchmark-methodology-end-to-end]]
- [[psraytracing]]
- [[16bpp]]

## 原文

- 链接：
  - <https://16bpp.net/blog/post/faster-asin-was-hiding-in-plain-sight>
  - <https://16bpp.net/blog/post/even-faster-asin-was-staring-right-at-me>
- 本地：
  - `raw/articles/16bpp.net/2026-03-11_quicker-trig.md`
  - `raw/articles/16bpp.net/2026-03-16_gotta-go-fast.md`
