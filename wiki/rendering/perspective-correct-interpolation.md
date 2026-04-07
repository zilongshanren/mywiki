---
tags: [渲染, 数学, 光栅化]
date: 2026-04-05
sources: 1
---

# 透视校正插值（Perspective-Correct Interpolation）

光栅化中，屏幕空间的**线性插值**不对应 3D 空间的**线性插值**——必须做透视校正。

## 问题

三角形的顶点在 world/view space 有属性值（UV、颜色、法线）。光栅化时插值给每个 fragment，按屏幕空间重心坐标线性插值会**错**，因为透视投影是非线性的——远处的三角形顶点在屏幕上收缩得更多，单纯屏幕线性插值会让远端的 UV 拉伸变形。

## 解法

对每个顶点属性 `a`，除以该顶点的 clip-space `w`，得到 `a/w`。对 `a/w` 做屏幕线性插值，最后除以屏幕线性插值的 `1/w` 得到正确值：

```
a_correct = interpolate(a/w) / interpolate(1/w)
```

## 硬件支持

现代 GPU 在光栅化阶段**自动做**透视校正插值（除非你用 `noperspective` 限定符显式要求线性）。

## 可见失败案例

关闭透视校正插值时，UV 在斜向拉伸的面上**扭曲**——经典调试信号。

## 相关

- [[rasterization]]
- [[coordinate-spaces]]
- [[mvp-transform]]

## Sources

- [[sources/rtr-day03]]
