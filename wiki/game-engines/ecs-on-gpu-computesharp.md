---
tags: [ecs, gpu, compute-shader, svelto]
date: 2026-04-19
sources: 1
---

# 在 GPU 上跑 ECS 系统（Svelto × ComputeSharp）

[[sebastiano-mandala]] 2023 年的实验：把 Svelto.ECS 的 **component 存储层**直接接到 GPU compute buffer，让"ECS engine"变成"compute shader"。编译器走的是 [Sergio Pedri](https://github.com/Sergio0694/ComputeSharp) 的 ComputeSharp——一个把 C# 子集自动翻译成 HLSL compute shader 的开源项目（思路类似 DOTS Burst，只是目标换成 GPU）。

## 可扩展存储的钩子

Svelto 核心是 `SveltoDictionary`——一个可以把键值存储策略注入的 hashmap。真正存 component 的数据结构背后是 `IBufferStrategy`、`IBuffer<T>`、`ITypeSafeDictionary`、`IComponentBuilder` 四个接口。把这四个都重写一遍，就能让某一类 component 整体落在自定义内存里。本实验写了 `Svelto.ECS.ComputeSharp` 扩展，让标了 `IEntityComputeSharpComponent` 的 component 天生存在 `UploadBuffer<T>` / `ReadWriteBuffer<T>` 里。

EntityDescriptor 里照常声明：

```csharp
ExtendWith(new IComponentBuilder[] {
    new ComputeComponentBuilder<ComputeMatrixComponent>(),
    new ComputeComponentBuilder<ComputePositionComponent>(),
    new ComputeComponentBuilder<ComputeVelocityComponent>(),
    new ComputeComponentBuilder<ComputeSpeedComponent>(),
    new ComponentBuilder<MealInfoComponent>(),  // 普通 CPU component
    new ComputeComponentBuilder<ComputeSpeedComponent>(),
});
```

从此以后，每次 entity submission 这些 component 的数据会直接落到 GPU 可读的 upload buffer。

## Engine 写法

Svelto engine 的 Step 里把 component 数组的 `ToComputeBuffer()` 传给 `graphicsDevice.For(count, job)`；`job` 是一个带 `IComputeShader` 的 struct：

```csharp
[AutoConstructor] readonly partial struct ComputePositionFromVelocityJob : IComputeShader {
    public void Execute() {
        var i = ThreadIds.X;
        var d = _deltaTime * _speeds[i].speed;
        var v = _velocities[i].velocity;
        _positions[i].position += v * d;
    }
}
```

`ThreadIds.X` 意味着每个 GPU 线程处理一个 entity，天然并行。Demo 用这套方式替换了 `VelocityToPositionDoofusesEngine` 和 `ComputeTransformEngine`。

## 性能：学术示范，不是生产可用

实验只做了**第三种最不划算**的模式——同步 dispatch 之后立即 readback 到 CPU。20000 个矩阵的 `ComputeTransformEngine.Step` 平均 2.7 ms：

- 1.2 ms 等 shader 完成
- 0.8 ms 上传 CPU → GPU
- 0.6 ms 回读 GPU → CPU

对比纯 CPU（Stride 数据结构）版本 4.79 ms，小胜；但切到 System.Numerics（SIMD intrinsics）的 CPU 路径直接降到 2.43 ms，GPU 的优势就没了。结论：**"同步 dispatch + 同步 readback"永远不会赢**，GPU 的价值只有在流水线里真正异步化才兑现。

## 尚未解决的问题

Mandalà 明确列出想把这套做成生产可用需要先解决的点：
- **能不能和宿主引擎共享 compute buffer**（让结果直接喂 vertex/pixel shader，不用回读）？他不知道 ComputeSharp 是否支持
- **异步 dispatch + sync point 等待**：ComputeSharp 的异步 API 存在但缺文档
- **buffer resize**：demo 里预分配死容量，因为 Mandalà 不确定 resize compute buffer 是否安全
- `UploadBuffer<T>` / `ReadBackBuffer<T>` 是否真走零拷贝路径没有确认

这个实验的真正意义不是"ECS 该跑在 GPU 上"，而是**展示 Svelto 的 component 存储层足够解耦**：换个 `IBufferStrategy` 就能把同一份 component 换到任意后端（pinned memory、映射文件、compute buffer 甚至跨进程共享内存）——这是 [[aos-vs-soa|SoA 布局]]的延伸价值。

## Sources

- [[sources/sebaslab-ecs-on-gpu-computesharp]]
