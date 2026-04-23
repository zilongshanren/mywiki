---
tags: [source, graphics, opengl, instancing, benchmark]
date: 2026-04-19
sources: 1
---

# Instancing Numbers（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2011 年 3 月 7 日的一则极短 post，直接公布 X-Plane 当时 GPU instancing 的吞吐数字，作为 OpenGL 论坛相关讨论的现场数据点。

## 摘要

在一台 2.8 GHz Mac Pro（几年前的机型）+ ATI Radeon 4870 + OS X 10.6.6 的组合上，X-Plane 可以用 OpenGL GPU instancing 在接近 60 fps 下渲染 87,000 个 mesh，平均每次 draw call 推 32 个 instance。Supnik 没有进一步解释场景组成、cull 策略或 mesh 三角形数——这就是一条「给数字、不做注释」的参考贴。

## 关键要点

- 2011 GPU instancing 的基线能力：**87K mesh / 60 fps / ~16 万 draw call/s**
- draw call 平均 32 instance：反映 X-Plane 同类 mesh 的分组粒度
- 没报 cull 前的原始 mesh 数 —— 跨家对比要谨慎
- 作为后来 [[opengl-draw-call-batching-sweet-spot|Outerra 2016 吞吐甜点测试]]的前向锚点

## 链接到的概念

- [[xplane-instancing-2011-numbers]]
- [[draw-call]]
- [[opengl-draw-call-batching-sweet-spot]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/03/instancing-numbers.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-03-07_instancing-numbers.md`
