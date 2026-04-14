---
tags: [渲染, 图像处理, 信号处理]
date: 2026-04-14
sources: 1
---

# Laplacian 金字塔

**Laplacian 金字塔**是 Burt & Adelson 1983 年提出的图像多分辨率分解方法。它把一张图像拆成多个尺度的「细节图」加一个最粗的低频残差。每一层 Laplacian 是相邻两层 Gaussian 金字塔之差，因此重建时把每一层 Laplacian 加回上采样后的下一层 Gaussian 即可。

## 构造

1. 从原图 $G_0$ 开始，反复降采样 + 模糊，得到 Gaussian 金字塔 $G_0, G_1, \ldots, G_n$
2. 对每一层（除最粗），$L_i = G_i - \text{upsample}(G_{i+1})$
3. 最粗层 $L_n = G_n$ 直接保留作为低频残差

重建：从 $L_n$ 开始向上累加 $\text{upsample}(L_{i+1}) + L_i$，最后还原出 $G_0$。

## 性质

- **频率分解**：每一层 Laplacian 大致对应一个 octave 的频率带宽。
- **冗余度低**：所有层加起来的像素数约为原图的 4/3。
- **可分尺度操作**：可以独立地放大、衰减、或替换某一层，常见用途包括：去噪、细节增强、风格混合、HDR 融合。

## 在图形/计算摄影里的用途

- **多带融合（Multi-band Blending）**：把两张图片在不同尺度上用不同半径的权重混合，实现无缝拼接。Burt 原论文的应用之一。
- **[[exposure-fusion]]**：每张曝光建一个 Laplacian 金字塔，每层用对应分辨率的 Gaussian 权重 blend。曝光过渡的尺度自动跟随图像内容的尺度。
- **Local Laplacian Filter**：Lightroom 的 Clarity 滑块所属算法家族的基础，对每一层 Laplacian 做非线性变换实现保边的局部对比增强。
- **HDR 融合**：早期 HDR 流水线常用 Laplacian 域融合避免 halo。

## GPU 实现要点

- 不需要为 Laplacian 单独分配存储——算成相邻 Gaussian 层之差即可。
- 用 mipmap 链构造 Gaussian 金字塔是最简单做法，但 box / 双线性下采样质量较差；高质量 LTM 通常用更好的下采样滤波器，并对应调整上采样核。
- compute shader 一次性产生多层金字塔可以省掉中间 store/load 带宽。

## 相关

- [[exposure-fusion]]
- [[local-tonemapping]]
- [[aliasing]]

## Sources

- [[sources/bartwronski-exposure-fusion]]
