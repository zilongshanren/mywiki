---
tags: [source, 渲染, 引擎架构, 多线程, data-oriented, stingray, bitsquid]
date: 2026-04-19
sources: 1
---

# Stingray Renderer Walkthrough #1: Overview（Tobias Persson / bitsquid 博客）

[[tobias-persson]] 发表于 2017-02-01 的博客，Stingray Renderer Walkthrough 系列开篇，把整条渲染架构的**设计哲学和骨架**讲清楚。

## 摘要

Bitsquid 2009 起步时多核已经是常态，加上 PS3 经验让他们明白"functional parallelism 不够用"，于是把一帧的 CPU 侧切成三段：**Culling**（从 mesh/particle/light 混合池里过滤可见对象）、**Render**（遍历 cull 结果把 draw call 录进中间 command buffer）、**Dispatch**（把中间 buffer 翻成具体图形 API 调用）。每段结果 pipe 给下一段，单向 data flow，每段都能 fork 到 worker 池上做 data parallelism。

渲染线程看只读快照：所有 `render()` 函数 `const`，渲染侧维护自己的对象表示（只含渲染关心字段），和 gameplay 彻底解耦。simulation 跑 frame N 时 renderer 处理 frame N-1——靠 [[main-render-thread-state-reflection|state reflection]]。两条 controller thread（simulation + render）都把 worker 喂饱，等 worker 时自己下场帮工；主线程永远不超前渲染线程 1 帧。代价是 mutable state 要 double buffer、immutable 要 lifetime 追踪。

为什么还要 overlay simulation 和 render：现实中总有不能 go wide 的段（旧 API 的同步提交、gameplay 里的串行逻辑），这些 bubble 靠 overlay 填掉。开篇明确声明接下来专题会讲 GPU 资源、RenderDevice、shader 系统这些 Render 阶段的构件，而 culling 和 state reflection 两条让给 Andreas Asplund 的专文。

## 关键要点

- 三阶段 Cull / Render / Dispatch 是 Stingray 渲染架构的命名根骨。
- Data parallelism 而非 functional parallelism 是他们选择三阶段的核心理由。
- 渲染代码偏 data-oriented：先想数据怎么流，再写 transform。
- Simulation/Render overlay 的真实价值来自同步段的 bubble filling，不是理论上限。
- Double buffering 与 lifetime tracking 是 overlay 的必然代价。

## 链接到的概念

- [[stingray-renderer-three-stage-pipeline]]
- [[main-render-thread-state-reflection]]
- [[stingray-simd-sphere-oobb-culling]]
- [[stingray-render-resource-context]]
- [[data-driven-architecture]]

## 原文

- 链接：https://bitsquid.blogspot.com/2017/02/stingray-renderer-walkthrough-1-overview.html
- 本地：`raw/articles/bitsquid.blogspot.com/2017-02-01_stingray-renderer-walkthrough-1-overview.md`
