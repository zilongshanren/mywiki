---
tags: [渲染, 光照, 阴影, 反射, sdf, 光线追踪]
date: 2026-04-14
sources: 1
---

# 稀疏阴影与 cone tracing（Sparse Shadows through Tracing）

**[[brian-karis|Brian Karis]] 2012 年 5 月在 Graphic Rants 上提出的 next-gen 渲染架构假设**：当光源数量爆炸、物理正确的 $1/d^2$ 光衰减让「影响范围」变成软概念时，单靠 shadow map 无法为所有 specular 高光提供阴影——需要让阴影从光源本身解耦出来，改用**对场景结构的 cone trace**来回答 specular 可见性的问题。

这篇博文是 [[tiled-light-culling]] 的直接续篇，也是后来 **UE5 [[lumen|Lumen]]** 架构的雏形之一。

## 起因：specular 高光的阴影怎么办

上一篇博文把 specular 高光的剔除做成了 tile 级的 cone 剔除——远处小光源能照到反光表面上的那一小块区域。但紧接着一个灵魂问题：**这些高光要不要投阴影？**

- 每个光源都做 shadow map：几百个光源都给一张阴影图在当时完全不可行。
- 完全不投阴影：墙后面的灯仍然能在角色金属腰带上反射出刺眼高光，马上穿帮。

## 核心论点：场景需要多套几何表示

> We will need geometry in similar formats as we've had in the past for efficient rasterization (vertex buffers, index buffers, displacement maps). This will be used whenever the rays are coherent ... Incoherent rays will be very important for next gen renderers but we need a different representation.

Karis 明确承认——这个观点来自 Matt Swoboda 在 GDC 2012 的 demo 演讲（directtovideo）。**一种几何表示不够**：

- **栅格化友好的 mesh**：VB + IB + displacement。用于**相干射线**（primary ray、shadow map 的 shadow ray——这些射线基本平行），硬件光栅器比其他任何算法都快。
- **trace 友好的场景表示**：用于**不相干射线**（间接 diffuse、间接 specular、远处 specular 的阴影）。更进一步，**能做 cone trace 的比只能做 ray trace 的更有用**。

Karis 列出的候选表示：

1. **[[sdf-ray-marched-shadows|Signed Distance Fields]]**（iq, Swoboda, Samaritan demo）—— 存进 volume texture 或做 clip-map stream
2. **稀疏体素八叉树 SVO**（Crassin 2011 GI Voxels）—— 见 [[virtualized-volume-textures]]
3. **Surfel trees**（Ritschel, Bunnell micro-rendering）—— 点云分层
4. **Billboard cloud trees**—— 老一代的简化
5. **屏幕空间结构**（半局部）：min/max depth mipmap（Drobot）、variance depth maps（VSM）、adaptive transparency buffer——后者只存屏幕可见部分，但对近场 cone trace 足够

## 方案：diffuse 归 shadow map，specular 归 cone trace

> **What I propose as the solution to our problem is to use traditional shadow maps only within the diffuse radius. Do a cone trace down the reflection vector. The cone trace will return a visibility function that any specular outside the range of a shadow map can cheaply use to shadow.**

光源的阴影被**按能量分成两部分**：

- **近场 diffuse + specular**：走传统 shadow map，和之前一样。范围限制在该光源的 diffuse tolerance 半径内。
- **远场 specular**：沿反射向量 $R$ 做 cone trace，得到一个 visibility 函数。所有离该光源超过 diffuse 半径但仍能在反光表面留下高光的光源，都**共享同一次 cone trace 的结果**——它只和**被着色的表面** 和**反射方向**有关，而不依赖具体是哪一个光源在提供高光。因此，所谓「每个光源都要一张 shadow map」完全不是这个问题该用的形式。

> Actually, having shadowing data independent from the lights means it can be used for culling as well. The max unoccluded ray distance can be accumulated per tile which puts a cap on the culling cone for light sources.

一个衍生好处——**cone trace 的 max unoccluded 距离可以反过来缩小 [[tiled-light-culling]] 里的剔除锥**，让被墙完全遮住的那半个 tile 不必再考虑墙外的光源。

## Epic Samaritan demo 先例

Karis 指出 Epic 自己的 Samaritan demo（2011 GDC）已经做过完全一样的事：他们对场景反射用**体积 SDF 做 reflection cone trace**，而 SDF 本身是为了 reflection 存的——reuse 做点光源的 specular 遮蔽不需要额外开销。这是他论点的存在性证明。

## 当前世代的「最粗陋的 cone trace」：SSR 的 glossy fade

Karis 同时指出——**screen space reflection 本身就是 cone trace 的最粗糙形式**。他在 Prey 2 里做的 SSR 并不是真的 cone trace，而是：

- **根据粗糙度缩短 trace 距离**
- **trace 末尾 fade out**
- 这两者合起来近似「cone 随距离变粗、末端 coverage 下降」的行为

换成真 cone trace 的时候，trace 距离可以恒定不变，cone 宽度由粗糙度直接给出。

## 没解决的部分

Karis 坦率地列出了自己没解决的问题：

- **上万个点光源到底要不要画都是难题**——Prey 2 单张地图就有 >10000 个。
- **diffuse shadow map 和 tile 光源剔除怎么高效耦合**，他留到下一篇（这个系列没有写完）。
- **cone 剔除能不能推广到 Blinn 分布**——Phong 有解析解，但 Blinn 的 $(n \cdot h)^k$ 形式没那么直接，他公开求助社区。
- 评论区里 Stephen Hill 提到一个实践疑虑——**表面高频 bumpy 会让 tile 内法线方向分散**，specular cone 的 union 退化成近乎整个半球，剔除失效。Karis 回应：高频 bump 本该做 **specular antialiasing**（把粗糙度提高）减少方差——这正好把问题转成低光泽度情形，而低光泽度下能量守恒保证 specular 作用范围小、受影响 pixel 数近似恒定，剔除又变得有意义。只有**刚好一个 tile 大小频率的 bump** 才能打破这个论证。

## 后续：十年后的 Lumen

Karis 博客里这些想法不只是 sketch——**UE5 Lumen 几乎是对着这篇博文实现的**：

- 静态几何：**Global SDF + Mesh SDF** 做远场 cone trace（正好对应 Samaritan demo 的做法）。
- 屏幕空间：HiZ + adaptive depth 做近场 trace。
- **hybrid**：cone trace 的结果缓存在 surface cache 里，着色阶段只从缓存查询。
- **screen probe GI**：per-tile 的反射 cone trace 结果被 tile 内像素共享——这正是 Karis 2012 年那句「visibility 独立于光源可以跨光源共享」的完整兑现。

## 相关

- [[tiled-light-culling]] —— 上一篇：specular cone 剔除
- [[sdf-ray-marched-shadows]] —— SDF cone trace 的 2D 版本
- [[hierarchical-z-buffer]] —— HiZ 做近场 cone trace
- [[virtualized-volume-textures]] —— SDF / SVO 存储用的 brick 结构
- [[visibility-buffer]] —— UE5 Nanite 里的对应几何表示
- [[physically-based-shading]]
- [[brian-karis]]

## Sources

- [[sources/karis-sparse-shadows-tracing]]
