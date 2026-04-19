---
tags: [渲染, 光谱, rgb, 颜色科学, 路径追踪]
date: 2026-04-19
sources: 1
---

# 光谱渲染 vs RGB 渲染：有图为证的对比

[[christoph-peters|Christoph Peters]] 的 Spectral Rendering Part 3（2025-11-20）是一个**实证**：同一场景、同一路径追踪器，切换 RGB 和 [[spectral-rendering|spectral rendering]]，对比不同类型光源下的**颜色再现**差别。结论：在日光 / LED 等平滑光谱下差别**可见但小**；在**峰谱** / 单色光源下，差别**戏剧性**。

## 测试设置

- 同一个场景（气球 + 地毯 + 墙壁），同一 path tracer（[Peters 的 open source 版本](https://github.com/MomentsInGraphics/path_tracer/tree/spectral)）。
- RGB 模式：光源和纹理的 RGB 三元组分量相乘。
- 光谱模式：光源谱来自 [LSPDD](https://lspdd.org)，反射率谱用 [[fourier-srgb-spectral-upsampling|Fourier sRGB]] 从 sRGB 上采样。

## Illuminant E / D65：差别最小

- **Illuminant E**（常数光谱）：两者**几乎一致**。因为 Fourier sRGB 的 lookup table 就是用常数光谱训练出来的，直接反射 illuminant-E 得到的 sRGB 会精确还原原纹理色。
- **Illuminant D65**（日光标准）：有可见但轻微的偏差，主要在红色区域。没有哪个结果"更正确"——看怎么定义参考。

## LED / 白炽灯：偏差开始有趣

- **Warm-white LED**：两个平滑 lobe，覆盖可见光大部分。RGB 和光谱的红色、绿色区域都有小偏移；绿色的偏移方向与 D65 下相反。
- **Incandescent**（白炽灯 / 老式灯泡）：可见光谱是一个上升斜坡，红外端主导。重要差别是**饱和度**：光谱渲染下蓝色表面饱和度降低、带点黄色（因光源在蓝段几乎没能量）。RGB 渲染做不出这种**去饱和**效果——它只能按通道乘，没法缩小向量长度。

## CFL / MH 灯：峰谱的戏剧

- **紧凑荧光灯（CFL）**：多个尖峰。在这个场景里绿色气球明显变亮。
- **金卤灯（MH）**：谱更尖锐。光源"看起来"接近白光、但**大量饱和表面在光谱渲染里变蓝、去饱和**，整个场景气氛巨变；RGB 渲染这种单纯缩 RGB 三分量做不到——它预先把光源折叠成三个数，信息已丢。

## 准单色光源：完全不同的画

- **HPS（高压钠）**：光谱几乎只在 589 nm 附近。光谱渲染里"无论表面什么色，反射光都近单色"——只是亮度不同，像真实街灯下的世界。RGB 渲染只把它当作红+绿的混合，表面颜色部分保留。
- **单色 500 nm**：极端情况。光谱渲染下**所有像素只差亮度**；RGB 渲染把 500 nm 当作绿+蓝，仍然显示五颜六色。

## Gamut 压缩

真正的单色光 500 nm 在 sRGB 空间 `(-1, 1, 0.36)`——**负分量即 out-of-gamut**。光谱渲染对此天然免疫（直到最后一步才进 RGB），RGB 渲染一开始就假定所有值可以放进三通道。Peters 直接 clamp 了负值，真正场景应该用 ACES gamut compression。

## 结论的几个层次

- **RGB rendering is wrong, but not by a lot** 在平滑白光谱下。
- **RGB rendering is wrong, and a lot** 在窄谱或峰谱下。
- **光谱渲染不是离线渲染专属**。Peters 的 Part 2 证明实时路径追踪里开销 2%–7%（见 [[hero-wavelength-spectral-sampling]]）；那么 Part 3 就是"值不值得做"的答案。
- **色域切换免费**：光谱渲染输出时再做 XYZ→任意 RGB space，不影响物理；RGB 渲染切色域必须重新 grading。
- **真实产业案例**：Wētā FX 自 Avatar: The Way of Water 起整个管线都是光谱，用的正是 Peters 的 Fourier sRGB 上采样。他们在访谈里还说**如果重来，所有光谱都用这个方法**。

## 开放问题

- 多光源场景下的波长重要性采样**仍是开放问题**——"先挑光源再挑波长"对长路径不够。
- Artist 流程：shader 经常对 RGB 直接运算，spectral 化不是零成本。

## 相关

- [[christoph-peters]]
- [[spectral-rendering]]
- [[fourier-srgb-spectral-upsampling]]
- [[hero-wavelength-spectral-sampling]]
- [[photometry-luminance]]
- [[color-space]]

## Sources

- [[sources/peters-spectral-rendering-3-vs-rgb]]
