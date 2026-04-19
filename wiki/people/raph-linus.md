---
tags: [人物, 作者]
date: 2026-04-14
sources: 9
---

# Raph Levien

**Raph Levien**（博客 raphlinus.github.io，常被简写成 "raphlinus"）是 Google Fonts 的研究软件工程师，[linebender](https://linebender.org/) 开源组织的主要发起人。他的工作集中在 **2D 图形 + 桌面 GUI 基础设施 + GPU compute**——一个被他自己形容为"学术界没有会议、没有像样教科书、全靠从业者口耳相传"的冷门领域。

## 主要项目

- **Vello**（前身 **piet-gpu**）：GPU compute-centric 的 2D 渲染引擎，用 compute shader 做 path geometry（flatten + offset、stroke、Euler spiral 曲线拟合），基于 WGSL + WebGPU 做跨平台 GPU 抽象。是 [[rust-gui-ecosystem|linebender]] 路线的基石。
- **Druid**：Rust GUI 工具包，Raph 定义它的首要使命不是"做 Rust 最好的 GUI"，而是**把 GUI 工程的暗知识系统梳理出来**。Runebender（字体编辑器）是它的 hero app。
- **Xilem**：2022 年开始的下一代反应式架构，假设是"Rust 上目前已知最简洁、最符合人体工学的反应式模型"。把不变数据结构作为核心研究课题。
- **Kurbo**：2D 曲线与路径的纯 Rust 库，包含他的 Bézier 曲线拟合研究。
- **xi-editor**（停止活跃）：早年的文本编辑器项目，"rope science" 系列文档是它的副产品。
- **fearless_simd**：Rust 下可移植 SIMD 的探索 crate，配套一篇同名文章提出 [[fearless-simd|Fearless SIMD]] 愿景。
- **pulldown-cmark、fancy-regex**：较早期的维护项目。

## 思路风格

- **研究即博客**：他自己明确说过不写学术论文，博客 + 开源代码就是他发表研究成果的方式。论点的演进（比如 parallel curves → Euler spirals → 集成到 Vello）常常能在博客时间线上追到最初的直觉。
- **GPU 优先于 CPU**：他反复强调"GPU 上每件事比 CPU 上难 5 倍"，但仍然把大赌注押在 compute shader 上，因为一旦做成就是一个数量级的性能提升。
- **"不写编程语言" 作为 2022 年的新年 resolution**：他明确把 shader 语言/DSL 归为"多年、回报未必有的投资"，宁可把设计留在 pseudo-code 层面再手翻 WGSL。这是对过度工程的清醒自省。
- **社区作为组织手段**：Druid / Vello / Xilem 之间的切换里，他越来越强调 office hours、mentoring PR、不要 "lick the cookie"（把自己可能做的东西占着位但不做）。
- **热爱"把 CPU 算法重做成 GPU 并行"这类谜题**。他自述 happiness 与 coding 时长直接正相关。

## 对本 wiki 的贡献

| 文章 | 贡献的概念 |
|---|---|
| Towards fearless SIMD | [[fearless-simd]] |
| The smooth resize test | [[smooth-window-resize]] |
| Rust 2021: GUI | [[rust-gui-ecosystem]]、[[reactive-ui-rust]] |
| Smooth resize in Direct2D | [[smooth-window-resize]]（Windows 侧 HWND / Sequential / Flip 路径细节）|
| A sketch of string unescaping on GPGPU | [[gpgpu-string-unescaping]] |
| ECS architecture for UI in Rust | [[ecs-for-rust-ui]] |
| Towards GPGPU JSON parsing | [[gpgpu-json-parsing]] |
| With Undefined Behavior, Anything is Possible | [[undefined-behavior-c-cpp]] |
| A Few of My Favorite Sigmoids | [[sigmoid-functions]] |

## 相关
- [[rust-gui-ecosystem]]
- [[reactive-ui-rust]]
- [[smooth-window-resize]]
- [[fearless-simd]]
- [[gpgpu-string-unescaping]]
- [[gpgpu-json-parsing]]
- [[ecs-for-rust-ui]]
- [[undefined-behavior-c-cpp]]
- [[sigmoid-functions]]
- [[good-parallel-computer]]
- [[gpu-queues-vs-dispatch-execution]]

## Sources
- [[sources/raphlinus-fearless-simd]]
- [[sources/raphlinus-smooth-resize-test]]
- [[sources/raphlinus-rust-2021-gui]]
- [[sources/raphlinus-smooth-resize-direct2d]]
- [[sources/raphlinus-gpu-unescaping]]
- [[sources/raphlinus-ecs-ui-rust]]
- [[sources/raphlinus-gpu-json-parsing]]
- [[sources/raphlinus-undefined-behavior]]
- [[sources/raphlinus-favorite-sigmoids]]
- [[sources/raphlinus-good-parallel-computer]]
