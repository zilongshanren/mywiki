---
tags: [source, 渲染, shader, blur, gaussian, post-processing, gamemaker]
date: 2026-04-14
sources: 1
---

# Blur Philosophy（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2024 年 2 月 17 日的 blur 系列开篇，用文章原话：这篇本来计划做订阅限定的 draft，但**重要到必须免费**——因为他早期那版 Gaussian shader 被 ShaderToy / Godot / Construct 到处抄，他需要公开改正自己的错误。

## 摘要

文章以最朴素的 **box blur** 开头：双层 for 循环遍历 `(-r, r)` 的邻域、`tex_sum / weight_sum` 做平均。问题有二：**样本数随半径平方增长**（r=2 就 25 次采样），以及 box blur 在硬边处会产生"方块状"阶梯。引入 **Gaussian distribution** 作为改进：Xor 没用数学推导而是用"对 box blur 多次迭代自然收敛到 normal distribution"作为直观解释，给出 GLSL 版公式 `0.3989423*exp(-0.5*dot(x,x)/(sigma*sigma)) / sigma`，并说明 sigma 控制曲线陡峭度，实用范围 5–8。下一步是**把 Gaussian 预计算为 kernel**，利用它的对称性只存半侧权重、用 `w[0]` 打底再 for loop 左右对称采样。

重点在两节：**Separable blurs**——17 tap 的 2D 卷积理论上需要 289 采样，但利用 `G(x,y)=G(x)·G(y)` 的可分离性，拆成水平 + 垂直两 pass 后只需 2×17 = 34 采样。**Dos and Avoids** 清单作为后续教程的索引：Dos = separable、pre-compute、linear filtering、gamma correction、downscale / power-of-2；Avoids = 过多样本、边界陷阱、过多 surface、循环里用 sin/cos。结尾特别推了 [Dual-Kawase blur](https://github.com/XorDev/Dual-Kawase/wiki) 作为"下采样 + 极少样本"的对数级代价 Gaussian 近似方案。

## 关键要点

- **Box blur 是起点但不是终点**：均匀权重 + 方形邻域在硬边处露出"方块感"。
- **Gaussian = 多次 box blur 的极限**：CLT 视角给出"为什么自然感"的非公式解释。
- **Kernel 预计算**：shader 里不跑 `exp`，CPU 侧算一次传进去；利用对称性只存一半。
- **Separable 核心性质**：`G(x,y) = G(x)·G(y)` 让 N² 采样降到 2N，这是大半径 blur 在实时下能用的根本原因。
- **Dos 清单**：separable、pre-compute、linear filter、gamma correction、downscale 是做高质量 blur 的五件套。
- **Avoids 清单**：多样本、边界、多 surface、循环里的 trig——这些是慢/糊/抖的常见来源。
- **Gamma correction 必须在 linear 空间做 blur**：否则深色会被低估，结果发灰。
- **Dual-Kawase 是对数级扩展**：下采样金字塔 + 极少样本，双倍半径只加 2 pass，是 Xor 推荐的现代 blur。
- **自我纠错动机**：作者为早期流传很广的错误 Gaussian shader 做公开修正——值得记录的开源贡献者礼仪。

## 链接到的概念

- [[separable-gaussian-blur]]
- [[mipmap-generation-sampling]]
- [[bloom-threshold-blur-composite]]
- [[image-convolution-kernel]]
- [[sampler-filter-wrap-modes]]
- [[ping-pong-surfaces]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/blur-philosophy
- 本地：`raw/articles/mini.gmshaders.com/2024-02-17_blur-philosophy.md`
