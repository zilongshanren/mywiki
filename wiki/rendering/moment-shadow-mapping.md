---
tags: [渲染, 阴影, 滤波, 数学, 矩]
date: 2026-04-14
sources: 2
---

# 矩阴影贴图（Moment Shadow Mapping）

**Moment Shadow Mapping（MSM）** 是 [[christoph-peters]] 与 Reinhard Klein 在 I3D 2015 提出的「可过滤硬阴影」方案。它的核心观察是：经典 [[shadow-mapping-basics|shadow mapping]] 的深度比较是**非线性**的，因此不能对 shadow map 做双线性、mipmap 或 gaussian 模糊——一旦线性滤波，结果就不再代表任何物理意义。Variance Shadow Maps（VSM）通过存一阶和二阶矩（均值 + 方差）避开了这个问题，但 Chebyshev 不等式提供的概率界太宽松，会出现严重的「light bleeding」。MSM 把这个思路推到**四阶矩**：每个 texel 存 `(z, z², z³, z⁴)`，然后用 [[polynomial-root-finding-gpu|GPU 上的多项式求根]] 在实时里解一个**截断的 Hausdorff 矩问题**，得到对阴影强度最锐利可能的下界。

## 为什么是四阶矩

论文最值得一读的不是算法本身，而是选择「为什么是 4」这一步——作者用自动评估枚举了成千上万种可选构造（不同阶数的幂矩、Fourier 矩、Chebyshev 矩…… ），让计算机跑实验挑出**在 quality / memory / cost 三角上帕累托最优**的那一个。结论是：四个幂矩在 16-bit 量化后以 64 bits/texel 的代价给出接近 ground truth 的硬阴影，且可以直接套用所有硬件纹理滤波硬件：双线性、mipmap、各向异性、MSAA resolve 都免费继承。

## 四矩问题的解

给定四个矩 `(b₁, b₂, b₃, b₄)`，算法要回答一个古老数学问题：在所有「前四阶矩等于这些值」的 [0,1] 上的概率分布里，点 z 处的累积分布函数 `F(z)` 能取到的**最大值**是多少？这个值正是「光被遮住的概率下界」，也就是最锐利的阴影强度估计。闭式解需要解一个 3×3 的 Cholesky 分解 + 一个二次方程 + 一个三次方程，全程可以在一个 fragment shader 里跑完，没有分支爆炸。

## 16 位量化

朴素做法用 `RGBA32F` 保存四个矩，那是 128 bits/texel，带宽上不划算。论文提出一个**定制的线性变换**，把四个矩映射到一个坐标系里，让每一维的取值范围尽量紧凑，再存成 `RGBA16_UNORM`——压到 64 bits/texel 且质量损失可忽略。这套量化也是论文一个很有代表性的「从纯数学里挖出工程收益」的例子。

## 超越硬阴影

2016 年的后续论文 *Beyond Hard Shadows* 把 MSM 的数学机制套到三个经典「可过滤阴影」的应用上：

- **Prefiltered single scattering**（参与介质里的体积阴影）——原本由 Convolution Shadow Maps 解决，MSM 给出更少的存储、更少的 ringing。
- **Moment Soft Shadow Mapping（MSSM）**——Variance Soft Shadow Mapping 的替代品，阴影半影更干净、漏光更少。
- **Moment Translucent Occluders**——Fourier Opacity Map 的替代品，用于半透明遮挡物（烟、叶子）。

三套应用的统一母题是：**如果我能把一个待滤波的量表达成「某个带界分布的一个函数的期望」，我就可以存这个分布的矩并在运行时重建**。MSM 是这个模版在「硬阴影」这一槽位的最优实例。

## 与 VSM、CSM、ESM 的关系

| 技术 | 存什么 | 概率界 | 漏光 | 代价 |
|---|---|---|---|---|
| VSM | `z, z²` | Chebyshev | 严重 | 64 bits |
| ESM | `exp(k·z)` | 指数拟合 | 中等 | 32 bits |
| CSM（Convolution） | 傅里叶基函数系数 | 截断傅里叶 | ringing | 可变 |
| **MSM** | `z, z², z³, z⁴` | Hausdorff 矩锐下界 | 极小 | **64 bits** |

MSM 的承诺是：**用 VSM 的存储预算拿到接近 ray-traced 硬阴影的质量**，并在全部可过滤阴影家族里保持一致的数学母题。

## 相关

- [[shadow-mapping-basics]] — 基线 shadow mapping
- [[christoph-peters]] — 作者，博客 momentsingraphics.de
- [[polynomial-root-finding-gpu]] — MSM 解码需要的稳定求根
- [[spectral-rendering]] — 同作者的另一个「矩方法」应用
- [[volumetric-fog-froxels]] — single scattering 的邻近话题
- [[non-linearly-quantized-msm]] — 64/32 bit 非线性量化 + on-chip compute filtering（HPG 2017）
- [[cubic-equation-solver-hlsl]] — 解码端的三次方程闭式 HLSL 子例程

## Sources

- [[sources/peters-moment-shadow-mapping]]
- [[sources/peters-beyond-hard-shadows-msm]]
- [[sources/peters-msm-gdce2016-talk]]
- [[sources/peters-msm-jcgt2016-demo]]
- [[sources/peters-improved-msm-jcgt2017]]
- [[sources/peters-non-linearly-quantized-msm]]
- [[sources/peters-cubic-equation-revisited]]
