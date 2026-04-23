---
tags: [渲染, 阴影, 优化, gpu]
date: 2026-04-14
sources: 1
---

# Cached Cascaded Shadowmaps（级联阴影贴图缓存）

**核心想法**：对于[级联阴影贴图（Cascaded Shadow Maps, CSM）](https://en.wikipedia.org/wiki/Shadow_mapping)中**远距离的级联**，大部分投射者都是静态的，视角变化也缓慢——**没必要每帧从零重绘**。把远级联的结果缓存下来，只为动态投射者做增量更新，就能省掉可观的阴影生成时间和带宽。

## 动机：阴影成本不对称

一帧里渲染多个阴影级联（通常 3-5 层）时，远级联覆盖范围大、投射者多，但投影到屏幕上像素密度低。相机/光源每帧移动不大时，大部分远级联的内容几乎和上一帧一致，重绘等于在反复做同一件事。

## Pesce 的「bad idea sketch」

2011 年 [[angelo-pesce]] 在博客上抛出一个半成品的想法：把远级联分帧更新——比如 5 个级联里，每一帧更新最近的第一层，加上剩余 4 层里的两层。他的团队当时正想优化一款游戏的 GPU，观察到 Crysis 2 似乎有类似行为。

他们的实验结论是：

- **纯分帧更新**有问题——动态投射者会「走进自己的旧阴影」，暴露缓存延迟。
- **改进方案**是缓存**静态投射者**，每帧只重绘动态的。
- 但在当时他们的 shadowmap 尺寸下，**阴影生成时间有一半花在 bandwidth 和 resolve 上**，缓存静态几何并没带来净收益。

Pesce 据此放弃了继续深挖，但仍在想：换更大/更小的 shadowmap、换主机世代，这个方案到底什么条件下会变划算？

## Mike Day 的完整实现（2012）

2012 年 SIGGRAPH 上，Insomniac Games 的 **Mike Day**（paper 由 [Mike Acton](https://www.insomniacgames.com/mike-day-siggraph-2012-csm-scrolling/) 代为展示）公开了一个非常详细的实现：

- **Reprojection**：把上一帧缓存的阴影同时在 **UV 空间和深度空间重新投影**，对准本帧的光源矩阵。
- **Dynamic splat**：然后把当帧的动态投射者「splat」到重投影后的缓存上。

这份工作给出了完整的数学与实现细节，相当于把 Pesce 那个「bad sketch」补成了工程可落地的方案。

## 未走完的优化方向

Pesce 在博客里提到他当时还在想另一些更激进的省带宽办法，但都因为「worst case 并没有改变」而没做下去：

- 用 **stencil** 标记每个区域实际用到的 z-near / z-far 范围（在 360/PS3 上可以利用 stencil 与 depth 的联合采样特性，但 DX9 上不行）。
- 其它一些 hack，复杂度高而收益不稳定。

这段经验也是一个典型的「带宽瓶颈压住算法创新」案例：当你在 [[rendering-pipeline|管线]]的某一步已经 bandwidth-bound 时，为了省计算而引入的任何算法复杂度，只要不能同步减少带宽，就都是无效优化（见 [[bottleneck-analysis]]）。

## 与其它阴影优化的关系

- 与 [[culling|culling]] 互补：culling 减少**每帧**的投射者数量；caching 减少**多帧**之间的重复工作。
- 与 temporal 重投影思路相同血缘：把「时间相干性」当成一种可压缩的信号。
- 现代引擎里类似思想演化成了 virtual shadow maps（UE5 Nanite shadows）——同样是「只重绘变化部分」，但粒度更细、做在 page 级别上。

## 相关
- [[angelo-pesce]]
- [[rendering-pipeline]]
- [[bottleneck-analysis]]
- [[culling]]
- [[z-buffer]]
- [[stencil-buffer]]
- [[shadow-mapping-basics]] — shadow mapping 的基础流程（hard / soft / Phong）
- [[occlusion-culling]] —— Conviction 的 HZB shadow caster culling 是另一种阴影优化思路
- [[cascaded-shadow-maps]] —— 可与级联缓存策略组合的基线

## Sources

- [[sources/c0de517e-cached-shadowmaps]]
