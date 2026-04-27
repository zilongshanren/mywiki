---
tags: [source, 渲染, 球谐, 面光源, LTC]
date: 2026-04-27
sources: 1
---

# Linearly Transformed Spherical Harmonics Expansions（Christoph Peters / Moments in Graphics）

[[christoph-peters]] 于 2020 年 12 月的博文，介绍其学生 Jan Allmenröder 的学士论文成果：**线性变换球谐（LT-SH）**——一种结合 SH 多边形积分与线性变换余弦（LTC）的技术，用于计算多边形面光源的高光着色。

## 摘要

文章是指向学生博文与论文的简短导言。核心思路来自 Laurent Belcour 的多边形 SH 积分工作，与 LTC 结合后形成 LT-SH。其渲染质量优于纯 LTC，但当前实现（基于 Jingwen Wang 的代码）速度明显更慢。相关演示基于 Falcor 框架公开在 GitHub。

## 关键要点

- LT-SH = 多边形上的 SH 积分（Belcour 2017）＋ 线性变换余弦（LTC）
- 目标：实时渲染中多边形面光源的镜面（specular）分量
- 质量高于 LTC，但性能代价更高
- 演示代码基于 Falcor（Microsoft 实时渲染研究框架）

## 链接到的概念

- [[spherical-harmonics]]
- [[lt-spherical-harmonics]]
- [[spherical-integration]]
- [[physically-based-shading]]

## 原文

- 链接：http://momentsingraphics.de/LinearlyTransformedSH.html
- 本地：`raw/articles/momentsingraphics.de/2020-12-02_linearly-transformed-spherical-harmonics-expansions.md`
