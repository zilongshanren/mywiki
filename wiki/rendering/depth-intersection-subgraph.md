---
tags: [shader, shadergraph, depth, intersection, unity, 渲染]
date: 2026-04-19
sources: 2
---

# Depth Intersection：一个子图撑起一个效果家族

很多"看起来很不一样"的透明物体效果——**屏幕空间环境光遮蔽**、**水面岸边的泡沫**、**能量护盾的边缘辉光**——在底层其实是同一个问题：**"当前透明片段"离"它身后已经渲染好的不透明几何"有多远？** 这个距离就叫 **depth intersection**。[[daniel-ilett|Daniel Ilett]] 的 Shader Graph Basics Part 8–9 把它抽成一个极小的子图，再用这一个子图换不同的后处理得到三种完全不同的视觉。

## 两个深度的取法

一张 Shader Graph 里取两个深度：

- **当前片段到相机的距离**：用 `Screen Position` 节点，**Mode 设 Raw**——Raw 模式下输出的其实是 clip-space 四维向量，Split 后 `W` 分量等于 view-space 下当前 vertex 到相机的距离。这是齐次坐标的副产品：clip space 投影后 `w = -z_view`，正好就是距离（见 [[mvp-transform]] 和 [[coordinate-spaces]]）。
- **场景里这个像素处本来画的物体到相机的距离**：用 `Scene Depth` 节点，**Mode 设 Eye**（`LinearEyeDepth`），它采样 `_CameraDepthTexture` 并线性化到世界单位（见 [[scene-color-depth-nodes]]）。

两个相减就是 intersection distance。这 4 个节点打包成 `DepthIntersection` 子图：`Scene Depth (Eye) - Split(Screen Position Raw).w → Output`。简洁到不可思议。

## 硬约束：shader 必须 Transparent

`_CameraDepthTexture` 是 Unity 在**所有不透明物体画完、但所有透明物体画之前**生成的一张快照。这意味着：

- **不透明 shader 读不到任何东西**——它读到的要么是全白（纹理还没填），要么是自己刚写进去的值（读自己等于零距离）。所以 Graph Settings 的 Surface 必须是 **Transparent**。
- **透明物体之间互相读不到**——两个半透明 mesh 谁也不会出现在对方的 depth texture 里，水面泡沫碰到另一面水就不会起泡沫。

这是一条根本性的时序约束，不是 bug，是整个[[rendering-pipeline|渲染管线]]透明物体排序带来的先天结构。

## 三种效果共享同一个子图

Ilett 用完全相同的 `DepthIntersection` 子图做了三件完全不同的事：

**1. 屏幕空间 AO（IntersectionOcclusion）**：得到 distance 后 `OneMinus + Saturate → Power(IntersectionPower) → Multiply(OcclusionStrength) → Lerp(BaseColor, Black)`。距离 intersection 近的片段被拉黑，就是最朴素版本的 **SSAO**——把真正的 SSAO 用作 post-process 需要采样多个邻近像素、代价更高，这个单像素版适合局部（例如"岩石和地面接触处"的软化）。

**2. 水面泡沫（IntersectionFoam）**：`distance / FoamDistance → Step → Multiply(FoamColor) → Add(BaseColor)`。但 Step 产生的直边缘不像泡沫，所以再叠一个 `Simple Noise`（用 `Time * FoamVelocity` 偏移 UV）当作 Step 的阈值——让泡沫边缘按噪声波动。

**3. 边缘辉光（IntersectionGlow）**：Intersection 值驱动一个 HDR 发光 color 加到 base color，正好是 [[fresnel-edge-highlight|Fresnel 边缘光]]的 depth 版——物体**物理接触**到其它几何时亮起。和基于 UV 的边缘光组合，就是 _Mass Effect_ 式能量护盾的两条边（UV 边 + 接触点）。

## 关键演化：给子图加 Offset 输入

原始版 `DepthIntersection` 没有入参，只能采样"自己这个像素的深度差"。问题是 Foam 效果：泡沫只能出现在**物体正下方**，物体右侧的水片段因为后面什么都没有、采到的是远处地面，吃不到 foam。

解法是给子图加一个 `Vector2 Offset` 参数，替换内部 `Scene Depth` 的输入。`Scene Depth` 的默认 UV 是 `Screen Position (Default)` 也就是 `[0, 1]` 的屏幕坐标，把它加上 `Offset` 就能读**偏移了几个屏幕像素之后**的深度——让当前片段"看向旁边"。

默认值 `(0, 0)` 保证不改动其它用了这个子图的图的行为——这是个**非破坏性的 API 演化**，Ilett 没提，但这是 subgraph 对上游稳定性最低成本的维护方式。

然后 Foam 图里 `Simple Noise` 被同时喂给两处：一处当泡沫边缘阈值，另一处作为 `Offset` 让采样点本身抖动。这样泡沫会"溢出"到物体旁边，看起来像真的水在向外涌。代价是出现了"过度溢出"的伪影——Ilett 用第二个 `Step`（把 `Negate(distance)` 和 noise 比较）把物体另一侧的错误泡沫剪掉，这是一条技巧，不是干净算法，暗示了纯 2.5D 近似的上限。

## 为什么这不是 SSAO

真的 SSAO（见[[hbao-interleaved-sampling|HBAO]] 类算法）采样**多个邻近像素**的深度 + 法线，重建局部几何形状再判断遮蔽。Ilett 的单像素版本：

- 对"薄物体擦地"会误判——一个平放的薄盒子所有像素的 intersection 都很小、整个盒子被拉黑。
- 对凹陷处感知不到——因为只看自己身后一根射线、看不到周围。

但这个简化有它的用处：它**只在透明 shader 里有效、且零额外内存**（只用一张已经存在的 `_CameraDepthTexture`），特别适合"把穿插进地面的岩石/植物软化"这类 asset-level 局部效果，不是做全屏 SSAO。

## 相关

- [[daniel-ilett]]
- [[scene-color-depth-nodes]] — `Scene Depth` 节点的完整解释
- [[depth-texture-silhouette]] — `_CameraDepthTexture` 的另一种玩法
- [[orthographic-depth]] — 正交相机下的 depth 差技巧
- [[coordinate-spaces]] — 为什么 `Screen Position Raw.w` 等于距离
- [[stylized-water-shader]]
- [[fresnel-edge-highlight]] — Glow 效果的姊妹
- [[z-buffer]]

## Sources

- [[sources/danielilett-shader-graph-intersections-1]]
- [[sources/danielilett-shader-graph-intersections-2]]
