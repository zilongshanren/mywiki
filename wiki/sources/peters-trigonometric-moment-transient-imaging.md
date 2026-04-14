---
tags: [source, 渲染, 成像, 矩, lidar]
date: 2026-04-14
sources: 1
---

# Solving Trigonometric Moment Problems for Fast Transient Imaging（Peters et al.）

[[christoph-peters]]、Jonathan Klein、Matthias B. Hullin、Reinhard Klein 在 SIGGRAPH Asia 2015 的论文摘要页。用**三角矩问题**的经典闭式解，把瞬态成像的捕获和重建速度提高几个数量级。

## 摘要

瞬态图像除了两个空间维还有一维飞行时间，能把直射、多次反射和次表面散射分开。传统捕获需要一分钟以上。本文改用**幅度调制连续波（AMCW）lidar**——在若干个调制频率上测量相位/幅度，得到的正是响应的**三角矩**。重建被表述成一个**截断三角矩问题**，并选用两条经典闭式路径：最大熵谱估计（用于连续分布）与 Pisarenko 估计（用于 m 个离散返回）。两者都适合 GPU，实现每秒可重建超过 10 万帧瞬态图像，结合对调制波形的改造，最终达到 18.6 FPS 的瞬态视频。副产物是对 range imaging 多径干涉的消除——非常实用的工程价值。

## 关键要点

- **三角矩 = 调制 lidar 的自然测量**：AMCW 在 m 个频率上采样，恰好是响应时域函数的前 m 阶三角矩。
- **闭式、无迭代**：最大熵谱估计给连续重建，Pisarenko 给 m 个 Dirac 的稀疏重建；两者都是古典数学里的「老朋友」。
- **m 个频率分离 m 个返回**：Pisarenko 的精确性承诺，论文用 m=3 的实测场景验证。
- **10 万帧/秒的 GPU 重建**、**18.6 FPS 的瞬态视频**——把一个此前停留在实验室的技术推进到接近实时。
- **去除多径干涉**：同一套稀疏模型可以把错误的「混合距离」拆成正确的第一返回，改进普通 ToF 深度相机。

## 链接到的概念

- [[trigonometric-moment-transient-imaging]]
- [[christoph-peters]]
- [[moment-shadow-mapping]]
- [[spectral-rendering]]

## 原文

- 链接：<http://momentsingraphics.de/SiggraphAsia2015.html>
- DOI：<https://doi.org/10.1145/2816795.2818103>
- 本地：`raw/articles/momentsingraphics.de/2015-01-01_solving-trigonometric-moment-problems-for-fast-transient-ima.md`
