---
tags: [数值计算, 浮点, 数学库, 编译器, SPU, 嵌入式]
date: 2026-04-14
sources: 1
---

# 快速数学函数实现（Faster Math Functions）

「怎么在没有 `libm` 的地方写出 `sinf`/`cosf`/`expf`/`powf`？」——这是 Robin Green 在给 PS3 SPU 写一个插值函数时被迫回答的问题，也是他 GDC 2002/2003 连续两次做 *Faster Math Functions* tutorial 的源头。这个话题在 SPU、GPU、嵌入式等「数学库贫瘠」的场景下长期存在，并在现代渲染里以「shader 里的 `fast_exp`/`fast_pow`」的形式延续至今。

## IEEE754 的「隐藏条款」

[IEEE754 标准](https://standards.ieee.org/findstds/standard/754-2008.html) 只规范了**五种**运算：加、减、乘、除、取负。对超越函数（sin、cos、exp、log、pow、tan…）它**显式放弃**任何精度或正确性保证，交给库实现者。于是:

- 同一个 `sinf(x)` 在 glibc / MSVC / Intel SVML / iOS libm 上可能给出略微不同的 ULP。
- 硬件上 PS2 的 ESIN/ECOS 指令、GPU 的硬件 `sin` 都是「low-accuracy but fast」版本——合法地存在 ULP 级差异。
- 超越函数的「正确性」其实是一个**各平台自行决定**的灰色地带。

Robin 在研究中发现 **PS2 的 ESIN/ECOS 硬件多项式系数被工程师手抄时截断了**，可以修；甚至可以写一段 SPU 软件用更好的系数**跑得比硬件指令还快**——「不是每天你都能用软件打赢一条硬件指令」。

## 实现套路：三段式

绝大多数单变量超越函数都按同一个套路写：

1. **Range reduction**：把输入从 $(-\infty, +\infty)$ 映射到一个小的「基准区间」，比如 $\sin(x)$ 先把 $x \bmod 2\pi$ 再映射到 $[-\pi/4, \pi/4]$。这一步的**精度陷阱**是大数做 $x \bmod 2\pi$ 会丢有效位，需要用 Cody-Waite 式的「分段常数减法」保精度。
2. **Polynomial approximation**：在基准区间上用低阶多项式逼近目标函数。
3. **Reconstruction**：把结果映射回原区间；复合函数（比如 `acosf` 通过 `asinf` 派生）用三角恒等式推出。

像 `acosf` 这样的派生函数完全依赖于「底层函数在短区间上的精度」，所以**短区间上的高精度多项式**是整个数学库的基石。

## 网上最大的误区：Taylor 级数

新手教程常常用 Taylor 级数截断来近似——这是错的。Taylor 级数在**单一点**（通常是 0）附近精度最高，离中心越远误差越大；你在一个区间 $[a, b]$ 上想要**最大误差最小**，Taylor 就远远不是最优。

Cephes 数学库里的多项式**长得像** Taylor 但系数略有不同，精度却高几个数量级。秘密是 **Minimax 多项式**——在给定区间和阶数下，让最大绝对误差最小化（min-max）的那个多项式。Chebyshev 多项式/Padé 近似只是「比 Taylor 好一点」的中间阶段，Minimax 才是真正的答案。

生成方法：Remez 交换算法；工具：Mathematica 的 `MiniMaxApproximation`、Maple 的 `numapprox[minimax]`、SollyLy 等。学会了它你可以给图形学常用函数（比如 BRDF 的幂函数、tonemap 曲线、滤波 kernel 的加权函数）按需产生「够精度、最小阶数」的多项式近似。

## 表法（Table-based）

8 位时代大家塞 256/512 项的 sin/cos 表，后来内存变大这事儿被淘汰了——然后 SPU/GPU/嵌入式又把它拉回来。Robin 分析过插值误差的上界：**33 项的 sin/cos 表加线性插值就足以重建 32-bit 单精度 sinf/cosf**——8 位时代大家过度保守了一个数量级。

## 印刷与解析浮点数

顺带提到一个冷知识分支：FP 的 `printf`/`scanf` 本身也是个开放问题。

- *What Every Computer Scientist Should Know About Floating-Point Arithmetic* 证明 9 个有效数字足以无损往返 32-bit float（15 位对 double）。
- **Grisu3**（Loitsch 2010 PLDI）用整数内部表示做快速打印，但在大约 0.6% 的值上 bail 到 **Dragon4** 慢路径。
- **Errol**（POPL 2016）提出 always-correct 的方案，比 Grisu3 只慢 2.5×。
- 解析 FP 需要正确实现 IEEE754 rounding modes（特别是 `round-to-half-even`）——这也是「所有语言都应该完整支持 rounding modes」的最强论据之一。

## 经典教材

- **Cephes 数学库**源码——源注释本身就是一本 pragmatic 的数学库开发手册。
- **Cody & Waite, *Software Manual for the Elementary Functions*, 1980**——IEEE754 之前的时代写的，处理各家硬件差异的经典；该书早已绝版，研究者们互相传手抄影印本。
- **Jean-Michel Muller, *Elementary Functions: Algorithms and Implementation*, 2005**——覆盖 range reduction、minimax 多项式、CORDIC 的详细教材。

## BitLog 翻车记

Robin 自己在给 tutorial 补料时临时加了一个叫 BitLog 的「快速对数 hack」，后来 Charles Bloom 在 cbloomrants 上一篇把他和原作者 Jack Crenshaw 一起拆了个底掉，并发出改进版本。这条教训值得所有打算发表「快速数学 hack」的人放在心上：**先让 Charles Bloom 当 reviewer**。

## 相关
- [[fast-exponentiation]] — 快速幂（整数版，另一条支线）
- [[sse-tricks]] — SSE 上实现向量化数学函数
- [[robin-green]]
- [[sigmoid-functions]] — Raph Levien 用「多项式变形」思路打败学术论文里的 tanh/erf 近似
- [[fp64-sincos-minimax]] —— Outerra 把同一套 minimax 三段式方法论搬到 GLSL fp64 sin/cos
- [[asin-cg-approximation]] —— Nvidia Cg 文档里躺了 13 年的 Abramowitz & Stegun 4.4.45 实现，Minimax 3 阶 asin 近似
- [[pade-approximants]] — 好于 Taylor、还不及 Minimax 的中间台阶
- [[estrin-scheme]] — 把 Horner 多项式求值改写成可并行的 ILP 风格，Intel 老 i7 上 +17%
- [[benchmark-methodology-end-to-end]] — 「运行时间永远比数指令更可靠」的一套方法论

## Sources

- [[sources/green-faster-math-functions]]
