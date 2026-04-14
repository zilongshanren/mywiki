---
tags: [source, 音频, dsp, 数学近似, 多项式, simd]
date: 2026-04-14
sources: 1
---

# A Few of My Favorite Sigmoids（Raph Levien / raphlinus.github.io）

[[raph-linus]] 发表于 2018 年 9 月的文章，从**听感 + 实现效率**两个角度比较几种 sigmoid 函数，并给出他给数字合成器 synthesizer-io 用的 Rust 实现。

## 摘要

Raph 选出四个候选作比较：**双曲正切 tanh**、**误差函数 erf**、**倒平方根 sigmoid** `x/sqrt(1+x²)` 和**硬剪裁**（严格讲不算 sigmoid 但作为失真踏板的经典模型必须对比）。他在衰减正弦波上跑这四种函数并分析频谱：tanh 听起来最饱满、谐波丰富且在 Nyquist 之前衰减最快，因此**混叠最轻**；erf 频谱里有奇怪的零点缺口；硬剪裁听起来生硬且高频混叠明显，但模拟踏板效果还不错的原因恰恰是电路无法产生理想硬剪裁曲线。tanh 也有个历史渊源——它是 Moog ladder filter 里差分晶体管对的响应模型，也是早期神经网络激活函数，Eurorack 模块 tanh3 用模拟电路实现它。在 i7-7700HQ 上的 benchmark 显示：直接调 `tanh` 需 5.9 ns/sample，倒平方根 sigmoid 只要 0.453 ns——**13 倍差距**。原因有两条：一是倒平方根 sigmoid 是纯代数表达式，Rust 能自动向量化；二是运算数量本来就少。ARM 上由于 `vrsqrte`/`vrsqrts` 近似指令存在但没有高精度 `sqrt`，显式 SIMD 差异会更大。Raph 的核心技巧是**多项式变形（morphing with polynomials）**：先把输入过一个低阶奇多项式再过某个基本 sigmoid，就能近似任意其他 sigmoid。对 tanh 他利用 `tanh x = sinh x / sqrt(1 + sinh²x)`，用五次多项式近似 sinh + 倒平方根 sigmoid，得到 2e-4 精度 / 0.55 ns—— 比 Deep Voice 论文基于 `e^x` 的有理多项式近似（1.5e-3 / 0.7 ns）又快又准。对 erf 他用七次多项式变形打败经典 Abramowitz & Stegun 近似（2.2e-4 / 0.63 ns vs 5e-4 / 0.86 ns）。多项式变形法的一个关键优势是误差**平滑**（非分段），频谱与真函数几乎一致——音频场景的必要性质。

## 关键要点

- **四个候选**：tanh、erf、x/sqrt(1+x²)、hard clipping
- **tanh 是「音乐味最好」的失真函数**：频谱衰减最快 → 最轻的数字混叠，也是 Moog ladder filter 的差分对响应模型
- **erf 频谱有奇异零点**——大多数听感场景下是缺点
- **硬剪裁混叠严重**：踏板听起来好是因为模拟电路的「不完美」软化了它
- **tanh 直接调 vs 倒平方根 sigmoid = 13×**：纯代数 + `sqrt` 指令 + 编译器自动向量化 vs 函数调用
- **ARM 与 x86 不同**：ARM 无完整 `sqrt` 但有 `vrsqrte`/`vrsqrts`，显式 SIMD 增益更大
- **多项式变形技巧**：用 `tanh x = sinh x / sqrt(1 + sinh²x)` 把 tanh 拆成 「多项式近似 sinh + 倒平方根 sigmoid」
- **精度/耗时**：5 次奇多项式 → 2e-4 / 0.55 ns，打败 Deep Voice 论文的 rational approximation
- **erf 七次变形** 打败 Abramowitz & Stegun 经典近似
- **误差平滑性**：多项式变形比分段近似更好，频谱行为与真函数几乎无差，人耳无法区分
- **与 Carmack fast inverse sqrt 同脉**：倒平方根 sigmoid 的核心操作是近似倒平方根，John Carmack 那段著名代码的现代 SIMD 后裔

## 链接到的概念

- [[sigmoid-functions]]
- [[faster-math-functions]]
- [[fearless-simd]]
- [[shaping-functions]]

## 原文

- 链接：https://raphlinus.github.io/audio/2018/09/05/sigmoid.html
- 本地：`raw/articles/raphlinus.github.io/2018-09-05_a-few-of-my-favorite-sigmoids.md`
