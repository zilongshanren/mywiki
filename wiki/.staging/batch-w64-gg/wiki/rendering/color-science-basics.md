---
tags: [渲染, 颜色, 色彩科学, cie, hdr, gamut]
date: 2026-04-19
sources: 1
---

# 图形工程师的色彩科学基础

做游戏十多年 HDR 渲染，却常常只在 sRGB 小框里展示——HDR 电视开始普及后，[[Jiayin Cao]] 在 Skull & Bones 上接 HDR TV 支持时补了一遍色彩科学。这页把他的笔记提炼为图形工程师的最小知识地图，和既有的 [[color-space]] 页互补——那页讲「色彩空间三要素」，这页讲它们怎么来的。

## 颜色远不止 RGB

除非做真谱渲染（[[spectral-rendering]]），我们都用三个数字表示颜色。底层事实是 **spectral power distribution (SPD)**：可见光 380–750 nm（PBRT 只考虑 400–700 nm），某个颜色对应一条光强 vs 波长的曲线。白光进棱镜分出的彩带就是可视化。

单波长光 → spectral color；日常看到的几乎都是多波长混合。

## 为什么只用三个数字够

眼睛的视锥有三种——长波（≈600 nm，红）、中波（≈550 nm，绿）、短波（≈450 nm，蓝）。大脑靠三通道积分识别颜色，所以**三原色线性组合**对人眼已近似充分。**Color matching experiment** 就是量化这点：挑 615/525/445 nm 三单色光作基，对每一个目标单色光调三者强度让人眼看起来匹配，得到 color matching functions。

**关键坑**：对某些波长，三原色需要**负强度**才能匹配——物理上做不到，实验里只能往目标侧加色「造减法」。

## CIE XYZ：把负数消掉

把 color matching 数据画在 RGB 三维空间，曲线会穿过 BR 平面（负值）。**XYZ 空间**用虚构的三原色让整条曲线都落在正区域。XYZ 不是物理可实现的色光，但它是所有色彩空间定义的**共同参考框架**。

把 XYZ 曲线投到 $x + y + z = 1$ 平面、降到二维，就是**CIE chromaticity diagram**——蹄形外缘代表纯单色，内部灰区才是 RGB 系统可实现的。

## 色彩空间的三要素怎么来

参见 [[color-space]] 的三要素结构——这里补完「数字怎么推」：

- **Primaries**：在 chromaticity diagram 上指定三点的 $(x, y)$ 坐标。
- **White point**：指定 $(1,1,1)$ 应该落在什么颜色（常用 D65: $(0.3127, 0.3290)$）。
- **Scaling**：chromaticity 只是二维投影，丢了强度。Cao 推了由 white point 反解 primaries 缩放 $S_r, S_g, S_b$ 的线性方程（约束：$R+G+B$ 的 Y 通道为 1）。

这决定了 XYZ ↔ RGB 的 3×3 转换矩阵。

## 三个常见色彩空间

- **Rec.709 / sRGB**：HDTV 和互联网标准，primaries 相同、transfer function 略不同（sRGB γ=2.4，Rec.709 γ=2.2）。只覆盖 CIE 1931 色域的 **35.9%**。
- **Rec.2020**：UHDTV 标准，primaries 是单色光谱位点（R=630 nm / G=532 nm / B=467 nm），覆盖 **75.8%**。transfer function 用 PQ（Perceptual Quantizer）。
- **Adobe RGB 等**：与游戏管线关系小，略过。

## 工程现实

- 大多数开发者显示器是 LDR sRGB，所以**线性渲染** = sRGB linear。
- 典型 HDR 流程：在 sRGB 线性域做光照积分 → 渲染结束前转到 Rec.2020 → 做 color grading → 走 PQ 编码送 HDR 显示。
- **注意**：转到 Rec.2020 并不能凭空创造原本 sRGB 色域外的颜色，除非在 Rec.2020 里做更饱和的 grading。

## 相关

- [[color-space]]
- [[spectral-rendering]]
- [[spectral-vs-rgb-comparison]]
- [[oklab-color-space]]
- [[hdr-video-edr-metal]]
- [[fourier-srgb-spectral-upsampling]]
- [[graphics-guy-notes]]

## Sources

- [[sources/graphics-guy-color-science-basics]]
