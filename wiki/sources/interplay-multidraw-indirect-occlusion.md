---
tags: [source, 渲染, gpu-driven, 剔除, multidraw, mesh-lod, dx11]
date: 2026-04-14
sources: 1
---

# Experiments in GPU-based occlusion culling part 2: MultiDrawIndirect and mesh lodding（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 2018 年 1 月的第二篇，接着 2017 年 11 月 [[gpu-based-occlusion-culling|Part 1]] 收尾，把 GPU-driven 剔除补上 *MultiDrawIndirect* 和 *mesh LOD* 两个缺口——同时保持「不改美术内容管线」的原则。

## 摘要

Part 1 的方案在 DX11 下每个 mesh 仍要一次 `DrawIndexedInstancedIndirect`，而且没有 mesh LOD。作者这次用 NVidia 的 `NvAPI_D3D11_MultiDrawIndexedInstancedIndirect` 扩展（AMD 也支持，Intel 不支持）把多 mesh draw 合成一次；同时把所有顶点、索引、instance data、material constant 批量到少数全局 buffer 里，走 **programmable vertex fetching**（在 VS 里用 `SV_VertexID + vertexBufferOffset` 手动采顶点 typed buffer）。DX11 里没有 `gl_DrawID` 的等价物，作者走了很迂回的路——最终方案是用一个 16-bit per-instance 的 vertex buffer（绑到 IA、走 instance step rate）来携带 DrawcallID，从而让每个 instance 在 VS 里知道自己归属哪个 mesh LOD。Mesh LOD 的接入很简洁：**每个 mesh LOD 就是一条独立 drawcall**，LOD 粒度的顶点/索引差异自然由 args buffer 的 offset 吸收；instance data 按 `(mesh, LOD)` 分组存放，空的 drawcall 也是合法的。Intel fallback 就是退回 for-loop 里顺次调 N 次 indirect draw——**大部分收益本来就来自 batching 而不是 MultiDraw 本身**。

## 关键要点

- DX11 下 MultiDrawIndirect 通过 IHV driver extension（NVAPI / AGS）获取，Intel 无解，fallback 无损。
- `DrawcallID` 在 DX11 没有 system value 可用——最终用 per-instance 16-bit vertex buffer + IA 绑定来绕过。
- 全局几何 buffer 布局：position / normal / uv 各一个 typed buffer；仍保留常规 index buffer，保住 post-transform vertex cache。
- Material constant 批量成数组（`PerObjectData[N]`），用 mesh ID 索引；上限 4096 float4，溢出转 structured buffer（性能代价 Nvidia 文档有记录）。
- Mesh LOD：每个 LOD 独立 drawcall，自然适配不同 vertex/index count，不需要 padding。
- 跨 mesh 的全局 instance 距离排序不可行——这是 `DrawInstanced` 家族的通用限制。
- 作者主张即便无法用 MultiDraw 扩展也值得做：**draw 成本的主要部分是 state setup，不是 draw 本身**。

## 链接到的概念

- [[multidraw-indirect-occlusion-culling]]
- [[gpu-based-occlusion-culling]]
- [[stream-compaction]]
- [[batching]]
- [[draw-call]]
- [[indirect-draw]]
- [[bindless-rendering]]
- [[kostas-anagnostou]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2018/01/15/experiments-in-gpu-based-occlusion-culling-part-2-multidrawindirect-and-mesh-lodding/
- 本地：`raw/articles/interplayoflight.wordpress.com/2018-01-15_experiments-in-gpu-based-occlusion-culling-part-2-multidrawi.md`
