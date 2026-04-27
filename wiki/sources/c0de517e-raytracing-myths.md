---
tags: [source, rendering, raytracing, rasterization, algorithms]
date: 2026-04-27
sources: 1
---

# Raytracing Myths（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2011 年 9 月的文章，回应一篇声称"光栅化的并行性远不及光线追踪"的 blog post，系统拆解光线追踪对光栅化的常见算法优越性神话。

## 摘要

文章通过对比两种算法的伪代码骨架，指出它们本质上是**对同一双重循环的不同遍历顺序**，由此产生对偶的内存与复杂度权衡。光线追踪的"O(log N)"复杂度论断在等价实现条件下也适用于光栅化（层次化 z-buffer + 遮挡剔除）；光线追踪"易于并行"的论断在加入加速结构和着色后崩塌，因为 BVH 遍历导致发散。文章最终把二者类比为静态 vs 动态类型语言：均图灵完备，从各自端点向对方靠近，不存在普遍胜者。

## 关键要点

- 两种算法的核心差异：外层循环（像素 vs 图元）颠倒，内存占用呈对偶（z-buffer vs 场景图元驻留）
- BVH 加速的对数复杂度可以等价地用层次化 z-buffer 给光栅化实现
- 动态场景下 BVH 重建成本抹平理论优势
- 光线追踪"并行性"神话：加入加速结构后相邻光线发散严重（不同层深度），SIMD 效率骤降
- 离线渲染（2011 年）：Pixar Renderman 仍以 REYES 光栅化器为主体，光线追踪是混合的一部分
- 实时光线追踪短期不可能取代光栅化，但二者最终走向混合管线
- 文章评论区有关于 primitive count scaling、power consumption、progressive refinement 的延伸讨论，提供了更丰富的视角

## 链接到的概念

- [[raytracing-vs-rasterization]]
- [[rasterization]]
- [[hierarchical-z-buffer]]
- [[culling]]
- [[path-tracing-basics]]

## 原文

- 链接：https://c0de517e.blogspot.com/2011/09/raytracing-myths.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-09-19_raytracing-myths.md`
