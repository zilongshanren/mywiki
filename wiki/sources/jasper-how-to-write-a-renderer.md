---
tags: [source, 渲染, 图形api, vulkan, d3d12]
date: 2026-04-14
sources: 1
---

# How to Write a Renderer for Modern Graphics APIs（Jasper St. Pierre）

[[jasper-st-pierre]] 2023 年 9 月发表于 blog.mecheye.net 的长文。把「写一个现代图形 API 渲染器」这件事的结构性蓝图讲清楚——不是堆 Vulkan API 细节，而是 **Draw Call / Render Pass / Data Upload** 三根轴线，以及它们在 Vulkan/D3D12/Metal 下共同要求你先想清楚再动手的缘由。

## 摘要

OpenGL 的设计允许你边写边摸索，Vulkan 逼你在动笔之前就拿出蓝图。作者从十几年 shipping game 渲染器经验出发，指出现代 API 的样板代码之所以吓人，不是 API 本身复杂，而是因为缺一层**更高的结构规划**——这一层恰恰是文档不写的。文章沿三条轴线讲这层规划：**Draw Call 是状态的最小单元**，必须从 gameplay 对象中分离出来并可以被多次、分路由地发射；**Render Pass 构成 acyclic dataflow graph**，决定后处理、阴影、deferred shading、mobile TBDR 的结构——Frostbite FrameGraph、AMD RPS 都围绕这个思路；**Data Upload** 必须围绕 fence/timeline semaphore 的生命周期组织，不能再像 GL 一样在两次 draw 之间偷偷更新 buffer。文末还批了 OpenGL "bind-to-modify" 的 API 设计债，建议改用 DSA 或自建状态跟踪层。

## 关键要点

- 现代 API 与旧 API 的真正差别不是 API surface，而是"结构性规划"这一层：必须先想清楚 pass 图和数据流，再动笔写。
- **Draw Call 结构化**：把 draw call 从 gameplay 对象里抽出来，放进可排序、可多路分发的列表。`void Player::render()` 风格的渲染器在加阴影、透明、多 pass 时会全线崩塌。
- **Render Pass 是 dataflow graph**：一个 pass 读取一组 render target、写入另一组，所有 pass 组成一张 acyclic graph。Frostbite [[frame-graph]] 就是把这个观察直接变成工具。
- **Hazard tracking 从驱动转交给你**：D3D11/GL 的 automatic hazard tracking 有误报（过粗粒度），且和 multi-threaded、multi-queue、bindless、indirect 等新特性冲突。D3D12/Vulkan 要求用户自己放 barrier；Metal 保留 optional 追踪但代价是放弃新特性。参见 [[gpu-hazard-tracking]]。
- **Buffer 生命周期由 fence/timeline semaphore 表达**：GPU 向一个特殊内存位写 integer，CPU 读回判断某帧结束没——于是"这个 buffer 还在不在用"有了廉价答案。参见 [[gpu-fence-timeline-semaphore]]。
- **D3D11/GL 时代 driver 偷偷 buffer renaming 的魔法不再存在**：现代 API 要求你自己管理 100 份 uniform 拷贝。建议架构成"帧首一次性上传"：走 [[linear-allocator]]，用 dynamic uniform buffer offset 供给每个 draw call。见 [[buffer-renaming]]。
- **Render pass 成为一等概念**的直接动因是 mobile TBDR：tile memory 的 load/store 语义只有在 begin/end render pass 的边界上才表达得清楚（参考 [[hsr-tbdr]]、[[tbdr-vs-imr]]）。
- **OpenGL bind-to-modify 反面教材**：`glBindTexture` 既是"我要改它"又是"我要画它"，同名 API 承担两种语义是历史债。Direct State Access 才是正路。
- PSO 的 hash-n-cache 模式——帧首几帧爬坡、之后全命中——是可以接受的权宜之计，但要小心 shader permutation 规模失控。

## 链接到的概念

- [[draw-call]] — 状态绑定的最小单位
- [[render-graph]] — FrameGraph / RPS 的思想源头
- [[rendering-api-depth]] — API 抽象深浅的对照
- [[d3d12-resource-binding]] — D3D12 资源绑定的 lesson 3 实践
- [[gpu-hazard-tracking]]（本次新增）
- [[gpu-fence-timeline-semaphore]]（本次新增）
- [[buffer-renaming]]（本次新增）
- [[hsr-tbdr]]、[[tbdr-vs-imr]] — 移动端 render pass 的存在理由
- [[linear-allocator]] — 帧首 uniform 上传的实现底

## 原文

- 链接：<https://blog.mecheye.net/2023/09/how-to-write-a-renderer-for-modern-apis/>
- 本地：`raw/articles/blog.mecheye.net/2023-09-03_how-to-write-a-renderer-for-modern-graphics-apis.md`
