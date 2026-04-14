---
tags: [source, 渲染, GPU, D3D12, workgraphs]
date: 2026-04-14
sources: 1
---

# A quick introduction to workgraphs（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou]] 发表于 2024 年 6 月的入门教程，通过一个混合 shadow raytracer 的三级分类管线实操讲解 [[d3d12-work-graphs]] 的编程模型。

## 摘要

文章用 Kostas 自己的 toy engine 把一个"tile 背面剔除 → hi-z raymarch → DXR inline raytracing"的 shadow 分类器改写成 work graph。从三段 shader 源码出发，作者依次讲清楚了 workgraph 的三大概念：节点 (`[Shader("node")]` + `NodeLaunch` + `NodeDispatchGrid`)、记录 (`NodeOutput<T>` + `MaxRecords` + `GetGroupNodeOutputRecords`/`OutputComplete`)、以及三种 launch 模式 broadcasting/thread/coalescing 的差异。CPU 端则讲了 `CD3DX12_STATE_OBJECT_DESC` 的构造、`CD3DX12_WORK_GRAPH_SUBOBJECT::IncludeAllAvailableNodes()`、backing memory 的预查与分配（`GetWorkGraphMemoryRequirements`），最后是 `DispatchGraph()` 的触发方式。末尾对比了"compute + ExecuteIndirect" 的老路子，点出 work graph 消除了保守 buffer 分配、compaction pass 和 UAV barrier drain 这三个结构性痛点。

## 关键要点

- **节点是带注解的 compute shader**：`[NodeIsProgramEntry]` 声明入口、`[NodeDispatchGrid]` 可以在 CPU 端被 override
- **broadcasting / thread / coalescing 对应不同的粒度和 groupshared 能力**：broadcasting 保留 threadgroup，thread 每线程独立，coalescing 是 GPU 自动打包
- **Record 的 API 必须 threadgroup uniform**：`GetGroupNodeOutputRecords(0)` 表达"不输出"而不是不调用
- **Backing memory 由应用自己分配**：大小通过 `GetWorkGraphMemoryRequirements` 查，首次 `DispatchGraph` 要带 `FLAG_INITIALIZE`
- **老 GPU-driven 管线的三大痛点**：预分配浪费、compaction pass、barrier drain——work graph 靠 ring buffer 直接接力解决
- **shadow 三级分类**是天然适配 workgraph 的场景：绿色区（背面）、蓝色区（hi-z 命中）、红色区（DXR）自然对应三个节点

## 链接到的概念

- [[d3d12-work-graphs]]
- [[gpu-based-occlusion-culling]]
- [[hybrid-raytraced-shadows-reflections]]
- [[multidraw-indirect-occlusion-culling]]
- [[screenspace-reflections]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2024/06/29/a-quick-introduction-to-workgraphs/
- 本地：`raw/articles/interplayoflight.wordpress.com/2024-06-29_a-quick-introduction-to-workgraphs.md`
