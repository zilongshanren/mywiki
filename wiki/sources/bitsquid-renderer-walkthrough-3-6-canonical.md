---
tags: [source, 渲染, 引擎架构, 多线程, command-buffer, stingray, bitsquid]
date: 2026-04-19
sources: 4
---

# Stingray Renderer Walkthrough #3-#6: RenderContext / Sorting / RenderDevice / RenderInterface（Tobias Persson / bitsquid 博客）

[[tobias-persson]] 2017 年 2 月 10-22 日连发的四篇博客，构成 Stingray 渲染 CPU 侧的**正典**——覆盖 Render 阶段的命令录制、sort_key 设计、dispatch 到具体图形 API、跨线程粘合层。这四篇内容高度耦合，因此合并为一条 source 记录；Walkthrough #1 / #2 已在 [[sources/bitsquid-renderer-walkthrough-1-overview]] 与 [[sources/bitsquid-renderer-walkthrough-2-resources]] 单独记录。Walkthrough 系列的开篇 index 博客（2017-02-01 同题文章）仅为系列目录，无独立技术内容，不单独入库。

## 摘要

### Part 3: RenderContext

[[stingray-render-context|RenderContext]] (RC) 是 [[stingray-renderer-three-stage-pipeline|三阶段架构]] 里 **Render 阶段的输出结构**，承接 culling 结果、由 worker 并行写入。内部维护两条并行 buffer：POD `Command` 数组（`{sort_key, head*, command_flags}`）和 `RenderPackageStream`（变长 package 的块式内存池，借鉴 Naughty Dog fiber allocator）。sort_key 独立于 package 数据的理由有四条（见概念页）。API 分三类：`begin/end_state_command` 包起的 state 批、`render(RenderJobPackage*, ...)`、`map_write(resource, ...)`。`RenderJobPackage` 是自包含描述：`BatchInfo` + `ComputeInfo` + shader handle + 常量 buffer + debug tags。`render()` 返回 patched copy 的指针，是因为 worker 并行访问不能 mutate 静态 prototype。新增了 fence / multi-GPU `gpu_affinity_mask` 等现代 API 所需的同步原语。

### Part 4: Sorting

[[stingray-sort-key-bit-layout|64-bit sort_key 位布局]]：`[2 Unused | 7 Layer | 3 Pass Deferred | 32 User | 1 Instance | 16 Depth | 3 Pass Immediate]`。灵感来自 Christer Ericsson ["Order your graphics draw calls around!"](http://realtimecollisiondetection.net/blog/?p=86)。Layer 7 位由 `render_config` 决定的宏观阶段 —— 每声明一层 +1。Depth 16 位由 `render()` 的 `job_sort_depth` 量化，BACK_FRONT 时按位翻转避免特判。Immediate vs Deferred 模式通过把 pass index 移到低位 / 中位来切换多-pass 执行顺序。**单次 stable radix sort** 搞定一切——坚决不做 bucket。

### Part 5: RenderDevice

[[stingray-render-device-dispatch|RenderDevice]] 是图形 API 抽象的唯一子类点。`dispatch(RRC[])` 同步执行；`dispatch(RC[])` 走 **merge + stable sort → instance merging → 切 worker → 串行扫 state 变更 → 并行翻 API 调用** 五个阶段。Instance merging 扫 sort_key "instance bit 置位 + 高位相同" 的区间，比对 `instance_hash` + shader 确认可合并，把 instance-specific 常量提取到 dynamic RawBuffer 当 VS 输入。DX12 下每个 worker 建自己的 `ID3D12GraphicsCommandList`，MRU cache 避免重复 bind，resource barrier 在扫描阶段记录。

### Part 6: RenderInterface

[[stingray-render-interface|RenderInterface]] 是渲染子系统的总装车间 + 跨线程通信边界。持有 Window/SwapChain 映射、RenderWorld 生命周期、data-driven 四件套（`LayerManager` / `ResourceGeneratorManager` / `RenderResourceSet` / `RenderSettings`）、Shader Manager、mip-level streamer。对外区分**阻塞**（flush + 直接动 state——开关 Device、load `render_config`、load shader）和**非阻塞**（投 ring buffer——`render_world`、state reflection、`present_frame`、stats、callback）。"shader 系统不 thread-safe、只能在渲染线程" 是一个显式约束。统计数据**晚 2 帧**返回以免阻塞。

## 关键要点

- **sort_key 分位是 data-driven render pipeline 的骨架**——layer / shader pass / depth / instance 全部变成**位算术**，排序只是一次 stable radix sort。
- **RenderContext 与 RenderResourceContext 是同一 pattern 的双生子**——都是 command-buffer 化、可并行录制、dispatch 时集中处理。
- **RenderJobPackage 必须自包含**——shader handle + resource handles + constant buffer 都嵌在 variable-size tail。避免 dispatch 阶段回查 engine 层。
- **render() 返回 patched copy 指针** 是因为 worker 并行进入同一 renderable 不能 mutate prototype——顺手把拷贝合进接口。
- **Instance merging 发生在 API 无关阶段**——只看 sort_key 位和 instance_hash，让 D3D11 / D3D12 / Metal 共享同一套 merger 逻辑。
- **DYNAMIC buffer 允许 worker 异步更新，UPDATABLE 串行更新**——作者承认此设计不优雅但务实。
- **RenderInterface 的阻塞/非阻塞二分** 让 API user 在写代码时立刻知道是否会 stall 渲染线程。
- **Shader 系统显式不 thread-safe**——shader load/reload 永远是阻塞操作。

## 链接到的概念

- [[stingray-render-context]]
- [[stingray-sort-key-bit-layout]]
- [[stingray-render-device-dispatch]]
- [[stingray-render-interface]]
- [[stingray-renderer-three-stage-pipeline]]
- [[stingray-render-resource-context]]
- [[main-render-thread-state-reflection]]
- [[stingray-data-driven-render-config]]
- [[render-config-extension-points]]
- [[bindless-rendering]]
- [[async-compute]]

## 原文

- 链接：
  - https://bitsquid.blogspot.com/2017/02/stingray-renderer-walkthrough-3-render.html
  - https://bitsquid.blogspot.com/2017/02/stingray-renderer-walkthrough-4-sorting.html
  - https://bitsquid.blogspot.com/2017/02/stingray-renderer-walkthrough-5.html
  - https://bitsquid.blogspot.com/2017/02/stingray-renderer-walkthrough-6.html
- 本地：
  - `raw/articles/bitsquid.blogspot.com/2017-02-10_stingray-renderer-walkthrough-3-render-contexts.md`
  - `raw/articles/bitsquid.blogspot.com/2017-02-14_stingray-renderer-walkthrough-4-sorting.md`
  - `raw/articles/bitsquid.blogspot.com/2017-02-17_stingray-renderer-walkthrough-5-renderdevice.md`
  - `raw/articles/bitsquid.blogspot.com/2017-02-22_stingray-renderer-walkthrough-6-renderinterface.md`
