---
tags: [source, rendering, screen-space-reflections, taa, reprojection, stingray]
date: 2026-04-19
sources: 1
---

# Reprojecting Reflections（Jean-Philippe Guertin, Stingray）

Bitsquid / Stingray 博客 2017-06-22，作者 **Jp（Jean-Philippe Guertin）**。讲 Stingray 的 [[screenspace-reflections|SSR]] 在开启 [[taa|TAA]] 时，如何把上一帧的反射结果重投影到本帧。

## 摘要

SSR 与 TAA 结合时最烦的问题：反射是视角相关的，直接用当前像素的 motion vector 把历史帧拉过来，会让镜面在相机移动时"拖尾"。Jp 先画了一张严格的几何图，列出把 v0 处反射重投影的十步：取入射点 surface motion vector → 反向得到上一帧入射点 v1 → 同样在反射点 p0 处做一次 motion vector 反查得到 p1 → 用上一帧视矩阵重建 v1 处法线 n1 → 把相机位置与 p1 投影到 n1/v1 平面 → 求出上一帧反射点 r，用上一帧 view-projection 采样历史反射 buffer。作者把这套塞进 Stingray 后（需要新增 history depth buffer），相机运动下的 ghosting 显著下降。

但精确法代价不小：要存 history depth 和上一帧 view 矩阵，还要做两次 motion-vector 反查。Jp 后续改成更务实的启发式——在几个候选 reprojection 向量中挑幅度最小的那个：ray incidence 处 motion vector、ray intersection 处 motion vector、以及参考 Frostbite *Stochastic SSR*（Stachowiak, Siggraph 2015）对两者做 parallax 修正后的版本。`parallax_velocity = velocity * saturate(1 - total_ray_length * PARALLAX_FACTOR)`——PARALLAX_FACTOR 需要手调，这是该启发式的弱点。

## 关键要点

- **SSR 在 TAA 下是双重噩梦**：法线贴图的高频会让反射命中点逐帧跳，neighborhood clamping 又会因 clip 太狠而闪烁。重投影是解决前两个的前提。
- **正确的重投影是几何题**：反射点 p1 在上一帧并不位于 v1 - reflect(viewVec, n1) 的方向上，因为相机也动了——必须先把相机和 p1 一起投到 v1 的切平面上再做相似三角形。
- **启发式折中**：取候选 MV 里幅度最小者近似等价于"最没动的那个才最可信"，对多条 ray 的情形还可以把所有成功重投影向量加权平均。
- **参考 Frostbite 的 parallax-corrected MV**：随 ray 长度线性削弱原 MV，是对"深层反射其实近似静止"的几何直觉编码。

## 链接到的概念

- [[reprojected-planar-reflection]]
- [[screenspace-reflections]]
- [[taa]]

## 原文

- 链接：https://bitsquid.blogspot.com/2017/06/reprojecting-reflections_22.html
- 本地：`raw/articles/bitsquid.blogspot.com/2017-06-22_reprojecting-reflections.md`
