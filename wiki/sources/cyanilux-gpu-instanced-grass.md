---
tags: [source, unity, urp, shader-graph, grass, gpu-instancing, compute-shader]
date: 2026-04-19
sources: 1
---

# GPU Instanced Grass Breakdown（Cyanilux）

[[cyanilux|Cyan]] 2025 年 10 月发的分段教程，把他 2021 年在 FAQ 页贴过的那段 `DrawMeshInstancedProcedural` demo 重写为完整的分版本（Unity 2021.2 前 / 2022+ / Unity 6）走读——从 `Graphics.RenderMeshPrimitives` 的基础骨架、Shader Graph 侧用 Custom Function 接入 `StructuredBuffer<InstanceData>`、可选的 Terrain 绑定 / 分 cell / 风摆增强、切到 `RenderMeshIndirect` 的间接绘制、最后用一个 compute shader 在 clip space 做 GPU frustum culling，并用 `GraphicsBuffer.CopyCount` 把"存活数量"不经 CPU 回传地写进 indirect args。

## 摘要

全文围绕"在 Unity URP + Shader Graph 的约束下尽量 GPU driven 地画草"展开，是**实用教程**而非架构设计文——教学设计上刻意做成"每小节停下都能跑"的增量式推进。技术重点是三条：(1) **Shader Graph + `StructuredBuffer` 怎么接通**——Custom Function 的 File 模式 + Unity 6 前靠 `procedural:InstancingSetup` pragma / Unity 6 后直接用 Instance ID 节点；(2) **`RenderMeshIndirect` 的 indirect args buffer 怎么被 compute shader 改写**；(3) **`UnityIndirect.cginc` 里文档几乎没人提的 `_Base` 版本函数**——跨 Vulkan/WebGPU 和 D3D 的 `SV_InstanceID` 语义差异被 Unity 藏进 `GetIndirectInstanceID_Base`，文章顺带指出官方示例里用错的地方。此外有两个易踩的坑值得独立记：`AppendStructuredBuffer` 的 hidden counter 每帧都要 `SetCounterValue(0)` 否则 instance count 会越界；`InstanceData` 结构体的 field 要按"从大到小、全 float4/float4x4"排布，否则不同图形 API 的 padding 差异会炸。

## 关键要点

- `Graphics.DrawMeshInstancedProcedural` → 2021.2 后改名 `RenderMeshPrimitives`；`DrawMeshInstancedIndirect` → `RenderMeshIndirect`，2022 起旧函数 obsolete。
- Unity 6 的 **Instance ID** 节点行为变了：从吐 `unity_InstanceID`（需要走 "procedural instancing path"）改为直接挂 `SV_InstanceID` semantic；代价是 graph 里 Object 空间变成相对 bounds，矩阵变换要自己在 Custom Function 里 `mul()`。
- Custom Function 的 File 模式用 `_float` / `_half` 后缀、`out` 参数表传出值，文件头用 `#ifndef`+`#define` 头卫防重复 include。
- `InstanceData` 必须跨 C# / HLSL 对齐——"从大到小 + 只用 float4 / float4x4" 避开不同图形 API 的 padding 差异。
- 可选增强：`[ExecuteAlways]` 让草在编辑器里出现；用 Terrain 的 `SampleHeight` 和 `GetInterpolatedNormal` 贴地形并继承法线；按 xz 网格分 cell 让分布更均匀且对 culling 更友好；`TerrainData.GetAlphamaps` 读 splatmap 第 3 维的 layer 权重只在 grass layer 生成；风摆一定放在 Custom Function 的**输出**后做 vertex offset，否则在 object 空间里每 instance 风向各自一套。
- Indirect 需要一个 5 uint 的 indirect args buffer（`IndirectDrawIndexedArgs`：`indexCountPerInstance` / `instanceCount` / `startIndex` / `baseVertexIndex` / `startInstance`），compute shader 通过 `GraphicsBuffer.CopyCount(appendBuffer, indirectBuffer, 1*sizeof(uint))` 更新第二项。
- Frustum culling 在 clip space 做——`abs(pos_cs.xyz) <= pos_cs.w` 就是在视锥里；XY 加 `* 1.1 + 0.5` padding 避免屏幕边缘 pop-in。
- `[numthreads(64, 1, 1)]` 的 64 匹配 AMD wavefront，NVIDIA 是 32；选 64 向下兼容、不浪费 occupancy。
- `SetCounterValue(0)` 每帧必须调；`_VisibleIDs[SV_InstanceID]` 作为两级索引替代直接 `unity_InstanceID` 用来在剔除后重映射。
- `UnityIndirect.cginc` 里的 `GetIndirectInstanceID_Base` / `GetIndirectVertexID_Base` 才是正确索引原始 buffer 的版本，Vulkan / WebGPU 把 startInstance 烘进了 `SV_InstanceID`，D3D 没烘——这个差异被 `_Base` 版本统一；文章顺带指出官方文档示例代码里用错了。

## 链接到的概念

- [[gpu-instanced-grass-urp]]
- [[shader-graph-custom-function-hlsl]]
- [[srp-batcher-cbuffer]]
- [[gpu-driven-grass-tiles]]
- [[waving-grass-shader-vertex-offset]]
- [[multidraw-indirect-occlusion-culling]]
- [[view-frustum-culling-ryg]]
- [[compute-shader-dispatch-ids]]
- [[terrain-splatmap-shader-graph]]

## 原文

- 链接：https://www.cyanilux.com/tutorials/gpu-instanced-grass-breakdown/
- 本地：`raw/articles/cyanilux.com/2025-10-03_gpu-instanced-grass-breakdown.md`
