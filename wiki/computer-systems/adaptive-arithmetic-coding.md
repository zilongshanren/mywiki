---
tags: [压缩, 算术编码, 信号处理, 数据结构]
date: 2026-04-14
sources: 1
---

# 自适应算术编码模型

算术编码（arithmetic coding）的两个核心组件是 **coder 后端**（怎么把概率变成 bit）和 **概率模型**（怎么估计每个符号的概率）。后者要求**自适应**——随数据流不断更新——才能压缩异质数据。Fabian Giesen 在介绍 Oodle LZNA 时把这套自适应模型从二元推广到多元，并给出一个意外简洁的实现。

## 二元模型：Howard-Vitter 的指数滑动平均

最朴素的二元自适应模型只是给 0 和 1 各开一个计数器。问题是几千个符号之后，单个符号几乎不再影响概率——模型「钙化」了，对数据特性变化反应迟钝。Howard 和 Vitter（1991）提出的「leaky」模型：

```
prob_for_1 = 0.5
f = 1 - 1/32  // 适应率，通常取 1/2^k
adapt(bit):
    if bit == 0: prob_for_1 *= f
    else:        prob_for_1 = prob_for_1 * f + (1 - f)
```

定点版本几乎是工业标准：

```c
prob_scaled = 2048;  // .12 fixed point
adapt(bit):
    if (bit == 0) prob_scaled -= prob_scaled >> 5;
    else          prob_scaled += (4096 - prob_scaled) >> 5;
```

注意一个细节：定点 + 整数右移让概率永远卡在 `[31, 4065]` 不会到 0/1。这等价于**把均匀分布混进真正的 H/V 模型里**——既是 bug 也是 feature，但你必须意识到它。

## DSP 视角：它是一个 1 阶低通滤波器

把 `(p₀, p₁)` 写成向量形式后，更新规则是

```
p' = (1 - α)·p + α·e_{bit}
```

也就是「向量 p 朝着观察到的符号的 one-hot 单位向量做线性插值」。这是一个 **多通道 leaky integrator**，每个符号一条通道。一旦看出这一点，几个事情自然涌现：

- 可以换成 2 阶低通（两套 accumulator 平均）：脉冲响应衰减更快但尾巴更长。
- 也可以用 FIR 低通——例如递增 box filter——这就成了「滑动窗口」模型。
- 唯一的硬约束是：滤波器要 **线性、单位增益、非负冲激响应**——否则概率不再是合法的 PDF。

## 推广到多元字母表

把 `(p₀, p₁)` 直接换成 `n` 维向量、把 `e_{bit}` 换成 `n` 维基向量，理论上就完了。但工程上还得处理 quantization：所有概率得是整数、和必须是固定的 2 的幂。Giesen 的做法是预计算 `n` 个 mix-in CDF（每个符号一个），更新时只做一次混合：

```c
int CDF[nsyms + 1];          // CDF[nsyms] 永远等于 1<<bits
int mixin_CDFs[nsyms][nsyms + 1];

void adapt(int sym) {
    int *mixin = mixin_CDFs[sym];
    for (int i = 1; i < nsyms; ++i)
        CDF[i] += (mixin[i] - CDF[i]) >> rate;
}
```

这是二元定点更新规则的直接推广，而且**一次更新只动 CDF 不动 PDF**——所以总和自动守恒、所有概率的下限自动保持为正（只要初始 CDF 和 mixin CDF 都正）。每个 `i` 之间没有依赖，可以 SIMD 化，对 16-symbol nibble 模型来说几乎免费。

## 为什么这件事现在才有意义：rANS 改变了成本结构

历史上多元自适应模型几乎不实用——传统算术编码在多元时每解一个符号要做一次整数除法 + 二分查找，慢到只能用「deferred summation」之类近似，或者干脆退化到二元 + 把字节切成 8 次 binary decode。

[[rans-coder|rANS]]（Jarek Duda 2014）改变了这一点：它仍然能直接用 CDF 编/解多元符号，但解码端**不需要除法**，速度只比二元 arith 慢一点点。于是 LZNA 把字节切成 nibble、用 16 元自适应模型，每字节只要 2 步 decode 就够，比二元的 8 步 decode 快得多——这是 rANS + 中等字母表自适应模型「中间路线」的产物。

## 哲学

ryg 这篇文章最有价值的一点是：**把信息论里的「概率模型」翻译成 DSP 里的「滤波器设计」之后，整个空间一下子打开了**。「我们应该用哪种模型」从「有没有论文」变成「我想要怎样的脉冲响应」。这种跨学科的视角迁移本身就是设计灵感的源泉。

## 相关

- [[probabilistic-algorithms]]
- [[bits-and-context]]
- [[fabian-giesen]]

## Sources

- [[sources/ryg-models-for-adaptive-arithmetic-coding]]
