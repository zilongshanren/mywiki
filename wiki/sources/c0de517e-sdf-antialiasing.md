---
tags: [source, rendering, sdf, antialiasing, 字体渲染]
date: 2026-04-27
sources: 1
---

# Supersampling and antialiasing distance fields（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2012 年 10 月的短文，描述一种用 4-tap 采样 + 凸多边形面积计算来精确求 SDF 覆盖率的抗锯齿方案，在 Capcom Vancouver 由学生实现并验证有效。

## 摘要

文章呈现的是 Pesce 整理旧笔记时发现的一个算法草图。问题背景是 signed distance field 字体渲染的抗锯齿：简单用 smoothstep 阈值的方式在边缘过渡上不够精确，而这个方案试图通过**精确计算 SDF 等值线与像素方格的交叉面积**来得到更准确的覆盖值。

算法核心：在一个单位方格上采 4 个距离场 tap（用 `ddx/ddy` 确定采样宽度），将四个顶点分为「在 distance field 内」和「在外」，然后逆时针遍历顶点和边——对「内」顶点保留坐标，对「内外交界边」计算交点——构成一个凸多边形，用行列式法增量计算其面积，即为覆盖率。整个算法展开在 shader 中内联运行（unrolled）。

UBC 学生 Jason Peng 在 Capcom Vancouver 实现了此算法，Pesce 注明「他说有效」。文章本身非常简短，配有手写笔记图，是 Pesce 特有的「half-baked idea」发布风格。

## 关键要点

- 4-tap SDF 覆盖率计算：对像素方格建凸多边形，面积 = coverage
- 用 `ddx/ddy` 确定采样范围，自适应分辨率
- 类 2D marching squares 的逻辑，但不生成等值线，直接算面积
- 行列式法（shoelace 公式）增量累加，可 unroll 进 shader
- 原理上比 smoothstep 阈值更精确，但实现复杂度明显更高

## 链接到的概念

- [[sdf-font-atlas-rendering]]
- [[analytical-antialiasing]]
- [[aa-techniques-survey-2011]]

## 原文

- 链接：http://c0de517e.blogspot.com/2012/10/supersampling-and-antialiasing-distance.html
- 本地：`raw/articles/c0de517e.blogspot.com/2012-10-07_supersampling-and-antialiasing-distance-fields.md`
