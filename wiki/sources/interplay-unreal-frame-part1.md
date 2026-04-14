---
tags: [source, rendering, unreal, frame-breakdown, occlusion-culling, shadow-map]
date: 2026-04-14
sources: 1
---

# How Unreal Renders a Frame（Part 1，Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 2017 年 10 月发表的 *How Unreal Renders a Frame* 系列第一篇。作者用 [[renderdoc|RenderDoc]] 抓取 UE4.17.1 编辑器里一个典型场景的一帧，对照引擎源码逐 render pass 分析其默认 deferred 管线。

## 摘要

Part 1 覆盖从帧首到 shadow map 生成的前半段：**ParticleSimulation**（GPU 粒子写 position/velocity RT，此时尚无深度故带碰撞的粒子后面再跑一次）、**PrePass** Z-prepass（reverse-Z 约定，近=1 远=0，由 DBuffer decal 触发）、**BeginOcclusionTests**（硬件 occlusion query 做 visibility，分 Individual 和 Grouped 两级——grouped 用上一帧判死的道具 AABB union，一旦整体可见再拆回 individual，从而削 8 倍 query 数）、**HZB SetupMipXX**（用 R16F min 降采样建 Hi-Z mip chain）、**ShadowDepths**（directional 光走 3×1 cascade atlas、null PS 写 depth 翻倍；stationary local light 对 dynamic 道具走 per-object shadow map atlas；movable local light 走 cubemap + shadow map caching，geometry shader 一次写 6 面）。文章也指出一个实践坑：stationary light 必须先 bake 再 profile，否则引擎会当 movable 走。

## 关键要点

- 默认用 **reverse-Z** 提高远处精度。
- Occlusion query 用「individual + grouped 合并」两级降 query 数。
- Query 结果延后若干帧读（避免 CPU-GPU 同步点），代价是 popping。
- Hi-Z 金字塔由 min 降采样（因 reverse-Z）。
- Directional light 的 cascade shadow map 整帧清空，不做 staggered split update。
- Stationary + dynamic prop 用 per-object shadow map atlas；Static light 完全烘焙进 lightmap，不出现在 draw-call list。
- Movable light 的 cubemap shadow 对静态部分做 caching，dynamic 道具只叠加增量。

## 链接到的概念

- [[unreal-frame-breakdown]]
- [[deferred-rendering]]
- [[occlusion-culling]]
- [[hierarchical-z-buffer]]
- [[shadow-mapping-basics]]
- [[cached-shadowmaps]]

## 原文

- 链接：<https://interplayoflight.wordpress.com/2017/10/25/how-unreal-renders-a-frame/>
- 本地：`raw/articles/interplayoflight.wordpress.com/2017-10-25_how-unreal-renders-a-frame.md`
