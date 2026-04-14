---
tags: [渲染, 数学, 积分, 球面, 坐标变换]
date: 2026-04-14
sources: 1
---

# 球面积分（Spherical Integration）

**问题**：在图形学里经常要对球面上的函数求积分——环境光、BRDF 的半球积分、重要性采样的归一化常数。一旦换到球坐标 $(\theta, \phi)$，积分里就会凭空冒出一个 $\sin\theta$ 因子，让初学者迷惑。这个因子不是哪条魔法规则，而是「微元面积」换坐标时的必然结果。

## 直观：为什么是 $\sin\theta$

想像把球面切成 $(\theta, \phi)$ 小方格。在赤道附近（$\theta \approx \pi/2$）方格比较方正；越靠极点（$\theta \to 0$ 或 $\pi$），同样的 $d\phi$ 对应的经线之间在空间里的弧长越小——因为**经线在极点汇聚**。具体来说，纬度 $\theta$ 处，一圈经度的半径是 $\sin\theta$，所以一个 $(d\theta, d\phi)$ 方块在球面上对应的面积是

$$ dS = \sin\theta\,d\theta\,d\phi $$

也就是渲染文献里的**微分立体角** $d\omega = \sin\theta\,d\theta\,d\phi$。若忽略这个因子、直接对 $(\theta, \phi)$ 双重积分 1，得到的是 $2\pi^2$，那是个平面矩形的面积，不是球面。正确积分应当给出 $4\pi$。

## 形式推导：参数化 + 雅可比

球坐标到笛卡尔坐标的参数化：

$$ \Phi(\theta, \phi) = (\sin\theta\cos\phi,\ \sin\theta\sin\phi,\ \cos\theta) $$

对任何三维中的参数化曲面 $\mathbf{r}(u,v)$，微元面积由两条切向量的叉积长度给出：

$$ dS = \left\|\frac{\partial \mathbf{r}}{\partial u} \times \frac{\partial \mathbf{r}}{\partial v}\right\|\, du\, dv $$

两条偏导数描述「沿每个参数轴把 $(du, dv)$ 小矩形在空间中如何拉伸」，叉积模长就是被拉伸出的平行四边形面积。对球面求出两条偏导并取叉积，模长恰好化简为 $|\sin\theta|$；因为 $\theta \in [0, \pi]$，$|\sin\theta| = \sin\theta$，于是 $dS = \sin\theta\,d\theta\,d\phi$。

## 更一般的陈述

坐标变换引起的尺度因子并不是球面才有的东西：

- **同维度坐标变换**（$\mathbb{R}^n \to \mathbb{R}^n$）：尺度因子是雅可比矩阵的**行列式绝对值**。这也是多重积分换元法则的出处。
- **嵌入曲面**（本例的 $(\theta, \phi) \to \mathbb{R}^3$）：尺度因子是**两条切向量叉积的模长**，等价于曲面的**第一基本形式** $\mathrm{I}$ 行列式的平方根：$\sqrt{\det\mathrm{I}}$。
- **更一般的流形积分**最干净的表述出自外微积分，「微分形式」让这些积分在任何维度上长得一模一样。

## 在渲染里的用处

一切写成「立体角积分」的量都需要这个因子：

- 环境光对 diffuse 材质的贡献 $\int_{\Omega} L(\omega) (n\cdot\omega)\,d\omega$
- BRDF 归一化：$\int_{\Omega} f_r(\omega_i, \omega_o) \cos\theta_i\, d\omega_i \le 1$
- 立体角采样：从 pdf $p(\omega) = 1/(4\pi)$ 均匀采样球面时，实际采样的是 $(\theta, \phi)$ 的联合 pdf $\frac{\sin\theta}{4\pi}$——采样器里 $\theta$ 不能简单从 $U[0, \pi]$ 取，而要从反 CDF $\theta = \arccos(1 - 2u)$ 取，这个 $\arccos$ 恰好来自 $\sin\theta$ 因子的积分。
- [[projected-solid-angle-sampling]] 在 spherical cap 上的闭式采样也依赖同一族坐标变换技巧。

## 相关

- [[projected-solid-angle-sampling]] — 半球上带 $\cos\theta$ 权的解析重要性采样
- [[spherical-harmonics]] — 球面函数的正交基展开
- [[needlets]]
- [[physically-based-shading]] — BRDF 积分的物理语境
- [[continuous-probability]] — 连续随机变量的积分基础
- [[max-slater]]

## Sources

- [[sources/slater-spherical-integration]]
