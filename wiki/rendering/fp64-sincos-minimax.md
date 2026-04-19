---
tags: [渲染, glsl, fp64, double-precision, 数学库, minimax, remez, outerra]
date: 2026-04-19
sources: 1
---

# GLSL 下 fp64 sin/cos 的 Minimax 近似

GLSL 在支持 `double` 之后**并没有同步提供 fp64 版本的 `sin`/`cos`**——`sin(double)` 在多数驱动上直接不存在，或者被悄悄降精度到 fp32 再执行。对于 Outerra 这种把整颗行星坐标放在 double 里做变换的引擎，这是硬伤：在 quad-sphere map projection 的角度处处都要 `sin`/`cos`，从 fp32 回路跳过去就失去了使用 double 的意义。

解法是**在 shader 里手写 fp64 近似**：用 [Remez exchange](http://lolengine.net/wiki/doc/maths/remez) 在 $[0, \pi/2]$ 区间上生成 minimax 多项式，再在运行时做 range reduction 回基准区间。方法论与 [[faster-math-functions]] 讲的「三段式」完全一致；差别只是这次的目标平台是 GLSL + GPU。

## 9 阶版本（误差 < 5e-9）

```glsl
// sin(x), 5e-9 absolute error
double sina_9(double x) {
    // minimax coefs for sin on [0, pi/2]
    const double a3 = -1.666665709650470145824129400050267289858e-1LF;
    const double a5 =  8.333017291562218127986291618761571373087e-3LF;
    const double a7 = -1.980661520135080504411629636078917643846e-4LF;
    const double a9 =  2.600054767890361277123254766503271638682e-6LF;

    const double m_2_pi = 0.636619772367581343076LF;   // 2/pi
    const double m_pi_2 = 1.57079632679489661923LF;    // pi/2

    double y = abs(x * m_2_pi);
    double q = floor(y);
    int    quadrant = int(q);

    // fold [0, pi/2] alternately forward/backward
    double t = (quadrant & 1) != 0 ? 1 - y + q : y - q;
    t *= m_pi_2;

    double t2 = t * t;
    double r  = fma(fma(fma(fma(a9, t2, a7), t2, a5), t2, a3), t2*t, t);

    r = x < 0 ? -r : r;
    return (quadrant & 2) != 0 ? -r : r;
}
```

## 11 阶版本（误差 < 2e-11）

```glsl
// sin(x), 2e-11 absolute error
double sina_11(double x) {
    const double a3 = -1.666666660646699151540776973346659104119e-1LF;
    const double a5 =  8.333330495671426021718370503012583606364e-3LF;
    const double a7 = -1.984080403919620610590106573736892971297e-4LF;
    const double a9 =  2.752261885409148183683678902130857814965e-6LF;
    const double ab = -2.384669400943475552559273983214582409441e-8LF;
    // range reduction identical...
    double r = fma(fma(fma(fma(fma(ab, t2, a9), t2, a7), t2, a5), t2, a3),
                   t2*t, t);
    // ...
}
```

`cos` 不需要单独拟合：`cos(x) = sin(x + π/2)`，直接复用 sin 即可。

## 实现细节

- **Horner + FMA 嵌套**：系数按 $a_3 t^3 + a_5 t^5 + \ldots$ 组装，最后一次乘以 $t^2 \cdot t$ 是为了保留奇次项的符号，同时让整条链全走 `fma`（GPU 原生指令，一次舍入，精度更好）。
- **Range reduction**：先 $y = |x \cdot \tfrac{2}{\pi}|$，$\text{quadrant} = \lfloor y \rfloor \bmod 4$，然后在奇数象限反向折叠 $t = 1 - y + q$。这比「简单 $x \bmod 2\pi$」更稳——对输入接近 $\pi/2$ 边界的数值避免一次灾难性相减。
- **符号恢复**：原始 $x$ 的符号 + 第 2/3 象限的符号反转在最后两步做完，避免在多项式评估里携带 branch。

## 精度的含义

5e-9 / 2e-11 是**绝对误差**，不是 ULP。对于 quad-sphere 上的经纬坐标（rad），这意味着地球半径 6371km 上角度误差带来的位移误差量级：

- 9 阶：$6371\text{km} \times 5 \times 10^{-9} \approx 3$ cm
- 11 阶：$6371\text{km} \times 2 \times 10^{-11} \approx 0.13$ mm

行星引擎用 11 阶版本能稳稳压进亚毫米，足够在地面载具视角下避免 Z-fighting 与坐标抖动。

## 与「快速数学函数」的关系

与 Robin Green 在 [[faster-math-functions]] 里讲的思路**完全一致**：

1. 认 IEEE754 对超越函数不保证精度——**各平台自己拟合**是合法且常见做法。
2. 用 **Minimax（Remez）替代 Taylor**：同阶精度通常高几个数量级。
3. **Range reduction → polynomial → reconstruction** 三段式不变，只是载体从 SPU / libm 换成了 GLSL。

Outerra 的贡献是把这套方法论**按在 GPU 端具体落地**，而且把系数直接贴了出来，别的 planet 引擎可以原样复用。

## 相关

- [[outerra-team]]
- [[faster-math-functions]]
- [[planet-terrain-dem-pipeline]]
- [[sigmoid-functions]]
- [[sse-tricks]]
- [[robin-green]]

## Sources

- [[sources/outerra-fp64-sincos]]
