---
tags: [source, rendering, 颜色, 数据可视化, shader, 感知均匀]
date: 2026-04-27
sources: 1
---

# "Coder" Color Palettes for Data Visualization（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2017 年 11 月的文章，针对渲染工程师调试时常用的「直接把数据映射到 RGB 通道」做法，提供了一组感知均匀、可直接嵌入 shader 的调色板函数。

## 摘要

「coder colors」指把调试值直接塞进 RGB 三个通道（R=数据1, G=数据2, ...），这是图形程序员最常见的快速可视化手段。问题在于：RGB 三通道感知亮度不等（绿通道最亮，蓝通道最暗），导致数据被系统性地扭曲，且同一亮度下很难区分超过十个值。

Pesce 提出在 CIELAB 色彩空间中沿感知均匀路径设计调色板，再把结果拟合为 GLSL 函数（可直接复制到任何着色语言），无需外部纹理。目标：感知线性、能区分 >10 档、对色盲友好（主要依赖亮度变化）。

## 关键要点

- **感知均匀性**：步进单位应为 JND（Just Noticeable Difference），在 CIELAB 中路径可以是曲线（via CIELCH / HSLUV），而不必是线段
- **通道不等性**：蓝通道感知亮度约是绿通道的 1/3，直接 RGB 映射严重扭曲数据的感知权重
- **避免纯黑**：sRGB 暗端感知非线性最差，且许多显示设备对黑色处理不精确
- **四类调色板函数**：
  - `ColorFn1D`：单维顺序数据（0~1），类 Viridis 风格，单通道有 sine 波分量
  - `ColorFn1Ddiv`：单维发散数据（-1~1），类红蓝渐变
  - `ColorFn1DtwoC/fiveC`：单维数据 + 分类标签（2类/5类），同亮度不同色调
  - `ColorFn2D/2Ddiv`：二维数据，红绿或红蓝映射，含 gamma 重映射步骤
- **代码可移植性**：函数体故意不用 GLSL 向量类型，可直接粘贴到 C/Java/HLSL

## 链接到的概念

- [[perceptual-palette-functions]]
- [[color-blindness-accessibility]]
- [[perceptual-colormaps]]
- [[color-space]]
- [[debug-visualization]]

## 原文

- 链接：https://c0de517e.blogspot.com/2017/11/coder-color-palettes-for-data.html
- 本地：`raw/articles/c0de517e.blogspot.com/2017-11-18_coder-color-palettes-for-data-visualization.md`
