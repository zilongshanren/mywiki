---
tags: [math, approximation, numerical-analysis]
date: 2026-04-19
sources: 1
---

# Padé 近似：用有理函数代替多项式

[Padé Approximant](https://en.wikipedia.org/wiki/Pad%C3%A9_approximant) 是用**分子分母都是多项式的有理函数**去逼近一个目标函数。给定 Taylor 级数 $\sum_k c_k x^k$，可以选择「分子 $m$ 阶 / 分母 $n$ 阶」推出 $[m/n]$ Padé 近似：

$$f(x) \approx \frac{P_m(x)}{Q_n(x)}$$

核心性质：**与原 Taylor 的前 $m+n+1$ 项匹配**，但在全区间上的误差通常**比同阶数 Taylor 小几个数量级**（因为分母能吸收「原函数在远处的极点／增长」）。

## 为什么比 Taylor 好

Taylor 只在展开点附近最优，离点越远误差指数级增大。Padé 的分母让它**隐式地编码函数在其它地方的行为**——对 $\arcsin$ 这类边缘增长很快的函数特别有用。16BPP.net 用 4 阶 Taylor 推出 [3/4] Padé：

```python
def asin_pade_3_4(x):
    a1 = -367.0 / 714.0
    b1 = -81.0 / 119.0
    b2 = 183.0 / 4760.0
    n = 1.0 + a1 * x**2
    d = 1.0 + b1 * x**2 + b2 * x**4
    return x * (n / d)
```

相比同 4 阶 Taylor，$|x|$ 靠近 1 的边缘误差从「肉眼可见」降到「几乎贴合真值」。

## 但它不是终点

Padé 仍然是**围绕展开点**做逼近的。在 $x=0$ 附近它最准，两端仍然有残差。要做「**整个区间**上最大误差最小」，要用 **Minimax 多项式**（Remez 算法生成）——参见 [[faster-math-functions]] / [[fp64-sincos-minimax]]。

16BPP.net 的故事恰好示范了这条攀升路径：
1. **Taylor** → 边缘误差爆炸，需要 fallback；
2. **Padé** → 边缘大幅改善，还需要 half-angle transform 补刀；
3. **Minimax**（Nvidia Cg 的 Abramowitz-Stegun 4.4.45 实现）→ 全区间误差几乎消失，branchless。

渲染耗时上 Padé 版本相较 Taylor 几乎无速度优势（因为多了有理除法），而 Minimax 3 阶版才是真正的赢家。

## 半角变换：把边缘问题转成中心问题

Padé 在 $|x|$ 接近 1 时仍有误差。利用 $\arcsin$ 的恒等式：

$$\arcsin(x) = \tfrac{\pi}{2} - 2 \arcsin\!\left(\sqrt{\tfrac{1-|x|}{2}}\right)$$

当 $|x| > 0.85$ 时把问题「传送」到原点附近（内层 $\arcsin$ 的输入幅值 < 0.27），再用低阶 Padé 或 Minimax 算内层。这不是 Padé 本身的功能，但是搭配 Padé 做 inverse trig 的标准套路。

## 计算细节

- **系数**用符号数学工具算（SymPy、Mathematica），不要手推——16BPP.net 给的 `-367/714`、`-81/119` 这些怪分数就是工具吐出来的；
- 有理函数除法不便宜，但一次除法能替代多次高阶乘加时仍划算；
- **极点**：$Q_n(x)=0$ 的根是函数的极点。逼近 $\arcsin$ 这种连续函数时要挑分母无零的 Padé 变体。

## 适用场景

- 目标函数的 Taylor 收敛慢（$\arcsin$、$\tanh$、$\mathrm{erf}$）；
- 要求闭式、可 SIMD 化、不依赖 LUT；
- 精度比 Minimax 差但比 Taylor 好、推导难度介于两者之间。

## 相关

- [[faster-math-functions]]
- [[asin-cg-approximation]]
- [[fp64-sincos-minimax]]
- [[estrin-scheme]]
- [[sigmoid-functions]]

## Sources

- [[sources/16bpp-quicker-trig-asin-cg]]
