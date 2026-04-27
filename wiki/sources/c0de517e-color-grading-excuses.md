---
tags: [source, rendering, 后处理, color-grading, 渲染哲学]
date: 2026-04-27
sources: 1
---

# Color Grading and Excuses（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2016 年 1 月的评论文章，质疑游戏行业沿用电影后处理流程的合理性，并呼吁探索游戏媒介自己的色彩控制语言。

## 摘要

文章以《谍影重重》在飞机上的观影感受为引，切入一个更大的问题：游戏后处理管线为什么几乎千篇一律地包含 bloom、filmic tone mapping、color cube grading、DOF、motion blur、vignette、色差——这些特效的根据是什么？作者提出两种流行辩护并逐一拆解：一是"电影史上研究充分"——但相机的物理限制并不适用于游戏渲染；二是"艺术家熟悉、受众可读"——有一定道理，但实际上业界大量复制彼此的流程，连"copy from film"也没做到位，最终成为不伦不类的混合物。真正的问题在于，游戏有一项电影没有的独特能力：可以直接修改光源颜色、材质属性，而不必在最终帧上做全局后处理。这种"源头控制"既物理正确，又给艺术家更细粒度的工具。文章最后承认游戏在工具开发上投入不足是客观限制，但主张行业应该开始寻找自己的视觉语言。

## 关键要点

- 游戏常见后处理（lens flare、色差、bloom grain）模拟的大多是镜头厂商想消除的**缺陷**，而非有意为之的美学
- 电影调色是逐镜头、带蒙版和旋转分析的精细工作，游戏所用的"全局 color cube"根本不是同一回事
- 游戏独有的优势：可以修改所有光源色温/强度、材质色调，成本等同于后处理但物理正确得多
- "从电影借来的视觉语言"的真正原因可能只是方便和惯性，而非深思熟虑的美学选择
- 部分后处理有实际功能价值（film grain 可以辅助打破几何锯齿），但应以功能为由，而非以"仿电影"为由

## 链接到的概念

- [[color-lut]]
- [[filmic-post-processing-critique]]
- [[local-tonemapping]]
- [[physically-based-shading]]

## 原文

- 链接：https://c0de517e.blogspot.com/2016/01/color-grading-and-excuses.html
- 本地：`raw/articles/c0de517e.blogspot.com/2016-01-24_color-grading-and-excuses.md`
