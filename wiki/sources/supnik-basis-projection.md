---
tags: [source, 线性代数, 渲染, 坐标变换]
date: 2026-04-19
sources: 1
---

# Basis Projection（Ben Supnik / The Hacks of Life）

[[ben-supnik|Ben Supnik]] 发表于 2010 年 11 月的续篇，把上一篇的「矩阵列是预制零件」翻过来问另一个问题：如果矩阵是 decoder，那么 encoder 长什么样？

## 摘要

给定世界空间里的一个点，如何把它编码回模型空间？Supnik 的答案是「basis projection」——与每根基向量做点积。把三根基向量写成矩阵的**行**而不是列，就是编码矩阵。令人愉快的结论：对正交矩阵，编码矩阵 = 原矩阵的转置 = 原矩阵的逆。所以同一块 3x3 float 数据，**从列看是 decoder（旧基在新坐标系的表达），从行看是 encoder（新基在旧坐标系的表达）**——两种语义互为转置。这条观察直接推出为什么 X-Plane 能用极少算术从 model-view 矩阵里拿到 camera 的朝向（行）和位置（右列 × 左上 3x3 的转置 × 负号）。

## 关键要点

- Encode = 对每根基向量做点积 = 把基放到矩阵的行里。
- Decode = 把基放到列里。
- 正交矩阵的转置 = 逆，这两种视角通过转置互换。
- 意义：同一个 model-view 矩阵，左上 3x3 的「行」直接给出相机 right/up/forward。

## 链接到的概念

- [[matrix-as-basis-vectors]]
- [[coordinate-spaces]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/11/basis-projection.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-11-29_basis-projection.md`
