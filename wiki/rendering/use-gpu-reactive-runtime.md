---
tags: [rendering, webgpu, reactive, engine-architecture]
date: 2026-04-19
sources: 2
---

# Use.GPU Reactive Runtime

[[steven-wittens]] 的 [Use.GPU](https://usegpu.live) 是一套基于 WebGPU 的声明式/响应式渲染运行时。核心哲学是把 shader permutation、binding 分配、pipeline 组装等原本发生在编译或离线 build 阶段的事全部搬到 run-time，用 reconciler（受 React 启发）把 draw call、buffer、pass 组织成一棵可增量更新的树。

## 核心抽象

- `<Pass>` 是"一次逻辑渲染"的顶层组件：接受 `lights`、`ssao={...}`、`overscan={...}` 这样的 flag，内部展开成一张 buffer + subpass 的有向图
- `<FooBuffer>` / `<FooPass>` 成对出现，前者只是 `<RenderTarget>` + data binding 的声明式 recipe，真正的 dispatch 在 pass 里
- pass 间通过"well-known names"（`normal`、`motion`、`depth` 等）自动接线，没有显式 input/output——理由是"如果要手接，只有一种正确接法，那就不该让用户接"

0.14 版本后还新增了 `<Pass overlay={true}>` 支持多 pass 串接，以及共享 Z-buffer 的 3D scene 合并。

## Binding 与 Shader Linker

Use.GPU 最初的设计目标是"每个 draw call 独立 shader"——所有 local binding 通过 `useShader(shader, [...args], defs)` hook 在声明时一并完成，不用先画 layout 再绑 data。pipeline/shader 的复用靠结构哈希在后台做：复用能省则省，复用不了也完全不 care。

WebGPU 只有 4 个 bind group。Use.GPU 0.13 用法是 `#0 View / #1 Pass / #2 Static / #3 Volatile`；0.14 把 View 并入 Pass，腾出 `#3` 给更传统的 sub-pipeline 风格——同 shader 模板、不同 texture/参数的大量 draw call 可以共享一套 bind group。Volatile bind group 的意义是承载"GPU 端自动轮转"的数据，例如 buffer history（见 [[ground-truth-ambient-occlusion]] 的 reprojection）和 just-in-time 分配的 atlas。

Shader linker 升级为能完整解析 `@binding` 与结构体类型（包括 `array<Light>` 这种跨模块可变数组），可以自动推导 minimum binding size。`useBindGroupLayout` 负责把这些片段打包成一个 static bind group，`useApplyPassBindGroup` 则让 pass 把自身数据延迟绑入——数据源可以模块化（lighting / shadow / SSAO 独立文件），而不是每个 pass 都得知道所有可能的 binding。

## WGSL 结构体即类型

`@use-gpu/shader` 的 `structType(...)` 可以在 run-time 生成 WGSL struct 类型，返回一个"带真实符号表的虚拟 shader 模块"。原始动机是绕 WebGPU "最多 8 个 storage buffer" 的硬限制：Plot API 要根据用户给的属性（每实例/每顶点/常量）把所有形状属性聚合进 struct，占一个 storage buffer 就够了。

这带来一个有趣的泛化：Use.GPU 的数据源格式可以写成 `T` 或 `array<T>`，其中 T 本身是一个 shader 模块。类型推断只发生在 link 阶段——binding 本身是 lazy、快速操作。对外暴露给用户的类型则尽量简洁：`TextureSource` / `StorageSource` / `LambdaSource`，它们自带绑定与访问所需的元数据。

## Inspector 与数据依赖图

Use.GPU 的 inspector 会显示整棵 reconciler 树，把 data / geometry / render / dispatch 这些 reconciler 节点作为不同过滤层展示，并依 component 间 data-dependency 高亮。Wittens 把它视作整套运行时的 "CT 扫描仪"：每一行都是一个普通函数调用，可以被当作 trace 点击。inspector 本身用 HTML+React 实现，比它要检查的 GPU 渲染还重——定位为开发工具，"关键是别的什么都崩了的时候它还能用"。

## 生态定位

WebGPU 在 2025-2026 仍未跨全平台普及，Use.GPU 因此只是小众工具，但在可控的客户内部项目里作用很强；社区例子涵盖 path tracer、voxel raytracer、3DGS 等。Wittens 把它视作 [[intent-vs-state|patch 驱动的数据流]] 在渲染层的投影：tree reconciler 负责把 declarative 的 `<Pass>` 配置 lower 成 concrete dispatch，一层套一层，代码与数据有相同形状。

## 相关

- [[ground-truth-ambient-occlusion]]
- [[render-pass-orchestration]]
- [[webgpu-intro]]
- [[intent-vs-state]]

## Sources

- [[sources/acko-occlusion-with-bells-on]]
- [[sources/acko-html-is-dead]]
