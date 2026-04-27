---
tags: [source, rendering, skinning, normals, character-animation]
date: 2026-04-27
sources: 1
---

# Skinning Normals Notes（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2011 年 5 月的技术笔记，讨论骨骼蒙皮（skeletal skinning）过程中法线权重计算的正确性问题。

## 摘要

文章指出法线在实时渲染中常被当作颜色对待，鲜少被认真推导——就像 gamma 校正或法线贴图混合在"流行之前"从未被认真推导一样。Pesce 以一个具体案例（格斗游戏中手臂腋窝区域的异常光照）为切入点，推导了蒙皮法线权重的正确计算方式：顶点法线由相邻面法线加权平均得到，蒙皮权重应当是作用在这些相邻面的骨骼权重的加权平均，权重由每个面的面积贡献决定。

文章还附有一处勘误：原始笔记中第二个顶点的权重写错，正确值为骨骼 1/2 按 0.75/0.25 分配，而非原始值。2023 年 Sergey Makeev 补充了一个更深的问题：如果骨骼允许平移（而非仅旋转），直接平均法线会产生更严重的错误，因为平移不改变法线方向，这在现代面部动画中是一个需要额外处理的边界情况。

## 关键要点

- 蒙皮法线权重 = 相邻面骨骼权重的面积加权平均
- 假设条件：蒙皮前后各面面积近似不变（旋转为主的骨骼动画下成立，平移为主时失效）
- 格斗游戏（Fight Night）案例：骨骼仅旋转，该假设成立
- 现代面部动画：骨骼大量平移，需要额外处理
- 同样适用于切线空间：法线、切线的正确性直接影响光照计算精度

## 链接到的概念

- [[rendering/gpu-skinning-matrix-palette]]
- [[rendering/tangent-space-normal-mapping]]
- [[rendering/normal-map-blending]]

## 原文

- 链接：https://c0de517e.blogspot.com/2011/05/skinning-normals-notes.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-05-15_skinning-normals-notes.md`
