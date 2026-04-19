---
tags: [source, graphics, compute-shader, hlsl, glsl]
date: 2026-04-19
sources: 1
---

# System Value Semantics in Compute Shaders - Cheat Sheet（Adam Sawicki）

[[adam-sawicki]] 发表于 2020 年 9 月的速查表，把 HLSL 与 GLSL 里四个线程 ID system-value 一一对齐，顺带吐槽 HLSL 的 `SV_GroupIndex` 命名严重误导。

## 摘要

Compute shader 的线程排列有 group（静态声明大小）和 dispatch grid（CPU 动态指定组数）两层，线程自己要靠 system-value 识别身份。HLSL 提供四个：`SV_GroupID`（整 group 的坐标）、`SV_GroupThreadID`（线程在 group 内 3D 坐标）、`SV_DispatchThreadID`（线程在整 dispatch 的 3D 坐标）、`SV_GroupIndex`（线程在 group 内的展平 1D 索引——容易以为是 group 的展平索引，其实不是）。GLSL 用 `gl_WorkGroupID` / `gl_LocalInvocationID` / `gl_GlobalInvocationID` / `gl_LocalInvocationIndex`，在 `WorkGroup` vs `Invocation`、`Local` vs `Global` 两对词上区分干净。Adam 把四对一对一列表，方便记忆。

## 关键要点

- HLSL `SV_GroupIndex` 是 group 内线程的展平索引，**不是** group 自己的展平索引。
- GLSL 变量名比 HLSL semantics 更自解释。
- `SV_DispatchThreadID` 通常直接当数据数组的 3D 下标。
- `SV_GroupIndex` 常用于 `groupshared` 内存的布局。

## 链接到的概念

- [[compute-shader-dispatch-ids]]

## 原文

- 链接：https://asawicki.info/news_1733_system_value_semantics_in_compute_shaders_-_cheat_sheet
- 本地：`raw/articles/asawicki.info/2020-09-29_system-value-semantics-in-compute-shaders-cheat-sheet.md`
