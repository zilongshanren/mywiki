---
tags: [渲染, 着色器, HLSL, GLSL, MSL, WGSL, SPIR-V, DXIL, 编译, shader-language]
date: 2026-04-27
sources: 1
---

# 着色器语言与 IR 编译链

[[people/alain-galvan|Alain Galvan]] 2022 年发布的着色器语言综述文章对 HLSL、GLSL、MSL、WGSL 四种主流实时渲染着色器语言从语法特征、编译链到 IR 做了系统比较。此页面补充 [[game-engines/slang-shader-language|Slang]] 等更高层抽象的背景。

## 四大着色器语言对比

| 语言 | 对应 API | 主要 IR | 特征 |
|------|----------|---------|------|
| HLSL | DirectX | DXIL / DXBC | 语义系统（Semantics）；分离采样器与纹理；支持 `#include`、命名空间 |
| GLSL | Vulkan / OpenGL | SPIR-V | 采样器与纹理绑定耦合；全局 `in/out` 变量；`layout` 声明 |
| MSL | Metal | 私有 ISA | 无 `uniform` 关键字；I/O 通过函数参数；`kernel` 标记 Compute shader |
| WGSL | WebGPU | 内部 IR | 语法混合 Rust/MSL/HLSL；类型更显式（如 `vec4<f32>`） |

所有着色器语言均以 C 为基础，共享向量数学、超越函数、GPU 内存同步等内建函数（名称有细微差异，如 `frac` vs `fract`）。

## 中间表示（IR）体系

着色器源码到 GPU 硬件机器码的路径：

```
HLSL ──dxc──► DXIL ──AMD driver──► RDNA ISA
HLSL ──dxc -spirv──► SPIR-V
GLSL ──glslang──► SPIR-V ──AMD/NV/Intel driver──► 硬件 ISA
MSL  ──metallib──► AIR ──Metal driver──► GPU ISA
WGSL ──naga/tint──► SPIR-V / HLSL / MSL
```

**SPIR-V Cross** 可在 SPIR-V 与 HLSL/GLSL/MSL 之间互转，是跨平台着色器分发的常用工具。

## 离线编译的重要性

应尽可能在构建期将着色器编译至目标 IR，避免运行时编译卡顿。主要工具：

- **DirectX Shader Compiler（dxc）**：同时支持 DXIL 输出和 `-spirv` 标志输出 SPIR-V
- **GLSLang Validator**：Khronos 官方 GLSL 前端，支持 GLSL → SPIR-V
- **metallib**：macOS 内置 Metal 编译器
- **Mozilla Naga**（Rust）/ **Google Tint**：两种 WGSL 编译器

## 设计差异要点

- **采样器绑定**：GLSL 将纹理与采样器绑定为一体（`sampler2D`），HLSL/MSL/WGSL 将二者分离——这对大规模绑定模型设计影响显著
- **Metal 输入模型**：I/O 通过函数参数而非全局变量，更接近普通函数，可读性更好
- **语义标注（HLSL Semantics）**：`float3 pos : POSITION` 的 `: POSITION` 不仅是注解，还充当绑定槽位声明，兼具 bitfield 语义
- **WGSL 显式类型**：`vec4<f32>` 而非 `float4`，类型更严格，对 WebGPU 沙箱安全有益

## Sources

- [[sources/alain-shader-languages-review]]
