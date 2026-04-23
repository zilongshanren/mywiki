---
tags: [采样, 重要性采样, 离线工具, ssao, 半球采样]
date: 2026-04-19
sources: 1
---

# 带重要性的样本点迭代松弛

生成一组「球形 / 半球形内部均匀分布」的采样点，离线生成、烘进代码，是 SSAO、shadow PCF、DoF bokeh 等效果的标准做法（[[poisson-disk-sampling|Poisson disk]] 是最常见版本）。**[[angelo-pesce]] 2010 年底的 *stupid sample generator 3d version* 给出了 Poisson-disk 思路的一个变体：每个点都带一个「重要性权重」，权重不仅影响最终烘出的 sample weight，还影响该点在松弛过程中的「排斥半径」。**这是一种**非均匀 Poisson**——密的地方权重大，稀的地方权重小，但最终覆盖的立体体积比之和要尽量接近理论半球体积。

## 算法本身（Processing 小沙盒）

- **初始化**：32 个点随机撒进 `[-1, 1]^3` 立方体
- **每帧一轮 relaxation**：
  1. **形状约束**：超出单位半球就投影回表面；`z < radius` 的点被顶到 `z = radius`——强制留在上半球
  2. **距离约束**：对每个点随机抽 50 个邻居，若距离小于 `importance * mindist`，沿两点连线把自己推开——这是随机梯度版的 Lloyd 式松弛
- **鼠标交互**：右键加一点噪声扰动跳出局部最优；中键减小 `mindist` 收紧半径；左键 dump 当前点集与权重，打印 `volume ratio = unit_hemisphere_volume / sum(point_volumes)`，给作者一个**是否对半球体积做了充分覆盖**的标量指标

关键的重要性函数是：

```
importance = 1.3 - (z/scale + z/len) / 2
```

它让靠近顶部（z 大）的点排斥半径更小、密度更大；靠近基底（z ≈ 0）的点排斥半径更大、密度更稀。对半球体积采样来说，这等价于**把更多样本投到"仰角大"的方向**——对 AO 这类 cosine-weighted integrand 天然有利，权重本身就隐含在点的排斥半径里，不需要额外 jitter。

## 为什么值得记一笔

2010 年工业实践里，SSAO / PCF 的 sample kernel 往往就是手动硬编码或静态 `rand` 出来的一张表，离「可控的重要性分布」很远。Pesce 这类 "stupid generator" 把两件事提前到离线：

1. **几何约束**（半球 / 球 / 方块 / 单位圆盘）在生成期静态保证
2. **非均匀密度**（importance）通过排斥半径本地化表达，不必事后乘 weight

后来 [[bartosz-wronski|Bart Wronski 的 Poisson Sampling Generator]]（[[poisson-disk-sampling]]）走的是同一条工作流，只是补上了"前 N 个样本本身也是一个良好分布"的**渐进性**属性、cache-friendly tile 排序、repeating square 等工业特性。Pesce 这篇是原始、未完工的版本。

## 和 Poisson-disk 的关系

Poisson-disk 标准做法（Bridson / Mitchell best-candidate）是**前进式填充**：只增点、不扰动。Pesce 这里是**Lloyd 式松弛**：固定点数、反复推挤直到能量最小。两条路径都能产生蓝噪声谱，但关注的指标略有差别：

- Bridson / Mitchell：保证最小距离下限、前缀也是 Poisson
- Lloyd relaxation：更均匀的 Voronoi cell 体积，但没有前缀性质

Pesce 的写法更接近 Lloyd 但用的是随机邻居抽样（50 sample / point），是一种**stochastic Lloyd**——在当年的 CPU 预算里兼顾简单与收敛速度。

## 相关

- [[poisson-disk-sampling]] —— 更成熟的渐进版蓝噪声生成器
- [[low-discrepancy-sequence]] —— 另一条走 QMC 的替代路径
- [[ground-truth-ambient-occlusion]] —— 半球 cosine-weighted 采样的典型消费者
- [[angelo-pesce]]

## Sources

- [[sources/c0de517e-sample-generator-3d]]
