---
tags: [source, cgal, 计算几何, arrangement, 多边形]
date: 2026-04-19
sources: 1
---

# Importing Faces Into CGAL Arrangements（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2010 年 5 月的短文，讲在 X-Plane 地图生成里怎么把脏多边形（自相交、互相碰撞、可能有 antenna）批量塞进 CGAL `Arrangement_2`，以及 sweep 后怎么判定哪些 face 是多边形内部。

## 摘要

外部来的多边形不能假设干净，进 arrangement 前要处理「自相交」「多边形互相切割」两种情况。Supnik 给出三条导入路径：general-polygon-set（做布尔代数）、overlay（自定义 face 组合）、curves 批量 insert（交给 sweep line 收拾烂摊子）。方法 3 最通用，但 sweep 后要回答「哪些 face 是内部」。三种判定：bounded 测试只适用于单多边形；外→内 toggle 策略受 antenna 破坏（零宽尖刺只 toggle 一次而非两次，且数据挂在 edge 不是 halfedge，拓扑查询也救不了）；winding rule 适用于 offset/Minkowski sum，同样被 antenna 干扰但实际场景里 antenna 不出现。工程结论：预处理阶段检测并剔除 antenna，比事后修拓扑便宜。

## 关键要点

- CGAL arrangement 是平面曲线排列的拓扑数据结构，能容忍脏输入但需要用户理解代价
- 批量 insert + sweep 是处理未知来源多边形的最稳路径
- antenna（零宽尖刺）是 toggle 策略和 winding rule 的共同失败点
- edge 粒度数据标签对 halfedge 粒度查询不够——这是 CGAL 干净抽象下的结构裂缝
- 工程折中：预处理剔 antenna，不要指望 CGAL 内部修

## 链接到的概念

- [[cgal-arrangement-import-antennas]]
- [[cgal-exact-arithmetic-mantissa-growth]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/05/importing-faces-into-cgal-arrangements.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-05-06_importing-faces-into-cgal-arrangements.md`
