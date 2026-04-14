---
tags: [source, 渲染, 光谱渲染, 蒙特卡洛, 路径追踪, BRDF]
date: 2026-04-14
sources: 1
---

# Spectral rendering, part 2: Real-time rendering（Christoph Peters）

[[christoph-peters|Christoph Peters]] 2025 年 11 月发表的光谱渲染三部曲第二篇。在 Part 1 解决了「谱从哪来」之后，这篇的任务是把整套东西塞进路径追踪器并证明它**在实时预算下是完全可承受的**。

## 摘要

一个像素的值是对整个可见光谱的积分。与其把 RGB 三元组替换成 16 维向量（精度差又贵），不如用 **Monte Carlo** 抽取 $m \approx 4$ 个波长、每条路径独立走。关键是把**光源谱**作为重要性采样密度的主导因子，$p(\lambda) \propto i(\lambda) \cdot \|(\bar{r}, \bar{g}, \bar{b})(\lambda)\|_1$，因为反射率谱平滑接近 1、不会引入大方差，而发射谱可以像金卤灯一样尖峰密布、必须先采中。实现上，每条光源谱预计算成一张 **8 KiB 的 1D CDF RGBA 纹理**，运行时一次查表拿到所有必要因子。波长采样时用 [Wilkie14] 的 **Hero Wavelength Sampling** 风格的分层抖动：只生成一个均匀随机数 $u$，然后 $u_k = (u+k)/m$，方差显著降低。BRDF 方面以 Frostbite 为例说明「base color + 纯白」两个权重就能概括大多数 PBR 模型——改造成本极小。实测 1920×1080 / 1 spp 下，Bistro 开销 **2%~7%**，Cornell Box 绝对开销 ≤ 0.3 ms。光谱渲染不再是离线渲染的奢侈品，已经是实时可部署的成熟技术。

## 关键要点

- **MC 估计 + 波长重要性采样**：用 $m=4$ 波长替代 16 维向量，精度更高、成本更低。
- **密度的合理选择**：$p(\lambda) \propto i(\lambda) \cdot \|(\bar{r}, \bar{g}, \bar{b})\|_1$。反射谱故意不参与——无法预知路径会打到哪。
- **CDF LUT**：8 KiB / 光源，lookup 极 cache coherent。同一张 LUT 顺带存好「波长 → 相位 $\varphi$」的 warp，免去后续一次计算。
- **Hero Wavelength Sampling**：一个 $u$ 分 $m$ 段的分层抖动，方差显著降低。Peters 沿用了这个技巧但没有突出"谁是 hero"。
- **Frostbite BRDF 的光谱化**：因为"所有颜色都是 base color 和纯白的线性组合"，BRDF 返回值从 RGB 三元组改成 2D 权重 `(w_base, w_white)`。改造量极小。
- **多光源是开放问题**：直接光照可行；长路径只能走 "先存 Fourier sRGB 三元组，后补波长" 或 wavelength guiding [Ruit21]；前者存储/时间都随路径长度膨胀。
- **实测开销**（RTX 5070 Ti / 1080p / 1 spp）：Bistro 2%~7%，绝对值 ≤ 0.3 ms。Cornell Box 相对更高（19%~36%），但只是因为 Cornell 本身极简单使绝对开销显得"占比大"。
- **比光谱渲染更重要的优势**：色域切换、HDR 显示、相机光谱响应模拟——RGB 渲染都很痛苦，光谱一切解耦。

## 链接到的概念

- [[spectral-rendering]]
- [[hero-wavelength-spectral-sampling]]
- [[spectral-brdf]]
- [[fourier-srgb-spectral-upsampling]]
- [[poisson-disk-sampling]]
- [[christoph-peters]]

## 原文

- 链接：http://momentsingraphics.de/SpectralRendering2Rendering.html
- 本地：`raw/articles/momentsingraphics.de/2025-11-13_spectral-rendering-part-2-real-time-rendering.md`
