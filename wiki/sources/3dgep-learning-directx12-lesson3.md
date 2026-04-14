---
tags: [source, 渲染, directx12, 资源管理]
date: 2026-04-14
sources: 1
---

# Learning DirectX 12 — Lesson 3（Jeremiah van Oosten / 3dgep.com）

[[jeremiah-van-oosten]] 于 2018 年 6 月发表的 DirectX 12 系列教程第三课，集中解决 D3D12 的资源管理与绑定难题：动态数据上传、CPU/GPU 描述符堆、跨线程资源状态跟踪。

## 摘要

D3D12 把之前由驱动兜底的资源绑定全部交给应用。作者把一整套实用封装抽象成四个类：`UploadBuffer` 作为 upload heap 上的线性分配器，服务每帧变化的常量、粒子、UI 数据；`DescriptorAllocator` 管理 CPU 可见描述符的分页池；`DynamicDescriptorHeap` 在录制命令列表时只 stage 描述符，等到 `Draw/Dispatch` 的前一刻才统一拷进 GPU 可见堆并调用 `SetDescriptorTable`；`ResourceStateTracker` 区分"局部状态"和"全局状态"，通过 pending barrier 机制支撑多线程录制而不需要锁共享状态。四者合起来把 D3D12 从"每一步都要自己管"变成"调用方只写逻辑、封装负责正确性"。

## 关键要点

- **D3D12 的特殊负担**：descriptor 堆类型每帧只能绑一个、GPU 还在跑的 descriptor 不能复用、多线程录制时 resource 当前状态是未定义的
- **UploadBuffer = linear allocator**：按 2MB 页分配，O(1) 分配，整页回收，典型用途是 constant buffer、dynamic VB、UI 顶点
- **DynamicDescriptorHeap 的关键**：StageDescriptors 先缓起来，CommitStagedDescriptorsFor{Draw,Dispatch} 在绘制前一刻才 CopyDescriptorsSimple 到 GPU 堆——把同一类型只能绑一个的硬约束化解掉
- **ResourceStateTracker 的多线程解法**：pending barrier 在录制阶段只记"我想从某未知状态转到 X"，全局状态在提交阶段回填 before，避免 lock
- **设计权衡**：为研究 demo 便利而非生产极致，但揭示了 D3D12 封装层的必要组件

## 链接到的概念

- [[d3d12-resource-binding]]
- [[linear-allocator]]
- [[render-graph]]
- [[rendering-api-depth]]

## 原文

- 链接：https://www.3dgep.com/learning-directx-12-3/
- 本地：`raw/articles/3dgep.com/2018-06-08_learning-directx-12-lesson-3.md`
