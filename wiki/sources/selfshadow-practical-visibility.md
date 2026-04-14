---
tags: [source, 渲染, 可见性, 剔除, 性能]
date: 2026-04-14
sources: 1
---

# Practical, Dynamic Visibility for Games（Stephen Hill & Daniel Collin）

[[stephen-hill|Stephen Hill]] 和 Daniel Collin（DICE / Frostbite）2011 年发表于 selfshadow.com 的长文，把**两个在同一时期、不同平台、不同硬件哲学、但都已经在 AAA 游戏里出货**的动态 visibility 方案并列呈现：Ubisoft Montreal *Splinter Cell: Conviction* 的 GPU 侧 HZB 查询系统，和 DICE *Battlefield: Bad Company 1/2* 的 SPU 软件光栅遮挡系统。

## 摘要

文章先分析为什么 Static PVS / Portals / Anti-portals 不再够用——它们都无法处理完全动态场景，或者被室内走廊门窗所限；然后指出 **Hardware Occlusion Queries (OQ)** 看起来万能、但实战中被延迟、popping、无法 batch、成本与屏占正相关等问题拖累。

**Conviction 方案**把占用 GPU 零碎时间的 [[hierarchical-z-buffer|HZB]] 用作剔除查询结构。具体流程：第一步渲染艺术家标注的 occluder 的深度到 512×256 的 render target；第二步生成 max-downsample mip 金字塔；第三步把每个物体的 world AABB 投影成屏幕矩形和 min depth，在合适的 mip level 上取 4（或 4×4）个 corner texel 做 max，用 `min_z > max_z` 判遮挡；第四步通过 memexport 把 1/0 结果回读 CPU。22000 个物体一帧总开销 **0.52 ms**（Xbox 360），**与物体屏占无关**——这是它优于 OQ 的关键。

同一系统被扩展成**shadow caster culling**：两轮 HZB 查询，第一轮在 light space 剔 caster，第二轮把 caster 的 active shaft bounds 变换到 camera space 再用主相机 HZB 剔一次。纯 GPU 查询，不需要 shadow volume。

**Battlefield 方案**选了另一条路：把 occluder 低模送到 SPU 上，每个 SPU 维护 256×114 的本地 z-buffer 做软件光栅化，最后用 mutex 串行合并；典型场景 5 SPU 并行约 **2.3 ms** 完成 6000 occluder triangle 和 3000 occludee 测试。好处是完全不占 GPU、CPU 侧直接拿到结果可以用来跳过动画 / 骨骼 / AI 更新。

文章最后讨论了艺术家手绘 occluder 的工程痛点（与视觉几何失同步、scope mode 下被放大）、对 min-max 双向 HZB 的展望，以及 GPU-driven visibility 的未来。

## 关键要点

- **OQ 的五大痛点**：无法 batch、延迟 / 同步、popping、GPU overhead、成本和屏占正相关。
- **HZB 查询解决前四点并拉平第五点**：固定成本、逐物体粒度、能顺手挂 contribution cull / LOD / texture streaming / shadow caster cull。
- **两方案的硬件哲学差异**：PS3 CPU 富余 ⇒ SPU 软光栅；Xbox 360 GPU 富余 ⇒ GPU HZB。今天 GPU-driven 路径是两者结合的自然演化。
- **艺术家手绘 occluder 不可靠**：更稳的路是自动从视觉几何合并 / 简化。
- **bounds 几乎不变的 occludee 是 HZB 的短板**：屏占大的大结构会被单一 min_z 保守接受；proof of concept 是直接硬件栅格化 occludee bounds，但没落地。

## 链接到的概念

- [[occlusion-culling]]
- [[hierarchical-z-buffer]]
- [[culling]]
- [[cached-shadowmaps]]
- [[stephen-hill]]

## 原文

- 链接：https://blog.selfshadow.com/publications/practical-visibility/
- 本地：`raw/articles/blog.selfshadow.com/2011-09-22_practical-dynamic-visibility-for-games.md`
