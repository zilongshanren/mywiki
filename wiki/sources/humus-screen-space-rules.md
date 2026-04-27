---
tags: [source, rendering, screen-space, filter-kernel, deferred-rendering, shadow, sss]
date: 2026-04-27
sources: 1
---

# Screen-Space: Rules for Designing Graphics Sub-systems Part I（Wolfgang Engel / Diary of a Graphics Programmer）

[[people/wolfgang-engel|Wolfgang Engel]] 发表于 2011 年 6 月的系列文章第一篇，提出"尽可能在屏幕空间完成计算"的设计原则，并详述大尺度屏幕空间滤波核的三个工程挑战。

## 摘要

Engel 把屏幕空间原则概括为：随着可用算力增加而内存带宽增长停滞，将更多操作移入屏幕空间在大多数情况下更高效。后处理（DoF、MotionBlur、Tone Mapping、MLAA）是最显然的案例；文章着重讨论**两类新兴系统**：延迟光照下屏幕空间的高代价材质（皮肤、头发）和阴影/GI 滤波核。核心难题有三：（1）滤波核随相机距离缩放，用线性化深度驱动采样步长；（2）各向异性滤波核，通过法线与视角向量的点积取平方根获得椭圆响应；（3）深度差异剔除，比较滤波核中心与每个采样点的深度差，超出阈值则放弃该采样，防止边缘漏光。

## 关键要点

- 屏幕空间滤波核是 Engel 三条设计规则之一（另两条为：禁用查找表、均匀误差分布）
- 线性化深度公式：`depthLin = (-Near * Q) / (Depth - Q)`，Q = Far/(Far-Near)
- 采样步长 ∝ `sqrt(1 / (depthLin² × bias))`，越远像素 footprint 越大而步长收缩
- 各向异性核：`Aniso = saturate(sqrt(dot(viewVec, normal)))`，把 WSN 与视角夹角投射成椭圆
- 深度剔除阈值 `errDepth` 防止宽滤波核在几何转角处将阴影/GI 值涂抹到遮挡边缘外侧

## 链接到的概念

- [[rendering/deferred-rendering]]
- [[rendering/screen-space-filter-kernel]]
- [[rendering/screen-space-shadow-map-urp]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2011/06/screen-space-rules-for-designing.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2011-06-13_screen-space-rules-for-designing-graphics-sub-systems-part-i.md`
