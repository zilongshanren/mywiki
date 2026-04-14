---
tags: [渲染, 光谱, BRDF, 材质]
date: 2026-04-14
sources: 1
---

# 光谱 BRDF（Spectral BRDF）

把 RGB 渲染器改造成 [[spectral-rendering|光谱渲染器]]时，BRDF 这一层需要从「返回一个 RGB 三元组」改成「能在任何波长 $\lambda$ 处给出反射率」。Christoph Peters 在[[sources/peters-spectral-rendering-2-real-time|Part 2]] 里以 **Frostbite BRDF** 为例演示了一种非常轻量的做法，核心观察是：

> 大多数 PBR BRDF 构造的各种颜色，都只是 base color 和纯白之间的线性组合。

## Frostbite BRDF 的结构

Frostbite BRDF 里**只需要美术家指定 base color**（通常是 sRGB 纹理）。所有其它颜色都是从它派生的：

- **介电质（dielectric）镜面反射**：纯白（按菲涅尔比例）
- **金属（metal）镜面反射**：等于 base color（按菲涅尔比例）
- **漫反射 albedo**：base color 的一个缩放
- **折射、SSS 等**：继续由 base color 派生

这意味着**最终反射率可以写成 `w_base · base_color + w_white · 1`** 两个权重。原来的 BRDF 实现只要把返回值从「RGB 三元组」改成「2D 向量 `(w_base, w_white)`」就行——**无需重写任何逻辑**。

## 怎么用这两个权重

一旦 BRDF 返回了 `(w_base, w_white)`，给定当前路径的采样波长 $\lambda_k$（见 [[hero-wavelength-spectral-sampling]]），反射率就是

$$a(\lambda_k) = w_\mathrm{base} \cdot a_\mathrm{base}(\lambda_k) + w_\mathrm{white} \cdot 1$$

其中 $a_\mathrm{base}(\lambda_k)$ 由 [[fourier-srgb-spectral-upsampling|Fourier sRGB]] 上采样方案当场算出，纯白是常数 1（本身就是能量守恒的上界）。路径 throughput weight 照旧是一个 $m$ 维向量（$m$ 是每路径采的波长数），每次反射乘一次 $a(\lambda_k)$ 即可。

## 可选：真正的光谱菲涅尔

这套框架**可以**进一步加成：

- **光谱菲涅尔**：金属的菲涅尔曲线本来就是波长相关的——铜在绿/红波段更亮。用测量到的 $\eta(\lambda), k(\lambda)$ 直接算出更物理的颜色。
- **大于 2 的 base**：线性组合可以扩展到多条谱——例如「base color × 反射谱 + 皮肤散射谱 + 金属高光谱」。

Peters 在博客里没有启用这些，**刻意保持「苹果对苹果」的对比**——只证明光谱替换是廉价的；物理精度的进一步提升是额外奖励。

## 和 shader graph 的摩擦

Frostbite 的这种「base color + 权重派生」结构很友好，因为美术只接触 base color。如果引擎的 shader graph 允许对 RGB 做任意运算（混合、加减、阈值），就很难用两个权重概括。这种情况下，只能对每条路径在每个顶点**真的存完整的 Fourier sRGB 三元组**，路径结束后再采波长评估——代价和实现复杂度都更高。

## 相关

- [[spectral-rendering]]
- [[fourier-srgb-spectral-upsampling]]
- [[hero-wavelength-spectral-sampling]]
- [[christoph-peters]]
- [[microfacet-brdf]] — 光谱 BRDF 底下的微表面骨架

## Sources

- [[sources/peters-spectral-rendering-2-real-time]]
