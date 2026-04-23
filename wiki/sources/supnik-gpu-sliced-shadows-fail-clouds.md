---
tags: [source, rendering, 体积阴影, 粒子系统, 飞行模拟, X-Plane]
date: 2026-04-19
sources: 1
---

# Why GPU Sliced Shadows Fail For Clouds（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2010 年 10 月发表的一篇工程笔记，讲 X-Plane 团队为什么把 NVIDIA *Smoke Particles* 白皮书推的 **sliced shadow** 算法从体积云的候选方案里划掉。

## 摘要

NVIDIA 白皮书把 sliced shadow 的 ideal input 假设为"**大量、偏半透明的粒子，不做空间分桶**"。真实飞行模拟云的工程约束恰好全部反着来：为了省 fill-rate 用**少量偏不透明**的粒子、为了剔远云必须做**空间分桶**，外加每加一片就要 rasterize-to-texture 再 sample-from-texture 的**驱动开销**，把可用切片数压到每桶 8 片都勉强。低切片数会让阴影变硬、相机旋转时粒子间阴影关系 popping、太阳穿过相机前后那一刻 front-to-back / back-to-front 排序切换导致切片方向整体 90° 翻转，产生大面积阴影跳变。

核心教训是**读 GPU 白皮书的隐含前提**：算法的性能曲线是在作者选定的输入分布下写出来的，脱离这个分布每个弱点都会暴露。

## 关键要点

- sliced shadow 依赖"单个粒子不够黑"来让自阴影柔和——没有主动控制自遮挡强度的机制；
- 粒子偏不透明时相邻粒子就会互相投很黑的阴影；
- 分桶 + slicing 互相争用切平面，推荐的 32–128 片在分桶后不可达；
- 切片数少 → popping；最坏是太阳在相机前/后翻转那一瞬间，切片方向 90° 翻。

## 链接到的概念

- [[gpu-sliced-volumetric-shadows-limits]]
- [[cloudscape-sdf-volumetric]]
- [[volumetric-cloud-quarter-res-upsample]]
- [[alpha-blending-front-to-back]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/10/why-gpu-sliced-shadows-fail-for-clouds.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-10-08_why-gpu-sliced-shadows-fail-for-clouds.md`
