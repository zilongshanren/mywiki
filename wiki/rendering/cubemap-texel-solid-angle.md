---
tags: [渲染, cubemap, 立体角, 积分, IBL]
date: 2026-04-27
sources: 1
---

# Cubemap Texel 立体角（Cubemap Texel Solid Angle）

在处理 cubemap 时（生成漫反射辐照度图、球谐系数近似等），需要在球面上对 texel 值做积分。正确的积分要求**每个 texel 乘以它在单位球上所占的立体角**——这个角不是均匀的：靠近 cubemap 面边缘和角落的 texel 投影到球面后面积更小，越靠近角落越小。若忽略这个差异，角落区域会被过高权重，导致偏亮的积分结果。

AMD CubeMapGen 已实现了正确的立体角计算。Rory Driscoll 在 2012 年详细推导了这一计算的数学来源。

## 推导思路

设 cubemap 一个面的 texel 中心坐标在 $[-1,1]^2$ 范围内为 $(x, y)$，将其投影到单位球上的点为：

$$
\mathbf{p}(x,y) = \frac{(x,\, y,\, 1)}{\sqrt{x^2+y^2+1}}
$$

对 $x$、$y$ 分别求偏导，得到投影点随 texture-space 坐标变化的切线向量：

$$
\frac{\partial\mathbf{p}}{\partial x} = \frac{(y^2+1,\,-xy,\,-x)}{(x^2+y^2+1)^{3/2}}, \quad
\frac{\partial\mathbf{p}}{\partial y} = \frac{(-xy,\,x^2+1,\,-y)}{(x^2+y^2+1)^{3/2}}
$$

这两个向量叉积的模即**微元面积**：

$$
\partial A = \frac{1}{(x^2+y^2+1)^{3/2}}
$$

对该微元积分：

$$
f(s,t) = \int_0^t\int_0^s \frac{1}{(x^2+y^2+1)^{3/2}}\,dx\,dy = \arctan\frac{st}{\sqrt{s^2+t^2+1}}
$$

一个 texel 的立体角通过四角 $A,B,C,D$ 的 $f$ 值叠加得到（加号对应右对角，减号对应左对角）：

$$
S = f(A) - f(B) + f(C) - f(D)
$$

这正是 AMD CubeMapGen 源代码中 `TexelCoordSolidAngle` 的实现逻辑：

```cpp
float AreaElement(float x, float y) {
    return atan2(x * y, sqrt(x * x + y * y + 1));
}
```

## 正确性验证

将整个面（$[-1,1]^2$）积分后结果应为 $\frac{2\pi}{3}$（六面合计 $4\pi$）。代入 $f(1,1) = \arctan(1/\sqrt{3}) = \pi/6$，乘以四个角的组合确实得到 $2\pi/3$，验证正确。

## 备选方法

- **Monte Carlo 估计**：统计上无偏，但会对某些 texel 过采样、某些欠采样，不如精确积分高效。
- **均匀权重**：忽略立体角差异，最简单但会导致角落偏亮。
- **Peter-Pike 归一化**：对所有 texel 用 $4/(1+s^2+t^2)^{3/2}$ 求和后归一化至 $4\pi$，无需 arctan，代码极简，微小精度损失。
- **Girard 定理（球面三角形面积）**：通过三角形内角和超出 $\pi$ 的部分计算面积，数学优雅但工程上计算角度较繁琐。

## 应用场景

- 球谐函数（[[spherical-harmonics]]）预计算辐照度时的权重
- 各面 IBL 预滤波（pre-filtered environment map）的正确积分
- 任何需要「把 cubemap 值当成球面信号积分」的操作

## 相关

- [[spherical-harmonics]] — SH 系数用 cubemap 积分时正是此公式的用场
- [[projected-solid-angle-sampling]] — 另一种与立体角有关的采样策略（面光源）
- [[env-mapping-cubemap-shader]] — cubemap 的基本使用
- [[parallax-corrected-cubemap]] — 更高级的 cubemap 反射
- [[physically-based-shading]] — IBL 作为 PBR 的重要组成部分
- [[rory-driscoll]]

## Sources

- [[sources/rory-cubemap-texel-solid-angle]]
