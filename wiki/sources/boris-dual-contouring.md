---
tags: [source, rendering, procedural-generation, mesh, dual-contouring]
date: 2026-04-27
sources: 1
---

# Dual Contouring Tutorial（Boris The Brave）

[[people/boris-the-brave]] 发表于 2018 年 4 月的教程，是 Marching Cubes 系列的第三篇，介绍更先进的等值面提取技术 Dual Contouring。

## 摘要

Dual Contouring 通过在每个单元格内放置一个顶点（而非像 Marching Cubes 那样在边上放置）来构建网格，从而解决了后者的三大缺陷：复杂的查找表逻辑、歧义性解析、以及无法表达尖锐边角。算法的关键在于利用梯度信息（法线/hermite data）：在每条有符号变化的边上采样梯度，然后用**二次误差函数（QEF）**求出单元格内最贴合所有法线的顶点位置。"Dual"之名来自图论对偶——原网格单元格变成输出顶点。文章指出 QEF 的实践难题：共线法线会导致顶点飞出单元格，推荐结合"约束QEF求解"和"QEF偏置向中心"两种技术处理。文章还介绍了非流形网格、自相交等边界情况，以及在八叉树上运行以支持多分辨率的扩展。

## 关键要点

- 每个单元格一个顶点；"连线"沿每条有符号变化的边，连接相邻单元格的顶点
- 需要梯度信息（可解析计算，也可数值近似）；梯度即法线/hermite data
- QEF = 各法线到理想直线距离平方之和，最小化得最优顶点位置
- 共线法线问题：加约束（限制在格内）+ QEF 向中心偏置
- Surface Nets 是简化变体（丢弃梯度信息，取均值），权衡简洁 vs 质量
- 八叉树扩展可实现 LOD，仅在需要细节处细分

## 链接到的概念

- [[rendering/dual-contouring]]
- [[rendering/marching-cubes]]

## 原文

- 链接：https://www.boristhebrave.com/2018/04/15/dual-contouring-tutorial/
- 本地：`raw/articles/boristhebrave.com/2018-04-15_dual-contouring-tutorial.md`
