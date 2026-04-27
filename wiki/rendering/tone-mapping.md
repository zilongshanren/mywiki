---
tags: [rendering, hdr, post-processing, color, pbr]
date: 2026-04-27
sources: 1
---

# 全局色调映射（Global Tone Mapping）

物理正确的渲染管线产出的 HDR radiance 值理论上无界，而标准 SDR 显示器仅接受 [0, 1] 范围内的 sRGB 值。**色调映射**（tone mapping）是把 HDR 线性场景值压缩到该范围的过程，同时尽量保留视觉上的真实感印象——因为 SDR 显示器无法真正重现真实世界的亮度，所以正确与否没有严格定义，最终是一个艺术与感知的权衡。

色调映射通常作为后处理的一部分在独立的 pass 中运行，输入来自 [[luminance-histogram-exposure|自动曝光]] 调整后的 HDR 缓冲区。典型流程：

1. 在 RGBA16F 浮点帧缓冲中渲染场景（线性空间）。
2. 用直方图计算平均场景亮度，推导曝光值，对 HDR buffer 做亮度缩放。
3. 将缩放后的亮度值送入色调曲线，输出 [0, 1]。
4. 应用 sRGB 或伽玛变换，写入最终 backbuffer。

## 常见曲线

### Reinhard 曲线

最简单的解析式：`L_d = L / (1 + L)`，永远不会真正到达 1。改良版加入白点控制 `L_d = L(1 + L/L_white²) / (1 + L)`，当 `L = L_white` 时输出恰好为 1。操作可以施加在 CIE xyY 的 Y 通道（保色相）或逐 RGB 通道独立（会出现饱和度下降）。

### ACES 与电影曲线

ACES（Academy Color Encoding System）是电影工业标准，Narkowicz 给出了可用于实时渲染的简化 S 曲线近似。UE4 使用基于 ACES 的色调曲线。Hajime Uchimura 的 Gran Turismo 曲线（GT 曲线）、Timothy Lottes 曲线均属电影曲线阵营，风格上比 Reinhard 更"胶片感"：高光不是简单衰减，而是有明显的 shoulder 控制。

电影曲线的共同特点是**深部（foot）和肩部（shoulder）均可调**，中间调保持近似线性，因此可以在保留高光细节的同时抑制阴影的黑色噪点。

### 逐亮度 vs 逐通道应用

色调曲线可以**只作用于亮度 Y**（CIE xyY 空间），再把缩放后的 Y 换算回 RGB，保色相但在极端高光处会出现"留住了蓝天而没变白"的反常感。另一种做法是**逐 RGB 通道独立应用**，这更接近 John Hable 等人的建议，允许高光自然饱和变白，但会引起色相漂移。两者都有实际应用，选择取决于创作意图。

## 伽玛与 sRGB 的关系

色调映射完成后仍需应用电光转换函数（EOTF 的逆变换）。对 SDR 显示器，这意味着把线性值转换为 sRGB 编码（约 `pow(x, 1/2.2)` 近似）。这一步是**必要的**：如果跳过，即便场景曝光正确，图像亮度感知仍会与预期相差很远。

## 与局部色调映射的区别

全局色调映射用单一曝光值统一处理整帧。这在动态范围极大的场景中无法同时保留亮区和暗区细节，需要 [[local-tonemapping]] 补充。两者并不互斥——工业实践中常用 LTM 处理整体，再附加全局曲线做最终"look"。

## Sources

- [[sources/bruop-tone-mapping]]
- [[sources/bruop-exposure-histogram]]
