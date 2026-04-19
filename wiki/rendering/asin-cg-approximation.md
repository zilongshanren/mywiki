---
tags: [math, trigonometric, approximation, minimax, graphics, ray-tracing]
date: 2026-04-19
sources: 1
---

# Nvidia Cg asin() 近似：躺在死掉的文档里 10+ 年

图形代码里 `asin()`、`acos()` 出现在球面纹理映射、normal 解码、[[path-tracing-monte-carlo]] 的角度采样里，频次很高。`std::asin()` 是精确但昂贵的 libc 调用——工程上只要近似到视觉无差就够。这条路上 16BPP.net 走了一圈弯路，最后发现**最优解在 2012 年停止更新的 [Nvidia Cg Toolkit 文档](https://developer.download.nvidia.com/cg/asin.html) 里**，而那个公式本身来自 1964 年的 Abramowitz & Stegun 手册公式 4.4.45。

## 起点：Taylor + fallback（错误示范）

作者自己搓的 `asin()` 近似是 4 阶 Taylor 级数（Maclaurin 展开），在 $x \in [-0.8, 0.8]$ 足够精确，但边缘误差爆炸，只能在 $|x| > 0.8$ 时 fallback 到 `std::asin()`。这符合 [[faster-math-functions]] 里强调的「Taylor 不是逼近工具」的教训——Taylor 只在展开点附近最优，不是最小化最大误差的方案。

PSRayTracing 上测出 +5% 渲染速度，作者当时挺满意。

## 第一次尝试：Padé Approximants

[Padé 近似](https://en.wikipedia.org/wiki/Pad%C3%A9_approximant)以「分子分母都是多项式的有理函数」逼近 Taylor 级数，在相同阶数下误差小得多。作者用 4 阶 Taylor 推出 [3/4] Padé：

$$p(x) = x \cdot \frac{1 + a_1 x^2}{1 + b_1 x^2 + b_2 x^4}$$

边缘误差仍不够小，继续用 **[Half-angle transform](https://en.wikipedia.org/wiki/Inverse_trigonometric_functions)**：$|x| > 0.85$ 时「传送」到原点附近，

$$\arcsin(x) = \pi/2 - 2\arcsin(\sqrt{(1-|x|)/2})$$

用 [1/2] Padé 计算内层（因为 $\sqrt{(1-|x|)/2} < 0.27$）。实现干净，精度好看。但 PSRayTracing 渲染耗时和 Taylor 版差不多（都比 `std::asin()` 快 ~5%），**努力没换来速度**。

## 问 LLM，然后羞愧

作者抛给 Gemini 一句「C++ 里 `asin(x)` 有什么快的近似」，LLM 给了这个：

```cpp
double asin_cg(double x) {
    constexpr double a0 =  1.5707288;
    constexpr double a1 = -0.2121144;
    constexpr double a2 =  0.0742610;
    constexpr double a3 = -0.0187293;
    const double abs_x = fabs(x);
    double p = a3 * abs_x + a2;
    p = p * abs_x + a1;
    p = p * abs_x + a0;
    const double x_diff = sqrt(1.0 - abs_x);
    const double result = M_PI_2 - x_diff * p;
    return copysign(result, x);
}
```

引用是 **Nvidia Cg Toolkit 的 `asin()` 文档**，系数来自 **Abramowitz & Stegun 公式 4.4.45**（这是一组 **Minimax 多项式**系数，不是 Taylor）。branchless、无 `if`、没有 fallback、从 $-1$ 到 $+1$ 的全区间误差几乎为零。

PSRayTracing 端到端测试：**101.5 秒 vs `std::asin()` 的 110.9 秒**，纯 microbench 上 **1.47× ~ 1.90× 加速**。

## 为什么会错过

**因为没人搜**。作者承认他从来没搜过「fast c++ asin approximation」，一上来就自己推 Taylor。这是他文章里最重要的 takeaway——

> 「先看看有没有人解决过你的问题。」

而且这段代码在 Cg 文档里躺了 13 年没人提。作者的 PSRayTracing README 里把 Taylor 版本当成就，C++ 和图形圈没人来提醒他。**整个生态里没人做 benchmark 也没人 cross-check 老公式**。

## 第二轮：Estrin's Scheme 再压榨

参见 [[estrin-scheme]]。把 Horner 展开写法改写成 Estrin 风格，缩短依赖链让乱序 CPU 并行执行，Intel 上再快 1.80x，M4 上再快 1.11x。这一轮只改了两行代码。

## 实现小结

- **推荐实现**：Cg Abramowitz-Stegun 4.4.45 3 阶多项式 + `sqrt(1-|x|)` + `copysign`；进一步走 Estrin。
- **避免的坑**：Taylor 级数做宽区间逼近（[[faster-math-functions]] 里 Robin Green 专门警告过）；手搓 Padé + half-angle fallback。
- **Minimax 本质**：不是在展开点附近最优，而是「在整个区间上最大误差最小」。生成工具是 Remez 算法 / Mathematica `MiniMaxApproximation` / Sollya。A&S 4.4.45 就是 1964 年用这个方法手算出来的结果。
- **LUT 作者也试过**，但误差更大且不比公式快——「数学公式还是首选」。

## 限制

这是 `arcsin` 的**近似**，图形里通常够用；精度敏感场合（如物理仿真、科学计算）仍需 `std::asin()`。PSRayTracing 默认行为可关，通过 CMake 选择用近似还是真版。

## 相关

- [[faster-math-functions]]
- [[estrin-scheme]]
- [[pade-approximants]]
- [[fp64-sincos-minimax]]
- [[benchmark-methodology-end-to-end]]
- [[psraytracing]]

## Sources

- [[sources/16bpp-quicker-trig-asin-cg]]
