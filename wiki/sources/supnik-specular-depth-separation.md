---
tags: [source, hacksoflife, vr, 高光, 立体渲染, 深度感知]
date: 2026-04-27
sources: 1
---

# Specular Hilites Have Their Own Depth（Ben Supnik / The Hacks of Life）

[[ben-supnik|Ben Supnik]] 发表于 2020 年 4 月的短文，记录一个刷牙时的日常观察引发的光学思考：镜面高光的视差深度与其所在表面不同，并由此理解了 X-Plane VR 中双眼独立光照计算的正确性。

## 摘要

Supnik 注意到水龙头上的高光与水垢污渍之间的相对位置，在闭一只眼换另一只眼时会发生位移——这意味着高光的视差深度与表面几何深度不同，高光在双眼视差意义上比表面**更远**。

物理解释很直接：镜中像距离是镜面距离的两倍，高光是光源经表面反射的像，其双目视差对应完整的光路长度（光源→表面→眼睛），而非单程的眼睛到表面距离。

X-Plane 的 VR 实现恰好正确：逐像素光照对左右眼分别用各自的相机原点计算，最初 Supnik 以为这种"不一致"是个奇怪的设计，但从未出现问题。这篇文章让他明白了原因：两眼间的高光位置差异**就是**深度线索本身。

## 关键要点

- 高光的视差深度比表面几何深度更远（完整光路 vs 单程距离）
- VR 正确渲染高光必须对每只眼独立计算光照向量
- "两眼光照不一致"不是缺陷，是正确的立体深度信息
- Reprojection 方案若强行对齐两眼高光位置会丢失深度线索

## 链接到的概念

- [[specular-parallax-depth-vr]]
- [[stereoscopic-3d-design]]
- [[stereo-reprojection-hole-fill]]
- [[physically-based-shading]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2020/04/specular-hilites-have-their-own-depth.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2020-04-16_specular-hilites-have-their-own-depth.md`
