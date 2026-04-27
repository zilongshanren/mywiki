---
tags: [渲染管线, forward, deferred, visibility-buffer, 分类学]
date: 2026-04-27
sources: 1
---

# 实时渲染管线分类学

**实时渲染管线的所有变体都是同一条流水线在不同位置被"切断"的结果**。[[people/angelo-pesce]] 在 2016 年提出这个统一框架，把 Forward、Deferred、[[visibility-buffer|Visibility Buffer]]、Texture-Space Shading 纳入同一个连续体，用"切断位置"和"切断后的通信数据结构"来解释它们的差异与权衡。

## 统一视角：切断点

把从顶点属性到最终像素颜色的完整计算链想象成一根绳子。任何"延迟"技术都是把这根绳子切断，把切断处的数据写到内存（G-buffer / visibility buffer / UV-space texture），然后在第二 pass 读回来继续计算。每次切断都带来相同的四种潜在收益：

1. **专化（Specialization）**：第二 pass 可以按数据特征分派不同的特化 shader
2. **线程间数据共享**：切断后可以跨像素、跨 tile 访问第一 pass 写入的数据
3. **计算重排布（wave efficiency）**：第二 pass 可以用不同的线程拓扑（如 CS tiles）替代光栅化的三角形 wave
4. **注入中间计算**：在两个 pass 之间可以插入修改数据的逻辑（如屏幕空间 decal、SSAO）

## 主要变体

### Forward 渲染

不切断，单 pass 从几何直达像素颜色。光源分配问题（哪个 draw call 受哪些光照）成为核心挑战：

- **Multi-pass Forward**：每个光源单独跑一次 draw，结果叠加。光源数量线性增加 draw call
- **Single-pass Forward（uber-shader）**：动态分支处理所有光源，shader 排列组合爆炸
- **Forward+（Tiled/Clustered）**：把光源存入屏幕空间 Tile 或视锥 Voxel，shader 动态遍历——代价是必须接受 ubershader 的动态分支，但光源剔除效率高

### Deferred Shading

在纹理/材质采样之后切断，写出完整的 G-buffer（albedo、法线、roughness 等），第二 pass 做光照。见 [[deferred-rendering]]。

- 擅长：大量动态光源、screen-space 效果（SSAO、SSR、decal）
- 弱点：G-buffer 带宽、MSAA 昂贵、透明物体必须另开 forward pass

### Visibility Buffer（细节见 [[visibility-buffer]]）

在光栅化后立刻切断，只写 primitive id（instance id + triangle id），完全不做材质采样。第二 pass 由 compute shader 反查顶点缓冲、材质参数，完成 shading。

- 消除 overdraw 浪费（只对可见像素做材质 shading）
- 失去固定功能硬件优化（mipmap 导数计算困难，需要解析导数）
- 顶点/对象数据访问的空间局部性更差（按屏幕空间模式而非几何模式访问）

### Texture-Space Shading

不写屏幕空间 buffer，而是写 UV 空间纹理。类似 Quake 的 surface cache 思想，2015 年前后在业界重新被关注。

- shading rate 与屏幕帧率解耦，支持时域复用
- 不会产生 shimmering（纹素不移动）
- 代价：cache invalidation 频率与粒度难以控制，内存占用大

## 选型决策树

[[people/angelo-pesce]] 给出的经验法则（2016 年，PS4 世代）：

- **带宽优先**：先看 G-buffer 的读写是否会成为带宽瓶颈；对 1080p + 薄 G-buffer，PS4 上通常不会
- **数据访问模式**：需要大量 per-vertex 表面数据（如 fat lightmap）？Forward 更合适；需要 screen-space 效果？必须写 G-buffer
- **动态光源数量**：大量小型动态光？Forward+ 或 Deferred；少量大型静态光？单 pass Forward 仍然很快
- **波（wave）效率**：小三角形、大量 draw call 导致 partial quad 惩罚？考虑 Visibility Buffer 重排计算

混合方案——[[deferred-rendering]] 与 [[forward-plus-rendering]] 共享同一套光源数据结构——在理论上是可行的，也是 2020 年代很多引擎的实际走向。

## 相关

- [[deferred-rendering]]
- [[forward-plus-rendering]]
- [[visibility-buffer]]
- [[tiled-light-culling]]
- [[tbdr-vs-imr]]
- [[shader-permutation-explosion]]

## Sources

- [[sources/c0de517e-rendering-continuum]]
