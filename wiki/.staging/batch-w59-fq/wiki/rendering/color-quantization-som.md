---
tags: [color-quantization, palette, self-organizing-map, gif]
date: 2026-04-19
sources: 1
---

# 自组织映射（SOM）调色板量化

**自组织映射**（Kohonen SOM）是一种把高维数据投影到低维**有序网格**的神经网络变体。用作 GIF 调色板提取时，把「网格」取成 1D 的 `M` 个神经元，每个神经元学到一个 RGB 颜色——训练收敛后这 M 个颜色就是调色板。更新规则会同时拉动**邻居神经元**朝同一方向，使得最终调色板沿着索引方向**平滑过渡**，而不是像 [[color-quantization-kmeans|K-Means]] 那样离散乱跳。[[pekka-vaananen]] 注意到知名的 GIF 录制工具 *ScreenToGif* 里的 `NeuralQuantizer` 本质就是 1D SOM，自己用 `sklearn-som` 复刻了一版。

## 流程要点

- **初始化成灰度渐变**（`np.linspace(0,1,M)` 复制到三通道）比默认高斯噪声收敛快得多，且调色板初始就有良好拓扑；
- `SOM(m=M, n=1, dim=3, lr=1.0, sigma=2, max_iter=3000)` 扫一遍像素即可；
- `predict` 给每个像素一个调色板索引，`cluster_centers_` 读出最终调色板；
- 部分槽位可能从未被分配，真实用到的颜色往往少于 `M`。

## SOM vs K-Means 直觉

| | K-Means | SOM |
|---|---|---|
| 调色板顺序 | 无意义，索引可互换 | 有意义，邻居像素索引相近 → 颜色相近 |
| 收敛特征 | 质心自由重分布 | 受邻居惯性约束 |
| 常见 side effect | 小 cluster 被吞并 | 末端若干槽位空转（近色扎堆） |

作者观察到的遗憾：**SOM 的平滑性是双刃**——平滑的代价是很多槽位被浪费在几乎相同的颜色上；想解这个问题，可在训练后期减小 `sigma` 让邻居约束退化，让最终每个槽位能独立调整（`NeuralQuantizer` 就这么做了）。

## 适用场景

- GIF / 索引色 PNG 编码时需要 ≤256 色；
- 像素画工具需要「生成的调色板在索引上可直接当渐变用」（相邻条目视觉相近）；
- 某些复古渲染 effect（LUT 横向插值）也受益于有序调色板。

## 相关

- [[color-quantization-kmeans]] —— 无序聚类调色板
- [[color-quantization-retro]]
- [[vector-quantization-tilemap]]
- [[color-lut]]

## Sources

- [[sources/30fps-som-palette]]
