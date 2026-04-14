---
tags: [数值近似, 数学函数, 音频, dsp, 神经网络, 多项式近似]
date: 2026-04-14
sources: 1
---

# Sigmoid 函数族：音频失真与快速近似

**Sigmoid 函数**是一类单调、带饱和两端渐近线的 S 形曲线，在机器学习里是神经元的经典激活函数，在音频工程里则是模拟过载/失真电路的数学模型。[[raph-linus]] 在 2018 年做数字合成器 [synthesizer-io](https://github.com/raphlinus/synthesizer-io) 的过程中专门写了一篇「我最喜欢的几个 sigmoid」，从听感与实现效率两个角度比较了它们——这里记录他的结论与方法。

## 候选函数

四个常被用作波形塑形（waveshaping）失真单元的函数：

- **双曲正切 tanh**——公认「最有音乐味」的 sigmoid。它也是 Moog ladder filter 中差分晶体管对的响应模型，Eurorack 里甚至有叫 *tanh3* 的模块用模拟电路实现它。从概率角度看 tanh 是 logistic function 的变体，可解释为贝叶斯证据的饱和映射，因此早年的神经网络激活函数也是它（后被 [ReLU](https://en.wikipedia.org/wiki/Rectifier_(neural_networks)) 取代）。
- **误差函数 erf**——比 tanh 更「锋利」，对大输入更快贴近渐近线。它的一个有趣非音频应用是「高斯与矩形盒的卷积」，这正是精确模拟示波器光迹所需要的 1D 卷积。
- **倒平方根 sigmoid**：`x / sqrt(1 + x*x)`——形状近似 tanh 但稍微平缓，低输入时失真略多。它的魅力在于「可以被极快地算出来」。
- **硬剪裁（hard clipping）**——严格讲因不可微其实不算 sigmoid，但作为 RAT 等失真踏板的理论模型必须列入对比。

## 听感与频谱

Raph 把一段衰减正弦波过四种函数生成了音频样本和频谱图，总结出几个经验：

- **tanh** 听起来最饱满，高输入时谐波更丰富，低输入时更温和；而且频谱在 Nyquist 之前衰减得最快，**混叠（aliasing）也就最轻**——这是数字音频里评判失真单元的关键。Raph 自己坦承「为什么 tanh 比倒平方根 sigmoid 衰减更快」在他那里还是个待解之谜，尽管后者形状「更圆」。
- **erf** 频谱里会出现奇怪的零点缺口（null），tanh 和倒平方根 sigmoid 里都没有。
- **硬剪裁**听起来生硬，高次谐波越过 Nyquist 变成典型的混叠噪声——模拟踏板之所以听起来还不错，可能恰恰是因为模拟电路无法产生理想的硬剪裁曲线，反而软化了结果。

结论：给数字合成器的塑形单元选失真函数时，**优先选 tanh**；需要极致性能时退让到倒平方根 sigmoid；erf 和硬剪裁留作特定风格。

## 性能：倒平方根 sigmoid 快 13 倍

Raph 在 i7-7700HQ 上用 Rust 跑 benchmark：直接调 `tanh` 每样本 5.9 ns，倒平方根 sigmoid 只要 0.453 ns——**13 倍差距**。原因是两条：

1. `tanh` 是函数调用，必须顺序执行；倒平方根 sigmoid 是纯代数表达式（含 `sqrt`），Rust 编译器能自动向量化。
2. 倒平方根 sigmoid 的运算数本身就少得多，每一条都能被硬件高效实现。

x86 上写显式 SIMD 只能再挤出很小一部分（0.4 ns），因为 `sqrt` 指令已经很快。但 ARM 上就完全不同——ARM 有 `vrsqrte`/`vrsqrts` 这类近似倒平方根指令却没有完整的高精度 `sqrt`，所以在 ARM 上显式 SIMD 收益更明显。这也跟 [Carmack 那段臭名昭著的 fast inverse sqrt](https://en.wikipedia.org/wiki/Fast_inverse_square_root) 及其后续 SIMD 衍生物是同一个技术脉络。

## 多项式「变形」法：用简单函数近似复杂函数

Raph 给出的核心技巧是：**先把输入经过一个低阶奇多项式预处理，然后再过基本 sigmoid**。对 tanh 来说，利用恒等式

```
tanh x = sinh x / sqrt(1 + (sinh x)^2)
```

可以把整个流程变成「先用五次奇多项式近似 `sinh`，再做倒平方根 sigmoid」。多项式本身不用非常精确，因为后续的 sigmoid 会把大值「挤」到渐近线上；五次多项式带来的精度是 **2e-4**，每样本耗时 **0.55 ns**——同时**比发表在 Deep Voice 论文中基于 $e^x$ 的有理多项式近似（~1.5e-3，0.7 ns）又快又准**。

erf 也可以用同样的方法：在 Abramowitz & Stegun 那条 0.86 ns / 5e-4 的经典近似面前，Raph 的七阶多项式变形方法能做到 **2.2e-4 / 0.63 ns**。重要的是多项式变形法的误差**平滑**（不像分段近似有突变），因而频谱与真函数几乎一致，听感上无法区分。

这套「把难函数转化为好函数 + 预处理多项式」的思路是 [[faster-math-functions]] 里 Minimax 多项式近似的**实用化延伸**：先选一个被硬件友好支持的基函数，再用短多项式去精修输入。它的好处是可以用较低阶多项式达到较高精度，而且误差行为平滑——对音频应用尤其重要，因为人耳对频谱细节极其敏感。

## 对 wiki 的位置

这篇文章正好是 [[faster-math-functions]]（Robin Green 在 PS3/SPU 时代总结的 minimax 多项式方法论）的一个现代落地案例：Raph 没有直接用 Remez 算法生成 minimax 系数，而是利用恒等式把难函数转化为「简单 sigmoid 套低阶多项式」的结构，用编译器的自动向量化 + 硬件 `sqrt` 指令打败学术界的经典近似。这也和 [[fearless-simd]] 里他对「Rust 下自动向量化 + 运行时选档」的持续兴趣是一条线的。

## 相关

- [[faster-math-functions]] — Minimax 多项式与通用快速数学库方法论
- [[fearless-simd]] — Raph 的另一个向量化方向
- [[shaping-functions]] — 着色器侧的塑形函数（与 DSP 的 waveshaper 在数学上是同一件事）
- [[raph-linus]]

## Sources

- [[sources/raphlinus-favorite-sigmoids]]
