---
tags: [渲染, 颜色, 光谱, 路径追踪, 实时渲染]
date: 2026-04-14
sources: 2
---

# 光谱渲染（Spectral Rendering）

**光谱渲染**用波长 $\lambda$ 的连续函数 $i(\lambda),\ a(\lambda)$ 代替 RGB 三元组，直接模拟光在不同波长上的传输。传统 RGB 渲染只在「红乘红、绿乘绿、蓝乘蓝」三个离散波长上做分量相乘，这对物理是一个粗糙的近似——很多「看起来不对的颜色」是被艺术家手工 color grading 压住的。光谱渲染提供更准确的颜色再现、对 [[color-space|色彩空间]]（sRGB / Rec.2020 / 特定相机光谱响应）的解耦、对**异常光源谱**（钠灯、金卤灯、荧光）的正确处理，而代价**在实时渲染里也只在 2%~7% 量级**。

## 问题陈述

像素颜色来自一个积分：

$$\begin{pmatrix}X\\Y\\Z\end{pmatrix} = \int_{360~\mathrm{nm}}^{830~\mathrm{nm}} \begin{pmatrix}\bar{x}(\lambda)\\\bar{y}(\lambda)\\\bar{z}(\lambda)\end{pmatrix} i(\lambda) \prod_{j=1}^{n-1} a_j(\lambda)\, \mathrm{d}\lambda$$

其中 $i(\lambda)$ 是光源的**发射光谱**、$a_j(\lambda)$ 是路径中每次反射面的**反射率光谱**、$\bar{x},\bar{y},\bar{z}$ 是 CIE 1931 色匹配函数。把这个 XYZ 再线性变换到 linear sRGB，最后 encode 回 sRGB，就得到屏幕像素。

RGB 渲染相当于**假设 $i(\lambda)$ 只在三个特定波长处有能量**，所以恰好退化成分量乘法。现实中没有一个真实光源是那样的——日光谱平滑、荧光灯有尖锐峰、钠灯只有黄色谱线，这些都不是三个 delta 能表达的。

## 为什么 RGB 就"够用"是错觉

- **色域切换灾难**：要从 LDR sRGB 转向 HDR Rec.2020，每个 RGB 纹理都要重新走一遍 grading。光谱渲染只要换一套色匹配函数，一次解决。
- **异常光源**：[[sources/peters-spectral-rendering-2-real-time|钠灯 + 金卤灯]]的场景里 RGB 和光谱结果差别巨大——RGB 的结果「颜色是对的但不像那种灯」。
- **相机响应**：如果需要匹配特定物理相机的光谱灵敏度（而不是人眼的 CIE XYZ），只要换一组曲线就行。RGB 渲染做不到。
- **荧光材质**：入射和出射波长不同，RGB 没有办法表达。

## 数据从哪来

两类光谱要解决：

- **发射光谱**：用光谱仪测量；或者欧盟法规强制公开的能效标签里就有；或者用 [LSPDD](https://lspdd.org) 这种公开数据库。一条 1 nm 间隔、32-bit 浮点的发射光谱只有 1880 B，500 种光源也不到 1 MB，储存不是问题。
- **反射率光谱**：每个纹素都要一条谱。如果存 30 个 10 nm 采样 + 1 B/sample，一个 4K × 4K 纹理集会膨胀到几百 GB，不现实。解决办法是**光谱上采样**——见 [[fourier-srgb-spectral-upsampling]]。

## 和实时渲染的接口

[[sources/peters-spectral-rendering-2-real-time|Christoph Peters 的 Part 2]] 证明光谱渲染可以嫁接到路径追踪和光栅化上，核心做法是用 Monte Carlo 积分 + 波长重要性采样（[[hero-wavelength-spectral-sampling]]），每条路径只采 $m \approx 4$ 个波长，throughput weight 从一个 RGB 三元组变成一个 $m$ 维向量，其余和普通 path tracer 一致。BRDF 里把 albedo 换成反射率光谱评估（见 [[spectral-brdf]]）即可。

实测在 1080p / 1 spp 下，Bistro 场景的额外开销只有 **2%~7%**——完全值得。

## 留下的挑战

- **多光源的重要性采样**：当一条路径的 throughput 可能命中多种完全不同的光源谱时，「先挑光源再挑波长」的简单策略会失效。guiding 方法可行但有自己的成本。
- **Shader graph 文化**：很多美术管线里 shader 直接对 RGB 三元组做运算。如果 shader 只生成 reflectance 纹理，可以离线 bake 后转换成 [[fourier-srgb-spectral-upsampling|Fourier sRGB]]；如果 shader 在运行时对 RGB 做复杂操作，就必须另找路径。

## 关键口号

> RGB 渲染把「人眼感知模型」和「光传输物理」搅在一起了；光谱渲染把它们解耦。

## 相关
- [[color-space]] — RGB 值只有在给定色彩空间下才有意义
- [[fourier-srgb-spectral-upsampling]] — 把 sRGB 纹理升格为反射率谱的方法
- [[hero-wavelength-spectral-sampling]] — 用少量波长做 MC 积分的采样策略
- [[spectral-brdf]] — BRDF 怎么配合反射率谱
- [[christoph-peters]]
- [[spectral-zucconi-rainbow]] — shader art 场景下 branchless 的波长→RGB 廉价拟合
- [[spectral-vs-rgb-comparison]] — 各类光源下 RGB vs 光谱的实证对比
- [[photometry-luminance]] — photometric 量与 CIE XYZ
- [[radiometry-integral-view]] — radiometric 量的积分式介绍

## Sources
- [[sources/peters-spectral-rendering-1-spectra]]
- [[sources/peters-spectral-rendering-2-real-time]]
- [[sources/peters-spectral-rendering-3-vs-rgb]]
- [[sources/peters-radiometry-1-backwards]]
- [[sources/peters-radiometry-2-photometry]]
