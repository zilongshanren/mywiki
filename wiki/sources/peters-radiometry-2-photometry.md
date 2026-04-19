---
tags: [source, 渲染, 辐射度量, 光度学, 光谱, 颜色]
date: 2026-04-19
sources: 1
---

# Radiometry, part 2: Spectra and photometry（Christoph Peters）

[[christoph-peters|Christoph Peters]] 2025 年 1 月系列第 2 篇，把第 1 篇的"色盲"radiometric 量加上波长维度变 spectral 量，再通过 CIE 色匹配函数衔接 photometric 量（luminance 等）。

## 摘要

radiometric 量把紫外/红外和可见光一视同仁——物理正确但**对渲染无用**。需要加波长 $\lambda$ 维度。从 "radiant energy of photons with wavelength ≤ $\lambda$" 起步，对 $\lambda$ 求导得 **spectral radiant energy**，单位 $\mathrm{J}/\mathrm{nm}$——其它光谱量同构构造。CIE XYZ 色匹配函数 $\bar{x}(\lambda), \bar{y}(\lambda), \bar{z}(\lambda)$ 把光谱 radiance 压成 XYZ 三元组；$L_Y$ 即 luminance（nit），是 photometric 量。完整 photometric 对照：radiance↔luminance (nit)、irradiance↔illuminance (lux)、intensity↔luminous intensity (cd)、flux↔luminous flux (lm)、energy↔luminous energy (talbot)。日常意义：灯泡标 lm、显示器标 nit、聚光灯标 cd。光谱存储是难题：80 个 5 nm 采样 × 百万像素 = GB 级纹理不现实；Peters 自己的 Siggraph 2019 方法用 Fourier 系数 + moment theory 做光谱上采样（[[fourier-srgb-spectral-upsampling]]），3–4 系数就能从 sRGB 还原反射率谱。光谱渲染 MC 积分用 [Wilkie14] Hero Wavelength Sampling 挑 4 波长——实时可行。文章末尾吐槽色彩空间乱象：CIE XYZ 自 1931 有修订、white point 选择、sRGB/Rec2020/P3、OS/browser/driver 的 color management 各自为政——人眼白平衡又把差异掩盖。建议：做 spectral rendering 前先锁定 XYZ 标准 + white point + RGB space。

## 关键要点

- **光谱 = 波长维度的密度函数**，不是"16 个通道的向量"。
- **CIE XYZ 色匹配函数**把光谱压到三元组；$L_Y$ 即感知 luminance。
- **radiometric ↔ photometric** 一一对应，单位对应 lm/nit/cd/lx/talbot。
- **光谱上采样**：把 sRGB 纹理变成 Fourier sRGB（3–4 系数），存储和带宽 ≈ RGB。
- **Hero Wavelength Sampling** [Wilkie14]：MC 积分挑 4 波长、方差低。
- **色彩管理是雷区**：提前锁定标准，否则几 GB 资产白做。

## 链接到的概念

- [[photometry-luminance]]
- [[radiometry-integral-view]]
- [[spectral-rendering]]
- [[fourier-srgb-spectral-upsampling]]
- [[hero-wavelength-spectral-sampling]]
- [[color-space]]
- [[christoph-peters]]

## 原文

- 链接：http://momentsingraphics.de/Radiometry2Photometry.html
- 本地：`raw/articles/momentsingraphics.de/2025-01-19_radiometry-part-2-spectra-and-photometry.md`
