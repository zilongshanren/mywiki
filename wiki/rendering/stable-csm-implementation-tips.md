---
tags: [rendering, shadows, csm, stable-csm, optimization]
date: 2026-04-19
sources: 1
---

# Stable CSM 实施要点（Pesce 2011 笔记）

**Stable cascade** 的本质：把整个世界看作一张无限大的纹理，每帧在这张纹理上截取一个固定大小的窗口——窗口**必须整像素滑动**，不然世界坐标到 shadow texel 的对应关系会抖，导致阴影边缘「爬行」。窗口尺寸一般用视锥外接球的半径决定，这样无论相机朝哪儿转都装得下。

[[angelo-pesce]] 在 2011 年的笔记里把实践中绕不开的工程点列了一遍，这些要点多数至今仍然适用。

## 级联的封装与分发

- **Deferred shadow buffer**——把所有级联的可见性结果打进一张屏幕空间 mask，再在主光照 pass 里采样。这样可以**一次只处理一个级联**，天然允许级联间淡入淡出、半分辨率 + bilateral 上采样等优化，还能用 hi-stencil / hi-z / depth range 做区域剪除。
- **按「最优级联」采样而非按视锥切分平面**——每个像素用能覆盖它的**最高分辨率**那一级，而不是严格按 frustum split 走。Microsoft 的 CSM 白皮书就是这套。代价是淡入淡出稍微麻烦一点，收益是高分级联不会在相机斜视光源时被浪费。
- **剔除不要做一半**——远级联可以用 scissor / clip plane 跳过已经被近级联完整覆盖的几何，但前提是「最优级联」策略成立；否则近级联里的物体仍然需要把阴影投到远级联里（评论里 Dark Helmet 提出的反例：光向与视向平行时的 corner case）。

## Pancake（近平面挤压）

为了让每级联的 z 范围尽可能贴紧内容，常用做法是把光空间近平面压到视锥最近点。但这会**剪掉近平面前方的投射者**，让它们自己的自阴影穿帮。

**工程对策**：在顶点着色器里把 `z` 夹到近平面而不是靠硬件裁剪——正交投影下这只是把被挤平的物体贴到近平面，不影响它投射的阴影；但**它自身的自阴影会失真**，所以近平面前要留一小段缓冲区。副作用是 hi-z 不再能 reject 被压平的几何，raster 压力上升——可以用 stencil 或 hi-stencil 把这些「被 pancake 过」的像素标记出来单独处理。

## 贴图打包

不要把光空间视锥后方的空白区域也渲染进去——把 shadowmap 的有效区域挤到视锥前方（见 [[the-witness]] 与 Sebastian Sylvan 2010 的笔记）。如果双深度填充（double-depth fill）在你的硬件上没什么加速，也可以把两张 shadowmap 打进一张双通道 16-bit target。

## Crysis 2 观察与分帧更新

Pesce 拿 Crysis 2 做了一次「rendering archeology」：deferred shadow buffer、环形 PCF、光空间 dither、级联不做淡入淡出——**远级联每隔一帧才更新**。

他据此推理出两条实现路径：

1. **粗暴分帧**——给远级联的窗口加一点 padding，相机转动产生的位移在 padding 内就不重渲染。简单，但动态投射者会「走进自己的旧阴影」。
2. **增量更新**——上一帧已经渲染过绝大多数 texel 了，只需要把原点偏移 + wrap，边界处渲染一小圈新数据即可。要做得正确还需要考虑 near/far 范围每帧会变（最大化分辨率的代价），以及动态物体需要单独缓冲或 splat 回来。

这条「增量更新」思路直到 2012 年 Mike Day 在 SIGGRAPH 上给出完整实现才真正落地（在 UV 和深度上同时 reproject，再把动态投射者 splat 到 cache）——见 [[cached-shadowmaps]]。Pesce 这篇是那条实现链的**最上游 sketch**。

## 评论区：SDSM 作为替代方向

评论者还提醒了 Sample Distribution Shadow Maps：用 compute（Cuda/OpenCL/DirectCompute）扫 z-buffer 推导最紧的级联范围。这是另一条正交的优化路线——不是缓存时间相干性，而是让每帧的级联范围都「长得正好」。

## 相关
- [[cached-shadowmaps]] —— Pesce 2012 service update + Mike Day 的完整实现
- [[cascaded-shadow-maps]] —— CSM 基础
- [[shadow-mapping-basics]]
- [[camera-relative-sun-shadows]]
- [[shadow-caster-culling-front-back]]
- [[angelo-pesce]]

## Sources

- [[sources/c0de517e-stable-csm-ideas]]
