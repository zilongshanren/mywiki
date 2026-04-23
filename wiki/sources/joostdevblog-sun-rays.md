---
tags: [source, rendering, light-shafts, god-rays, screen-space, post-process]
date: 2026-04-19
sources: 1
---

# Sun rays（Joost van Dongen / Joost's Dev Blog）

[[joost-van-dongen]] 2010 年 11 月发表的文章，讲 *Proun* 第三赛道里加的 god rays / light shafts 效果，以及他为什么把这个 shader 当成「shader 创意美学」的最好样本。

## 摘要

真正的体积光要求 ray-march + 每采样点查 shadow + 查密度场，2010 年的硬件跑不起。GPU Gems 3 第 13 章给出一个**几乎零物理**的替代：从当前像素出发、沿屏幕空间走一条朝向太阳投影点的 2D 直线，按距离衰减累加沿路的图像亮度，就得到体积光的视觉效果。Far Cry 2、Crysis 都用这种做法。van Dongen 把它接到 *Proun* 第三赛道。**硬约束：太阳必须在屏幕里可见**——屏外 / 背向光源完全失效。他借这个例子自白：shader 对他的吸引力不是 low-level 优化（他不喜欢），而是「物理被简化到没意义时，只能靠创意和实验」——这是他写 shader 的精神核心。

## 关键要点

- 物理正解：ray-march + 体积内 shadow sampling，离线都吃力
- 屏幕空间近似：像素 → 太阳投影点走直线，采样图像亮度累加，忽略密度 / shadow / 散射
- 硬约束：太阳必须在屏幕内
- 不适合：手电筒 / 室内聚光 / 背向相机的光源
- 作者哲学：shader 是「物理没用、创意和实验才算数」的游戏
- 出处：GPU Gems 3 第 13 章

## 链接到的概念

- [[screen-space-light-shafts]]
- [[volumetric-raymarching-intro]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2010/11/sun-rays.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2010-11-13_sun-rays.md`
