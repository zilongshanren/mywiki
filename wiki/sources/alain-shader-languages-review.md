---
tags: [source, 渲染, 着色器, HLSL, GLSL, MSL, WGSL, SPIR-V, 编译]
date: 2026-04-27
sources: 1
---

# A Review of Shader Languages（Alain Galvan / alain.xyz）

[[people/alain-galvan]] 发表于 2022 年 2 月的文章，对 HLSL、GLSL、MSL、WGSL 四种主流实时渲染着色器语言进行系统对比，覆盖顶点着色器与计算着色器两类典型用例，以及离线编译和跨语言转译工具链。

## 摘要

文章首先厘清 shader 的执行模型：在 SIMD 架构上以 wavefront（AMD 32/64 work-items）或 warp（NVIDIA）为单位执行相同指令。四种语言均以 C 为基础，共享向量数学和超越函数等内建函数，差异主要体现在：采样器与纹理是否分离（HLSL/MSL/WGSL 分离，GLSL 耦合）、I/O 声明方式（GLSL 用全局 `in/out`，MSL/HLSL 用函数参数，WGSL 用 `@location` 装饰器）和绑定模型。IR 层面：HLSL → DXIL（DirectX 12）/ DXBC（DX11），GLSL/HLSL → SPIR-V（Vulkan），MSL → 私有 AIR，WGSL → 经 naga/tint 转出 SPIR-V。实践建议：尽量离线编译到目标 IR；跨平台可用 SPIRV-Cross 互转；AMD RDNA2 ISA 和 NVIDIA PTX 是理解 shader 最终执行形态的参考。

## 关键要点

- GLSL 采样器-纹理绑定耦合是与其他语言的最大设计差异，影响大规模绑定架构
- HLSL 的语义标注（`:POSITION` 等）兼具绑定槽位声明功能，不只是注解
- WGSL 的类型语法更显式（`vec4<f32>` vs `float4`），设计面向 Web 沙箱安全
- Slang 作为 HLSL 超集/后继被提及，可编译至 GLSL/HLSL/SPIR-V
- AMD 在 RDNA2 中将 DXIL 的 AABB/triangle 相交指令映射到专用 ASIC 硬件（与加速结构构建侧呼应）
- DirectX Shader Compiler（dxc）同时支持 DXIL 和 `-spirv` 输出，已取代旧版 FXC

## 链接到的概念

- [[rendering/shader-ir-pipeline]]
- [[game-engines/slang-shader-language]]
- [[rendering/graphics-api-history]]
- [[rendering/bvh-traversal-hardware]]

## 原文

- 链接：https://alain.xyz/blog/a-review-of-shader-languages
- 本地：`raw/articles/alain.xyz/2022-02-12_a-review-of-shader-languages.md`
