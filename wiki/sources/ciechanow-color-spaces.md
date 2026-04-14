---
tags: [source, 渲染, 颜色]
date: 2026-04-14
sources: 1
---

# Color Spaces（Bartosz Ciechanowski）

[[bartosz-ciechanowski|Bartosz Ciechanowski]] 2019 年 2 月发表的长文，用一连串交互式 color picker 讲清楚「RGB 值本身没有意义，只有在一个 color space 的上下文里才有意义」。

## 摘要

文章从「同一组 RGB 值在两个色彩空间里看起来完全不同」开始，逐步拆开一个色彩空间的三要素：**tone response curve（TRC）**、**primaries**、**white point**。重点讲了为什么光照计算必须在线性空间进行——sRGB 的 TRC 是编码优化，不是数学意义上的颜色。文末对比了 sRGB / DCI-P3 / ProPhoto 的 gamut 差异。

## 关键要点

- **RGB 无意义**：同样的 (0.6, 0.0, 0.0) 在不同色彩空间里是完全不同的物理光。
- **TRC 的作用**：用非线性编码最大化 8-bit 存储在暗部的精度——因为人眼对暗部更敏感。
- **线性域运算**：所有混合、滤波、光照乘法必须在线性值上做，否则红绿中间会变暗。
- **三原色矩阵**：色彩空间 A 到 B 的转换 = 一个由两组 primaries 定义的 3×3 矩阵。
- **白点**：定义 (1,1,1) 的物理白色，常用 D65，换白点需要 chromatic adaptation。

## 链接到的概念

- [[color-space]]
- [[alpha-blending]]
- [[color-lut]]
- [[deferred-rendering]]
- [[bartosz-ciechanowski]]

## 原文

- 链接：https://ciechanow.ski/color-spaces/
- 本地：`raw/articles/ciechanow.ski/2019-02-15_color-spaces-bartosz-ciechanowski.md`
