---
tags: [source, 渲染, 引擎架构, 数据驱动, stingray, bitsquid]
date: 2026-04-19
sources: 1
---

# Stingray Renderer Walkthrough #7: Data-driven rendering（Tobias Persson / bitsquid 博客）

[[tobias-persson]] 2017-03-09 发表的 Stingray 渲染器 Walkthrough 第 7 篇，把前 6 篇搭好的底层 CPU 机制升到"一帧怎么被 json 驱动"的层面。已有的 [[stingray-data-driven-render-config]] 是高层总述；本篇则是**机制层正典**——拆清楚 render_config 的四个组成部分在 C++ 端的具体结构。

## 摘要

Stingray 的 data-driven rendering pipe 由四种 json 文件驱动：`.render_config` / `.render_config_extension` / `.shader_source` / `.shader_node`。本篇只讲 `.render_config`，它用 [sjson](http://bitsquid.blogspot.se/2009/10/simplified-json-notation.html) 表达四件事：**render_settings**（全局 key:value，可被 `settings.ini` 及用户 config 覆盖；key 走 murmur hash 到 32 位）、**render_caps**（只读硬件能力，`RenderDevice` 启动时填）、**global_resources**（声明本帧所有 GPU 资源——render target、DependentRenderTarget 继承、`size_from_render_setting` 动态分辨率等）、**layer_configurations**（一帧的 GPU 调度顺序）。branching 分两种：`static_branch` 载入时求值并剔除失败分支；`dynamic_branch` 每次 `render_world` 都重算。Layer 的 C++ 表示是一个窄结构（`sort_key` / `name` / `depth_sort` / `render_targets[]` / `depth_stencil_target` / `resource_generator` / `clear_flags` / `profiling_scope`），由 `LayerManager` 持有。每条 layer **递增 sort_key 的 Layer 位**——这就是一帧 GPU 顺序的唯一骨架。Resource Generator 是描述 modifier 数组的框架，内置 `fullscreen_pass` / `compute_kernel` / `cascaded_shadow_mapping` / `atlased_shadow_mapping` / `generate_mips` / `clustered_shading` / `deferred_shading` / `stream_capture` / `fence` / `copy_resource` 等类型；modifier 可以任意创建 RenderContext、开 worker、访问引擎全部 API，生成的 context 最后一起 dispatch。Generator 内部调度靠 sort_key 的 32-bit "user" 位段。

文章末尾 Tobias 自陈三条工程债：跨平台 + 多 stereo 路径导致 config 里分支密度过高（PC 上 mono + 4 种 stereo = 5 条路）；`global_resources` 生命周期过静态、缺 transient aliasing；resource 绑定靠 shader 名字隐式查找，导致 DX12/Vulkan 的 barrier 追踪复杂。他点名想借鉴 Yuriy O'Donnell 的 Frostbite FrameGraph 和 Aras 的 Unity Scriptable Render Pipeline——实际上这两条 2017 年的演讲就是下一代声明式渲染的风向。

## 关键要点

- **render_config 四件套**：render_settings / render_caps / global_resources / layer_configurations，每一件都在 engine 侧有极简 C++ 对应物。
- **Layer struct 是 data-driven 的物理接口**——把"层"编成位段而不是语义 enum，让一次 stable radix sort 搞定全帧。
- **layer 既能是 draw target 也能触发 resource_generator**，但"双重身份"实际从不使用。
- **`fullscreen_pass` 是最常用的 modifier**——绝大多数 post / lighting / SSAO 都是 fullscreen_pass 链。
- **`static_branch` 在启动时求值、彻底剔除**；`dynamic_branch` 每帧求值——前者省运行期开销，后者换灵活性。
- **Resource Generator 任意性**：modifier 可创建 RenderContext、spawn worker、摆弄任意引擎 API——没有沙箱、靠 sort_key user 位保证内部调度正确。
- **`global_resources` 启动分配、关闭释放**——这是 Tobias 想改掉的最大静态性债务，transient aliasing 是未来方向。
- **barrier 追踪是隐式的**——shader 按名字绑 resource，dispatch 阶段才知道读写边界；他想要 layer/resource_generator 显式声明输入输出让 barrier 可静态推导。

## 链接到的概念

- [[stingray-data-driven-render-config]]
- [[render-config-extension-points]]
- [[stingray-sort-key-bit-layout]]
- [[stingray-render-interface]]
- [[stingray-render-context]]
- [[stingray-renderer-three-stage-pipeline]]
- [[render-pass-orchestration]]
- [[render-graph]]
- [[data-driven-architecture]]
- [[clustered-shading]]
- [[cascaded-shadow-maps]]

## 原文

- 链接：https://bitsquid.blogspot.com/2017/03/stingray-renderer-walkthrough-7-data.html
- 本地：`raw/articles/bitsquid.blogspot.com/2017-03-09_stingray-renderer-walkthrough-7-data-driven-rendering.md`
