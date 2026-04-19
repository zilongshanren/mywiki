---
tags: [source, ecs, svelto, gpu, compute-shader]
date: 2026-04-19
sources: 1
---

# Svelto ECS 3.4 internals: How to run ECS systems on the GPU（Sebastiano Mandalà / Seba's Lab）

[[sebastiano-mandala]] 2023 年 3 月的实验性长文，演示如何把 Svelto.ECS 的 component 存储切到 GPU compute buffer，让 engine 以 compute shader 形式直接在 GPU 上跑。

## 摘要

实验的目标不是"ECS 该跑在 GPU 上"，而是**展示 Svelto 的存储层完全可插拔**——Svelto 的核心 `SveltoDictionary` 允许注入 `IBufferStrategy`，把 component 存到任意后端。作者借助 Sergio Pedri 的 [ComputeSharp](https://github.com/Sergio0694/ComputeSharp)（把 C# 子集翻译成 HLSL 的开源编译器）写了 `Svelto.ECS.ComputeSharp` 扩展：实现 `IBufferStrategy`、`IBuffer<T>`、`ITypeSafeDictionary`、`IComponentBuilder` 四个接口，标了 `IEntityComputeSharpComponent` 的 component 数据会直接落到 `UploadBuffer<T>` / `ReadWriteBuffer<T>` 里。engine 的 `Step` 把这些 buffer 传给 `graphicsDevice.For(count, job)`，job 是带 `IComputeShader` 的 struct，用 `ThreadIds.X` 做线程索引。demo 把 `VelocityToPositionDoofusesEngine` 和 `ComputeTransformEngine` 搬到 GPU，20000 个矩阵变换在 GPU 上 2.7ms（其中 1.2ms 等 shader、0.8ms 上传、0.6ms 回读），CPU（Stride）版本 4.79ms，但换用 System.Numerics 的 SIMD 版本只要 2.43ms——说明在同步 dispatch+同步 readback 的模式下 GPU 优势不明显。作者列出要做生产可用还需要解决的问题：能否和宿主引擎共享 compute buffer、异步 dispatch+ sync point、compute buffer resize、UploadBuffer 是否零拷贝。

## 关键要点

- Svelto 核心的 `SveltoDictionary` 存储可插拔；四个接口组合就能换后端
- ComputeSharp 自动把 C# 子集编译成 HLSL compute shader，`ThreadIds.X` 即线程索引
- Engine 的 `Step` 用 `graphicsDevice.For(count, computeShaderJob)` 启动 dispatch
- Demo 模式是"同步 dispatch + 同步 readback"——性能最差的模式，只是学术示范
- 20000 矩阵 GPU 2.7ms / CPU Stride 4.79ms / CPU System.Numerics 2.43ms：SIMD 把 CPU 追上来了
- 要变生产可用需要解决：共享 buffer、异步 dispatch、resize、零拷贝 upload

## 链接到的概念

- [[ecs-on-gpu-computesharp]]
- [[svelto-ecs]]
- [[sebastiano-mandala]]

## 原文

- 链接：https://www.sebaslab.com/svelto-ecs-3-4-internals-how-to-integrate-computesharp/
- 本地：`raw/articles/sebaslab.com/2023-03-31_svelto-ecs-3-4-internals-how-to-run-ecs-systems-on-the-gpu-s.md`
