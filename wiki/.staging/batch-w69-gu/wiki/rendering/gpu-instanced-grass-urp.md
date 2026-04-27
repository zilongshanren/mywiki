---
tags: [grass, gpu-instancing, indirect-draw, compute-shader, frustum-culling, unity, urp, shader-graph]
date: 2026-04-19
sources: 1
---

# URP + Shader Graph 的 GPU 实例化草地

[[cyanilux|Cyan]] 2025 年 10 月那篇《GPU Instanced Grass Breakdown》把他 2021 年在 FAQ 页丢过的一小段 demo 重写成了一篇完整的分段教程。和 [[gpu-driven-grass-tiles|Marco Giordano 的自研引擎版本]] 是同一个问题（一片实时草 + GPU 剔除）但彻底不同的技术栈——Cyan 的版本**完全站在 Unity URP + Shader Graph 的约束里**：用 `Graphics.RenderMeshPrimitives` / `RenderMeshIndirect` 下发实例、用 [[shader-graph-custom-function-hlsl|Shader Graph Custom Function]] 把 HLSL 缝进图里访问 `StructuredBuffer`、再加一个 compute shader 做 GPU frustum 剔除。主要价值是**把一堆 Unity 版本差异（2021.2 前、2022 后、Unity 6）的坑一次性讲清**。

## 为什么是 GPU Instancing，而不是 SRP Batcher

Unity 自己的引导是：绝大多数场景应该靠 [[srp-batcher-cbuffer|SRP Batcher]] 拉平 draw call——它优化的是"同 shader、不同模型"的常见情况。但是草的特征正好相反：**同一个 mesh、同一个材质，只是矩阵不同，数量以百万计**，这种拓扑下 GPU Instancing 才是合适的形状。Cyan 也承认 [`BatchRendererGroup`](https://docs.unity3d.com/ScriptReference/Rendering.BatchRendererGroup.html) 可能更快，但 setup 更复杂，所以这篇不碰。

三条 Unity 版本线索值得单独记住：

- **2021.2** 引入 `Graphics.RenderX` 系列函数替换旧的 `DrawX`。新旧的映射很直接：`DrawMeshInstancedProcedural` → `RenderMeshPrimitives`，`DrawMeshInstancedIndirect` → `RenderMeshIndirect`，名字里的 "Procedural" 被改成 "Primitives"。
- **2022** 起旧 `DrawX` 被标为 obsolete。
- **Unity 6** 改了 **Instance ID** 节点的语义——以前它吐的是 `unity_InstanceID`，要靠 "procedural instancing path" 这种别扭的 pragma 组合才能正常工作；现在它直接挂在 `SV_InstanceID` semantic 上，不用再强行走 procedural 路径了。但代价是 graph 里的 Object 空间变成了**相对于 bounds**，不再是**相对于每个 instance**——也就是说矩阵变换要自己在 Custom Function 里用 `mul()` 做。

## Procedural vs Indirect 的分工

两个 API 对应两种 "instance 数量控制权"：

- **`RenderMeshPrimitives`（procedural）**——instance count 由 CPU 指定并写在 `Update()` 调用里。适合你在 C# 端就知道草的总数。
- **`RenderMeshIndirect`（indirect）**——instance count 存在一个 GPU 上的 **indirect args buffer** 里（`IndirectDrawIndexedArgs`：index count / instance count / start index / base vertex / start instance 五个 uint），让 compute shader 直接改这个数。这是做 [[view-frustum-culling-ryg|GPU 端剔除]] 的前置条件——因为剔除后的"要画的数量"只有 GPU 才知道。

Cyan 的教程按这个顺序推进：先搭 procedural 的最小骨架看到草出现，再加可选功能（编辑器可见、地形绑定、分 cell、风摆），再切到 indirect，最后加 compute frustum cull。每一步都还能跑起来，这个增量路径本身就是教学设计的样本。

## Shader Graph 端：Custom Function 把 `StructuredBuffer` 接进来

核心矛盾是 Shader Graph 不能直接声明 `StructuredBuffer<InstanceData>`。解决方式是一个 File 模式的 Custom Function 节点，指向一个 `.hlsl` 文件；文件里声明 buffer，并暴露一个 `Instancing_float(Position, InstanceID, out OutPosition, out OutNormal)` 函数给图调用——这个函数内部 `mul(data.m, float4(Position, 1))` 把 object space 位置打到 world space，同时用 `(0,1,0,0)` 方向的法线跟上。Instance ID 端口连接 Shader Graph 的 **Instance ID** 节点（Unity 2021.2+）或者在 Unity 6 之前走 "procedural instancing path" 的 hack——那个 hack 的逻辑是：

```hlsl
// String 模式的 Custom Function 节点
Out = In;
#pragma multi_compile _ PROCEDURAL_INSTANCING_ON
#pragma instancing_options procedural:InstancingSetup
```

`instancing_options` pragma 必须在主 shader 里（include 文件里无效），所以这段必须放进 String 模式节点。配合 File 模式节点里实现的 `InstancingSetup()` 函数——它在 `#if UNITY_ANY_INSTANCING_ENABLED` 里改写 `unity_ObjectToWorld` / `unity_WorldToObject` 矩阵，让 graph 原生的 Object↔World 变换自动带上每个 instance 的偏移。Unity 6 之后这一整套可以扔掉。

`InstanceData` 的 C#/HLSL layout 要对齐——Cyan 给的经验准则是**"从大到小、全用 float4x4 和 float4，不用 float3"**，因为不同图形 API 对结构体 pad 的处理不一样，混用 float3 会炸。

## 五个可选增强

1. **编辑器可见**——`[ExecuteAlways]` 加在 MonoBehaviour 上。但 `OnValidate` 用来检测 inspector 改动会泄漏资源（Unity 会从其他线程调它），所以改用 `[CustomEditor]` 加一个 "Refresh" 按钮、按钮里 `OnDisable` + `OnEnable` 重建 buffer。
2. **Terrain 绑定**——用 `terrain.SampleHeight` 抬高 y，用 `terrainData.GetInterpolatedNormal` 拿法线，然后用 `Quaternion.LookRotation(forward, normal)` 对齐草到地形斜面。法线还可以存进 InstanceData，在 shader 里把光照也按地形法线算——让草"融进地形"而不是像糖葫芦一样戳在上面。
3. **分 cell**——把 instance 按 xz 网格组织，而不是全局 random。对后面的 GPU culling 更友好，也让分布更均匀。
4. **只在 grass layer 生成**——读 `terrainData.GetAlphamaps(0, 0, w, h)`，第三维是 TerrainLayer 索引，查 `grassLayerIndex` 对应通道的权重 > 0.5 才生成。alphamap 就是 [[terrain-splatmap-shader-graph|地形 splatmap]]——只是 Unity 把每个 TerrainLayer 的权重打包进不同通道。
5. **风摆**——Time → Sine 节点在 Custom Function **输出后**做 vertex offset。Cyan 强调：Unity 6 里一定要加在 output，不能加在 input，否则 displacement 是按每 instance 的 object 空间算的，风向会随机。这和 [[waving-grass-shader-vertex-offset|Linden Reid 的世界空间风场]] 是同一条经验的另一种形态——共享风必须在共享空间里采样。

## Compute 端的 Frustum Culling

剔除的形状是：

- 一个 `AppendStructuredBuffer<uint> _VisibleIDsAppend`，存活 instance 把自己的原始 index append 进去。
- Compute kernel 把 instance 位置（从矩阵的 `_m03_m13_m23` 取）变换到 clip space：`mul(mvp, pos)`。clip space 的可见性判定很清爽——XYZ 分量 `abs()` 后都小于等于 W 就是在视锥里，因为 OpenGL 约定下 viewport 是 `[-W, W]` 的立方体。作者特意在 XY 上加了 `abs <= w * 1.1 + 0.5` 的 padding，避免屏幕边缘 pop-in。
- `GraphicsBuffer.CopyCount` 把 append buffer 的 **hidden counter** 复制到 indirect args 的 instance count 字段（偏移 `1 * sizeof(uint)`）。**这一步 GPU 内完成，不回 CPU**，否则等于把并行的意义让出去。
- Shader 里 instance 数据查询改成两级索引：`_PerInstanceData[_VisibleIDs[SV_InstanceID]]`。

两个踩坑细节值得单独记：

- **`SetCounterValue(0)` 必须每帧调**，否则 `Append()` 会继续往后挪写指针，不是不 append 而是 append 到已有数据之后——一段时间后 indirect args 的 instance count 会大到开始越界。
- `[numthreads(64, 1, 1)]` 的 64 是 AMD wavefront 的最小代数；NVIDIA 是 32。选 64 是向下兼容——维持满 occupancy。

## `startInstance` 和 `UnityIndirect.cginc`

如果 indirect args 的 `startInstance` 不是 0（想复用一个大 buffer 画不同段），不同图形 API 的行为会分叉：Vulkan / WebGPU 把 offset 烘进了 `SV_InstanceID`，Direct3D 不烘。Unity 2021.2+ 通过 `UnityIndirect.cginc` 的 `GetIndirectInstanceID_Base(svInstanceID)` 把这个差异藏起来——但文档几乎没人提 `_Base` 版本。Cyan 顺手吐槽 Unity 官方的 `RenderPrimitivesIndirect` 示例代码里用的是 `GetIndirectVertexID` 而不是 `_Base` 版本，**只有在 startIndex 为 0 且用 submesh 0 时才对**。这是官方文档的一个错误。

## 和相关方案对比

- [[gpu-driven-grass-tiles]]——Marco Giordano 自研 Vulkan/DX12 + mesh shader，全 GPU driven，技术天花板高；Cyan 这套是**在 Unity URP 既有 SRP 里尽量 GPU driven 的实用折衷**。
- [[waving-grass-shader-vertex-offset]]——Linden Reid 讲的是单株草的风场共享，不涉及 instance 管线。但两篇合起来覆盖"一个 mesh 的可视动画 × 百万 instance 的渲染管线"两个维度。
- [[multidraw-indirect-occlusion-culling]]——multi-draw indirect + occlusion cull 的 web/D3D12 思路，概念同构但 API 栈不同。
- [[compute-shader-dispatch-ids]] / [[view-frustum-culling-ryg]]——compute shader 的 dispatch id 语义和视锥测试是这套方案的底层基础。
- [[shader-graph-custom-function-hlsl]]——Custom Function 挂 HLSL 的约定，Shader Graph 的万能逃生舱。
- [[terrain-splatmap-shader-graph]]——教程里"只在 grass layer 生成"一节用到的 alphamap。

## Sources

- [[sources/cyanilux-gpu-instanced-grass]]
