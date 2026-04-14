---
tags: [渲染, 颜色, 光谱, 上采样, 纹理压缩]
date: 2026-04-14
sources: 1
---

# Fourier sRGB 与光谱上采样（Spectral Upsampling）

**光谱上采样**是把一个 sRGB 三元组 $(R,G,B)$ 变成一条平滑的反射率光谱 $a(\lambda)$ 的问题，要求：

1. $a(\lambda) \in [0, 1]$——能量守恒；
2. 把该光谱通过 CIE XYZ 色匹配函数积分、再转回 sRGB，**精确还原原始 sRGB 颜色**；
3. 光谱形状**类似真实测量到的反射率光谱**（平滑、无尖锐峰）。

这是 [[spectral-rendering|光谱渲染]]落地到 RGB 美术管线的关键一环。没有它，每个 4K 纹理集会因为「每像素存一条谱」膨胀到不可接受（几百 GB）。

## Fourier sRGB：一次预处理换一辈子的轻量

Christoph Peters 在 SIGGRAPH 2019 和 MAM 2019 提出的方案是**对每张 sRGB 纹理做一次离线 3D LUT 查表**（$256^3$），把 $(R,G,B)_\mathrm{sRGB}$ 映射到一套新的三元组 $(R,G,B)_\mathrm{Fsrgb}$，称为 **Fourier sRGB**。关键性质是：

- 纹理**仍然是三通道**，可以继续用 BC1 压缩，半字节/纹素——内存和带宽代价和普通 sRGB 纹理完全一样；
- 采样时用 `VK_FORMAT_BC*_SRGB_BLOCK` 这类格式，硬件会自动做 sRGB 解码；
- 运行时从采样到的线性 Fourier sRGB 三元组 $(R_\mathrm{LF}, G_\mathrm{LF}, B_\mathrm{LF})$，可以在几条指令内算出一组 **Lagrange 乘子** $L \in \mathbb{R}^3$，之后任何波长 $\lambda$ 的反射率就是：

$$a(\lambda) = \tfrac{1}{\pi} \arctan(\text{一个关于 } L, \varphi(\lambda) \text{ 的线性组合}) + \tfrac{1}{2}$$

$\arctan$ 的作用是**把任何输入挤进 $(0, 1)$**——这是能量守恒的硬保证。Lagrange 乘子是使得 $a(\lambda)$ 在积分回 XYZ 时精确匹配原 sRGB 颜色的最优化解（最大熵谱估计 MESE 家族）；波长 $\lambda$ 先经过一个单调的 warping 函数变成相位 $\varphi \in [-\pi, 0]$。

## 为什么不直接存 Lagrange 乘子

理论上 $(L_0, L_1, L_2)$ 就是最紧凑的反射率谱表示，只要存这三个数就行——事实上 [Jakob19] 就是这个路子。但 Peters 给出两条反对理由：

- **数值范围极大**：Lagrange 乘子可以非常大或非常小，16-bit 浮点是最低要求；而三通道 FP16 纹理格式硬件支持差，通常要 pad 到 8 B/texel——**比 BC1 大 16 倍**；
- **纹理滤波语义崩坏**：硬件双线性过滤两个相邻纹素的 Lagrange 乘子，得到的谱往往和两个原谱的平均差得很远，视觉上很诡异。

Fourier sRGB 的优势正好就是**在数学上和「感知接近」的 sRGB 值足够像**，所以 BC1 压缩和双线性过滤都不会出大问题。

## 预处理成本

离线把每张 sRGB 纹理跑过 $256^3$ 的 LUT 一次，比起重新烘焙整套 PBR 资产小得多。如果有 shader graph 在运行时产 sRGB 颜色、需要做光谱渲染，也可以把 LUT 搬到运行时采样——代价不便宜但也不贵。

## 和其它方案的关系

- **Jakob19**：同一类问题的另一条路径，同样用三个参数重建谱；Peters 的 Fourier sRGB 主要优势是「能复用 sRGB 纹理的硬件采样路径」。
- **MESE 矩方法**：这套推导的学术根源——有界信号用矩来表示。Peters 的博客是论文的「可读版」。
- **更精细的表示**：对肤色、植被、头发、金属这种「特别重要」的材料，可以单独存储测量到的真实反射率谱，而不依赖 sRGB 上采样。论文里也给出了压缩任意谱的方式。

## 相关

- [[spectral-rendering]] — 为什么需要这个
- [[color-space]] — sRGB / XYZ / linear 的上下游
- [[color-lut]] — 3D LUT 作为工具
- [[christoph-peters]]
- [[functions-as-vectors]] — 「函数是无限维向量」的泛函分析视角
- [[spherical-harmonics]] — 同一视角下在球面上的 Fourier 基

## Sources

- [[sources/peters-spectral-rendering-1-spectra]]
