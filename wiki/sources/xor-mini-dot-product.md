---
tags: [source, 渲染, shader, 数学, 向量]
date: 2026-04-14
sources: 1
---

# Functions: Dot Product（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2022 年 9 月的 "Functions" 系列第一篇，用 shader 实战的角度把**点乘**从一个枯燥的线性代数公式拆成 shader 作者的瑞士军刀。

## 摘要

文章先给点乘的两个定义——代数上是"分量对乘求和"，几何上是 `|a|·|b|·cos(θ)`。shader 里算的是前者，但后者能让你从几何直觉出发想问题：两个向量**同向**时 cos=1，**垂直**时 cos=0，**反向**时 cos=-1。接着展开三个典型用途：1）**任意方向条纹**——`mod(floor(dot(position, direction)), 2.)` 把"某个方向走了多远"打包成一条条纹图案，direction 长度就是频率；2）**平方反比衰减**——`1.0 / dot(a, a)` 直接算出 Pythagorean 距离平方，避开 `sqrt`/`pow` 的来回；3）**Lambert 光照**——`max(0, dot(N, L))` 就是完整的漫反射 shading 公式。文末说：点乘是理解矩阵和旋转数学前的最后一道门槛，值得反复重读。

## 关键要点

- **代数** `a.x*b.x + a.y*b.y`，**几何** `|a||b|cos(θ)`，shader 里走代数，思考走几何。
- **条纹** trick：`dot(p, dir)` 给"沿 dir 走了多远"，换面 `mod` 就出斜条纹。
- **距离平方** trick：`dot(d, d)` = 距离²，用来做光照衰减比 `length` + `pow` 便宜。
- **Lambert** trick：`dot(N, L)` 直接是 cos 夹角，负值即背光。
- 点乘理解是矩阵 / 投影 / 旋转数学的前置条件。

## 链接到的概念

- [[vector-dot-product]]
- [[diffuse-lighting-lambertian]]
- [[shader-vector-math-primer]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/gm-shaders-mini-the-dot-product-1329407
- 本地：`raw/articles/mini.gmshaders.com/2022-09-03_functions-dot-product.md`
