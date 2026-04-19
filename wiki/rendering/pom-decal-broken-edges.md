---
tags: [渲染, decal, 视差遮挡贴图, cyberpunk, 边缘破碎]
date: 2026-04-14
sources: 1
---

# POM Decal 破碎混凝土墙边（Cyberpunk 2077: Phantom Liberty）

**《Cyberpunk 2077: Phantom Liberty》** 里有一面混凝土墙，边缘看起来被砸出不规则的碎石凹陷，沟壑里露出粗糙骨料。直觉告诉你这是一个独特的 mesh 加一张手绘贴图，但事实是 **一个简单的倒角盒子 + 一堆 decal**。Simon 拆解这一帧时揭开了 CDPR 的分层做法，正好可以看作 [[normal-decal-edge-blending|Fallout 3 边缘 decal]] 技法的现代 PBR 版本。

## 分层结构

从下往上一共四层：

1. **底层几何**——一面倒角 (chamfered) 的方盒子做墙体，轮廓是直线。
2. **Overlap mesh**——一块独立的、详细凿痕形状的 mesh 被「扎进」墙体里。因为它使用了 3 种不同材质，所以渲染时拆成 **3 次 draw call**（Simon 通过 wireframe 的 fade-in 看出了这点）。
3. **修补 decal**——overlap mesh 与墙体的交线很刺眼，CDPR 在交界处先盖一张修补 decal，但效果仍然不够。
4. **POM decal**——再在顶部盖一层视差遮挡贴图的 decal，这层才是魔法：它让两种几何的接缝融合成一整片凹凸的石头。

## 为什么是 POM 而不是真几何

POM decal 的关键数据是一张灰度高度图，pixel shader 里做 **ray-marching** 沿着视线推入表面，读出一个 UV 偏移来伪造深度。相比直接建凹凸几何，POM 的优势是：

- **一张平面 decal 投影到任意表面** 都能贴合——墙、柱子、地面复用同一个资产
- **几何预算 0**，省 vertex shader 和 overdraw 的顶点成本
- **可以用 alpha 做柔和渐变**，让 decal 边缘自然融入周围

代价是，POM 只在法线方向有深度，极端掠射角会出现「游泳」（POM swimming）。CDPR 的应对方式是把步数做成 **与角度相关**：当视角与表面夹角变平时把步数降到很低、甚至直接关闭效果。Simon 注意到在远处和极端角度下 POM 的深度会「被压平」，Tech Art Aid 的 Oskar Świerad 在 Bluesky 上确认：**步数随角度可变** 确实是优化的代价，既节省 ALU 又避免 swimming 伪影。

## 从 Fallout 3 到 Phantom Liberty 的谱系

Simon 自己把这篇和 [[normal-decal-edge-blending|Fallout 3 — Edges]] 连在一起。两者都是 **用 decal 盖住低多边形的直线廓**，区别在于：

- Fallout 3 的 decal 只是 **一层带 alpha 的 normal map**，不改变 silhouette，破碎感靠边缘几何本身（见原文）
- Phantom Liberty 把 decal 升级成 **POM**，让 decal 在 pixel shader 里伪造 silhouette 切入
- 再早一些的 CryEngine 文档里已经有同样的思路（往被破坏建筑的硬边塞 decal）

三代技术都在回答同一个问题：**如何用最少几何做出「这块墙被敲碎过」的视觉冲击**。POM 让答案更接近一张贴纸。

## 相关

- [[normal-decal-edge-blending]] — Fallout 3 的同族边缘 decal 做法
- [[parallax-corrected-cubemap]] — 同属「用 shader 伪造几何」家族的另一招
- [[tangent-space-normal-mapping]] — decal 本身仍然是切线空间的 normal map + heightmap

## Sources

- [[sources/simonschreibt-cyberpunk-broken-edges]]
