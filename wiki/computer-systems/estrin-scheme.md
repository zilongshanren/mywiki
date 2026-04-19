---
tags: [instruction-level-parallelism, compiler, math, performance]
date: 2026-04-19
sources: 1
---

# Estrin's Scheme：用 ILP 打 Horner

多项式求值的标准写法是 **Horner 法则**：

```cpp
// p(x) = a0 + a1*x + a2*x^2 + a3*x^3
double p = a3 * x + a2;
p = p * x + a1;
p = p * x + a0;
```

优点是乘加次数最少（$n$ 阶多项式只要 $n$ 次 FMA），但**每一步都依赖上一步结果**——依赖链长 = 多项式阶数。现代乱序 CPU 的 FMA 延迟通常 4~5 个周期；依赖链长意味着整个循环的 throughput 被延迟锁死。

[Estrin's Scheme](https://en.wikipedia.org/wiki/Estrin%27s_scheme) 通过**代数重排**缩短依赖链，把多项式切成可以并行计算的小段。对 3 阶多项式：

$$p(x) = (a_3 x + a_2) \cdot x^2 + (a_1 x + a_0)$$

写成代码：

```cpp
const double x2 = x * x;
const double p = (a3 * x + a2) * x2 + (a1 * x + a0);
```

数值上和 Horner 完全相同，但**依赖链从 3 降到 2**：`(a3*x+a2)` 和 `(a1*x+a0)` 可以并行，`x2` 也能提前算。乱序 CPU 的调度器会把它们塞进不同的 FMA 执行端口。

## 实测（16BPP.net 的 asin_cg）

把 [[asin-cg-approximation]] 的 Horner 3 阶改成 Estrin，对 10,000,000 次 `asin` 调用：

| 平台 | `asin_cg` Horner | `asin_cg_estrin` | 提升 |
|---|---|---|---|
| Intel i7 + Linux GCC `-O3` | 48.4s | 41.4s | **1.80×** |
| Intel i7 + Linux Clang `-O3` | 47.2s | 41.4s | **1.78×** |
| Intel i7 + Windows MSVC `/O2` | 53.6s | 45.0s | **1.88×** |
| AMD Ryzen 9 + Linux GCC | 53.1s | 52.2s | 1.44× 总 |
| AMD Ryzen 9 + Linux Clang | 52.8s | 51.9s | 1.45× 总 |
| Apple M4 + GCC | 25.8s | 25.7s | 1.02× |
| Apple M4 + Clang | 32.8s | 30.2s | 1.11× |

与 `std::asin()` 的总加速比：Intel 1.88×、AMD ~1.45×、Apple M4 1.02~1.11×。

## 为什么差异这么大

- **Intel i7 + Ubuntu/MSVC**：收益 **+17~20%**（相对 Horner 版）。
- **AMD Ryzen 9**：几乎没有额外收益——Ryzen 的乱序窗口和 FMA 调度已经把 Horner 的依赖链隐藏得很好。
- **Apple M4 + Clang**：+11%；M4 + GCC 几乎无差。Arm 上 SIMD / FMA 端口的调度能力更强，Horner 的串行已经被并行到几乎最优。
- **Windows GCC**：数据反常（Intel 只有 1.25×），但与另外几个编译器对比仍然正面。

结论是 **Estrin 的收益和 CPU 的 OoO 窗口负相关**——越「笨」的 CPU 越能靠这个写法捡速度。

## 何时用

- 写 hot-path 的浮点多项式近似（`asin` / `exp` / `sigmoid` / [[faster-math-functions]] 里的 minimax）；
- 依赖链长度超过 2~3 时（低阶 Horner 本身就只有 1~2 步，改不改都差不多）；
- 需要跨老 x86 微架构保持 worst-case 性能。

**不用**：SIMD 环境下编译器常常会自己做 Estrin；深度学习里每层 kernel 有更大的吞吐来源；依赖链不是瓶颈（算法整体 memory-bound）。

## 和现代编译器的关系

理想情况下 `-O3` 应该能自动做 Estrin。实际 GCC 和 Clang 并不总是做——尤其系数不是 compile-time 常量、或者依赖链被 `-ffast-math` 禁止重排时。手写 Estrin 是把意图表达清楚、绕过编译器保守路径的一种方式。

## 相关

- [[asin-cg-approximation]]
- [[faster-math-functions]]
- [[fp64-sincos-minimax]]
- [[benchmark-methodology-end-to-end]]

## Sources

- [[sources/16bpp-quicker-trig-asin-cg]]
