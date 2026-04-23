---
tags: [引擎架构, 渲染, 多线程, data-oriented, stingray, bitsquid]
date: 2026-04-19
sources: 1
---

# Stingray 渲染的三阶段数据并行流水

Tobias Persson 2017 年"Stingray Renderer Walkthrough #1"这篇文章把 Bitsquid/Stingray 渲染架构的哲学讲得最清楚——**CPU 一帧切成三段、每段都能数据并行、渲染线程只认只读快照**。

## 为什么是 Cull / Render / Dispatch 三段

2009 年 Bitsquid 起步时多核 CPU 已经是常态，PS3 的痛苦经历也把"functional parallelism 不够用"写在每个人脑门上——他们想要**data parallelism**。CPU 侧的一帧于是被划成：

- **Culling**：从 "meshes + particles + lights + ..." 这一大堆对象里，根据某个相机过滤出"可能可见"的子集。具体实现参见 [[stingray-simd-sphere-oobb-culling]]。
- **Render**：遍历 culling 结果，把要发的 draw call / state change 以**中间表示**录进一条 command buffer。这一阶段纯 CPU，不碰图形 API。
- **Dispatch**：把上一步的中间 command buffer 翻成具体图形 API 调用（D3D / GL / Metal / GNM）。

每段的结果 pipe 给下一段；数据单向流。只要允许"无视最终 API 调用顺序"，每段都能轻松 fork 成 N 块丢给 worker thread。渲染 data flow 天然线性：input → state mutation → figure out what to render → generate API calls，反复这么走。

## 渲染线程必须看只读世界

data parallelism 的前提是 worker 不能互相覆盖写。于是 Stingray 立下规矩：

- 所有 `render()` 函数都是 `const`。
- 渲染侧维护**自己的对象表示**，只装渲染关心的字段。gameplay 关心 "entity" 这种高层抽象，渲染侧只想拿到 "一个内存布局漂亮的 renderable 数组"。
- gameplay 和渲染彻底解耦。主线程跑 frame `N` simulation 的同时，渲染线程处理 frame `N-1`——这就是 [[main-render-thread-state-reflection|state reflection]] 系统的职责范围。

## Simulation / Render 并行的真实价值

有人会说"如果每段都完美 parallelize 了，overlay 没意义"。Tobias 的反驳很务实：**现实里总有不能 go wide 的同步段**——老图形 API（DX11 / GL）本身就要求同步提交，gameplay 里也总有需要主线程串行的逻辑。这些段会在 worker 池上制造 bubble。

把 simulation 和 render overlay 起来之后：

- 两条 controller thread（simulation + render）都把 worker 喂饱；
- 谁等 worker 完成谁就自己下场帮工（help-if-idle，和 culling 的 `wait_atomic` 同一 pattern）；
- 一条线程因同步段停下时，另一条的 worker 还在跑。

代价：

- **任何跨帧 mutable state 必须 double buffer**——simulation 在改 frame `N`，renderer 正读 frame `N-1`。
- **immutable 数据（VB/IB 等）也要 lifetime 追踪**——不能在 renderer 还引用时就释放。
- **主线程不能领先渲染线程超过 1 帧**——防止帧堆积造成延迟。

## 与 data-oriented programming 的关系

Stingray 渲染代码明显偏 DOD：设计新系统时先琢磨数据怎么存、怎么流，再写 transform。这直接决定了下游子系统的长相——比如 [[stingray-simd-sphere-oobb-culling]] 用 SoA `ObjectSet`、[[stingray-render-resource-context]] 用 command buffer 化的资源分配——都是这一哲学的直接后果。

这篇算是一个总纲——作者在文末声明接下来要讲 GPU 资源、RenderDevice、shader 系统等 Render 阶段的构件，而 culling 与 state reflection 两条他让给了 Andreas Asplund 的专题文。

## Sources

- [[sources/bitsquid-renderer-walkthrough-1-overview]]
