---
tags: [渲染, 几何, tessellation, displacement, nanite, ue5, 软光栅]
date: 2026-04-19
sources: 2
---

# Nanite Tessellation 的流水线与实现

UE5.4 Shipping 在 Fortnite 地面和 *Marvel 1943: Rise of Hydra* 里的动态 tessellation + 位移系统。本页整理 [[brian-karis|Brian Karis]] 在 *Nanite + Reyes* 博文里披露的具体阶段、数据结构与踩过的坑。整体框架参见 [[tessellation-approaches-overview]]，Reyes 渊源见 [[nanite-reyes-comparison]]。

## 为什么还需要"放大"

Nanite 解决了几何虚拟化的**通用**问题（可改变 genus、可大幅简化），但对**位移**这一场景并非最优——位移把 1 个标量 + 2D 正则化数据对应到 5+ 个属性的完整顶点，数据压缩、**程序化纹理**（tiling / detail texture / shader mix）、animator 工作流、低端 fallback 都更倾向"放大"而不是"下采样"。Fortnite 的 scalability 跨度尤其需要 art 按低多边形基础资产 + 位移放大到高端。

## 高层流水线

Nanite 原本是 **Cull → ClusterRasterize**（软件路径，小三角形；大三角形走 HW）。Tessellation 在末尾追加：

```
Cull → ClusterRasterize ──┬── SW raster（老路径）
                           │
                           └── PatchSplit ──▶ PatchRasterize（纯 SW）
```

**关键约束**：每个 cluster 可以**同时**被 Nanite 简化（小 patch 合并掉）和被 tessellation 放大（大 patch 细分）。Nanite 的 LOD 仍然按**原始表面**的位置误差 + 法线误差来决定——位移的影响被忽略，因为位移是用户 shader，预处理阶段不可知。

所有"需要执行位移函数"的 shader 都是**可编程阶段**（per-material 编译），需要 `DispatchIndirect` 启动。其它阶段尽可能保持**全局 shader**，因为全局 shader 才能在一次 dispatch 里处理所有材质、允许 async overlap、避免 per-material spin-up 的开销。

## ClusterRasterize 的扩展

原本每个线程对应一个三角形，现在先判 TessFactor：

- 所有 edge TessFactor ≤ 1 → 正常走位移 + 直接 rasterize；
- 所有 ≤ MaxDiceFactor → 进 **dice queue**；
- 否则 → 进 **split queue**。

位移函数在这里已经要执行（所以仍是 per-material shader）。第一步 split 会就地完成（见 [[variable-sized-work-pattern]]），避免把明显能就地处理的 patch 真的写进内存队列。

## PatchSplit：递归展开

每个线程从 split queue 取一个 subpatch，算 TessFactors，视情况：

- 若 TessFactors ≤ MaxDiceFactor → 推进 dice queue；
- 否则按 SplitFactor 产生若干子 subpatch，写回 split queue。

subpatch 存储结构紧凑到 16 字节：

```cpp
struct Subpatch {
    uint32 VisibleClusterIndex : 25;
    uint32 TriIndex : 7;
    uint32 BarycentricsUV[3]; // 16:16
};
```

**核心工程决策——这是 global shader**：

- 它要从不同材质的 patch 里收集工作，若是 per-material dispatch，要么每次都要把机器填满（多数会立刻退休），要么无法 async overlap；
- 因此**一切 split 决策必须是 fixed-function**——不能执行位移函数、不能读 programmable normals、不能让艺术家自定义 dicing rate。

**可见性剔除**仍用 frustum / HZB / [[virtual-shadow-maps|VSM]] page mask，但位移后的真实 bounds 是鸡生蛋问题——artist 需要手动给**位移范围上下限**。这是 Karis 坦承的"最常被艺术家踩坑"的地方：范围估得太大就破坏剔除。屏幕空间 bounds 用 Niessner-Loop 的 prism 并集（比原来的球帽锥更紧）。

**递归调度**曾用 persistent threads + 全局 lockless work queue（和 Nanite 簇层级同一套工具）。但这种做法不是 D3D spec 保证前进的，PC 上不能假设所有硬件 happy。所以：

- 固定平台（主机）继续 persistent threads；
- PC 改成 **multipass**——多次 dispatch，递归深度有上界（16-bit barycentric 被 MaxSplitFactor 反复除最多除这么多次），async overlap 本来就帮助掩盖 drain。

## PatchRasterize：dice + 软光栅

dice queue 的 entry 比 subpatch 小（因为 TessFactors 已计算、已知 Tessellation Pattern 索引）。每个 patch 已经是接近均匀 + 接近 MaxDiceFactor 的小补丁。

```
scalar:    load cluster + patch + corners, transform corners
per-vert:  read barycentrics from Tess Table, lerp corners,
           evaluate displacement, transform to clip, store in groupshared
per-tri:   read indices from Tess Table, raster triangle
```

**踩过的坑**：

- **scalar float 太重**。每 patch 有大量 scalar 工作（前置 per-patch transform）。RDNA3 和更早**没有 scalar float**，这些只能在 vector unit 上跑且只占一条 lane。Rune Stubbe 的优化：一个 wave 跑**多个 patch**，把 3x patch-corner 工作摊到 32 lane，用 `WaveReadLaneAt` 在 "VS phase → DS phase" 之间搬数据——本质上把 DS 的工作搬到 VS。
- **跳过 normal 归一化**。不归一化 interpolated normal 之后，后续所有 transform 都是线性的，基础 patch 的 position/normal 可以预先 transform 到 clip 空间、整 patch 共享。
- **没有 HW rasterizer**。dice 出来的本来就是 micropoly，不存在"大到需要 HW"的情况；省掉一份 shader permutation 和 drawcall。near plane 不做 clip，直接 cull 穿近裁剪面的**三角形**（不是 subpatch，subpatch bounds 过粗会误杀）。
- **没有 MaxEdgeLength 保护**。位移的陡变可能让 diced 三角形被拉得很长——软光栅设了 64 像素的覆盖上限，超过就看起来像**表面撕裂**。这可能迫使未来加回 HW 路径。

## DS 导数的老问题

**domain shader 没有自动导数**。texture sample 要 UV derivative 做 mipmap（不仅是抗锯齿，还影响 cache coherency——用 mip 0 会严重掉速）。传统 Reyes dice 成方格用有限差分就够，但 Tessellation Table 的不规则网格没有简单的邻居查找。

Karis 给的解法是 chain rule：

$$\frac{dUV}{dTessFactors} = \frac{dUV}{dXYZ} \cdot \frac{dXYZ}{dTessFactors}$$

第二项其实就是 `1 / DicingRate`（TessFactor 原本就是这么算出来的），在 XYZ 空间连续、跨 patch 自动一致。第一项是逐面 piecewise constant，**corner 处 valence 不定**，只能 preprocess 时按顶点预算并存储（类似 tangent basis），而且多套 UV 要分别存——额外的 heavyweight data，艺术家需显式开启。

## 相关

- [[tessellation-approaches-overview]] —— 为什么选这条路
- [[nanite-reyes-comparison]] —— Reyes 经典与这里的区别
- [[variable-sized-work-pattern]] —— split 和 dice 都用它分发工作
- [[nanite-virtualized-geometry]]
- [[visibility-buffer]]
- [[brian-karis]]

## Sources

- [[sources/karis-nanite-tessellation-intro]]
- [[sources/karis-nanite-reyes]]
