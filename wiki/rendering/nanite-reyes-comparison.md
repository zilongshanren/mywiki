---
tags: [渲染, 几何, reyes, nanite, ue5, 历史, 架构]
date: 2026-04-19
sources: 2
---

# Nanite Tessellation 与经典 Reyes 的关系

Pixar 的 **Reyes**（1987）是史上第一个围绕**位移贴图**和**微多边形**设计的渲染架构。UE5.4 的 [[nanite-tessellation-approach|Nanite Tessellation]] 保留了 Reyes 的高层算法，但几乎每个细节都因实时约束 + Nanite 基础而改过。据 [[brian-karis|Brian Karis]] 所知，这是**第一个在游戏里 shipping 的实时 Reyes 实现**（Fortnite 地面）。

## Reyes 的五步流水线

```
Bound → Split → Dice → Shade → Rasterize
```

- **Bound** —— 计算 primitive 的 AABB，屏外就 cull。
- **Split** —— 如果仍然太大，一般二分，子 primitive 回到 Bound。递归到足够小。
  - **为什么需要 split？** 更细的 split 让可见性测试按接近均匀的粒度发生；跨越大深度范围的表面能按视距分别采用不同细分密度。和 Nanite 本身的 cluster 层级遍历同构。
- **Dice** —— 把足够小的 primitive 一次性网格化成 micropolys 的均匀网格。
  - **为什么要单独的 dice 阶段？** 叶节点有很多只对 dice 有效的优化，不必摊给 split。
- **Shade** —— 在 micropoly 顶点上求值——包括 displacement。
- **Rasterize** —— 写 framebuffer。

即便电影圈转 path tracing 之后，Manuka / PRMan 等 production tracer 仍然在跑前半段流水线——只是最后一步从光栅化变成"micropoly vs ray 测试"。

## Nanite Tessellation 的改造

| 维度 | 经典 Reyes | Nanite Tessellation |
|---|---|---|
| Primitive | 一般是 NURBS/subd surface、四边形 patch | **三角形** patch；起点是 Nanite 三角网 |
| Split 粒度 | 二分 | 更宽 branching（Tessellation Table 决定） |
| Dice 网格 | 规则的 `N × M` 四边形 | Tessellation Table 预计算的**不规则**等边 triangulation，密度更均匀 |
| Shade | full shading on micropoly vertices（object-space shading） | 仅在 dice 顶点上求值**位移函数**；其余材质 shading 走 [[visibility-buffer]] 的 **deferred material**（像素空间） |
| Shading 频率 | object space，贴图滤波依赖 micropoly 位置 | 像素空间；object-space shading 因 overshade 太贵已被现代 path tracer 放弃 |
| 光栅化 | 软光栅，像素原子写 | Nanite 的 software rasterizer（本来就为 micropoly 设计）；不走 HW 路径 |

Karis 对"object-space shading 是历史遗迹"的断言有佐证——现代 production path tracer 要么 on-hit 全着色，要么最多把 material 预求值成 BxDF lobes（类似 GBuffer）再 on-hit 混合。

## 设计约束与 Reyes 的天然契合

**split 既是 Reyes 核心，也是 Nanite 核心**——Nanite 的 cluster hierarchy 遍历本质上就是一棵 implicit tree 的递归展开，和 Reyes split 的 persistent-threads 实现同构（详见 [[variable-sized-work-pattern]]）。这是为什么 Karis 在放弃"在 Nanite 簇层级内部做 amplification"之后，自然滑向 Reyes 风格。

**dice 的均匀密度假设**也自然契合 Tessellation Table：Reyes 的 dice 要求"最小化三角形数 + 所有边 ≤ 目标长度"，正是 Botsch-Kobbelt isotropic remesh 的优化目标。

## 为什么这条路"不便宜"

[[tessellation-approaches-overview]] 解释了 Karis 放弃在 Nanite 簇层级里做 amplification 的原因。转向 Reyes 后仍然要付：

- 每帧动态跑 split/dice，而不是一次 offline tessellation 摊到所有帧；
- `MaxEdgeLength` 保护缺失导致陡位移 shader 下的表面撕裂；
- Nanite 的 pow2 LOD 在每帧重新 tessellate 时粒度仍然粗，Reyes 的动态切法恰好抹平了这一点——但换来 shader 端 DS 自动导数缺失（见 [[nanite-tessellation-approach#DS 导数的老问题]]）。

所以 Nanite Tessellation **不是免费**地"把 Nanite 的所有好处扩展到位移"——它是付出了 Reyes 固有的 split/dice cost，换来 shader-programmable displacement + Fortnite 级的 scalability。

## 相关

- [[tessellation-approaches-overview]] —— 为什么走 Reyes
- [[nanite-tessellation-approach]] —— 具体流水线
- [[variable-sized-work-pattern]] —— split/dice 用的 wave intrinsics 原语
- [[nanite-virtualized-geometry]]
- [[visibility-buffer]] —— deferred material shading 的基础
- [[brian-karis]]

## Sources

- [[sources/karis-possible-approaches-tessellation]]
- [[sources/karis-nanite-reyes]]
