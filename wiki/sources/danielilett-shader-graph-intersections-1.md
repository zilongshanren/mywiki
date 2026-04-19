---
tags: [source, unity, shadergraph, depth, intersection, ssao]
date: 2026-04-19
sources: 1
---

# Unity Shader Graph Basics Part 8 - Scene Intersections 1（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 2024 年 5 月的 Shader Graph 入门系列第 8 部。主题是**场景相交检测**——让透明物体的 shader 知道"我身后的不透明几何离我有多远"，并把这个距离用于视觉效果。这一部先建立基础设施（一个叫 `DepthIntersection` 的子图）并做第一个应用：基于屏幕空间相交的**环境光遮蔽**。

## 摘要

文章分三段。第一段解释原理：透明 shader 无法访问其它物体的几何，唯一能用的是 **`_CameraDepthTexture`**——Unity 在所有 opaque 物体画完之后、在画透明物体之前的 depth buffer 快照。这意味着"相交检测"必须在**透明** shader 里做（graph settings → surface = transparent），且两个透明物体之间互不可见。

第二段构造基础节点链：`Scene Depth`（Eye 模式，拿到邻居的线性距离）减去 `Split(Screen Position Raw).w`（拿到当前片段的 clip space w，等价于 view-space 距离）。两个深度相减就是 intersection distance。Ilett 把这 4 个节点封成 `DepthIntersection` 子图——这是 Shader Graph 里**首次演示 subgraph 功能**，他特地解释了 subgraph 和普通 graph 的区别（需要手动定义 Output 节点的字段）、为什么要用 subgraph（`"这组节点我会用超过一次"`）。

第三段用子图做 `IntersectionOcclusion` 效果：`DepthIntersection → OneMinus → Saturate → Power(IntersectionPower) → Multiply(OcclusionStrength) → Lerp(BaseColor, Black)`。结果是透明物体底部/边缘处靠近其它几何时变暗，模拟接触阴影。Ilett 明确指出这不是真正的 SSAO——真 SSAO 要采多个邻近像素重建局部几何——这是一个"够用就好"的局部近似，在岩石陷入地面这种场景下能有效软化边界。

文章尾部附一大段**homogeneous coordinates 速成**：为什么 GPU 用 4D 向量表示 3D 点（4×4 矩阵才能表达平移），为什么 clip space 的 w 分量等于视点到 vertex 的距离（view→clip 变换把 view z 搬到了 w），以及 perspective divide（除 w）如何把 4D 压回 2D 屏幕坐标。

## 关键要点

- **Scene Depth 节点 + `Screen Position(Raw).w` 是 Shader Graph 里做相交检测的标准两件套**，放在一个 `DepthIntersection` 子图里反复用。
- **深度相交只在 transparent shader 里有效**——这是 `_CameraDepthTexture` 在渲染管线里的时序决定的，不是 bug。
- `Saturate` 是 HLSL 里的 `clamp(x, 0, 1)`，Ilett 当作概念课讲，配了"一个最多能装 1 的盒子"比喻。
- Shader Graph 的 `Scene Depth Difference` 节点理论上是为此而生但 Ilett 吐槽"不知道它在干嘛"，实测行为和文档对不上，老派的"两个深度相减"更可靠。
- **Subgraph 首次出场**：定义 inputs / outputs 的方式和普通 graph 不同——要点开 Output 节点的 Node Settings 手动加字段。这一部的 `DepthIntersection` 子图会在 Part 9 里再扩展（加一个 `Offset` 输入）。
- 该 shader 的局限：**"薄物体擦地"会误判**——一个贴地薄盒子所有像素相交距离都小，整个盒子会被拉黑。这暗示该技巧最适合"软化局部接触"而不是全场景 AO。

## 链接到的概念

- [[depth-intersection-subgraph]]
- [[scene-color-depth-nodes]]
- [[coordinate-spaces]]
- [[mvp-transform]]
- [[depth-texture-silhouette]]
- [[z-buffer]]

## 原文

- 链接：<https://danielilett.com/2024-05-21-tut7-12-intro-to-shader-graph-part-8/>
- 本地：`raw/articles/danielilett.com/2024-05-21_unity-shader-graph-basics-part-8-scene-intersections-1.md`
