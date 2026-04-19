---
tags: [渲染, 着色器, 离线渲染, 语言设计, 路径追踪]
date: 2026-04-19
sources: 1
---

# Tiny Shading Language：为 CPU 离线渲染器量身定做的着色语言

Tiny Shading Language（TSL）是 [[graphics-guy-notes|Jiayin Cao]] 为自己的 CPU 路径追踪器 SORT 写的着色语言，总工作量约四个月。它回答了一个具体问题：当你拒绝依赖 OSL（及其 OpenImageIO、OpenEXR、libpng 等一长串依赖）时，如何让一个人在可控时间内做出够用的 offline shader stack？答案是**站在 Flex + Bison + LLVM 的肩膀上**，把前端（词法、语法、AST）与后端（IR → JIT 机器码）都交给成熟工具，自己专注于离线渲染特有的语言系统设计。

## 与 GPU 着色语言的本质差异

TSL 语法是 C 风格的（贴近 GLSL/HLSL/OSL），但语义选择完全由"CPU 光追"这一运行上下文决定：

- **一对一执行**：GPU shader 是海量并行，常需 Warp/Wavefront 级同步；CPU 路径追踪器的线程互不同步，每次 shader 调用相当于一次普通的 C++ 函数调用，只是机器码由 TSL JIT 出来。因此 TSL 不针对 SIMD 批处理做设计（OSL 的 SIMD 路线图在此方向上走得更远）。
- **允许调用栈**：GPU shader 通常没有 call stack，TSL 则让 shader 作者自由使用递归与深调用，反正最终落到 x64/arm64 的 ABI。
- **输出是 closure tree，不是颜色**：这是与 GPU shader 最大的概念差。

## Closure 与 Closure Tree

TSL 里的 closure 是**延迟求值的占位符**：它带着一个 type id 与构造所需的参数（base color、normal、roughness……），把"这是哪种 BXDF / medium"这件事告诉渲染器，但 BXDF 的真正评估（evaluate / importance sample / PDF 查询）留给 C++ 侧的 BXDF 库。

这样做有两个理由：

1. **BXDF 接口多**（evaluate、sample、pdf、albedo……），若全部在 shader 里实现，每新增一个接口就要生成一种 shader，组合爆炸；
2. **渲染器常已有成熟 BXDF 实现**，不该要求集成方重写一遍。

Closure 的合法操作只有两类：closure + closure、closure × 颜色（颜色充当权重）。这与 BSDF = 多个 BXDF 线性组合的数学直觉一致。此外允许**递归 closure**——把一个 closure 当作另一个 closure 的输入参数，用来表达 "Coat 覆盖在 Disney BRDF 之上且两层法线不同" 这种材质。

最终从 TSL 执行出来的是一棵 closure tree：叶子是具体 BXDF，内部节点是 add / multiply，渲染器遍历这棵树即可重建本次 shading point 的 BSDF。

## Shader Unit / Shader Group Template

TSL 把材质图（material graph）一路下放到语言本身：

- **Shader Unit Template**：最小编译单元，对应材质图的一个节点（OSL 叫 shader layer）。输入输出参数都不需要在编译期绑定具体值，可以留到组装阶段再填。
- **Shader Group Template**：用一组 shader unit template + 连接关系 + 默认值 + 暴露参数，表达一整张材质图。

作者最得意的改动是**让 shader group template 本身也成为 shader unit template**，于是材质图递归嵌套成了一等公民（A 里可以放 B、B 里可以放 C……），带来的好处是群组节点可以在多个材质间复用，改一处自动传播；对应在 Blender 插件里，原先必须先"ungroup"再喂给 OSL 的 hack 自然消失。

## 全局常量与回调

每个 shading point 才知道的数据（uv、世界坐标位置、shading normal 等）通过 `DECLARE_TSLGLOBAL_VAR` 宏声明的 TslGlobal 结构传入，该结构对 shader 与 C++ 侧同时可见。纹理采样用 `texture2d_sample<g_texture>(u,v)` 写进 shader，但真正的采样、过滤、缓存仍在 C++ 侧，TSL 通过回调委回宿主——shader 继续只负责"安排 BSDF 评估所需的信号"。

## 与 [[path-tracing-basics|路径追踪]] 集成的切入点

在 "spawn ray → 找交点 → 用材质构造 BSDF → 评估与重要性采样" 的循环里，TSL 插在第 3 步。核心收益是把硬编码材质（PBRT 里的模式）换成运行时可编译、可视化图形化作业的材质系统，而渲染器本身不需要重新编译。

## Sources

- [[sources/graphics-guy-tsl-shading-language]]
