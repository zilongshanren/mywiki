---
tags: [渲染, 深度缓冲, 常见问题]
date: 2026-04-05
sources: 1
---

# Z-fighting

**两个表面在 Z 缓冲中不可分辨，每帧随机决定谁在前**——导致闪烁条纹。

## 根源

[[z-buffer]] 精度非线性分布：近平面密，远平面稀。两个在视觉上几乎重合的远处表面（500m 处相差 1cm）可能被 Z 缓冲的 24 位精度映射到同一值。

## 典型场景

- 两个几乎重合的贴花 / 墙面。
- 远处的道路 + 路标。
- 多层透明贴纸。

## 解决方案

1. **拉近远平面**（far plane）或远离近平面（near plane）——改善整体精度。
2. **Reversed-Z**：见 [[reversed-z]]。
3. **Polygon Offset / DepthBias**：强制深度偏移。
4. **手动分离物体**：几何上拉开距离。
5. **Stencil Buffer**：用模板代替深度判断。

## 相关

- [[z-buffer]]
- [[reversed-z]]
- [[coordinate-spaces]]

## Sources

- [[sources/rtr-day03]]
