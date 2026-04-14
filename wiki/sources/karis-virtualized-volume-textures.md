---
tags: [source, 渲染, 体积纹理, 虚拟纹理, 全局光照]
date: 2026-04-14
sources: 1
---

# Virtualized volume textures（Brian Karis / Graphic Rants）

[[brian-karis|Brian Karis]] 2011 年 1 月 30 日发表在 Graphic Rants 的一篇博文。出发点是**irradiance volume 用整张高分辨率体积纹理太费**、而大部分数据又是空气——于是提议把 2D 虚拟纹理的**索引纹理 + brick 物理池**机制整体 3D 化。

## 摘要

Karis 指出 volume texture 做 irradiance 的好处（动态物体也能采样同一个解）和痛点（空间浪费严重：实体附近需要高频、空气里可以粗粒度）。他描述了最直观的解法——**一张小的 indirection volume 做页表，把 XYZ 坐标翻译到物理 volume texture cache 里的 brick 起点**。和 Sean Barrett / id Tech 5 的 2D virtual texture 完全同构，三维下 border 开销更痛。另一种等价描述是**稀疏体素八叉树 SVO**：八叉树遍历在「brick 为最小单位、不在单 voxel 粒度」下可以折叠成一次查表。SVO 视角的额外好处是稀疏性更自然——空气里只留一个覆盖世界的根 brick 给动态物体用；靠屏幕空间反馈决定加载哪些 page，甚至不需要提前烘焙或存盘。评论区指出 VRVis 2008 的 *Smooth Mixed-Resolution GPU Volume Rendering* 和 Crassin 的 **GigaVoxels** 已经实现了这个思路。Karis 当时正在 Human Head 做 Prey 2 的照明研究，所以最后一句是「如果我真做了也不能公开说」——这个视角多年后在 UE5 Lumen 的 Global SDF + Surface Cache 里得到真正落地。

## 关键要点

- **irradiance volume 的浪费**：高分辨率体积纹理绝大部分体素是空气，和实体表面同样细粒度没必要。
- **indirection volume = 2D 虚拟纹理的页表**：低分辨率索引体积 → 物理体积纹理里的 brick。
- **2D 虚拟纹理的所有限制都搬过来**：brick 需要 border 做三线性过滤、border 占比随 brick 大小变化。
- **SVO 视角是等价的**：八叉树遍历折叠成一次查表（只要不在单 voxel 粒度工作）。
- **稀疏性更自然**：空气里只一个大 brick，实体附近细 brick；**屏幕反馈**就能决定 page 加载，甚至不需要存盘、甚至不需要预先计算。
- **不是 2D lightmap 杀手**：高分辨率场合仍然赢不过只铺表面的 lightmap。
- **先例**：VRVis 2008 *Smooth Mixed-Resolution*、GigaVoxels（Crassin 2009）。

## 链接到的概念

- [[virtualized-volume-textures]]
- [[spherical-harmonics]]
- [[brian-karis]]

## 原文

- 链接：http://graphicrants.blogspot.com/2011/01/virtualized-volume-textures.html
- 本地：`raw/articles/graphicrants.blogspot.com/2011-01-30_virtualized-volume-textures.md`
- 先例：Beyer et al., *Smooth Mixed-Resolution GPU Volume Rendering*, VG'08
- 先例：Crassin et al., *GigaVoxels: Ray-Guided Streaming for Efficient and Detailed Voxel Rendering*, I3D 2009
