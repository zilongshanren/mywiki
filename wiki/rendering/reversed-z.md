---
tags: [渲染, 深度缓冲]
date: 2026-04-05
sources: 1
---

# Reversed-Z

**把深度缓冲范围从 [0,1]（近→远）翻转为 [1,0]（近→远）**，利用 float 的非线性精度分布改善远平面深度精度。

## 原理

IEEE 754 float 的精度在 0 附近最密，远离 0 越来越稀疏。传统 Z buffer 把远平面映射到 1.0，近平面到 0.0——和投影矩阵的"近密远稀"叠加后，**远平面的双重低精度**导致严重 [[z-fighting|Z-fighting]]。

Reversed-Z 反过来：远 → 0.0（float 密），近 → 1.0（float 稀）。**远处获得了 float 的高精度，抵消投影矩阵的稀疏**。

## 配合

必须：
- 翻转投影矩阵的对应项。
- Clear depth 用 0.0 而不是 1.0。
- Depth test 用 `GREATER` 而不是 `LESS`。
- 使用 float depth format（D32F 而非 D24）。

## 在 Unity

Unity 的 URP/HDRP 默认启用 Reversed-Z（对应 `UNITY_REVERSED_Z` 宏）。写 shader 时要意识到深度纹理的含义是反的。

## 相关

- [[z-buffer]]
- [[z-fighting]]

## Sources

- [[sources/rtr-day03]]
