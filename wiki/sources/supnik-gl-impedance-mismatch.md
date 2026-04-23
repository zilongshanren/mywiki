---
tags: [source, 图形, opengl, 驱动, gpu, metal, vulkan]
date: 2026-04-19
sources: 1
---

# The OpenGL Impedance Mismatch（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2015-04 的第二篇，把 GL 状态机与现代 GPU 真实状态之间的错位量化。

## 摘要

OpenGL 从来不是硬件的精确映像。作者用三个例子展开：第一，R300 级固定管线时代寄存器布局已经和 GL enum 错位——`glBlendFuncSeparate` 跨两个寄存器，blend enable 与「分离 blender 开关」共享寄存器；第二，现代可编程 GPU 把 vertex fetch 完全 inline 在 VS 前置片段、fragment MRT 映射 inline 在 FS 后置片段，驱动被迫维护「vertex layout × MRT layout × GLSL program」组合 cache，每次 `glVertexAttribPointer` 都可能让 layout 失效；第三，`GL_ARB_vertex_array_object`（GL 3.0）把 vertex fetch + base pointer 打包为对象，但两半在硬件上耦合度不同，合并是错的——`GL_ARB_vertex_attrib_binding`（GL 4.3）在 API 上拆开，向现代硬件靠回一步。结论是 pipeline-and-state 模型越来越不合身，这正是 Mantle / Metal / Vulkan / D3D12 出现的理由——**把隐式的 combination cache 改回显式的 pipeline 对象**。另有评论补充：只有 AMD GCN 的 vertex fetch 真正走 shader 前置；其它硬件（AMD 更早代、Intel、NVIDIA）仍有专用 vertex fetch 硬件；Vulkan / D3D12 也把黑盒 fetch 回补进来。

## 关键要点

- 固定功能时代 GL 状态已经和寄存器错位——blend 分 separate / share 的布局是典型。
- 现代 GPU：**vertex format、MRT 映射都在 shader 里**；改它们就是改 shader。
- **驱动必须维持 combination cache**（layout × MRT × program），每 `glVertexAttribPointer` 可能触发查询或 patch。
- **VAO 是 day-one mistake**——vertex fetch 和 base pointer 耦合度不同，不该是一个对象。
- **`GL_ARB_vertex_attrib_binding`**（GL 4.3）拆开，**`glVertexAttribFormat`** 才触发 shader patch。
- VAO mutability 还有第二层：VBO **数据位置**本身是 mutable 的（VRAM ↔ 系统内存 ↔ DMA），绑定 VAO 不能省掉验证/同步。
- 评论补充：AMD 非 GCN、Intel、NVIDIA 仍有专用 vertex fetch 硬件；Mantle 完全取消，Vulkan / D3D12 回补。

## 链接到的概念

- [[opengl-hardware-impedance-mismatch]]
- [[opengl-state-change-deferral]]
- [[mtl-render-pipeline-state]]
- [[vulkan-explicit-performance]]
- [[compact-vertex-format]]
- [[draw-call]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2015/04/the-opengl-impedance-mismatch.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2015-04-14_the-opengl-impedance-mismatch.md`
