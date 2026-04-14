---
tags: [source, 数学, 旋转, 线性代数, 李群, 动画]
date: 2026-04-14
sources: 1
---

# Exponentially Better Rotations（Max Slater）

[[max-slater|Max Slater]] 2022 年 4 月发表，基于 Keenan Crane CMU 15-462 课件改写的长文：用矩阵指数 / 对数 **统一** 旋转矩阵、欧拉角、四元数、轴角四种表示，并演示一个 **四元数都不容易做** 的应用——**多个旋转的几何平均**（Karcher mean）。

## 摘要

文章先快速过一遍四种表示的优劣：旋转矩阵能用一次 `mat * vec` 变换点、能与其它线性变换合成，但 **不是向量空间**（相加会得到带缩放的非旋转矩阵）；欧拉角直观但有 gimbal lock 和插值断裂；四元数能 slerp 但不直观、没标量乘几何意义、平均不靠谱；**轴角是普通 3D 向量**——可加可缩，但「轴角→正确旋转矩阵」不显然。

接下来是文章的核心：**$\exp$ 把反对称矩阵映射到旋转矩阵**。在 2D 里，$J = \begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}$ 是 90° 旋转，$e^{\theta J}$ 的 Taylor 级数自然分裂为 $\cos\theta\,I + \sin\theta\,J$——标准 2D 旋转矩阵。在 3D 里，把叉乘 $\mathbf{u}\times$ 写成反对称矩阵 $\hat{\mathbf{u}}$，对 $\theta\hat{\mathbf{u}}$ 做矩阵指数得到 $I + \sin\theta\,\hat{\mathbf{u}} + (1 - \cos\theta)\,\hat{\mathbf{u}}^2$——**Rodrigues 公式**。Slater 严格验证了它是合法旋转矩阵（$R^T R = I$、$\det R = 1$），并通过 trace 提取角度、反对称化提取轴向量，给出 **$\log$ 的闭式公式**。

应用部分有两个：**插值** 公式 $R(t) = \exp(t \log(R_1 R_0^{-1}))R_0$ 在任意维度下都是最短路径、恒定角速度，与 slerp 等价但完全用矩阵；**Karcher mean** 则用迭代方式把「点的几何中位数」算法搬到旋转上——避开 catastrophic cancellation（朴素「平均轴角向量」会让 $[\pi, 0, 0]$ 与 $[-\pi, 0, 0]$ 平均成零）。

文末的「Quaternions Again」节把同样推导平移到四元数：纯虚四元数指数等价于反对称矩阵指数，给出单位四元数版的 Rodrigues。最后指出：上面用到的反对称 3×3 矩阵空间正是 **李代数 $\mathfrak{so}(3)$**，$\exp$ 把它映射到李群 $SO(3)$；四元数则是 $SO(3)$ 的双覆盖 $SU(2)$。

## 关键要点

- **轴角是向量空间，但旋转矩阵不是**——这是为什么需要 $\exp$/$\log$ 在两者间穿梭。
- **Rodrigues 公式 $\exp(\theta\hat{\mathbf{u}}) = I + \sin\theta\,\hat{\mathbf{u}} + (1 - \cos\theta)\,\hat{\mathbf{u}}^2$** 来自把 $\hat{\mathbf{u}}^{k+2} = -\hat{\mathbf{u}}^k$ 代入指数 Taylor 级数，再折叠出 $\sin/\cos$。
- **$\log$ 用 trace 提取角度**：$\theta = \arccos\frac{\operatorname{tr}(R) - 1}{2}$，再反对称化 $R - R^T$ 提取 $\hat{\mathbf{u}}$。
- **slerp 的矩阵等价物** 是 $R(t) = \exp(t\log(R_1 R_0^{-1}))R_0$——同样的最短路径与恒定角速度。
- **Karcher mean** 把「点的迭代质心」推广到旋转：$\bar{R} \leftarrow \exp(\tau\,\overline{\log(R_i\bar{R}^{-1})})\bar{R}$。比朴素「平均轴角」稳健得多。
- **复数指数 $\to SO(2)$，四元数指数 $\to SO(3)$ 双覆盖**——同一个 $\exp$ 框架在不同维度的实例。
- 反对称矩阵的向量空间 $= \mathfrak{so}(3)$，李群是 $SO(3)$——这是李群 / 李代数视角的入门。

## 链接到的概念

- [[exponential-map-rotations]]
- [[3d-rotation-math]]
- [[functions-as-vectors]]
- [[spherical-harmonics]]
- [[mvp-transform]]
- [[max-slater]]

## 原文

- 链接：https://thenumb.at/Exponential-Rotations/
- 本地：`raw/articles/thenumb.at/2022-04-15_exponentially-better-rotations.md`
