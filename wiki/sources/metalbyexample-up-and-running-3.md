---
tags: [source, 渲染, metal, 光照, blinn-phong, 深度测试, 教程]
date: 2026-04-14
sources: 1
---

# Up and Running with Metal, Part 3: Lighting and Rendering in 3D（Warren Moore）

[[warren-moore|Warren Moore]] 2014 年 9 月发表的 *Metal by Example* 系列第三篇，把前两篇的 2D 三角形升级成"带 Blinn-Phong 光照、可手势旋转的 Utah 茶壶"——这一跳正好跨过一条 3D 渲染的基准线：资产加载、矩阵 uniform、深度测试和逐像素光照。

## 摘要

文章从**OBJ 模型加载**开始，用一个迷你 parser 把茶壶 `.obj` 的 vertex / normal / index 读进连续数组；然后把顶点交给一个 interleaved 的 `Vertex { float4 position; float4 normal; }` 结构，通过 `MTLVertexDescriptor` 告诉 Metal 每个 attribute 在结构里的 offset 和 stride。光照采用**环境光 + 漫反射 + Blinn-Phong specular** 三项相加的经典公式，放在 fragment shader 里逐像素算：用 `N·L` 取 diffuse 强度、用 halfway vector `H = normalize(L + V)` 取 specular 项。Vertex shader 负责**三把矩阵变换**——`modelViewProjection` 把顶点推到 clip space，`modelView` 用来算 view-space 位置和视线方向，`normalMatrix`（`transpose(inverse(modelView))` 的 3×3 块）保证法线在非均匀缩放下仍垂直于表面。渲染前要启用**`MTLDepthStencilState`** 做 Z-test（`compareFunction = Less`、`depthWriteEnabled = YES`），并把 `frontFacingWinding` 设为 `CCW`、`cullMode` 设为 `back` 以省掉背面 fragment。最后用 `UIPanGestureRecognizer` 接管触摸，把手势速度转成角速度做茶壶自旋——再加一个 damping 系数让旋转松手后逐渐衰减，视觉上更自然。评论区里有 index buffer 对 cube 无效的经典问答、`vertexDescriptor` attribute format 写成 float4 但 shader 里是 float3 的 bug 订正、以及 iOS 9 之后 `depthAttachment` 为 nil 时 `validateDepthStencilState` 报错的回帖。

## 关键要点

- **Uniform 包含三把矩阵**：`modelViewProjection`（vertex 主变换）、`modelView`（fragment 光照用的 view-space）、`normalMatrix`（法线变换）——分开保留而非只预乘 MVP 是因为光照需要 view-space 向量。
- **`normalMatrix` 必须是 `(M⁻¹)ᵀ`**：直接乘 modelView 会让非均匀缩放把法线扭歪，这条规则对所有带 scale 的 rigging 都适用。
- **Vertex descriptor = CPU 侧描述顶点布局**：attribute 的 `format` / `offset` 必须和 shader 端 struct 匹配，interleaved 布局比分散 buffer 更有利于 cache。
- **Index buffer 的收益前提**：只有当 `position + 其它 attribute` 组合能被复用时才省内存——cube 的 24 个带法线顶点恰好互不相同，indexing 退化成无用功，smoothing group 模型才是典型受益者。
- **Winding + cull 要一致**：Warren 选 CCW 前向 + 背面 cull，这和右手系 + OBJ 约定一致；clockwise 模型会整个翻过来。
- **Blinn-Phong 的 halfway 取 `normalize(L+V)` 而非平均**：后者数值不稳定；`saturate(dot(N, H))^power` 是整段计算量最小的 specular 近似。
- **每帧重建 Uniforms buffer** 是 Part 3 的简化写法——生产代码应当用三 buffer 轮转（triple buffering）避免 CPU/GPU 争用。

## 链接到的概念

- [[metal-3d-rendering-pipeline]]
- [[metal-api-overview]]
- [[metal-shading-language-basics]]
- [[mvp-transform]]
- [[shader-vector-math-primer]]
- [[diffuse-lighting-lambertian]]
- [[normalised-blinn-phong-shader]]
- [[z-buffer]]
- [[warren-moore]]

## 原文

- 链接：https://metalbyexample.com/up-and-running-3/
- 本地：`raw/articles/metalbyexample.com/2014-09-22_up-and-running-with-metal-part-3-lighting-and-rendering-in-3.md`
