---
tags: [source, rendering, gpu, compute, unity]
date: 2026-04-14
sources: 1
---

# Graphics.DrawProcedural（Ronja's Shader Tutorials）

[[ronja-bohm|Ronja Böhm]] 于 2020 年 9 月发表的 Unity GPU-driven rendering 入门教程，接在一篇 Compute Shader 基础之后——这次讲怎么**不把 compute 的结果读回 CPU，而是让 GPU 直接画出来**。

## 摘要

文章从「Compute → CPU 回拷 → 更新 Transform → 渲染」的常规慢路径讲起，提出 `Graphics.DrawProcedural` 把整条路径短路的想法：CPU 只下达「画 N 个三角形、这个 material」，**所有 vertex 数据由 shader 从 `StructuredBuffer` 里自己读**。教程的示例用三个 buffer——`SphereLocations`（compute 写入，material 读取，每帧更新每个实例位置）、`Triangles`（mesh 的 index buffer，只读）、`Positions`（mesh 的 vertex positions，只读）。后两者在 `Start()` 里从一个 Unity Mesh 一次性上传 —— 数据甚至不必真正存在于 CPU 内存里。Vertex shader 的输入结构彻底改变：没有 `appdata`，只有 `SV_VertexID` 和 `SV_InstanceID` 两个整数，shader 手动查 buffer 得到 position，再加上 instance 偏移、手动 `mul(UNITY_MATRIX_VP, ...)`——教程顺便拆解 `UnityObjectToClipPos` 的内部就是 `VP * world * p` 这两层矩阵乘。关键细节是 `DrawProcedural` 需要手动提供 AABB bounds 用于 frustum culling，以及 vertex count 是「triangle 数 × 3」而非三角形数。整篇是进入更高级 GPU-driven 管线（DrawProceduralIndirect、BRG）的最小入口。

## 关键要点

- **`Graphics.DrawProcedural` = 一次 draw call + 不依赖 mesh + 不依赖 GameObject**：数据完全驻留 VRAM，CPU 只发命令。
- **三个 buffer 的典型组合**：动态 per-instance 数据（RWStructuredBuffer，compute 写 + material 读）+ 静态 mesh 索引 + 静态 mesh 位置。
- **同一个 ComputeBuffer 既是 compute 输出又是 material 输入**——GPU-driven 渲染的核心连接方式。
- **手动提供 AABB bounds**：引擎没法自动 frustum cull 你画的东西，必须显式给出包围盒，与 compute kernel 的坐标范围对齐。
- **Vertex shader 输入退化为 `SV_VertexID + SV_InstanceID`**，自己查 `Triangles[vid]` → `Positions[idx]` → 加 `SphereLocations[iid]` → 手动 MVP。
- `UnityObjectToClipPos(v)` 内部 = `UNITY_MATRIX_VP * unity_ObjectToWorld * float4(v, 1)` —— 当 object-to-world 的概念消失时必须手动拼。
- **StructuredBuffer stride 最好是 2 的幂**（文档建议能被 128 整除），但 Ronja 实测 float3 / float4 差异很小。
- `DrawProcedural` 是一家子 API 的最简入口，上面还有 `DrawProceduralIndirect`、`DrawMeshInstancedIndirect`、BRG 等更 GPU-driven 的层次。

## 链接到的概念

- [[draw-procedural-gpu]]
- [[draw-call]]
- [[compute-vs-raster-points]]
- [[custom-srp]]
- [[batching]]

## 原文

- 链接：<https://www.ronja-tutorials.com/post/051-draw-procedural/>
- 本地：`raw/articles/ronja-tutorials.com/2020-09-16_graphics-drawprocedural.md`
