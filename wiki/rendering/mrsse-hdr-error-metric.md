---
tags: [渲染, 纹理压缩, bc6h, hdr, 误差度量]
date: 2026-04-19
sources: 1
---

# MRSSE：HDR 纹理编码的相对均方误差

**MRSSE**（Mean Relative Sum of Squared Errors）是 Oodle Texture BC6H encoder 采用的 HDR 误差度量。[[fabian-giesen|Fabian Giesen]] 的结论很干脆：他们评估过 8–9 种 HDR 误差度量，最终只有 3 种活到量产阶段，而**MRSSE 既便宜又视觉上最优**——没有一张测试图能证明别的度量更好。

## 问题：log-space SSD 在饱和色上失效

BC6H 本质把 float16 当 16-bit 整数编码（这是一个**半对数映射**）。最朴素的 encoder error 就是在这个整数域上做 SSE / SSD。问题是：对于亮红色像素比如 `(2.34, 0.02, 0.01)`，log-space 里「绿通道差 0.001」和「红通道差 0.1」看起来同样严重，encoder 会为了避免几乎不可见的色调偏移而把总亮度大幅改动。结果是发光红色被"压绿"——Jon Olick 发过一篇著名的反例图。

## MRSSE 的定义

对称版本：

$$\text{MRSSE}(x, y) = \frac{\|x - y\|^2}{\|x\|^2 + \|y\|^2 + \varepsilon}$$

分母里那个 $\varepsilon$ 是一个**极小偏置**（量级是最小 normalized float16），防止 0 向量除零并让度量对 $x \leftrightarrow y$ 对称。物理意义：这是一个**相对平方误差**，对暗区给出适度容忍、对亮区保持严格。

## 非对称快速版

实际使用时 $x$ 是源像素、$y$ 是候选编码——$x$ 固定，encoder 反复试 $y$：

$$\text{MRSSE}_{asym}(x, y) = \frac{\|x - y\|^2}{\|x\|^2 + \varepsilon}$$

每 block 预计算一次 $\|x\|^2$，循环里退化成**加权 SSE**，每像素一个权重因子。由于 MSE 的导数是线性的，**求极值 = 解线性方程组**——BC6H endpoint search 的内循环要做几百次线性最小二乘，保持这个性质意义重大。如果换成非二次度量，线性系统变非线性系统，encoder 速度直接爆炸。

## 为什么这个设计选择值得写下来

- **度量的选择大于算法复杂度**。Oodle 评估过 ICtCp + SMPTE 2084 PQ 版本、log2 原生版本、MRSSE 等 8–9 种，量化结果差别可以**大于 encoder 搜索策略的差别**。
- **"够简单、够好"胜于"理论最优"**。PQ 版本或许最接近感知均匀，但计算更贵，视觉上没有看得见的优势。
- **保线性是硬约束**。对 encoder 内环，误差函数必须二次——否则优化算法要大改。

这是一个**domain-specific 的工程判断**的范例：正确性评估（大量真实图片的 A/B 对比）做足，剩下的就是选最简单能赢的那个。

## 相关

- [[fabian-giesen]]
- [[bc7-solid-color-blocks]]
- [[hdr-tonemapping-basics]]
- [[oodle-compression-suite]]

## Sources

- [[sources/ryg-mrsse]]
