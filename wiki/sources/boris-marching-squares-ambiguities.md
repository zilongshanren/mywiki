---
tags: [source, rendering, marching-squares, mesh, algorithm]
date: 2026-04-27
sources: 1
---

# Resolving Ambiguities in Marching Squares（Boris The Brave）

[[boris-the-brave]] 发表于 2022 年 1 月的文章，介绍用 **Asymptotic Decider** 解决 Marching Squares（2D [[marching-cubes]]）歧义情形的方法。

## 摘要

Marching Squares 在两对对角顶点符号相反的情形下存在两种合法的边界连接方式，朴素实现通常随机选择一种，可能导致 3D 中的网格漏洞或 2D 中的拓扑不一致。本文指出，当顶点存储的不只是布尔值而是**连续数值**时，可利用双线性插值对格子内部进行分析，从而确定性地选择正确的连通方式。

判别量 `Q = top_left * bottom_right - bottom_left * top_right`：Q 为正时两个"正"角在内部连通，Q 为负时不连通。这一公式来自 Nielson & Hamann（1991）的原始论文。文章还简介了 3D 推广：Marching Cubes 33 和 Lewiner Marching Cubes，它们通过引入更多情形加上类似判别量来系统消除所有歧义。[[dual-contouring]] 则从根本上绕开了这一问题。

## 关键要点

- 歧义情形由两对对角顶点符号相反引起，存在两种等效拓扑连接
- Asymptotic Decider：用 Q = TL·BR - BL·TR 的符号确定连通性
- Q 的物理含义是双线性插值曲面在格内的鞍点朝向
- 3D 推广：Marching Cubes 33 / Lewiner MC，系统处理全部歧义情形
- Dual Contouring 规避了查找表拓扑假设，不存在此类问题

## 链接到的概念

- [[marching-cubes]]
- [[marching-squares-multicolor]]
- [[dual-contouring]]
- [[marching-squares-ambiguities]]

## 原文

- 链接：https://www.boristhebrave.com/2022/01/03/resolving-ambiguities-in-marching-squares/
- 本地：`raw/articles/boristhebrave.com/2022-01-03_resolving-ambiguities-in-marching-squares.md`
