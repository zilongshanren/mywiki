---
tags: [rendering, post-processing, blur, radial-blur, unity]
date: 2026-04-19
sources: 1
---

# Radial Blur 后处理

**Radial Blur**（径向模糊）是一种**空间变化 kernel 强度**的模糊：屏幕中心近乎不模糊、越往四周模糊越强。它的观感是"对焦在中心、边缘晕开"，常用于加速感、隧道视觉、焦点引导、受击眩晕等情境。和景深（DoF）不同，它不依赖深度——只按**屏幕空间到中心的距离**加权。

## 两种实现路线

- **Zoom blur / 径向采样**：沿 `uv → center` 的矢量方向做多点采样并平均，越远采样数越多或步长越大。真正的"径向"视觉——像朝镜头方向加速。
- **空间变化高斯 blur**：在每像素位置以高斯 kernel 采样邻居，kernel 半径按 `length(uv - 0.5)` 缩放。没有矢量方向，只是"边缘更糊"——更像散光。

Daniel Ilett 的 *Snapshot Shaders Pro* Radial Blur 走的是第二路——"A Gaussian Blur which gets stronger towards the edges of the image"。它把 [[separable-gaussian-blur|分离高斯]] 的 kernel 半径拿一个 `saturate(length(uv - 0.5) - threshold)` 做 weight 来 lerp 到原图。

## 参数设计

Pro 版只暴露两个参数：

- `Strength` —— kernel 尺寸。越大越糊、每帧像素操作数越多（线性 / 平方关系取决于 kernel 可否分离）。
- `Luminance Threshold` —— 中间保持锐利的比例。命名误导：它不是"按亮度阈值"而是"按径向距离阈值"。实际作用是 `weight = saturate((r - threshold) / (1 - threshold))`，threshold 外才开始模糊。

把它和 [[convolution-separability-blur|可分离卷积]] 的假设放在一起看：一旦 kernel 半径逐像素变化，严格意义上 pass 不再可分离，但实践中仍用"两个 pass、每 pass 各自读半径"的近似——误差小到肉眼看不出。

## 和其他模糊的关系

- [[dual-kawase-blur]] —— 下采样迭代式快速模糊，整屏均匀
- [[depth-aware-gaussian-blur]] —— 按深度变化 kernel，服务于 DoF
- [[convolution-separability-blur]] —— 分离卷积的数学基础
- [[bloom-threshold-blur-composite]] —— 辉光，亮度阈值后均匀模糊

Radial Blur 在"kernel 随屏幕位置变化"这个维度上，属于**空间变化 blur**的一类，和按深度变化的 DoF-style blur 是平行的设计分支。

## 相关

- [[separable-gaussian-blur]]
- [[dual-kawase-blur]]
- [[bloom-threshold-blur-composite]]
- [[urp-volume-post-processing]]

## Sources

- [[sources/danielilett-snapshot-pro-radial-blur]]
