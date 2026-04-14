---
tags: [渲染, lod, alpha, 优化]
date: 2026-04-14
sources: 1
---

# Fizzle / Checkerboard LOD Fading

**一种把 LOD 级别之间的切换「藏在噪声里」的 fading 技术**，常见别名 fizzle、checkerboard fade、dither fade。核心做法是把两个相邻 LOD 的网格**同时提交**，每个 LOD 在像素着色器里用一张伪随机纹理 + 一个阈值做 `discard`，让两个 LOD 的「未被 discard 的像素」恰好互补。远处看上去像一个普通的 crossfade，近处看是密集的棋盘格噪点。

## 为什么不用 alpha blending

直觉上 LOD fade 应该用 alpha blending——平滑地把一个模型淡入、另一个模型淡出。但在现代延迟渲染管线里，alpha blending 有一堆致命缺点：

- **破坏 [[early-z-late-z|early-z pre-pass]]**：alpha blended 物体不能写深度 buffer，拿不到 pre-pass 的加速。fizzle 物体本质上是不透明的，pre-pass 正常工作。
- **要双份 shader**：[[deferred-rendering|deferred renderer]] 里不透明物体的 shader 不做光照，如果切换成 transparent 版本必须单独再写一套会做光照的 shader——而且两者结果要完全一致才不 pop，非常难。
- **overdraw 放大**：alpha blending 会让 fragment 数量翻倍甚至更多，在带宽瓶颈的场景下代价不可接受。
- **z-fighting**：两个 LOD 位置几乎完全重合，浮点精度会让它们互相穿插闪烁，需要额外 bias 才能稳定。
- **断掉后续深度 pass**：SSAO、SSR 等都依赖深度 buffer。如果 transparent 物体在 AO pass 之后渲染，它们就不会被 AO 考虑进去。

fizzle 用**空间噪声**替代了时间 blending，把这些问题一次性绕开——所有东西都是不透明的、都写深度、都有 early-z 加速、都进入 pre-pass、都参与 SSAO。

## 噪声的来源

实现上需要一张伪随机纹理（或者一个确定性 hash 函数），每个像素根据屏幕坐标（或世界坐标）采样一个值，和 `fadeThreshold` 比较，低于阈值就 `discard`。调整 threshold 就能控制 fade 进度。

Rise of the Tomb Raider 里的例子很直接：一辆远处的卡车同时提交了两个 LOD（182k 顶点 和 47k 顶点），一个在淡出一个在淡入，屏幕上两者各取一半像素。远处几乎看不出差别，而成本已经从 LOD0 转移到 LOD1。

## 缺点：噪声可见

fizzle 最大的槽点是近距离下能看到颗粒感。解决方案：

- **post-fizzle blur**：对噪声区域做一点模糊掩盖
- **temporal AA 掩盖**：[[temporal-antialiasing|TAA]] 的 accumulation 正好把 fizzle 噪声滤成时间上的平均，肉眼看不出来——这是 TAA 意外的副作用收益
- **蓝噪分布**：用低差异序列（blue noise）代替纯白噪声，让噪点在感知上更均匀

好的噪声 pattern + TAA 是现代游戏的标准组合。

## 相关

- [[early-z-late-z]]
- [[alpha-blending]]
- [[deferred-rendering]]
- [[temporal-antialiasing]]
- [[overdraw]]
- [[z-fighting]]
- [[texture-dissolve]] —— 同样基于 `clip`，但是面向可见的 VFX 演出，不是 LOD 切换
- [[dither-alpha-clipping]] —— 同样用 `clip(col.a - threshold)` 的技术在 Bayer 矩阵上的通用版本
- [[normal-decal-edge-blending]] —— Fallout 3 的做法：直接在 LOD 里把 decal 壳删掉，作为最简单也最有效的 LOD 策略

## Sources

- [[sources/elopezr-rotr-rendering]]
