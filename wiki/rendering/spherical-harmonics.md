---
tags: [渲染, 数学, 线性代数, 全局光照, 环境光, 球谐]
date: 2026-04-14
sources: 1
---

# 球谐函数（Spherical Harmonics）

**球谐函数 $Y_\ell^m$** 是单位球面 $S^2$ 上 Laplace 算子的正交归一特征基——一句话说，就是「球面上的 Fourier 基」。图形学用它来用极少几个系数**压缩球面信号**：diffuse environment map、辐照度缓存、ambient probe、预计算辐射传输（PRT）等等。

## 数学来源

[[functions-as-vectors|把函数看作向量]]的视角告诉我们：**在任何能定义 Laplace 算子的域上，我们都能找到对应的 Fourier 变换**。在球面上的 Laplace 算子（球坐标下的二阶导数之和）是自伴的，其特征函数按惯例写作：

$$
Y_\ell^m(\theta, \varphi) = N_\ell^m \cdot P_\ell^m(\cos\theta) \cdot e^{im\varphi}
$$

- $\ell \ge 0$ 是 **degree**（频率的类比）；
- $m \in [-\ell, \ell]$ 是 **order**；
- $N_\ell^m$ 是归一化常数；
- $P_\ell^m$ 是 **associated Legendre polynomials**（关联勒让德多项式）。

第 $\ell$ 带（band）共有 $2\ell + 1$ 个基函数。前 3 带加起来就是 **9 个实值系数**——这正是图形里 `SH[9]` 或 `SH L2` 的来源。

## 为什么是 9 个系数

漫反射（diffuse）对环境光的响应本身就是一个低通滤波（$\cos\theta$-加权积分），其频谱几乎全在 $\ell \le 2$ 的三个带里——Ramamoorthi & Hanrahan 2001 证明了**用 L2 SH 重建 diffuse 光照，最大误差低于 1%**。所以 diffuse envmap 可以被压成 9 个 RGB 系数（27 个 float），相比一张 $512 \times 256$ 的 cubemap，这是几个数量级的差距。

## 在游戏引擎里的典型用法

- **Ambient probe**：一个 SH L2 系数集合当作环境光代表，给动态物体简单的间接照明。
- **Light probe volume / LPV**：在场景里离散地放 probe，用三线性插值得到任意位置的 SH 系数。
- **PRT（Precomputed Radiance Transfer）**：把 visibility 和 BRDF 的乘积在 SH 下预计算，运行时只做一次点积。
- **Irradiance volume**：类似 light probe volume 但存的是 irradiance 而非 radiance。

## 操作上的便利

球谐的魅力是大量操作**在系数空间里都是线性的**：

- **加法 / 混合**：两个 probe 的 SH 系数直接按权重相加。
- **旋转**：把一个方向的 SH 乘一个 $(2\ell+1) \times (2\ell+1)$ 的块对角矩阵即可——每个 band 独立。虽然旋转矩阵推导复杂，运行时是 $O(\ell^2)$ 的小矩阵乘。
- **卷积（diffuse lobe）**：漫反射的积分在 SH 下等价于逐 band 乘一个常数（Funk-Hecke 定理）——「glossy 的积分 = 逐 band 乘某个低通」。
- **和几何 normal 的积分**：用方向向量代入 $Y_\ell^m$ 即可算出该方向上的重建值。

## 和其它球面表示的对比

- **Cubemap**：采样便宜（硬件原生），但一张 HDR cubemap 是 MB 级；L2 SH 是几十字节。
- **Spherical Gaussians / lobes**：比 SH 更擅长高频光源（主光、bright spot），但通用运算少，不是线性空间。
- **Wavelets on sphere**：能表示高频+低频混合，但渲染里不流行——实时图形偏爱「便宜、线性、可插值」三件套，SH 恰好都有。
- **Ambient Dice / H-basis**：为特定用途优化的球面基，在某些引擎里替代 SH。

## 局限

- **高频不适用**：反射类高光（glossy spec）需要 L4 甚至 L8 以上才能看，就不值得——此时用 cubemap 或 SG。
- **负值**：L2 的 SH 重建结果可能是负数，要 clamp，容易产生微小 artifact。
- **ringing**：加入高频之后，`max(0, ...)` 形状的光照信号会有振铃，和 JPEG 的 8×8 块振铃是一个味儿。

## 相关

- [[functions-as-vectors]] — 球谐的理论根源
- [[fourier-srgb-spectral-upsampling]] — 同样是把带界信号展开到正交基
- [[needlets]] — 球面上的局部化 wavelet 基，遮挡振铃时的替代方案
- [[max-slater]]
- [[robin-green]] — GDC 2003 *SH Lighting: The Gritty Details* 的作者
- [[valve-ambient-cube]] —— 非正交的六方向紧凑表示，shader 指令更便宜，精度逊于 L2 SH
- [[lt-spherical-harmonics]] — LT-SH：多边形面光源高光的线性变换球谐技术
- [[sh-glyphs-ray-tracing]] — SH 字形的光线追踪渲染与多项式求根

## Sources

- [[sources/slater-functions-are-vectors]]
- [[sources/green-sh-lighting-gritty-details]]
- [[sources/green-implementing-needlets]]
- [[sources/slater-spherical-integration]]
- [[sources/c0de517e-mathematica-spherical-harmonics]]
- [[sources/peters-lt-spherical-harmonics]]
- [[sources/peters-rt-sh-glyphs]]
