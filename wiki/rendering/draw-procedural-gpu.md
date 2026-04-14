---
tags: [渲染, gpu, compute, unity, draw-call, instancing]
date: 2026-04-14
sources: 1
---

# GPU-driven 绘制：Graphics.DrawProcedural 与 StructuredBuffer

`Graphics.DrawProcedural`（及其姊妹方法 `DrawProceduralIndirect`）是 Unity 暴露出来的**最接近底层 GPU 绘制命令**的 API：它允许一次性发起一个 draw call，但**不传入 mesh、不传入 transform、不使用 `GameObject`**，全部顶点数据由 shader 自己从 `StructuredBuffer` 里读取。这是一种典型的 **GPU-driven rendering** 入口——CPU 只下达「画 N 个三角形」，而「三角形长啥样、在哪儿」完全由 GPU 上驻留的数据决定。

## 动机：CPU-GPU 拷贝是敌人

常规做法是：compute shader 算出一堆位置 → CPU 用 `ComputeBuffer.GetData` 读回 → 挨个 `GameObject.transform.position = ...`。每一步都在**把数据从 VRAM 搬回 RAM 再搬回去**，并且为每个物体付出一份 `GameObject` 的抽象成本。Ronja 的这篇教程直接把这个流程打穿：位置留在 VRAM、mesh 数据也塞进 VRAM、shader 从 VRAM 直接读出来用——**整条路径上没有任何一次回拷**。相应的权衡是：你失去了 Unity 的 `Transform`、`Collider`、`MeshRenderer` 这一整套引擎设施，必须自己处理视锥剔除、物理、交互。

## 关键结构：三个 ComputeBuffer

教程里示范了最小可用版本：`SphereAmount` 个球体，每帧位置由 compute shader 决定，然后一次 draw call 全部画出来。

需要三个 `ComputeBuffer`：

1. **`SphereLocations`** (`RWStructuredBuffer<float3>`)——由 compute kernel 每帧写入每个实例的位置。`RW` 是因为 compute 既读又写。
2. **`Triangles`** (`StructuredBuffer<int>`)——mesh 的 index buffer，只读。每 3 个整数是一个三角形。
3. **`Positions`** (`StructuredBuffer<float3>`)——mesh 的顶点位置数组，只读。`StructuredBuffer`（非 `RW`）的好处是 shader 能更激进地优化读取。

后两个 buffer 在 `Start()` 里从一个普通 `Mesh.triangles`/`Mesh.vertices` 上传一次——**数据源甚至不必是真的 mesh**，只要是合法的索引 + 位置数组就行。这为程序化几何（voxel meshing、marching cubes、动态 LOD）打开了大门。

## DrawProcedural 的调用形态

```csharp
Graphics.DrawProcedural(
    Material,
    bounds,          // 用来给 frustum culling
    MeshTopology.Triangles,
    meshTriangles.count,   // vertex count（不是三角形数！）
    SphereAmount           // instance count
);
```

几个关键参数：

- **`bounds`**：因为引擎不知道你会画到哪里，必须手动给一个 AABB 用来剔除。太小会误剔（物体看不到），太大会浪费 GPU。教程里直接给一个原点半径 20 的方盒——简单暴力，但必须和 compute kernel 的坐标范围对齐。
- **`vertexCount = triangles.length`**：注意这是**顶点次数**，等于三角形数 × 3。DrawProcedural 会把 `SV_VertexID` 从 0 跑到这个数。
- **`instanceCount`**：走一次 instancing，每个 instance 重跑同样的顶点调用，但 `SV_InstanceID` 不同。

## Vertex Shader 的角色完全变了

常规 vertex shader 从 mesh 拿 `POSITION` / `NORMAL` / `TEXCOORD` 数据。用 DrawProcedural 时 **vertex shader 的输入只有两个整数**：

```hlsl
float4 vert(uint vertex_id: SV_VertexID, uint instance_id: SV_InstanceID) : SV_POSITION {
    int idx = Triangles[vertex_id];            // 查三角形索引
    float3 p = Positions[idx];                 // 查顶点位置
    p += SphereLocations[instance_id];         // 加上 instance 偏移
    return mul(UNITY_MATRIX_VP, float4(p, 1)); // 手动 MVP
}
```

- **没有 `appdata` / `v2f` 结构**——因为没有 mesh 属性可往里填。
- **`UnityObjectToClipPos` 被手动拆开了**。它内部做的是 `UNITY_MATRIX_VP * unity_ObjectToWorld * v`。这里因为 object 到 world 的概念已经不存在，内层 `unity_ObjectToWorld` 被 `SphereLocations` 的加法取代——每个 instance 自己的「object 到 world」就是一个位置偏移。
- **缺少 normal 意味着没有光照**——教程里直接只发射纯色。要做光照得把 normal 也塞进一个 buffer。

这里暴露出的事实是：Unity 的整套 VP 矩阵宏只是把标准管线打包了一下，一旦你走 procedural 路径就必须自己实现同等逻辑。

## 和 Compute Shader 的协作节奏

完整节奏是：

1. **Start** 一次：准备 mesh buffers、分配 result buffer、连接 compute 的输出和 material 的输入到**同一个** `ComputeBuffer`。
2. **Update** 每帧：`Shader.Dispatch(...)` 让 compute 写 `SphereLocations`；`Graphics.DrawProcedural(...)` 立刻把它画出来。数据**从未离开 VRAM**。
3. **OnDestroy**：`Dispose()` 每个 buffer——Unity 的 `ComputeBuffer` 是非托管资源，忘记 dispose 会泄漏。

一个细节：**同一个 `ComputeBuffer` 既是 compute 的输出又是 material 的输入**——这是 GPU-driven 鞍点的典型写法。数据的生命周期是 `Dispatch → DrawProcedural → Dispatch → DrawProcedural` 这样的循环，只要保证 draw 发生在 dispatch 之后即可（两者都在同一条 CommandBuffer 上，顺序天然保证）。

## 更广阔的图景

DrawProcedural 是一家子 API 的最简入口：

- **`DrawProceduralIndirect`**：进一步把「画多少个」也放到 GPU buffer 里，CPU 连 instance count 都不必知道。这是 [GPU culling → GPU-driven pipelines](https://advances.realtimerendering.com/s2015/aaltonenhaar_siggraph2015_combined_final_footer_220dpi.pdf)（参见 [[gpu-hazard-tracking]] 里的现代管线话题）的关键。
- **`DrawMeshInstancedIndirect`**：给一个真 mesh + 一个 instance buffer，仍然省掉 per-instance 的 CPU 逻辑。比 DrawProcedural 保留更多 Unity 语义（mesh、subshader LOD），但没那么自由。
- **Unity BRG（BatchRendererGroup）**：更高层的抽象，2022+ 上 ECS / DOTS 渲染路径用的就是这个。

把这些 API 组合起来就能做「CPU 只启动一次、剩下全在 GPU 自循环」的渲染系统——现代 [[custom-srp|自定义 SRP]] 和大规模植被 / 粒子 / 体素系统的基础。

## 相关

- [[draw-call]]
- [[compute-vs-raster-points]] —— 另一种 GPU-only 渲染路径的权衡
- [[batching]]
- [[custom-srp]]
- [[gpu-fence-timeline-semaphore]]
- [[fragment-shader]]
- [[procedural-rendering-ps2]] —— PS2 时代另一种意义上的 procedural rendering

## Sources

- [[sources/ronja-draw-procedural]]
