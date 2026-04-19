---
tags: [source, graphics, stencil, reflection, game-art-tricks]
date: 2026-04-19
sources: 1
---

# Sims 4 Mirrors（Simon Trümpler）

[[simon-trumpler]] 2025 年 3 月的短篇 breakdown。他在 Sims 4 里抓帧，看游戏如何实现「可以真实反射房间」的镜子——因为每个镜子需要**再渲染一次房间**，而一户人家常有多面镜子，性能势必压力很大。作者好奇的是：**culling 和 stencil mask 是怎么把每面镜子的可见几何精确分隔的？**

## 摘要

关键观察：

1. **远距离 fallback**——镜子距离玩家远时只显示**静态贴图**，不做真实反射，靠近再淡入切换。
2. **每面镜子一次独立重绘**——这是平面镜的传统做法（[[parallax-corrected-cubemap]] 等近似在 Sims 这种室内几何完整的场景里不适用）。
3. **Culling 极其干净**——作者在 profiler 里让 floor 渲染失败（bug 副作用），结果看到「镜像空间」里的房间已经被精确 cull，几乎没画多余物体，甚至笔记本屏幕内容都在外面被 cull 了。
4. **Stencil buffer 辨识每面镜子**——profiling 抓到 3 个独立 stencil buffer（ref 2、3、4），作者推测每面镜子先渲自己的 mask，再用对应 mask 约束几何渲染。

工程链条大致是：

```
for each mirror:
    1. 用镜子表面写一次 stencil（每面镜子分配不同 stencil ID）
    2. 基于镜子位置做 oblique 投影，把相机「翻到镜后」
    3. cull 镜像空间里可见的几何
    4. 在 stencil 通过的像素上渲染几何
```

最精巧的细节是 **shower pixelation 效果也只在镜子区域内部限制**——也就是说像素化后处理的 mask 也按 stencil 剪裁，保持了「镜里的世界遵守同样规则」的逻辑一致。

## 关键要点

- **镜子是每帧每面一次额外 rendering pass**——数量直接乘倍 GPU 负载；LOD + 静态贴图 fallback 是必要优化。
- **Stencil ID 是隔离多面镜子的关键**——和 [[stencil-portal-shader-antichamber]] 的思路完全一致，只是这里是镜面反射 portal 不是空间 portal。
- **culling 要对镜像相机独立做一遍**——作者在 profile 里看到的 clean culling 正是这一步高质量实现的证据；如果偷懒用主相机 frustum，会渲染一堆看不见的东西。
- **post-process mask 跟随 stencil**——像素化、粒子等效果必须都知道当前是在「镜子内还是外」，否则反射会露馅。

## 链接到的概念

- [[planar-mirror-rendering]]
- [[stencil-portal-shader-antichamber]]
- [[stencil-buffer]]

## 原文

- 链接：https://simonschreibt.de/gat/sims-4-mirrors/
- 本地：`raw/articles/simonschreibt.de/2025-03-28_simonschreibt.md`
