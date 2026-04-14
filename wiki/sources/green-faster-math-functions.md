---
tags: [source, 数学, 数值计算, 浮点, SPU, 编译器]
date: 2026-04-14
sources: 1
---

# Faster Math Functions（Robin Green / Bases and Frames）

[[robin-green]] 2016 年回顾其 GDC 2002/2003 tutorial *Faster Math Functions* 的起源和内容——这是 Robin 在给 PS3 SPU 写一个插值缩放函数时发现 SPU 没有数学库，逼着他钻研了 `powf()` 该怎么在没有 libm 的情况下实现，一路滑坡进入 transcendental function 的源流研究。

## 摘要

IEEE754 标准只规范了五种基本运算（加减乘除与取负），**明确放弃**对超越函数（sin、exp、log、pow、…）提供精度保证——所以不同平台的 `sinf()` 结果有细微差异是合法的。真正的「如何实现」散落在 Cephes 数学库的源码注释、Cody & Waite 的 1980 年教材，以及 Muller 2005 年的 *Elementary Functions* 里。

几个关键点：

- **IEEE754 的诞生故事**本身就是产业史上的经典段子：微处理器新兴厂商推 K-C-S（Kahan-Coonen-Stone）提案，大型机厂商（DEC 的 VAX 格式）试图抵抗 gradual underflow（denormals）；DEC 委托 Pete Stewart 做独立评估，期望他证伪 gradual underflow，结果 Stewart 站队 K-C-S，DEC 从此沉默。Intel 不能泄露他们把 FP 异常用 pipeline bubble 实现的专利方法，但 40,000 门的目标让别人不相信能做到。
- **表法（table-based）**：33 条目的插值表就足以重建 32-bit 单精度 `sinf`/`cosf`——8 位时代塞 256/512 项的习惯远远过量了。SPU/GPU/嵌入式把这类空间取舍又拉回前台。
- **多项式逼近的三件套**：range reduction → polynomial approx → reconstruction。大多数函数（`acosf` 等）用三角恒等式从更基本的函数推出，所以「短区间上精准」是关键。
- **误区**：网上大量教程用 Taylor 级数截断做逼近。Cephes 库里的多项式**长得像** Taylor 但精度高得多——秘密是 **Minimax 多项式**（Chebyshev / Padé 只是铺垫），这是「网上几乎没人写」的神来之笔。学会用 Mathematica / Maple 生成低阶 minimax 多项式后，可以把很多图形常用函数做快得多。
- **硬件打脸**：Robin 在调研时发现 **PS2 的 ESIN / ECOS 指令**的多项式系数有一个工程师转录时截断的 bug——不仅可以修，还可以写一段 SPU 代码在更低精度下**跑得比硬件指令还快**。
- **BRDF power 分离**的小插曲：他试图把 specular BRDF 的 $x^n$ 拆成若干简单幂的组合，结果发现 paper 中那个「能用」的例子恰好落在一个全局误差极小点——除此之外都不 work。
- **BitLog 翻车**：他顺手加了一个 BitLog 快速对数的 hack，Charles Bloom 在 cbloomrants 上一篇把他和原作者 Jack Crenshaw 一起拆了个底掉，并给出改进版本。
- **浮点打印的历史**也没完——Grisu3 快但在少数值上 fallback 到 Dragon4；2010 年 Loitsch PLDI 论文；2016 年 POPL 的 *Errol* 提出 always-correct 且只比 Grisu3 慢 2.5×。读 FP 同样需要 IEEE754 rounding modes（尤其 round-to-half-even）。

## 关键要点

- IEEE754 不保证超越函数精度——这是库实现者的领地。
- 写 `powf()` 的标准套路是 range reduction + minimax 多项式 + reconstruction，**不是** Taylor 级数。
- Minimax 多项式（在区间上最小化最大误差）才是 Cephes 那种「惊人小」的多项式的来源。
- 33 项插值表就够 32-bit 精度的 sin/cos——早年大家过度保守。
- 硬件 sin 不一定是对的：PS2 ESIN 系数被工程师手抄时截断，可以修也可以跑赢。
- 浮点的 `printf`/`scanf` 正确性至今（2016 时）没完全解决——Errol 是当时最新的 always-correct 方案。
- BitLog 翻车是警示：发表前先让 Charles Bloom 当 reviewer。

## 链接到的概念

- [[faster-math-functions]]
- [[robin-green]]

## 原文

- 链接：https://basesandframes.wordpress.com/2016/05/17/faster-math-functions/
- 本地：`raw/articles/basesandframes.wordpress.com/2016-05-17_faster-math-functions.md`
