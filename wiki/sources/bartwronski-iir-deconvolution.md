---
tags: [source, 渲染, 信号处理, 优化]
date: 2026-04-14
sources: 1
---

# Gradient-descent optimized recursive filters for deconvolution（Bart Wronski）

[[bartosz-wronski|Bart Wronski]] 2022 年 9 月发表的文章，是他「图像反卷积 / 去模糊」系列的续篇。前一篇讲传统 FIR 反卷积；这篇补上他刻意忽略的部分——**IIR（recurrent）滤波器**——并提出一种**用梯度下降直接学 IIR 系数**的数据驱动方法，绕过 Z 变换那套理论门槛。

## 摘要

文章先用最简单的 [0.5, 0.5] box blur 演示一个事实：把卷积写成等式做代数变换，立刻得到一个只有两个抽头的 IIR 滤波器，**精确**反演了原卷积。这是 17 抽头 FIR + Hann window 都做不到的事情。代价是冲激响应无限振荡、Nyquist 频率被放大到无穷，输入只要混入一点高频就会数值爆炸——「黑雾吃掉整个屏幕」是作者在 God of War 上修过的真实 bug。

接下来作者诚实列出 IIR 在图形里不普及的原因：不稳定、数值精度敏感、数据并行差、需要多次扫描带宽高。**但也指出 TAA 实际上就是 IIR**——0.9 的指数移动平均等价于 ~40 帧 FIR，而显然没人会真的存 40 帧 framebuffer。

正题是数据驱动方法。要反演一个对称 binomial filter，传统做法是正反向各跑一次 IIR（数学上对应解三对角矩阵的 LU 分解）；作者直接用 Jax 写一个可微 IIR 实现，定义 L2 loss，几千次梯度下降迭代就拿到接近理论解的系数。代码极短，不需要任何 Z 变换知识。

文章的两个亮点是：

1. **噪声正则化**：在输入序列上加一点高斯噪声做训练，等价于隐式给每个频率加了一个 SNR 权重——SNR 低的频段自动被压低。这就是 Wiener deconvolution 的本质，但用数据驱动方式得到。
2. **数据分布的影响**：在白噪声上学和在 1/f 自然图像分布上学得到的系数差别巨大——前者宽响应、容易振铃；后者更温和、空间支持更小。这条经验推广到所有数据驱动方法。

## 关键要点

- **IIR 能精确反演线性卷积**：[0.5, 0.5] 反演成 $x[n] = 2 y[n] - x[n-1]$，对应卷积矩阵的下三角 LU。
- **IIR 在图形里不流行的真实原因**：不稳定 + 数值精度 + 串行 + 多次扫描带宽——单遍 21×21 FIR 反而带宽更优。这也是 ML 圈从 RNN 转 attention 的同一类原因。
- **TAA 是隐藏的 IIR**：0.9 EMA ≈ 40 帧 FIR，IIR 让「时间累积」可行。
- **双向 IIR 处理对称非因果滤波**：正反向各跑一次同一个 IIR，相位偏移抵消，频率响应是单遍响应的平方。
- **梯度下降学 IIR**：可微实现 + L2 loss + 几千次迭代，绕过整个信号处理理论。
- **加噪声 ≈ 隐式 Wiener**：噪声幅度 ≈ 信号时滤波器自动变成低通去噪。
- **训练分布很关键**：白噪声 vs 自然图像统计的最优反卷积系数差别巨大。

## 链接到的概念

- [[iir-filter-deconvolution]]
- [[bartosz-wronski]]

## 原文

- 链接：https://bartwronski.com/2022/09/05/gradient-descent-optimized-recursive-filters-for-deconvolution-deblurring/
- 前篇：https://bartwronski.com/2022/05/26/removing-blur-from-images-deconvolution-and-using-optimized-simple-filters/
- 本地：`raw/articles/bartwronski.com/2022-09-05_gradient-descent-optimized-recursive-filters-for-deconvoluti.md`
