---
tags: [渲染, opengl, 驱动, gpu, vulkan, metal]
date: 2026-04-19
sources: 1
---

# OpenGL 与现代 GPU 的阻抗不匹配

硬件从**固定功能管线**演进到**通用并行计算架构**之后，OpenGL 的「上下文 + 状态机 + 对象」模型和 GPU 真正做的事不再是一一对应，中间那层「让 GL 继续看起来像 GL」的成本由驱动扛下来。Ben Supnik 在 *The OpenGL Impedance Mismatch*（2015-04）里用三个例子把这条裂缝量化出来。

## 例子 1：固定管线的寄存器对应不上 API

R300（Radeon 9700）这一代，整个 raster operation 由少数寄存器控制。但就算在那时 GL 的映射已经有错配：

- blend function 和 sources 共享一个寄存器——OK。
- **alpha / RGB 的 blend function 不在同一个寄存器**——单次 `glBlendFuncSeparate` 会跨寄存器更新两段。
- **alpha-blend enable 跟「分离 blender 开关」共寄存器**——动一个会动到另一个。
- clear color **恰好**有自己的寄存器——少数直接对应的情形。

固定功能时代寄存器布局就不是按 GL enum 设计的，驱动必须在每个 draw 前合成正确的位图案。

## 例子 2：现代可编程 GPU——更深的错位

进入可编程时代，GPU 侧的真实状态组合变成：

- **Shader 常量在内存里**（匹配 UBO，但**错配**glUniform 式「挂在 program 对象上的 loose uniform」——硬件上 shader 对象和 uniform 是彼此独立的）。
- **Vertex fetch 完全在 shader 里**——驱动自动写入 VS 的前置片段。因此**改变 vertex 对齐/格式（不是 base 地址）= 一次 shader 编辑**。
- **Fragment shader 的 MRT 输出映射在 shader 里**——`glDrawBuffers` 换一次 = 又一次 shader 编辑。

结果驱动不得不**维护「vertex layout × MRT layout × GLSL program」的组合 cache**，每次 `glVertexAttribPointer` 都可能让 vertex layout 失效，接下来要么重跑很重的 state-change 检查，要么重新 patch shader。**两个选项都很差**。

> 注：这描述准确对应 AMD GCN；AMD 早期硬件、以及所有 Intel / NVIDIA 硬件仍有**专用的 vertex fetch 硬件**，vertex format 不改 shader。Mantle 直接取消 vertex fetch 让你自己写；Vulkan 和 D3D12 回补了一个「给驱动的黑盒 fetch」——因为这是特别通用的任务，让 driver writer 写比每个 app 自己写好。

## 例子 3：VAO 与 ARB_vertex_attrib_binding

- **`GL_ARB_vertex_array_object`**（GL 3.0 core）把 vertex fetch 与 base pointer 打成一个对象，想法是「一次绑定省去一堆 setup」。但其实 VAO 里**一半属性真正是 shader 的一部分（layout），另一半是真正的 VBO 数据位置**——两半在硬件上处于不同耦合度，打成一个 object 是**早就错了的决定**（Ben 的原话：「VAOs were a mistake from day one」）。
- **`GL_ARB_vertex_attrib_binding`**（GL 4.3 core）把 vertex format（shader 那一半）和 VBO source（数据位置）**分开**。`glVertexAttribFormat` 仍然可能 patch shader，但应用可以更换 VBO 源而不触发它。这是 GL 往现代硬件靠拢的一次**往回搬家**。

## VAO 还有一层 mutable 陷阱

即便你把 VAO 视为 immutable 对象，VBO 数据位置**在驱动层仍是 mutable 的**——VBO 可能在 VRAM 也可能在系统内存，可能需要 CPU 侧 memory map 更新或一次 DMA 拷贝。绑定一个 VAO 不能跳过 base pointer 挪动带来的验证/同步——这是「显式 API」（见 [[mtl-render-pipeline-state]]、[[vulkan-explicit-performance]]）出场的根本理由。

## 一句话总结

> OpenGL 从来不是硬件的精确映像；硬件越朝「通用计算 + 内存缓冲」发展，pipeline-and-state 模型越不合身。

这条结论正是 Metal、Mantle、Vulkan、D3D12 出现的动因——**把隐式推给驱动的 combination cache 改回显式 pipeline 对象**。

## 相关
- [[opengl-state-change-deferral]]
- [[mtl-render-pipeline-state]]
- [[vulkan-explicit-performance]]
- [[metal-api-overview]]
- [[draw-call]]
- [[compact-vertex-format]]

## Sources
- [[sources/supnik-gl-impedance-mismatch]]
