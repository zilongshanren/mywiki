---
tags: [source, 渲染, directx12, 显式api, 多线程渲染, agraphicsguynotes]
date: 2026-04-27
sources: 1
---

# Unleash the Power of Direct3D 12（A Graphics Guy's Note）

[[people/graphics-guy-notes]] 发表于 2015 年 6 月的 D3D12 概览文章，从 D3D11 对比切入，系统梳理 D3D12 最重要的七项架构变化，并着重讲解显式内存管理、资源状态管理、资源绑定（[[d3d12-root-signature]]、PSO）和多线程绘制命令提交模型。

## 摘要

文章以 D3D12 相对 D3D11 的核心设计目标为纲——降低 CPU 开销、开放多线程——逐一拆解七大变化：消除 immediate context 改为全延迟 command list；PSO 把几乎所有硬件状态压缩为单一对象；内存由强类型资源改为通用 heap，顶点、索引、常量缓冲可共用同一块内存；资源绑定由 root signature 统一接管 CBV/SRV/UAV/Sampler；资源生存期与 residency 管理责任完全移交给开发者；command queue 取代 immediate context 支持真正的多线程录制；back buffer 也需开发者显式管理。文章还详细解释了 root signature 的三种根参数类型（descriptor table / descriptor / constant）的性能差异，以及 PSO 如何消灭渲染循环中的按需 shader 重编译。

## 关键要点

- D3D12 的核心哲学：用开发者的高层知识替代驱动程序的保守运行时推断，以此换取 CPU 开销
- 内存模型：heap 是通用内存块，vertex buffer / index buffer / constant buffer 均可共存于同一 heap
- 资源状态（resource hazard）：开发者负责 ResourceBarrier，驱动不再自动推断读写顺序
- Command list + Command queue：命令录制线程安全，支持多线程并行录制，最后统一提交到 queue
- Root signature 三档性能：root constant（零间接）> root descriptor（一级间接）> descriptor table（两级间接）
- PSO 的编译时效益：所有硬件指令在创建 PSO 时预烘焙，渲染循环中无按需 shader 重编译
- Bundle：跨帧复用一组绘制调用的预烘焙硬件指令，减少重复录制开销

## 链接到的概念

- [[d3d12-root-signature]]
- [[d3d12-resource-binding]]
- [[d3d12-resource-alignment]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/unleash_the_power_of_direct3d_12/
- 本地：`raw/articles/agraphicsguynotes.com/2015-06-17_unleash-the-power-of-direct3d-12.md`
