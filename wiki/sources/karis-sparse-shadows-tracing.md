---
tags: [source, 渲染, 阴影, 反射, sdf, cone-tracing]
date: 2026-04-14
sources: 1
---

# Sparse Shadows through Tracing（Brian Karis / Graphic Rants）

[[brian-karis|Brian Karis]] 2012 年 5 月 14 日发表在 Graphic Rants，是 [[sources/karis-tiled-light-culling]] 的直接续篇。主题：既然 tile 级的 specular cone 剔除让远处光源可以廉价地投射 specular 高光，这些高光的**阴影**怎么办？

## 摘要

Karis 先引用 Matt Swoboda 在 GDC 2012 的观点——**next gen renderer 需要多套几何表示**：栅格化友好的 mesh（用于 primary ray 和 shadow map 的相干射线）+ trace 友好的结构（用于不相干射线，能做 cone trace 的比只能做 ray trace 的更有用）。他列出候选表示：**SDF volume**（iq/Samaritan demo）、**SVO**（Crassin GI Voxels）、**surfel tree**（Ritschel microrendering）、**billboard cloud tree**，屏幕空间则有 HiZ min/max mipmap（Drobot）、VSM、adaptive transparency buffer。Epic 的 Samaritan demo 是他论点的存在性证明——他们对反射做了 SDF cone trace，顺便用同一个 SDF 给点光源提供了 specular 阴影，几乎是零额外成本。Karis 的提案：**diffuse radius 内走传统 shadow map；超出部分的 specular 沿反射向量做 cone trace**，返回一个 visibility 函数供**所有**远处光源共享——可见性独立于光源，跨光源复用，不需要每个光源一张 shadow map。副产品：cone trace 的 max unoccluded 距离可以回馈到 [[tiled-light-culling]]，给 per-tile 剔除锥设一个上界——他预测这会成为重要的优化。cone trace 在当前世代已经有最粗糙的形式：**SSR 用低粗糙度缩短 trace 距离 + 末端 fade out** 来模拟 cone 随距离变粗，到了下一代可以升级成真 cone trace。最后 Karis 坦率地列出未解：上万个点光源的选择问题、diffuse shadow map 和 tile 剔除的耦合问题、cone 剔除能不能推广到 Blinn 分布。评论区 Stephen Hill 提问高频 bumpy 内容是否会破坏 specular cone 的有效性，Karis 回应 spec AA 会把 bumpy 变成低光泽 case。

## 关键要点

- **多几何表示假设**：相干射线用 mesh + HW raster；不相干射线用 trace 友好结构——**可 cone trace 的比 ray-only 的更有用**。
- **Trace-friendly 候选**：SDF / SVO / surfel tree / billboard cloud tree + 屏幕空间 HiZ / VSM / adaptive transparency buffer。
- **核心方案**：diffuse 半径内 shadow map；超出部分的 specular = 反射向量 cone trace；**visibility 独立于光源，跨光源共享**。
- **副产品**：cone trace 的 max unoccluded 距离作为 per-tile 剔除锥上界——occlusion 反哺 light culling。
- **Samaritan demo 是先例**：SDF 本来为反射服务，复用做 specular shadow 几乎零成本。
- **当前世代 SSR = 最粗糙的 cone trace**：降 gloss 时缩短 trace 距离、末端 fade，是对 cone 随距离变粗的定性近似。
- **未解问题**：> 10000 点光源的选择、diffuse shadow map 与 tile 剔除的耦合、Blinn 分布下的锥角推导。
- **Stephen Hill 的 bump 担忧**：specular AA 把高频 bump 转低光泽（能量守恒让 specular 影响像素数近似常数），只有 tile 大小频率的 bump 真正让剔除失效。
- **十年后的兑现**：UE5 **Lumen** 的 Global SDF + Surface Cache + screen probe GI 架构几乎一字不差实现了这篇博文提出的所有思想。

## 链接到的概念

- [[sparse-shadows-cone-tracing]]
- [[tiled-light-culling]]
- [[sdf-ray-marched-shadows]]
- [[virtualized-volume-textures]]
- [[hierarchical-z-buffer]]
- [[physically-based-shading]]
- [[brian-karis]]

## 原文

- 链接：http://graphicrants.blogspot.com/2012/05/sparse-shadows-through-tracing.html
- 本地：`raw/articles/graphicrants.blogspot.com/2012-05-14_sparse-shadows-through-tracing.md`
- 参考 [1]: Swoboda, *get my slides from GDC2012* — directtovideo
- 参考 [2]: iquilezles, *Rendering Worlds with Two Triangles*, NVScene 2008
- 参考 [3]: Crassin et al., *Interactive Indirect Illumination Using Voxel Cone Tracing*, PG 2011
- 参考 [4]: Ritschel et al., *Microrendering*
- 参考 [9]: Epic + NVIDIA, *Samaritan Demo*, GDC 2011
