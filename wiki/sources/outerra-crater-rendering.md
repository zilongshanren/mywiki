---
tags: [source, rendering, procedural-terrain, planet-engine, outerra, vector-overlay]
date: 2026-04-27
sources: 1
---

# Craters（Outerra）

[[people/outerra-team]] 发表于 2013 年 3 月的文章，介绍 Outerra 地形引擎中动态弹坑的向量覆盖层实现方案。

## 摘要

Outerra 的地形生成器包含一个**向量覆盖处理器（vector overlay processor）**，可在程序化生成的地形基础上叠加精细几何——此前已用于生成样条道路（seamless blend、毫米级道路标线厚度）。弹坑是该系统的新增能力。

弹坑通过直径与深度两个参数动态创建，每个坑仅占 64 bit（整个缓冲区可容纳"几乎无限"数量）。系统依据表面类型（沥青/混凝土 vs 泥土）生成不同形状：硬面仅轻微向外弯曲，软地会把碎土大范围抛散。爆炸深度影响坑边坡度，越深的爆心产生越陡的坑壁。创建延迟通常在半秒以内，足以被爆炸粒子特效遮蔽。弹坑形变**同步写入碰撞数据**，对物理模拟立即生效。目前坑数据不持久化跨 session，只在运动时（新地形 tile 生成时）才影响动态性能。最大支持直径约 1 km。

## 关键要点

- 弹坑作为向量覆盖层叠在程序化地形上，与道路系统共享同一管线
- 64 bit per crater，存储开销极低
- 表面类型识别：asphalt/concrete 与 dirt 生成差异化形状
- 爆心深度参数控制坑壁坡度
- 碰撞数据实时同步，物理立即响应
- 最大直径 1 km，生成延迟 < 0.5 s

## 链接到的概念

- [[terrain-vector-overlay-crater]]
- [[planet-terrain-dem-pipeline]]
- [[procedural-grass-rendering]]

## 原文

- 链接：https://outerra.blogspot.com/2013/03/craters.html
- 本地：`raw/articles/outerra.blogspot.com/2013-03-27_craters.md`
