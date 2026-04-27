---
tags: [source, 渲染, cubemap, 立体角, IBL]
date: 2026-04-27
sources: 1
---

# Cubemap Texel Solid Angle（Rory Driscoll / CodeItNow）

[[people/rory-driscoll]] 发表于 2012 年 1 月的数学推导文章，完整推导 cubemap texel 在单位球上所占立体角的计算公式，并解释 AMD CubeMapGen 中 `TexelCoordSolidAngle` 函数的数学来源。

## 摘要

处理 cubemap 积分（辐照度图、球谐系数等）时，每个 texel 对应的球面面积（立体角）并不均匀——角落处面积远小于中心。文章从 cubemap 面上的 texel 坐标 $(x,y)$ 出发，通过对 $\mathbf{p}(x,y) = (x,y,1)/\|(x,y,1)\|$ 求偏导、取叉积，得到微元面积 $\partial A = 1/(x^2+y^2+1)^{3/2}$，再积分得到封闭形式 $f(s,t) = \arctan(st/\sqrt{s^2+t^2+1})$。单个 texel 的立体角由四角处 $f$ 值通过「加右对角、减左对角」得到，与 CubeMapGen 代码一致。文章还提及 Girard 定理法和 Peter-Pike 归一化近似法作为备选。

## 关键要点

- 朴素均匀权重会使角落区域过亮，正确积分需按立体角加权
- 微元面积：$\partial A = (x^2+y^2+1)^{-3/2}$
- 封闭积分：$f(s,t) = \arctan\bigl(st/\sqrt{s^2+t^2+1}\bigr)$（即 `atan2(xy, sqrt(x²+y²+1))`）
- 验证：$f(1,1) = \pi/6$，单面面积 $= 2\pi/3$，六面合计 $4\pi$
- 备选方案：Peter-Pike 的归一化求和，无 arctan，精度略低但实现极简

## 链接到的概念

- [[rendering/cubemap-texel-solid-angle]]
- [[rendering/spherical-harmonics]]
- [[rendering/projected-solid-angle-sampling]]

## 原文

- 链接：https://www.rorydriscoll.com/2012/01/15/cubemap-texel-solid-angle/
- 本地：`raw/articles/rorydriscoll.com/2012-01-15_cubemap-texel-solid-angle.md`
