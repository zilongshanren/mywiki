---
tags: [数学, 线性代数, 泛函分析, 信号处理, 图形学]
date: 2026-04-14
sources: 1
---

# 函数即向量（Functions as Vectors）

**「函数是无限维向量」**是泛函分析的入门视角，它把线性代数工具（基、内积、特征分解、对角化）搬到函数空间上，给信号处理、图像压缩、几何处理、机器学习、量子力学提供了一把统一的钥匙。Max Slater 在同名长文里用 finite ↔ infinite 类比的方式推到 Fourier 变换和[[spherical-harmonics|球谐]]。

## 直觉：长度无限的向量就是映射

一个 $N$ 维向量可以看作「从索引 $1, \dots, N$ 到数值的映射」。把 $N \to \infty$（可数无穷）得到「从 $\mathbb{N}$ 到数值的映射」——就是一般的序列。再把 $\mathbb{N}$ 换成不可数的 $\mathbb{R}$，向量就变成了**一般的实函数** $f: \mathbb{R} \to \mathbb{R}$。

形式化地，只要定义好加法（`(f + g)[x] = f[x] + g[x]`）和标量乘（`(αf)[x] = α · f[x]`）并验证 8 条向量空间公理，函数空间就是一个合法的向量空间。

## 内积空间：从求和到积分

欧几里得点积 $\mathbf{u} \cdot \mathbf{v} = \sum u_i v_i$ 在连续版本里变成积分：

$$
\langle f, g \rangle = \int_a^b f[x] \overline{g[x]}\, dx
$$

（复值情形要取共轭。）这给出了**正交性**（$\langle f, g \rangle = 0$）和**范数** $\|f\| = \sqrt{\langle f, f \rangle}$ 的定义。满足 $\int |f|^2 < \infty$ 的函数构成 $L^2$ 空间——这是泛函分析里最常用的 Hilbert 空间。

## 线性算子：矩阵的连续版本

矩阵乘法 $A\mathbf{x}$ 在无限维下变成**线性算子** $\mathcal{L}f$。一个典型例子是**微分** $\frac{d}{dx}$——对多项式基 $\{1, x, x^2, x^3, \dots\}$，微分可以写成一个无限维「矩阵」：每一列把 $x^i$ 映到 $i \cdot x^{i-1}$。对 analytic 函数（Taylor 级数），微分也是一个线性变换。

## 对角化：Laplace 算子与 Fourier

在有限维下，对称矩阵的谱定理告诉我们它有正交特征基。对函数空间的类比：**自伴算子（self-adjoint operator）** 允许我们找到一组正交归一的**特征函数**。

**Laplace 算子**（一维上就是二阶导数 $\Delta = \frac{d^2}{dx^2}$）对 $[0, 1]$ 上周期函数是自伴的。它的特征函数是 $e^{2\pi i \xi x}$（其中 $\xi$ 是整数），特征值是 $-4\pi^2 \xi^2$——**这正是 Fourier 级数！** 一个函数的 Fourier 变换就是它在 Laplace 特征基下的坐标：

$$
\hat{f}[\xi] = \int_0^1 f[x] e^{-2\pi i \xi x} dx
$$

## 应用：为什么很多东西都是 Fourier

「只要能定义 Laplace 算子的地方，就能找到一个对应的 Fourier 变换」——这是这篇文章的核心 payoff：

- **2D Laplace on $[0,1]^2$** → 2D Fourier → **JPEG 的离散余弦变换**
- **Laplace on $S^2$（单位球面）** → **[[spherical-harmonics|球谐函数]]** → 图形里的 diffuse envmap 压缩、GI probes
- **mesh Laplace matrix**（每顶点一个值）→ **mesh 上的 Fourier** → 几何处理、mesh 压缩、diffusion filtering
- **analytic functions 上的微分**（非自伴）→ 需要进入复平面 → **Laplace 变换**

「Functions are vectors」也是**离散微分几何（DDG）**、**有限元法**、**Monte Carlo 几何处理** 的共同基础——它们都把 mesh 上的函数当向量做线性代数。

## 代价

- 无穷维下许多「显然」的性质需要小心——比如 delta 函数不是 $L^2$ 里的元素，却是标准基的自然类比。
- 严格地证明这些类比需要**测度论** / **Hilbert 空间** / **紧自伴算子的谱定理**，这些门槛本身不低。
- 数学家的 $\delta$-$\epsilon$ 严谨和工程师的「先用了再说」之间永远有张力。

## 相关

- [[spherical-harmonics]] — 球面上的 Fourier 基
- [[sampling-theorem-sinc]] — 另一个「函数就是无限维向量」的实例
- [[fourier-srgb-spectral-upsampling]] — 渲染里拿 Fourier 正交基做反射率谱压缩的应用
- [[max-slater]]

## Sources

- [[sources/slater-functions-are-vectors]]
