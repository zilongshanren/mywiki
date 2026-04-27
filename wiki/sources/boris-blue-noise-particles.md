---
tags: [source, procedural-generation, blue-noise, sampling]
date: 2026-04-27
sources: 1
---

# Blue Noise Particles（Boris The Brave）

[[people/boris-the-brave]] 发表于 2017 年 5 月的短文，介绍其为 Blender 发布的蓝噪声粒子插件。

## 摘要

Boris 发布了一个 Blender 插件，能够生成具有**蓝噪声（Blue Noise）**分布的粒子排列。蓝噪声分布等同于**泊松磁盘采样（Poisson Disk Sampling）**，其关键保证是任意两个粒子之间不会过于靠近。与均匀随机分布相比，蓝噪声排列更具视觉"有机感"，适用于自然物体散布（如植被、石块）以及网格的随机非碰撞放置。文章内容极为简短，仅为发布公告性质。

## 关键要点

- 蓝噪声分布 = 泊松磁盘采样，保证最小间距
- 比 Blender 默认均匀采样在视觉上更自然
- 特别适合有机排列与无碰撞网格摆放

## 链接到的概念

- [[poisson-disk-sampling]]

## 原文

- 链接：https://www.boristhebrave.com/2017/05/14/blue-noise-particles/
- 本地：`raw/articles/boristhebrave.com/2017-05-14_blue-noise-particles.md`
