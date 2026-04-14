---
tags: [source, 渲染, metal, shader, msl, 教程]
date: 2026-04-14
sources: 1
---

# Up and Running with Metal, Part 2: Drawing Triangles（Warren Moore）

[[warren-moore|Warren Moore]] 2014 年 8 月的 *Metal by Example* 系列第二篇，在 Part 1 清屏代码的基础上，把 Metal 的 **shader 子系统**和 **render pipeline state** 拉进来，最终在屏幕中央画出一个顶点颜色分别为红绿蓝的 2D 三角形。

## 摘要

文章把初始化流程拆成三个步骤：`buildDevice`、`buildVertexBuffers`、`buildPipeline`。`MTLBuffer` 的作用是承载两段静态数据——顶点位置和顶点颜色——都以 4 分量 float 形式存放（位置用齐次坐标，最后一维固定 1）。接着 `Shaders.metal` 里写出最小的 MSL 代码：一个 `ColoredVertex` 结构体（`float4 position [[position]]; float4 color;`），一个 `vertex_main` 函数接收两个 `[[buffer(0/1)]]` 的 `constant float4*` 参数和一个 `[[vertex_id]]` 索引，一个 `fragment_main` 函数接收 `[[stage_in]]` 的 `ColoredVertex` 直接返回 `in.color`。host 侧通过 `[device newDefaultLibrary]` + `newFunctionWithName:` 按名字查函数，塞进 `MTLRenderPipelineDescriptor`，再 `newRenderPipelineStateWithDescriptor:` 得到一个可复用的 pipeline state 对象。draw 时 command encoder 调用 `setRenderPipelineState:` + 两次 `setVertexBuffer:atIndex:` + `drawPrimitives:MTLPrimitiveTypeTriangle vertexCount:3`，最后借 `CADisplayLink` 每一帧刷新。Warren 在评论区还补充了 Retina `drawableSize` 要手动对齐、packed / non-packed 向量对齐，以及默认 **perspective-correct 插值**的 MSL 语义。

## 关键要点

- **Pipeline state 是昂贵的重对象**，里面是 shader 的编译 + 链接结果；每种 shader 组合建一次，长期持有。
- **MSL 用 `vertex` / `fragment` / `kernel` 限定符区分用途**，一个 `.metal` 文件可以同时放多种函数；pipeline 靠名字选择，不需要写 program。
- **属性限定符 `[[buffer(n)]]` / `[[vertex_id]]` / `[[position]]` / `[[stage_in]]`** 是 shader 与 host 之间的数据契约——`atIndex:n` 和 `[[buffer(n)]]` 一一对应。
- **光栅化自动插值**：`vertex_main` 返回的 `ColoredVertex` 与 `fragment_main` 接收的并不是同一个对象，后者是**每像素由光栅化器从三个顶点浮点成员 [[perspective-correct-interpolation|perspective-correct]] 插值**得到的；整数成员走 flat 插值。
- **[[coordinate-spaces|NDC]] 简化**：Part 2 的三角形仍写在 [-1, 1] 的 NDC 里，避开了 MVP 变换，把注意力集中在 API 流程上。
- **CADisplayLink** 是 iOS 上与显示刷新同步的帧驱动方式，比 NSTimer 更稳定。

## 链接到的概念

- [[metal-shading-language-basics]]
- [[metal-api-overview]]
- [[cametal-layer-drawable]]
- [[perspective-correct-interpolation]]
- [[fragment-shader]]
- [[warren-moore]]

## 原文

- 链接：https://metalbyexample.com/up-and-running-2/
- 本地：`raw/articles/metalbyexample.com/2014-08-26_up-and-running-with-metal-part-2-drawing-triangles.md`
