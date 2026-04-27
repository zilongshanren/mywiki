---
tags: [渲染, fp64, double-precision, map-projection, glsl, planet-engine, 数学库, minimax]
date: 2026-04-27
sources: 1
---

# GPU fp64 地图投影近似

在行星尺度引擎中，将 3D 球面坐标转换为屏幕空间地图投影（等经纬投影、墨卡托投影）需要高精度三角与对数函数。问题在于 `ARB_gpu_shader_fp64` 扩展只提供加/减/乘/除/sqrt——`atan`、`ln`、`tan` 等超越函数**刻意缺失**，部分厂商还通过降低 fp64 吞吐量（相对 fp32 有时慢 16-64×）来区隔消费与专业显卡市场。

## atan2 的 Minimax 近似

fp64 `atan2` 可用 **lolremez 工具**生成 9 阶 minimax 多项式实现，误差 < 5×10⁻⁹（地球表面约 3 cm）。评估时全程走 Horner+FMA 链，系数 10 个，argument reduction 利用 ax/ay 做象限折叠后在 $[0,1]$ 上求值，再还原符号。这套方法与 [[fp64-sincos-minimax]] 中 sin/cos 的处理思路完全一致：**Remez minimax 替代 Taylor，Horner+FMA 提升稳定性。**

## 墨卡托投影的代数变形

墨卡托 y 轴公式为 $y = \ln\!\bigl(\tan(\pi/4 + \varphi/2)\bigr)$，直接实现需要 fp64 的 `ln` 和 `tan`，两者均不可用。Outerra 的技巧分两步：

1. **消去 tan**：在 ECEF 坐标系下，$\tan\varphi = z / \sqrt{x^2+y^2}$，即可用三维坐标的 sqrt 与除法表达，完全在 `ARB_gpu_shader_fp64` 支持范围内。

2. **消去 ln**：利用对数差值——CPU 预计算屏幕中心点的参考值 $\ln(\sqrt{k^2+1}+|k|)$，shader 只需计算关于参考点的**相对偏移**，此时 $a/b \approx 1$，可用 $\ln(x) \approx 2(x-1)/(x+1)$（fp64 版本，在 x 接近 1 时误差极小）甚至单精度 `log` 处理。

最终 shader 中只剩 fp64 的加/乘/sqrt 与一次精度要求宽松的对数，全部在扩展支持范围内。

## 与 fp64 sin/cos 的关系

两篇文章（[[fp64-sincos-minimax]] 与本文）体现同一设计思路：**能用代数变形消去超越函数就消，消不掉的用 Remez minimax 多项式近似**。区别在于 sin/cos 在 GLSL 里完全没有 fp64 实现，只能全靠多项式；而地图投影因为有坐标代换的自由度，能把大部分超越函数归结为基本运算，多项式只作最后一步的补丁。

## 相关

- [[fp64-sincos-minimax]] — 同一作者对 fp64 sin/cos 的 minimax 实现，系数与方法论互补
- [[huge-world-coordinate-precision]] — 行星引擎中 fp64 精度问题的宏观视角
- [[single-precision-float-world-offset]] — fp32 世界坐标偏移量的经典解法（camera-relative）
- [[planet-terrain-dem-pipeline]]
- [[outerra-team]]

## Sources

- [[sources/outerra-dp-map-projections]]
