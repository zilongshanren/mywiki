---
tags: [数学, 旋转, 李群, 插值, 动画]
date: 2026-04-14
sources: 1
---

# 旋转的指数映射与对数映射

3D 旋转有四种常见表示：**旋转矩阵**、**欧拉角**、**四元数**、**轴角**（参见 [[3d-rotation-math]]）。各有各的痛点：旋转矩阵不是向量空间，相加会引入缩放；欧拉角有 gimbal lock；四元数能 slerp 但不直观、没有标量乘的几何意义、平均不靠谱；轴角是一个普通 3D 向量，可加可缩——但「线性插值的轴角向量乘以一个矩阵就变成正确旋转」并不显然。Max Slater 借 Keenan Crane 的 CMU 15-462 教材展示：把 $\exp$ 和 $\log$ 推广到矩阵上，可以把这四种表示串成一条干净的转换链，**还能做矩阵都不能做的「平均一组旋转」**。

## 2D 的预演：用 $e^{\theta J}$ 推出旋转矩阵

2D 里旋转只有一个轴。考察反对称矩阵 $J = \begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}$，它的几何意义是「逆时针 90 度旋转」——验证 $J^2 = -I$ 即可。把它代入指数函数的 Taylor 级数：

$$
e^{\theta J} = I + \theta J + \frac{(\theta J)^2}{2!} + \frac{(\theta J)^3}{3!} + \cdots
$$

利用 $J^2 = -I, J^3 = -J, J^4 = I, \ldots$ 把级数拆成两堆，正好分别凑出 $\sin\theta$ 和 $\cos\theta$ 的 Taylor 展开：

$$
e^{\theta J} = \cos\theta \cdot I + \sin\theta \cdot J = \begin{bmatrix}\cos\theta & -\sin\theta \\ \sin\theta & \cos\theta\end{bmatrix}
$$

这就是标准 2D 旋转矩阵——也是 Euler 公式 $e^{i\theta} = \cos\theta + i\sin\theta$ 的矩阵版本。**$\exp$ 把「角度 $\theta$」翻译成「旋转矩阵」**，对应的 **$\log$**（用 `atan2` 提取最小角度）做反向翻译。

## 3D 的关键：把 $\mathbf{u}\times$ 写成反对称矩阵 $\hat{\mathbf{u}}$

3D 里 $J$ 的角色由「绕单位向量 $\mathbf{u}$ 转 90°」承担。注意叉乘 $\mathbf{u}\times\mathbf{p}$ 在几何上正好等于 $\mathbf{p}$ 投影到 $\mathbf{u}$ 的法平面后旋 90°。把叉乘写成矩阵：

$$
\hat{\mathbf{u}} = \begin{bmatrix}0 & -u_z & u_y \\ u_z & 0 & -u_x \\ -u_y & u_x & 0\end{bmatrix}
$$

这是个 **反对称矩阵**（$\hat{\mathbf{u}}^T = -\hat{\mathbf{u}}$），就像 2D 的 $J$。所有反对称 3×3 矩阵构成一个 3 维向量空间——这正是李代数 $\mathfrak{so}(3)$。把 $\theta\hat{\mathbf{u}}$ 代入指数级数，利用恒等式 $\hat{\mathbf{u}}^{k+2} = -\hat{\mathbf{u}}^k$ 重新折叠：

$$
\exp(\theta\hat{\mathbf{u}}) = I + \sin\theta\,\hat{\mathbf{u}} + (1 - \cos\theta)\,\hat{\mathbf{u}}^2
$$

这就是 **Rodrigues 公式**——和 [[3d-rotation-math]] 里 Fabrice Neyret 那行 `mix(dot*axis, vec, cos) + sin*cross` 一一对应。可以验证：$\theta = 0$ 给出 $I$；$\theta = \pi/2$ 给出绕 $\mathbf{u}$ 的 90° 旋转；$\theta = \pi$ 给出半圈。同时验证 $\exp(\theta\hat{\mathbf{u}})^T \exp(\theta\hat{\mathbf{u}}) = I$ 与行列式连续从 1 出发不会变号——**结果一定是合法的旋转矩阵**，即元素属于李群 $SO(3)$。

## 反向：从矩阵恢复 $\theta\hat{\mathbf{u}}$

$\log$ 的存在依赖：$\exp$ 不是单射（绕同一轴转 $\theta$ 与 $\theta + 2\pi$ 给同一个矩阵），所以约定 $\log$ 返回最小幅度。

第一步：取迹（对角和）。$\operatorname{tr}(I) = 3$，$\operatorname{tr}(\hat{\mathbf{u}}) = 0$（反对称矩阵对角全零），$\operatorname{tr}(\hat{\mathbf{u}}^2) = -2|\mathbf{u}|^2 = -2$。所以

$$
\operatorname{tr}(R) = 3 - 2(1 - \cos\theta) = 1 + 2\cos\theta \implies \theta = \arccos\!\frac{\operatorname{tr}(R) - 1}{2}
$$

第二步：反对称化 $R$ 提取 $\hat{\mathbf{u}}$。$\hat{\mathbf{u}}^2$ 是对称的，所以 $R - R^T = 2\sin\theta\,\hat{\mathbf{u}}$。读出 $\hat{\mathbf{u}}$ 的三个独立元素就得到 $\mathbf{u}$。

## 干净的旋转插值公式

有了 $\exp$ 和 $\log$，从 $R_0$ 平滑插值到 $R_1$ 的公式不再依赖于哪种表示：

$$
R(t) = \exp\bigl(t \log(R_1 R_0^{-1})\bigr)\, R_0
$$

**意思是**：先算「从 $R_0$ 一步直达 $R_1$」的相对旋转 $R_1 R_0^{-1}$，用 $\log$ 把它折成轴角，按 $t$ 缩放（这一步是合法的——轴角是向量空间），再 $\exp$ 回矩阵，最后乘上起点。这套公式 **总是走最短路径，恒定角速度**——和四元数 slerp 等价，但完全是矩阵运算。

## 旋转矩阵的平均：Karcher mean

四元数和 slerp 能漂亮地解决两个旋转之间的插值，但 **平均一组旋转** 是另一回事。最朴素的「先 $\log$ 取轴角、平均、再 $\exp$」会被 catastrophic cancellation 击穿——平均 $[\pi, 0, 0]$ 和 $[-\pi, 0, 0]$ 给零向量，但两个旋转其实是同一个。

借鉴普通点的迭代平均（梯度下降找质心），可以推广到旋转：

```
R̄ ← I
重复:
    u_i ← log(R_i R̄⁻¹)            # 每个旋转相对当前估计的「轴角偏移」
    u   ← (1/n) Σ u_i              # 平均
    R̄  ← exp(τ u) R̄              # 沿平均方向小步
直到 |u| < ε
```

收敛点叫做 **Karcher mean**——「最小化到所有 $R_i$ 的角度距离平方和」的旋转。它本质是李群上的几何中位／均值，不依赖具体表示，对任何一组旋转都给出直观、对称的结果。

## 与四元数的连接

完全平行的故事在四元数侧：把轴角向量 $\mathbf{u}$ 变成纯虚四元数 $\mathbf{q} = u_x i + u_y j + u_z k$ 然后 $e^{\mathbf{q}}$，因为四元数乘法满足类似的反对称恒等式，结果是 $\cos|\mathbf{u}| + \frac{\sin|\mathbf{u}|}{|\mathbf{u}|}\mathbf{q}$——一个单位四元数。**2D 时复数指数给出 $SO(2)$，3D 时四元数指数给出 $SO(3)$ 的双覆盖 $SU(2)$**。如果不需要旋转矩阵，四元数指数是同一套 $\exp/\log$ 框架的最便宜实现。

## 为什么这套框架值得记住

- 它把「轴角是向量空间」这件事 **形式化** 了——反对称矩阵的加法/数乘构成 $\mathfrak{so}(3)$，$\exp$ 把它映射到 $SO(3)$。
- 它给出 **不依赖于四元数的** slerp 等价物。
- 它支持 **多个旋转的平均**（Karcher mean），是动画 retargeting、SLAM 位姿融合、刚体姿态估计的基础。
- 它和高维李群（$SE(3)$ 含平移、$SO(n)$）共用同一套语法——是机器人学和几何深度学习中的通用工具。

## 相关

- [[3d-rotation-math]] — 四种表示的概览，以及 Rodrigues 公式的直觉拆解
- [[functions-as-vectors]] — 同属 Slater 的「线性代数推广到无限维 / 流形」长文系列
- [[spherical-harmonics]] — 也是「在某个对称空间上做特征展开」
- [[mvp-transform]]
- [[max-slater]]

## Sources

- [[sources/slater-exponential-rotations]]
