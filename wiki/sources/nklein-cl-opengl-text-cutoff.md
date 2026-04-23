---
tags: [source, rendering, 字体渲染, common-lisp]
date: 2026-04-19
sources: 1
---

# Better Text Rendering with CL-OpenGL and ZPB-TTF（Patrick Stein / nklein software）

[[patrick-stein]] 2010 年 1 月发表在 nklein.com 上的一篇续作，讨论如何修掉自己上个月 CL-OpenGL + ZPB-TTF 文本渲染 demo 里的反走样缺陷——过度细分导致小字号糊成一坨。

## 摘要

Stein 上一版代码在递归细分二次 Bézier 弧线时用「弧中点到弦中点的平方距离 < 1」作为终止条件。这个「1」是模型空间的绝对单位，和屏幕像素没关系，于是当字被缩小后，同一个像素里会堆进几十个顶点（他贴的对比图里最坏情况一条弧贡献 63 个顶点），反走样被重复叠加反而变得比真实覆盖更实心，细节丢失。修法是每次开始渲染字符串前，拿当前 `gl:get-double :modelview-matrix / :projection-matrix / :viewport`，用 `glu:un-project` 把屏幕空间的原点与两个相邻像素点反投影回模型空间，取距离一半作为 cutoff，再把阈值从「`< 1`」改成「`< cutoff²`」。代码片段是 Common Lisp，但思路跟语言无关——任何 CPU 侧做曲线细分再丢给 GPU 光栅化的路线都适用。

## 关键要点

- 曲线细分的终止阈值必须跟随当前变换动态计算，不能硬编码模型空间常数
- 反投影单位像素边得到的模型空间距离是天然的 cutoff 尺度
- 阈值错误会让小字号下顶点数量爆炸，同时反走样退化——重复覆盖同一像素导致 alpha 叠加过深
- 这个技巧是 [[slug-gpu-glyph-rendering|Slug]] 类 GPU 方案出现前的典型 CPU-tessellation workaround

## 链接到的概念

- [[screen-space-curve-tessellation-cutoff]]
- [[slug-gpu-glyph-rendering]]
- [[patrick-stein]]

## 原文

- 链接：http://nklein.com/2010/01/better-text-rendering-with-cl-opengl-and-zpb-ttf/
- 本地：`raw/articles/nklein.com/2010-01-19_better-text-rendering-with-cl-opengl-and-zpb-ttf-nklein-soft.md`
