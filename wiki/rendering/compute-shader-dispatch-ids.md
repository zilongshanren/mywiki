---
tags: [compute-shader, hlsl, glsl, gpgpu]
date: 2026-04-19
sources: 1
---

# Compute Shader 线程 ID 速查

Compute shader 里的线程不是简单的一维索引：线程先按静态声明的大小组成 **group**（本地组），再由 dispatch 时指定的 **grid** 大小排布多少个组。HLSL 与 GLSL 为此提供了四组 system-value，命名风格差异很大，Adam Sawicki 做了一张速查表。

## 对照表

| HLSL Semantics | GLSL Variable | 维度 | 指代 | 坐标系 |
|---|---|---|---|---|
| `SV_GroupID` | `gl_WorkGroupID` | uint3 | 整个 group | dispatch 内全局 |
| `SV_GroupThreadID` | `gl_LocalInvocationID` | uint3 | 单个线程 | group 内局部 |
| `SV_DispatchThreadID` | `gl_GlobalInvocationID` | uint3 | 单个线程 | dispatch 内全局 |
| `SV_GroupIndex` | `gl_LocalInvocationIndex` | uint（展平） | 单个线程 | group 内局部 |

## HLSL 命名的坑

Adam 抱怨 HLSL 命名误导人：

- `GroupID` 是整个 group 的 id ——合理。
- `GroupThreadID` 是 group 内线程 id ——也行。
- 那么 `GroupIndex` 听起来应该是 group 的展平索引？**错。** 它是 group 内某个线程的展平索引，本质上是 `GroupThreadID` 的 1D 版本。

GLSL 则用 `WorkGroup` vs `Invocation`、`Local` vs `Global` 两对词划清层级，这套词汇对应更干净。所以同一个概念在两套 API 里，HLSL 的 `SV_DispatchThreadID` ↔ GLSL 的 `gl_GlobalInvocationID`，名字完全不互文。

## 用途

- `GlobalInvocationID` 通常直接当数组下标（像素、矩阵元素、粒子索引）。
- `LocalInvocationIndex` 常用于 `groupshared` / shared memory 的布局，配合 barrier 做 block reduction。
- `WorkGroupID` 用于计算本 group 负责的 tile 偏移，例如 tiled light culling。

## Sources

- [[sources/asawicki-compute-shader-sv-cheat-sheet]]
