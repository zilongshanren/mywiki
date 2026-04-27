---
tags: [source, graphics, color-quantization, self-organizing-map, gif, notebook]
date: 2026-04-19
sources: 1
---

# Color quantization with a self-organizing map（Pekka Väänänen / 30fps.net）

[[pekka-vaananen]] 2024 年 3 月 notebook，复刻 ScreenToGif 里 `NeuralQuantizer` 的做法：用一维 Kohonen 自组织映射（SOM）学 256 色调色板。

## 摘要

GIF 录制工具 ScreenToGif 把"神经量化"命名为 NeuralQuantizer，原以为是全连接网络，作者读源码后发现其实是**一维 SOM**——邻居神经元一起更新，最终调色板沿索引方向平滑过渡。用 `sklearn-som` 配 `m=256, n=1, dim=3` 就能复刻；关键 trick 是把权重初始化成 `linspace(0, 1)` 的灰度渐变，远胜默认随机初始化。输出调色板拥有**拓扑**：相邻索引颜色相近，渐变天然可控。副作用是容易浪费槽位在几乎重复的颜色上，解法是训练末期减小 `sigma`，让"邻居约束"衰减，让末尾若干神经元独立微调。

## 关键要点

- SOM vs K-Means：前者调色板有序、后者调色板无序；前者槽位浪费、后者主色饱和度更高。
- 灰度初始化让 SOM 收敛又快又稳。
- NeuralQuantizer 成功的关键：后期衰减邻居半径，近似回到纯聚类。
- 适合 GIF、像素画、LUT 等要求调色板"索引方向可读"的场景。

## 链接到的概念

- [[color-quantization-som]]
- [[color-quantization-kmeans]]
- [[color-quantization-retro]]
- [[color-lut]]

## 原文

- 链接：<https://30fps.net/notebooks/sompalette>
- 本地：`raw/articles/30fps.net/2024-03-08_color-quantization-with-a-self-organizing-mapp.md`
