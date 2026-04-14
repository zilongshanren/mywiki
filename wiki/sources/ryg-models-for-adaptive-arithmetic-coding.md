---
tags: [source, 压缩, 算术编码, 信号处理]
date: 2026-04-14
sources: 1
---

# Models for Adaptive Arithmetic Coding（Fabian Giesen）

[[fabian-giesen|Fabian "ryg" Giesen]] 2015 年 5 月发表的长文，介绍 Charles Bloom 在 RAD Oodle LZNA 里采用的**中等字母表自适应模型**——并把整套自适应建模思想从信息论翻译成 DSP 滤波器视角。

## 摘要

文章先回顾经典的 **Howard-Vitter 二元自适应模型**：两个累加器、指数滑动平均、定点版用右移代乘法。这个模型背后真正的数学结构是「向量 `(p₀, p₁)` 朝着 one-hot 单位向量做线性插值」——也就是一个 **多通道 1 阶 leaky integrator / IIR 低通滤波器**。一旦用 DSP 视角看，整个空间打开了：可以换成 2 阶低通（两套 accumulator）、可以换成 FIR 低通（box filter = sliding-window 模型）、可以借用 Heckbert 的 repeated integration 实现任意分段多项式权重——只要保证滤波器线性、单位增益、非负冲激响应。

把同一个更新规则推广到多元字母表后，问题在 quantization：所有概率得是整数、和必须是 2 的幂。Giesen 的解决方法是为每个符号预计算一个 mix-in CDF，更新只是

```c
for (int i = 1; i < nsyms; ++i)
    CDF[i] += (mixin[i] - CDF[i]) >> rate;
```

这是二元定点更新规则的自然推广，每个 `i` 之间没有依赖，可以 SIMD 化。

为什么这个想法此前没成主流？历史上多元算术编码的 per-symbol 开销极高（除法 + 二分查找），自适应版本更糟（Fenwick tree）。**[[rans-coder|rANS]]** 改变了成本结构：它解码端不需要除法，速度只比二元算术编码慢一点点，于是「中等字母表 + 快速自适应」终于划算。LZNA 把字节切成 nibble、用 16 元自适应模型，每字节 2 步 decode 取代了传统二元的 8 步。

## 关键要点

- **二元自适应模型的本质是一个 1 阶低通滤波器**：「概率向量 ← 旧概率向量 与 one-hot 的线性插值」。
- **DSP 视角打开整个设计空间**：滤波器只需要「线性 + 单位增益 + 非负冲激响应」三个约束，2 阶 IIR、FIR、滑动窗口都行。
- **定点版隐含均匀混合**：固定 `>>5` 的版本会让概率永远卡在 `[31, 4065]`——等价于把均匀分布按权重混进 H/V 模型，必须意识到这一点才能正确分析。
- **多元更新只动 CDF，不动 PDF**：自然守恒、不会跌到 0、SIMD 友好。
- **rANS 让中等字母表重新可用**：8 步二元 → 2 步 nibble。LZNA 的核心创新就是这个。
- 评论里 ryg 还澄清：**单 pass rANS 加自适应模型不可行**，必须先正向建模 + 推 interval，再反向 rANS 编码。decoder 自然按数据顺序看到符号。

## 链接到的概念

- [[adaptive-arithmetic-coding]]
- [[fabian-giesen]]
- [[probabilistic-algorithms]]
- [[bits-and-context]]

## 原文

- 链接：https://fgiesen.wordpress.com/2015/05/26/models-for-adaptive-arithmetic-coding/
- 本地：`raw/articles/fgiesen.wordpress.com/2015-05-26_models-for-adaptive-arithmetic-coding.md`
