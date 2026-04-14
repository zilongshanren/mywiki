---
tags: [渲染, gpu, api, webgpu, wgsl, 跨平台, compute]
date: 2026-04-14
sources: 1
---

# WebGPU 与 WGSL 入门

**WebGPU** 是 W3C 和各大浏览器厂商合作制定的新一代 GPU 图形与计算 API，定位上**取代 WebGL** 成为 web 端的图形标准，但设计语言直接对齐 Vulkan / D3D12 / Metal 这一代现代底层 API。它对 web 并不仅仅是"WebGL 2.5"——真正重要的变化有三个：**低层级资源绑定**、**原生 compute shader**、以及一门新的着色语言 **WGSL（WebGPU Shading Language）**。[[xor-shader-artist|Xor]] 在 GM Shaders 的入门短文里从 GameMaker 用户的视角给出了一个浓缩概览，顺便点明它对非 web 引擎也有意义——GameMaker 的新 runtime 将使用 WebGPU 作为底层。

## 为什么 web 需要一个新 API

WebGL 本质上是 OpenGL ES 2/3 的子集，为「单线程、同步、driver 隐藏一切」的 2010 年代设计。而现代 GPU 编程的核心诉求已经变成：**让驱动做更少的判断、让应用显式管理资源**。WebGPU 学了这条思路，具体体现是：

- **显式的 pipeline state**：把 shader 阶段、光栅化、blend、depth/stencil 等所有状态打包成一个不可变的 `GPURenderPipeline`，提交时只做合法性验证而非每次 draw call 反复 patching。
- **uniform / storage buffer + bind group**：数据通过 `@group(x) @binding(y)` 显式绑定，不再依赖「按名称查 uniform location」的隐式查询；storage buffer 允许大块、可读可写、甚至 GPU 侧跨 kernel 共享。
- **compute shader 原生支持**：不依附于 pixel/vertex 阶段，可以用于粒子/流体模拟、图像滤波、机器学习推理等不再是「画三角形」的任务。
- **跨平台抽象**：Chrome/Edge 实现走 D3D12，Firefox/Chrome 在 Linux 走 Vulkan，Safari 走 Metal——应用写一套代码，映射层负责把 WebGPU command encoder 翻译成对应底层命令。对于游戏引擎开发者，这等于一次性解决了**一个 API 三套平台后端**的老问题。

## WGSL：类 Rust 风格的新着色语言

WebGPU 不再沿用 GLSL。WGSL 的语法参考了 Rust/Swift，比 GLSL 严格得多，**在离线阶段就做完类型检查与大部分验证**，避免了 WebGL 时代不同 GPU 驱动对 GLSL 解析结果略有差异的顽疾。

几项基础特征：

```wgsl
var a: f32;                 // 32-bit float
var b = 50f;                // 用后缀初始化
let d = 8u;                 // let = 常量
var e: vec2<f32>;           // 向量必须指定元素类型
var f = vec3f(50);          // vec3f 是 vec3<f32> 的别名
```

- **四种核心标量**：`f32` / `i32` / `u32` / `bool`。`var` 可变、`let` 不可变。
- **函数**用 `fn` 定义，参数和返回值都要写类型，返回类型用 `->` 指示。
- **主入口**通过 `@vertex` / `@fragment` / `@compute` 注解标注，输出用 `@builtin(position)` 或 `@location(i)` 明示语义。
- **资源绑定**显式写 `@group(0) @binding(0) var<uniform> u: vec2f`，没有隐式 uniform block；I/O 变量也靠 `@location(i)` 匹配相邻 shader 阶段。
- **原生 64 位暂不支持**：只有抽象字面量层面的高精度，变量类型实际全部 32 位。

相比 GLSL，WGSL 的"啰嗦"换来的是**跨设备一致性**：以前 GLSL 代码能在 NV 跑但在 Intel 炸的情况在 WGSL 里会被提前拒绝。对于库作者和引擎维护者，这是一笔相当划算的交易。

## 为什么 GameMaker / 游戏引擎用户也要关心

Xor 的切入角度更贴地气——他代表的是"被困在 GLSL 1.00 多年、连 texelFetch 都没有"的那一群用户。对他们来说，WebGPU 带来的最实际好处不是 web 平台，而是**终于可以用 compute shader 做真正并行的非 raster 任务**：粒子系统、流体、形态学滤波、甚至 CPU 侧的暴力数组计算全都可以甩给 GPU。许多小引擎此前用纹理当"数据 buffer"、用 fragment shader 做 GPGPU 的技巧（[[gpgpu-json-parsing]] / [[gpgpu-string-unescaping]]）本质都是"没有 compute shader 的 workaround"，WebGPU 落地后都可以正常写了。

GameMaker 宣称会在 runtime 层把 GLSL 自动翻译成 WGSL，这也是大多数引擎的过渡方案——用户不必立刻改写 shader，但在新 API 的加持下才能解锁 compute、storage buffer、显式资源绑定这些之前够不着的能力。

## 现状与注意事项

- **尚未完全稳定**：2024 年初部分浏览器仍把 WebGPU 放在 origin trial 或 flag 后面，规格虽进入 Candidate Recommendation 阶段但仍有 API 细节在调整。
- **学习曲线**：从命令式 GL 到「显式 pipeline + command encoder + bind group」是一次思维转变，和 Vulkan/D3D12 的心智代价类似（虽然比它们小一圈）。
- **最佳入门**：MDN 的 [WebGPU API 指南](https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API) + Google 的 [Tour of WGSL](https://google.github.io/tour-of-wgsl/) 基本够用；更多实战可以对照 WebGPU samples 仓库里的 compute / render 模板。

## 相关

- [[rendering-api-depth]] —— 现代图形 API 的层级与对齐
- [[d3d12-resource-binding]]
- [[metal-api-overview]]
- [[fragment-shader]]
- [[compute-vs-raster-points]] —— compute shader 对比 raster 的一个具体场景
- [[gpgpu-json-parsing]]
- [[gpgpu-string-unescaping]]
- [[gpgpu-transform-feedback-ios]]
- [[shaderlab-hlsl-basics]]
- [[xor-shader-artist]]

## Sources

- [[sources/xor-mini-webgpu]]
