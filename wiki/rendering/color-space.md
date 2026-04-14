---
tags: [渲染, 颜色, 色彩管理]
date: 2026-04-14
sources: 1
---

# 色彩空间（Color Space）

RGB 值本身**没有意义**——「R=0.6, G=0.0, B=0.0」代表哪种颜色，完全取决于当前色彩空间如何解释它。色彩空间 = **编码方式（TRC）+ 三原色坐标（primaries）+ 白点（white point）**。

## 三要素

### 1. Tone Response Curve（TRC）

**做什么**：把 8-bit 存储值映射到线性光强。人眼对光强的感知是非线性的——两倍光子数不等于两倍亮度。如果用线性 8-bit 编码，暗部会出现明显色带，亮部又浪费了大量 code points。

sRGB 的 TRC 是近似 γ≈2.2 的分段幂函数，**代价是编码后的值不能直接做数学运算**：

> 所有光照、混合、滤波必须在**线性空间**里做，存储/显示前再 encode 回 sRGB。

这是 [[alpha-blending]] 和 [[deferred-rendering]] 经常出问题的地方——把 sRGB 值当线性值混合，红绿过渡会在中间出现不自然的变暗。

### 2. Primaries（三原色色度）

**做什么**：定义 (1,0,0) / (0,1,0) / (0,0,1) 在 CIE XYZ 空间里具体是哪三点。三点连成的三角形就是该色彩空间的 **gamut**（色域）。sRGB 的 gamut 小，DCI-P3 / Rec.2020 大得多。

两个色彩空间之间的 RGB 转换，数学上是一个 3×3 矩阵乘法——矩阵由两组 primaries 唯一决定。

### 3. White Point（白点）

**做什么**：定义 (1,1,1) 对应哪种白色。最常用的是 **D65**（≈6500K 日光）。换白点会触发 chromatic adaptation 变换（如 Bradford 矩阵）。

## 为什么引擎不能偷懒

- **纹理采样**：UI 图标通常是 sRGB，但法线贴图、roughness、AO 贴图必须是 linear。采样时标错 sRGB flag 直接毁掉光照。
- **Gamma-correct rendering**：延迟渲染的 G-Buffer 必须存线性值；输出 tonemap 之后才 encode 回 sRGB。
- **HDR 显示**：现代管线需要处理 sRGB / Rec.2020 / DCI-P3 多目标输出，色域不同，primaries 不同。

## 关键教训

> RGB 值不是颜色——色彩空间才是颜色。数学运算在线性域，存储显示在感知域。

## 相关

- [[alpha-blending]] — 混合必须在线性空间
- [[color-lut]] — color grading 的查找表
- [[deferred-rendering]] — G-Buffer 存线性
- [[local-tonemapping]] — 线性 HDR → 感知域的艺术选择
- [[exposure-fusion]] — 多曝光融合也是 tonemap 家族
- [[spectral-rendering]] — 彻底绕开「RGB 当作颜色」的物理近似
- [[fourier-srgb-spectral-upsampling]] — 把 sRGB 纹理升格为反射率谱
- [[oklab-color-space]] — 感知均匀色彩空间，混合 / 渐变时用
- [[display-edid-colorspace]] — 从 EDID 读出显示器原生 gamut
- [[bartosz-ciechanowski]]
- [[color-banding]] — 量化精度不足在深色渐变上的可见性
- [[perceptual-colormaps]] — 感知均匀 colormap 的科学可视化标准

## Sources

- [[sources/ciechanow-color-spaces]]
- [[sources/peters-spectral-rendering-1-spectra]]
- [[sources/green-display-edid-colorspace]]
