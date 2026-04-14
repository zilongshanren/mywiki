---
tags: [渲染, 光栅化, 齐次坐标, 数值稳定性, debugging]
date: 2026-04-14
sources: 1
---

# 齐次坐标三角形光栅化的转置陷阱

Olano & Greer 1997 年的论文 *Triangle scan conversion using 2D homogeneous coordinates* 提出了一种把三角形 setup 与边判别统一在齐次坐标下的优雅方案：把三个顶点的 `(x, y, w)` 列拼成 3×3 矩阵 `M`，对它求逆得到 `M⁻¹`；`M⁻¹` 的三行就是三条边方程的系数，同时也是用于属性插值的重心坐标变换。和经典的 [[pineda-edge-rasterization|Pineda 边方程]] 比，这套方案不需要在 viewport 之前显式做透视除法，对 [[perspective-correct-interpolation|透视校正插值]] 与裁剪的处理也更自然，是现代 GPU triangle setup 文献里的一个常用底子。

[[matthaeus-chajdas]] 在 2010 年的一篇短笔记里记录了一个**几乎抓不到**的 bug：当 `M⁻¹` 在某一步**不小心被转置**——典型原因是手写 3×3 [伴随矩阵求逆](https://en.wikipedia.org/wiki/Matrix_inverse) 时漏写了一次 transpose，或者向量是从「错的一边」乘进矩阵的——光栅化几何上看起来仍然正确，但**整个三角形被插值出同一个 z 值**。

## 为什么这个 bug 难抓

抓 bug 的过程像在拆三层套娃：

1. **错误的 z 值刚好等于某一个顶点的 z**。如果你只画 1 px 大小的三角形做单元测试，结果完全正确——没有 quad 之间的差异，也没有 z-fighting。错误只在跨像素插值时浮现。
2. **`M` 远非对称**，所以「转置后还能算出正确值」违背直觉。任何人第一反应都不会怀疑转置；更可能的怀疑对象是数值稳定性，因为齐次坐标下的 setup 矩阵 [[bottleneck-analysis|条件数]] 普遍不好。Chajdas 自述他花了**大量时间改善矩阵 conditioning、换不同的 inversion 算法**，结果证明这些都不是病根。
3. **`M⁻¹` 的列（或行，依 layout 而定）同时被边判别用**——既然边方程跑得对，三角形覆盖区域也对，那矩阵的项肯定算对了……除了它们其实是被「以 3 行 3 列对角翻转」过一次。

把 transpose 加回来后，z 沿三角形线性变化，结果与参考一致。

## 一个顺手的微优化

修正后还有一个细节：用 `(x, y, 1)` 乘 `M⁻¹` 得到的三个分量，三个分量加起来本身就等于 `w`——也就是说**插值常数 1 的那一行不需要做矩阵乘法**，把另外两行求和就得到 `w`，省下三次乘法。`1/w` 又是 [[perspective-correct-interpolation|透视校正插值]] 的核心，所以这个优化在 inner loop 里值得做。

## 给 debugging 实践的启示

这个故事是 [[debug-visualization|可视化 debug]] 的一个反面教材：单单看「图像看上去对吗」会通过测试，因为转置后的几何与覆盖完全正确。真正暴露问题的可视化是**把 z 渲染成灰度图**——一旦三角形内部是平坦的色块而不是渐变，bug 就一目了然。再加上「拿一个超大三角形画一遍」可以让 1-pixel 偶合消失。这是「单元测试要选不会侥幸通过的输入」的具体例子。

## 相关

- [[pineda-edge-rasterization]]
- [[triangle-setup]]
- [[perspective-correct-interpolation]]
- [[rasterization]]
- [[debug-visualization]]
- [[matthaeus-chajdas]]

## Sources

- [[sources/anteru-homogeneous-rasterization-gotcha]]
