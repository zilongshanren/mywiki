---
tags: [渲染, 光度学, 色彩, 光谱, 物理渲染]
date: 2026-04-19
sources: 1
---

# Photometry 与 Luminance

[[radiometry-integral-view|辐射度量]]是物理量，按光子能量计数，对人眼不可见的紫外/红外一视同仁。**Photometry**（光度学）则是**按人眼感知权衡后的量**。两者通过 CIE 的色匹配函数衔接——[[christoph-peters|Christoph Peters]] 在 Radiometry Part 2 里把这个衔接讲得很清楚。

## 光谱化：给每个量加一维

Radiometric 量「色盲」，假设所有波长等权。现实里一个 photon 的能量 $E = hc/\lambda$ 与波长有关，而且眼睛只对 400–700 nm 敏感。要区分波长，把 radiant energy 先写成「只计 $\lambda' \le \lambda$ 的光子」形式，对 $\lambda$ 求导得到**光谱辐射能**：

$$Q_A(t_0, t_1, \lambda) = \frac{\partial}{\partial \lambda} Q_{A, [0, \lambda]}(t_0, t_1)$$

单位 $\mathrm{J}/\mathrm{nm}$。同样的构造也给出 spectral radiance、spectral flux、spectral irradiance ——每个量都附带一个 $\lambda$ 维度。

## CIE 色匹配函数与 XYZ

三条曲线 $\bar{x}(\lambda), \bar{y}(\lambda), \bar{z}(\lambda)$ 描述**人眼标准观察者**的感知。对 spectral radiance $L(x,t,\omega,\lambda)$，屏幕色（CIE XYZ）是：

$$L_X = \int L(x,t,\omega,\lambda)\,\bar{x}(\lambda)\,\mathrm{d}\lambda$$

类似地得 $L_Y, L_Z$。**不同的 spectral radiance 可能映射到相同的 XYZ**——这就是 metamerism（同色异谱），解释了为什么 RGB 渲染能"糊弄"很多场景。

## Photometric 量：Luminance 等

$L_Y$（用 $\bar{y}(\lambda)$ 加权积分）恰好是 CIE 定义的**luminance**（亮度），也是 photometric 的基石。完整对照表：

| Radiometric | 单位 | Photometric | 单位 |
|---|---|---|---|
| Radiance $L$ | W/(m²·sr) | Luminance | nit = cd/m² |
| Irradiance $E$ | W/m² | Illuminance | lux |
| Intensity $I$ | W/sr | Luminous intensity | candela (cd) |
| Radiant flux $\Phi$ | W | Luminous flux | lumen (lm) |
| Radiant energy $Q$ | J | Luminous energy | talbot (lm·s) |

日常生活里其实都能对上号：买灯泡看 **lumen**（光通量）、显示器峰值亮度看 **nit**（luminance）、聚光灯看 **candela**（朝某方向的强度）。

## 实际建议：光源用 flux / 亮度用 luminance

- **光源标定用 radiant flux (W) 或 luminous flux (lm)**：修改光源大小时，场景总亮度不变，符合艺术家直觉。
- **显示映射用 luminance (nit)**：目标是 screen 像素值（linear RGB），Y 通道就是感知亮度。
- **radiance 在 renderer 内部传递**：光子级别物理量，沿射线守恒。

## 光谱渲染的存储与采样问题

光谱"原则上"是连续函数。存成 80 个 5 nm 采样的纹理对于 4K textures 完全不现实（TB 级）。Peters 的方案（[[fourier-srgb-spectral-upsampling]]、[[hero-wavelength-spectral-sampling]]）用 Fourier 系数压缩 + MC 波长采样，**存储和带宽几乎和 RGB 一样**。详细讨论见 [[spectral-rendering]]。

## 混乱根源

Peters 坦言这个领域**水很深**：CIE XYZ 自 1931 以来修订过、white point（D65 常用但不唯一）、sRGB / Rec.2020 / P3 等色彩空间选择、各 OS/浏览器/driver 的色彩管理各不相同。人眼自身的白平衡又把大部分差异掩盖掉——**最难检测、最难调试**。结论：做 spectral rendering 前，**提前锁定 XYZ 标准、white point、输出色彩空间**，否则资产可能被重做。

## 相关

- [[christoph-peters]]
- [[radiometry-integral-view]]
- [[spectral-rendering]]
- [[color-space]]
- [[fourier-srgb-spectral-upsampling]]
- [[hero-wavelength-spectral-sampling]]

## Sources

- [[sources/peters-radiometry-2-photometry]]
