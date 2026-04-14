---
tags: [gui, rust, 反应式, druid, xilem]
date: 2026-04-14
sources: 2
---

# Rust 下的反应式 UI 架构

"Reactive UI" 这个词在 JavaScript 世界被 React / Vue / Elm 用到近乎泛滥，但落到 Rust 里却成了一个开放研究问题。Rust 没有垃圾回收、没有便宜的运行时多态、对象所有权严格——那些建立在 JS 可变引用与闭包自由度之上的反应式 API，到了 Rust 里都要**重新设计**才能跑得动。[[raph-linus]] 通过 Druid → Crochet → Xilem 三代原型把问题逐步收敛。

## 反应式的目标

反应式 UI 本质是一道**增量计算**题：给定"应用数据"和一个从数据到 widget 树的纯函数，当数据变更时，只重新计算受影响的那部分 widget 并把差异打到屏幕上。大家都同意这是好事，但在 Rust 里怎么表达这个"纯函数"、以及怎么让"增量"这件事既高效又符合借用规则，没有标准答案。

## Druid 的 lens 模型

Druid 的第一代方案是 **lens**——Haskell 风味的一对 `(get: S -> T, set: S -> T -> S)`，允许一个 widget 聚焦到 app data 里的一个子结构，对它进行局部变更。lens 在数学上漂亮、性能上高效，但 Raph 自己也承认这个模型**门槛很高**：app data 必须为了贴合 Druid 的 lens 模型而刻意设计，不是随便写个 struct 就能直接用。2020 年他明确把这个学习曲线列为 Druid 的主要设计债。

## Crochet 与简化反应式

Druid 之外 Raph 发了一个研究原型 Crochet，目标是**在不丢 lens 的效率**前提下降低门槛。Crochet 那篇 "Towards a unified theory of reactive UI"（2020）是他对反应式 UI 的一次综述——从 React 的 virtual DOM diff、Elm 的纯函数 update、Jetpack Compose 的 memoized composable，梳理到 immediate mode GUI，试图找出这些看似不同的模型在计算语义上共享的结构。

## Iced 的 Elm-like 路径

对照之下，**Iced** 走的是 Elm 语义的直译：`Message` 枚举 + `update(&mut State, Message)` + `view(&State) -> Element`。对初学者门槛低，async 集成也做得好，能作为 guest window 嵌入宿主（重要场景是 VST 插件）。Raph 在 2020 年的文章里明确表扬 Iced，承认"对大多数 app 来说它可能就够好"，并把它当作学习对象。

## Xilem：2022 的新假设

2022 年 Raph 把研究重心转向 Xilem，他对 Xilem 的假设毫不含糊：

> **Xilem 是 Rust 上目前已知最好的反应式架构**——比 Dioxus、Sycamore、pax-lang 和各种 Elm 变种都**更简洁、更符合人体工学、更高效、async 集成更好**。

他同时承认自己可能是错的，但坚持要把这条路走通才能验证假设。Xilem 最有意思的是把**不变数据结构**（用于对大集合做稀疏 diff）当作核心课题——他在 RustLab 2020 的演讲里提过这是 UI 工具包里"从未被好好解决过"的问题：要么用复杂脆弱的增量 DOM 机制，要么每次都 diff 整个 collection。

## 为什么 Rust 让反应式变难

- **没有自由变量的闭包捕获**：借用检查把"同时持有 state 和 handler"这件事变成设计问题
- **没有 GC 兜底**：React / Elm 里随手构造的一次 view tree 在 JS 里由 GC 回收；Rust 里要决定生命周期归属
- **动态多态成本高**：trait object 有 vtable 开销，generic 展开则导致编译时间爆炸
- **monomorphization 与类型擦除的取舍**：性能 vs 编译时间之间常常没有甜蜜点

## 观察：收敛条件还没出现

Raph 在 2020 年说过一句冷静的话：**反应式 UI 在 Rust 里可能永远不会收敛到单一架构**，因为不同应用类型（文档编辑器、3D / 视频、VST 宿主、行业表单）对反应式表达力的需求本来就不同。更务实的合力目标是共享**底层基础设施**——wgpu 做 GPU 抽象、Vello 做 2D 渲染、文本布局、a11y——反应式层之上百花齐放。

## 相关

- [[rust-gui-ecosystem]]
- [[smooth-window-resize]]
- [[raph-linus]]

## Sources

- [[sources/raphlinus-rust-2021-gui]]
- [[sources/raphlinus-smooth-resize-test]]
