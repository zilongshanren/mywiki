---
tags: [rendering, render-graph, engine-architecture]
date: 2026-04-19
sources: 1
---

# Render Pass 的声明式编排

[[steven-wittens]] 在 Use.GPU 0.14 把 render pass 抽象整个重做，写出的版本是一个很干净的"声明式 render graph"样例：用户面对的是"一次逻辑渲染"的 flag 列表（lights/ssao/overscan/picking 等），内部 lower 成一张 buffer 加 subpass 的有向图。

## 为什么不暴露 input/output

传统 render graph（[[render-graph]] 页上讨论的 FrameGraph 式）让用户显式声明每个 pass 读/写哪些 resource，依赖关系由 graph 系统拓扑排序。Wittens 的观察是：在 SSAO/GTAO/shadow/picking 这种"大家都要深度、都要 normal"的组合里，用户能给出的正确 wiring 只有一种。于是他把 resource allocation 与 pass sequencing 切成两步：

1. 所有 `<FooBuffer>` 提前声明（`use(NormalBuffer, options)`、`use(SSAOBuffer, options)` 等），统一一次分配
2. 所有 `<FooPass>` 再声明（`use(NormalPass, options)`、`use(SSAOPass, options)` 等），通过"well-known names"（`normal`、`motion`、`depth`）自动找 buffer

两段都是普通 JSX/use(...)，可以被用户替换为自己的 pass recipe，而不用理解内部 wiring。Wittens 把这个称作 "pave the cow paths"：常用组合用一行 prefab，专业用户随时 à la carte。

## Buffer history 是一等公民

多数现代 TAA/SSAO/SSR/motion blur 都需要访问上一帧甚至更早的 render target。Use.GPU 把"带历史的 render target"作为 built-in：你绑一个 virtual source，每个使用者拿到 `history[0..N]` 的某一槽位，运行时在每次渲染到 target 后自动轮转。Wittens 的观点直接："任何重新想象的 GPU API 都应把 buffer history 当一等概念"。这和 [[ground-truth-ambient-occlusion]] 的 reprojection 流程完全是同构的。

## Overscan 作为 pass option

为解决 SSAO 边缘失效，Use.GPU 允许 `<Pass overscan={0.05}>`：framebuffer 按百分比扩张，`projectionMatrix` 同步扩张并保持 `[-1..1]` clip-space 一致，最终 resolve 时裁掉。这让 overscan 从"要改 90% render code 的破坏性改造"变成 "pass 级 flag"。

## 声明式 Renderer 的退化

走到这一步后，Use.GPU 的 `<Renderer>` 本身几乎没剩什么东西了——它只是把"compute → render → readback"的顺序约束和一些跨组件数据收集塞好，剩下全部交给 reconciler。Wittens 的总结："这清楚地说明 renderer 本来就想是个 reactive run-time"。这和他反复鼓吹的 [[intent-vs-state]] / patch 驱动的数据流是同一个观察：把"当前做什么 pass"这件事降级为可以 patch 的声明式数据，系统复杂度自然崩塌。

## 相关

- [[render-graph]]
- [[use-gpu-reactive-runtime]]
- [[ground-truth-ambient-occlusion]]
- [[temporal-antialiasing]]

## Sources

- [[sources/acko-occlusion-with-bells-on]]
