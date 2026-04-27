---
tags: [人物, 作者, 渲染, 光谱渲染, 数学]
date: 2026-04-14
sources: 3
---

# Christoph Peters

**Christoph Peters** 是德国图形学研究者，博客 [momentsingraphics.de](http://momentsingraphics.de/) 写的是「把漂亮的数学工具稳稳塞进实时渲染器」这类题目。他的研究主线是**用矩（moments）和傅里叶系数来压缩带界信号**——阴影、光谱、体积——从而用极少的系数就能在 GPU 上高效重建。

## 风格

- **数学驱动 + 工程意识**：他的论文通常从一个古典数学问题（矩问题、最大熵谱估计、Lagrange 乘子）出发，但每篇都会交代「为什么 GPU 可以跑」、「寄存器够不够」、「带宽代价几何」。
- **每个博客配可玩的 Shadertoy / 代码仓**：读者可以直接点开看反射谱长什么样，或者拉一个 path tracer 跑起来。
- **和 Siggraph / i3D / EGSR 接轨**：博客里的长文几乎都对应一篇学术论文，博客是论文的「走心版」——没有审稿人限制的充分解释。
- **关心稳定性和性能边界**：特别爱讨论 [[register-spilling-avoidance|寄存器溢出]]、numerical stability、误差边界证明。

## 对本 wiki 的贡献
| 文章 | 贡献的概念 |
|---|---|
| Spectral rendering, part 1: Spectra | [[spectral-rendering]]、[[fourier-srgb-spectral-upsampling]] |
| Spectral rendering, part 2: Real-time rendering | [[hero-wavelength-spectral-sampling]]、[[spectral-brdf]] |
| Finding Real Polynomial Roots on GPUs | [[polynomial-root-finding-gpu]]、[[register-spilling-avoidance]] |
| Sampling Projected Spherical Caps in Real Time | [[projected-solid-angle-sampling]] |
| Moment Shadow Mapping (I3D 2015) | [[moment-shadow-mapping]] |
| Beyond Hard Shadows: MSM for Single Scattering, Soft Shadows, Translucent Occluders (I3D 2016) | [[moment-shadow-mapping]]（应用扩展） |
| Solving Trigonometric Moment Problems for Fast Transient Imaging (SGA 2015) | [[trigonometric-moment-transient-imaging]] |
| Path tracing workshop | [[path-tracing-basics]] — 76 分钟 GLSL/ShaderToy 入门 |
| Path tracing lectures | [[path-tracing-basics]]（进阶：重要性采样、MIS） |
| Linearly Transformed SH (via student thesis) | [[lt-spherical-harmonics]] — 多边形面光源高光 |
| Ray Tracing Spherical Harmonics Glyphs (VMV 2023) | [[sh-glyphs-ray-tracing]] — SH 字形光线追踪，荣誉提名奖 |
| Radiometry, part 1: I got it backwards | [[radiometry-integral-view]] — 从 radiance 起步的积分式重构 |
| Radiometry, part 2: Spectra and photometry | [[photometry-luminance]] — 光度量与 CIE XYZ 衔接 |
| Spectral rendering, part 3: Spectral vs. RGB | [[spectral-vs-rgb-comparison]] — 实证对比 RGB 与光谱渲染 |

## 相关
- [[spectral-rendering]]
- [[color-space]]
- [[polynomial-root-finding-gpu]]
- [[projected-solid-angle-sampling]]
- [[moment-shadow-mapping]]
- [[trigonometric-moment-transient-imaging]]
- [[cubic-equation-solver-hlsl]]
- [[non-linearly-quantized-msm]]
- [[path-tracing-basics]]
- [[radiometry-integral-view]]
- [[photometry-luminance]]
- [[spectral-vs-rgb-comparison]]
- [[lt-spherical-harmonics]]
- [[sh-glyphs-ray-tracing]]

## Sources
- [[sources/peters-spectral-rendering-1-spectra]]
- [[sources/peters-spectral-rendering-2-real-time]]
- [[sources/peters-gpu-polynomial-roots]]
- [[sources/peters-projected-spherical-caps]]
- [[sources/peters-moment-shadow-mapping]]
- [[sources/peters-beyond-hard-shadows-msm]]
- [[sources/peters-trigonometric-moment-transient-imaging]]
- [[sources/peters-msm-gdce2016-talk]]
- [[sources/peters-cubic-equation-revisited]]
- [[sources/peters-msm-jcgt2016-demo]]
- [[sources/peters-improved-msm-jcgt2017]]
- [[sources/peters-non-linearly-quantized-msm]]
- [[sources/peters-path-tracing-workshop]]
- [[sources/peters-path-tracing-lectures]]
- [[sources/peters-radiometry-1-backwards]]
- [[sources/peters-radiometry-2-photometry]]
- [[sources/peters-spectral-rendering-3-vs-rgb]]
- [[sources/peters-lt-spherical-harmonics]]
- [[sources/peters-rt-sh-glyphs]]
