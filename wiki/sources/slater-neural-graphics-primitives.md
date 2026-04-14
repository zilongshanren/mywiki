---
tags: [source, 渲染, 神经渲染, 机器学习, NeRF]
date: 2026-04-14
sources: 1
---

# Exploring Neural Graphics Primitives（Max Slater）

[[max-slater|Max Slater]] 2022 年 11 月的长文，从「神经网络能表示任何函数」这条简单观察出发，把 **神经图形原语** 这条路线一口气铺到 Instant NGP。典型 Slater 风格：数学与工程交织，每换一个技术就给一张同参数下的复现图做对比。

## 摘要

文章以一张 Perth Zoo 的 numbat 图作为「被压缩的信号」，逐步训练一个小 MLP 去过拟合它。一路下来展示：ReLU 的折线伪影 → 输出加 sigmoid → SIREN 的 sinusoid 激活（对权重初始化极端敏感）→ Gaussian 激活（鲁棒、外推行为合理）→ 加位置编码 / Fourier features（质量戏剧性提升）→ Instant NGP 的多分辨率哈希编码（近乎无损 + 训练时间从小时级压到秒级）。最后扩展到 Neural SDF、NeRF 与 Neural Radiance Cache——说明「输入编码 + 小 MLP」这套范式已经不只是图像压缩的玩具。

## 关键要点

- **过拟合即压缩**：当目标只是在训练集上复现信号时，神经模型就是一种有损编码。
- **激活函数决定高频上限**：ReLU 出折线痕，SIREN 出高频但敏感，Gaussian 鲁棒但低频易糊。
- **输出层 sigmoid 几乎永远是好主意**，因为它把网络的输出空间显式约束到 $[0,1]$。
- **位置编码（Fourier features）**是 NeRF 兴起的真正原因——它是一个固定的、不可学习的初始层，把 $x$ 映成 $[\sin 2^0 x, \cos 2^0 x, \dots]$，大幅提升 ReLU/Gaussian 网络的高频表示能力。
- **Instant NGP 的多分辨率哈希编码**：多层分辨率网格，每层查哈希表拿 $F$ 个可学习参数，拼接后送进两层 MLP。哈希冲突不处理，由 SGD 学会抵抗。
- **可学习编码 + 极小 MLP** 是 Instant NGP 的关键，不只是哈希本身。作者选 2 层 × 64 维 MLP，$T=1024\sim 2^{14}$ 等超参很关键。
- **通用范式**：把任意数据集改写成 $f : \text{坐标} \to \text{值}$ 就能用这套流程——图像、SDF、光场、体积都是它的实例。

## 链接到的概念

- [[neural-graphics-primitives]]
- [[spherical-harmonics]]（类比：另一种「信号用基函数展开」）
- [[raymarching-intro]]
- [[max-slater]]

## 原文

- 链接：https://thenumb.at/Neural-Graphics/
- 本地：`raw/articles/thenumb.at/2022-11-27_exploring-neural-graphics-primitives.md`
