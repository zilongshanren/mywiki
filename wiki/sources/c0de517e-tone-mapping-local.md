---
tags: [source, graphics, 色调映射, 局部色调映射, 光照分解]
date: 2026-04-27
sources: 1
---

# Tone mapping & local adaption（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2016 年 9 月的文章，探讨局部色调映射在游戏中的定位，并提出用渲染器内部的光照分解（illuminance / reflectance 分离）来替代基于邻域滤波的 LTM 方案。

## 摘要

Pesce 先梳理了全局 TM 在游戏中更受欢迎的原因：游戏比摄影更在意亮度感知，bloom 和自动曝光都是为此服务的工具。局部 TM 理论上可以保留高光与阴影细节，但极端应用会产生"photographic HDR"的不真实感。

文章的核心提案是：既然实时渲染器已经在光栅化阶段把 diffuse + specular 与材质 albedo 分开，可以直接提取一张"无贴图场景"作为 illuminance 图，把 tone mapping 曲线只施加在光照上（reflectance 分离出来不压缩），最后再乘回去做全局 TM。这实质上是一种零滤波成本的局部 TM，避免了 bilateral 的 halo 和振铃问题，且完全不依赖邻域像素，因此天然无 halo。

文章结尾批评了游戏渲染过度依赖电影视觉语言，呼吁开发属于虚拟世界自己的工具。

## 关键要点

- 游戏 bloom 和曝光适应是亮度感知的工具，与摄影中的"镜头缺陷"不是同一回事
- 局部 TM 的本质是对图像做光照/反射率的 intrinsic image 分解（Retinex 理论）
- 渲染器已有的 illuminance pass 可以直接利用，无需邻域滤波
- 局部 TM 应在低空间频率操作，保留高频细节，边缘保持滤波（bilateral、local laplacian）是实现此目的的一种方式
- 适当的曝光自适应应参考全局光照标记（light probe），而非 screen-space 平均亮度

## 链接到的概念

- [[local-tonemapping]]
- [[exposure-fusion]]
- [[filmic-post-processing-critique]]
- [[physically-based-shading]]

## 原文

- 链接：https://c0de517e.blogspot.com/2016/09/tone-mapping-local-adaption.html
- 本地：`raw/articles/c0de517e.blogspot.com/2016-09-11_tone-mapping-local-adaption.md`
