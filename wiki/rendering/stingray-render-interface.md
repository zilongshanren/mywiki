---
tags: [渲染, 多线程, ring-buffer, api抽象, stingray, bitsquid]
date: 2026-04-19
sources: 1
---

# Stingray 的 RenderInterface：跨线程交换的粘合层

Walkthrough 系列第 6 篇。Tobias 自己都觉得这篇的内容 "大部分会显得很明显"——但为完整性还是写了。`RenderInterface` 是 Stingray 渲染子系统的**总装车间**：它不做图形 API 调用，只负责**把一堆 subsystem 粘在一起**，同时提供**非渲染线程与渲染控制线程之间的唯一合法通信通道**。

## RenderInterface 的责任清单

- **Window / SwapChain 映射**：Window 由 simulation 线程管，SwapChain 由渲染线程管。RenderInterface 负责从 Window 建 SwapChain、维护映射、把 resize 等窗口事件传到渲染侧。
- **RenderWorld 生命周期**：渲染侧有自己的 World 表示（只装渲染关心字段）。RenderInterface 负责 register/unregister——每个 RenderWorld 有自己的 allocator，释放时路径明确（评论区有人问到资源 ownership，作者答：`WorldRenderInterface` 和 `RenderWorld` 共享同一 allocator）。
- **Data-driven 四件套**：`LayerManager` / `ResourceGeneratorManager` / `RenderResourceSet` / `RenderSettings` 全部由 RenderInterface 持有。
- **Shader Manager**：集中管理所有 shader 的 load / unload / hot-reload。因为 shader 系统**本身不 thread-safe**，任何涉及 shader 的操作必须同步到渲染线程。
- **资源流送**：基于 view frustum culling 的 mip-level streamer。piggyback 在 culling 数据上，所以归 RenderInterface 持有并驱动。

## 阻塞接口 vs 非阻塞接口

RenderInterface 把操作分成两类：

### 阻塞（blocking）——直接 flush + 操纵状态

阻塞调用会让 caller 等渲染线程 flush 所有 outstanding 工作——调用方拿到 renderer 的一致状态后直接动它。**不适合游戏循环**（会导致帧率抖动），适合做**大状态切换**：

- 开关 `RenderDevice`（对应图形 API 的 init/shutdown）
- Swap chain 创建/销毁
- 载入 / 切换 `render_config` —— 因为这会重配 `LayerManager` 等四件套
- Shader load / unload / reload —— shader 系统不 thread-safe
- World 注册/注销

### 非阻塞（non-blocking）——通过 ring buffer 投信

非阻塞调用往一条 **渲染线程消费的 ring buffer** 里 post message。正常一帧里也就 10~20 条消息——`RenderWorld` 有自己的对象表示，frame-by-frame 的差异走 [[main-render-thread-state-reflection|state reflection]] 而不走这条 ring buffer。

关键的非阻塞入口：

- `render_world(World&, Camera&, Viewport&, ShadingEnvironment&, swap_chain)`：一帧里最常调的入口。post `RenderWorldMsg`，渲染线程拿到后进入 [[stingray-renderer-three-stage-pipeline|Cull / Render / Dispatch]] 的第一段。
- State reflection：每帧从 simulation `World` 反射 delta 到 `RenderWorld`。
- `create_fence()` / `wait_for_fence(uint32_t)`：渲染同步；也用于保证 simulation 不超前渲染 > 1 帧。
- `present_frame(swap_chain)`：本帧所有 `render_world` 调完之后，对每个被触及的 swap chain 投 `PresentFrameMsg`。
- 渲染统计读取：从 `RenderContext` / `RenderDevice` 采集的数字（draw call 数、state 切换、GPU timing），对外非阻塞返回——代价是返回的数据**晚 2 帧**（GPU timing 更老），对波动不大的指标无所谓。
- 回调投递：`run_callback(Callback, user_data, size)` 允许任意线程把一段代码丢到渲染线程执行。
- `RenderContext` / `RenderResourceContext` 创建/dispatch/release：大多数系统从渲染线程做这些，但资源线程也会建 RRC——RenderInterface 提供线程安全的路径避免 block 渲染线程。

## 为什么单独抽一个 RenderInterface

一句话：**renderer 有一条自己的 controller thread，其他线程不许直接动它**。RenderInterface 就是那条边界。

- 对内：把 shader manager / layer manager / swap chain 等各自独立的 subsystem 拢在一起，给它们一个统一的创建顺序和生命周期。
- 对外：把 "是否需要 block" 显式区分——阻塞接口走同步 flush 路径，非阻塞接口走 ring buffer 投信路径。用户写代码时就知道这次调用是不是会卡住。

这和 `render()` 函数 `const` + 渲染线程只读对象表示 + state reflection ring buffer 是**同一个哲学的三个面**：**数据单向流、线程边界清晰、任何跨线程写都走一个可审视的中间表示**。

## 相关

- [[stingray-renderer-three-stage-pipeline]]
- [[stingray-render-device-dispatch]]
- [[stingray-render-context]]
- [[main-render-thread-state-reflection]]
- [[stingray-data-driven-render-config]]

## Sources

- [[sources/bitsquid-renderer-walkthrough-3-6-canonical]]
