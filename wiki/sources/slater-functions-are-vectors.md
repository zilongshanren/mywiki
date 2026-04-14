---
tags: [source, 数学, 线性代数, 泛函分析, 信号处理, 图形学]
date: 2026-04-14
sources: 1
---

# Functions are Vectors（Max Slater）

[[max-slater|Max Slater]] 2023 年 7 月发表的长文——**3Blue1Brown Summer of Math Exposition 3 的 honorable mention**。核心论点：把函数看作无限维向量，线性代数的所有工具（基、内积、特征分解、谱定理）就都能迁移到信号处理、图像压缩、几何处理、物理模拟、机器学习。

## 摘要

文章从「有限维向量 = 从 index 到 value 的 mapping」类比出发，一步步扩展：$\mathbb{R}^N$ → 可数无穷序列 → 不可数无穷的 $\mathbb{R} \to \mathbb{R}$ 函数。然后构造函数的**向量空间公理**（加法、标量乘、零向量）、**标准基**（impulse functions $\mathbf{e}_x$）、**线性算子**（微分作为无限维矩阵）。

下半部分进入**对角化 / 谱理论**：在有限维下对称矩阵 $= A^T$ 蕴含正交特征基，等价的无限维概念是**自伴算子**——微分不自伴（不能对角化），但 **Laplace 算子 $\Delta = \frac{d^2}{dx^2}$ 在周期函数域上自伴**。它的特征函数是 $e^{2\pi i \xi x}$（$\xi \in \mathbb{Z}$），特征值是 $-4\pi^2 \xi^2$——这正是 **Fourier 级数**的数学来源：**Fourier 变换就是 Laplace 特征基下的坐标变换**。

应用部分举了多个「换一个域就换一个 Fourier」的例子：一维 → Fourier series、二维 $[0,1]^2$ → JPEG 里的 2D DCT、**$S^2$ → [[spherical-harmonics|球谐函数]]**（图形里压缩 diffuse envmap 和 GI probe）、mesh 上的 Laplace 矩阵 → mesh 上的 Fourier（离散微分几何、mesh 几何处理的根基）。文末给出了**离散微分几何**、**有限元 / Monte Carlo PDE**、**inverse rendering**、**DiffusionNet 类 ML on meshes** 等延伸阅读。

## 关键要点

- **函数是无限维向量**不是比喻——只要定义好加法、标量乘、内积，就得到合法的向量空间（$L^2$ 是规矩的那个 Hilbert 空间）。
- **内积从求和变积分**：$\langle f, g \rangle = \int f \bar{g}$；正交性、范数、Cauchy-Schwarz 一应俱全。
- **Laplace 算子是连接线性代数和 Fourier 的关键**：它在周期函数上自伴，特征基就是波——这是「Fourier 变换 = 对角化 Laplace」的一句话概括。
- **Fourier 的普适性**：任何能定义 Laplace 的域都有自己的 Fourier——2D、球面（SH）、mesh。
- **JPEG / 球谐 / mesh 压缩** 是同一套数学在不同域的表现形式。
- **微分不能对角化**（实数域上不自伴），进入复数域可以通过 Laplace 变换对角化，但难逆。
- **图形里球谐存在的理由**就是「$S^2$ 上的 Fourier」——用几个系数压掉整张 diffuse envmap。
- **离散微分几何 / 几何处理** 的算法本质是「对 mesh Laplace 做线性代数」。

## 链接到的概念

- [[functions-as-vectors]]
- [[spherical-harmonics]]
- [[fourier-srgb-spectral-upsampling]] — 相邻应用：同样拿正交基压缩有界信号
- [[sampling-theorem-sinc]] — 同一视角下的 sinc 插值
- [[max-slater]]

## 原文

- 链接：https://thenumb.at/Functions-are-Vectors/
- 本地：`raw/articles/thenumb.at/2023-07-29_functions-are-vectors.md`
