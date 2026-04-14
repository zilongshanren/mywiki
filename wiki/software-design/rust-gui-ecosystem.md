---
tags: [rust, gui, 生态, druid, xilem]
date: 2026-04-14
sources: 2
---

# Rust GUI 生态与 linebender 路线

Rust 社区对 GUI 的渴望由来已久——2019 年 Rust 调查里它排第 6 位"阻碍采用 Rust 的难题"，仅次于 async I/O。然而一个事实长期悬置：**每两三个月就冒出一个新 Rust GUI 工具包**，社区却始终没收敛出共识。[[raph-linus]] 从 Druid 一路开发到 Xilem 的经历，把这个生态的结构性问题写得最透。

## 为什么 Rust 适合写 GUI

Raph 的判断来自三个理由。一是 Rust 的**动态范围**——同一门语言既能把高层应用逻辑描述得精炼，又能一路下钻到位运算；传统 C++ OO GUI 框架里靠 C# / TypeScript / QML 等"粘合层"承担的职责，在 Rust 里可以留在语言内。二是**跨平台一致性**：crate 生态对 Windows / macOS / Linux 的覆盖度从 2019 年起持续成熟。三是**内存安全**：C++ 的 GUI 里对象生命周期出了名地复杂，takeoff / landing 时崩溃是家常便饭，而 Rust 的借用检查把这类 bug 从类别上消除。

## 为什么迟迟不收敛

Raph 把 Rust GUI 的发散状态类比 async Rust 的早年：callback vs poll future、`.await` vs `await!()`——当时每隔几个月就有人发一个号称"解决了 async 问题"的新 crate。他认为 GUI 的收敛比 async**更难**，因为不同人要构建的东西在语义层就不同：文档编辑器、3D / 视频内容、VST 嵌入宿主窗口、医疗设备界面、企业表单——它们对 reactive 表达力、帧率、与外部 3D 内容的兼容性的要求南辕北辙。

结果是一个**多峰生态**：

- **Druid / Xilem**（linebender）：研究导向，[[reactive-ui-rust|自研反应式架构]]，字体编辑器 Runebender 作为 hero app；Raph 把 Druid 主要定位为"教学和知识梳理"，不是产品
- **Iced**：Elm-like 反应式，async 友好，能作为 guest window 嵌入（VST 等场景），wgpu 做 3D
- **egui**：immediate mode，极低门槛，游戏内嵌调试 UI 的事实标准
- **Slint**：嵌入式 / 资源受限设备导向，DSL + Rust

Raph 明确表扬 Iced 的 Elm-like 架构比 Druid 的 lens 模型更易上手，并把它当作学习对象而非竞争对手。

## Druid 作为"学习载体"

Raph 对 Druid 的定位特别值得细读。他认为 Druid 的首要使命**不是**"做 Rust 里最好的 GUI"，而是**把 GUI 工程里那些分散在 Chromium / Gecko 代码库里、从没被系统文档化过的暗知识挖出来**——键盘事件处理、文本布局、脏区增量绘制、多窗口与 HiDPI 动态切换、焦点跳转、[[smooth-window-resize|平滑缩放]]……这些都是"看似简单其实有魔鬼"的细节。Druid 的成功标准于是变成「有人想知道 GUI 某个问题怎么解决时，Druid 代码库是最好的参考之一」。

## Vello：2D 渲染基础设施

上面这些收敛难题还有一个底层前提：**一套值得信赖的 2D 渲染引擎**。Raph 的 Vello（前身 piet-gpu）是 GPU compute-centric 的 2D 渲染器，直接用 compute shader 做 path geometry（flatten + offset、stroke 处理、font stem darkening 基于 Euler spiral），押注 wgpu / WebGPU 作为跨平台 GPU 抽象。2022 年他在 Xilem 和 Vello 之间明确"Vello 先"——因为 Xilem 的成败最终取决于能不能跑在一个达到生产质量的 2D 引擎上。

## Xilem：下一代反应式

Druid 的 lens 模型被社区批评门槛太高之后，Raph 在 2022 年把研究重心转向 Xilem——一个比 Dioxus / Sycamore / pax-lang 和各路 Elm 变种在他看来更简洁、更贴 Rust、async 兼容度更好的反应式架构。Xilem 的实现大部分靠社区，Raph 自己专注在不变数据结构（做高效稀疏 collection diff）等"纯算法"部分。这一步的动作结构很像：**先把研究原型（Crochet、High Performance Rust UI 演讲）和假设写清楚，然后让社区用真实应用去证伪或验证**。

## 愿望清单与阻碍

Raph 2020 年写的 wishlist 揭示了 Rust GUI 的几处硬依赖：

- **wgpu 成熟**：所有 GPU 侧路线都压在它上面
- **macOS Objective-C 绑定**：子类化 + autorelease 池 + 异构包装约定（foreign_object vs TCFType）至今让 macOS 平台层不好写
- **纯 Rust OpenType shaping**：Allsorts / rustybuzz 出现之前，Rust 想做 Linux 上的文本排版就得 FFI HarfBuzz
- **语言层面的 keyword arguments**：builder 模式和"struct + default"都嫌笨重
- **accessibility**：Raph 认为没有 a11y 的 GUI 工具包算不上"生产就绪"，而当时 Rust 社区还没人在做

## 判断

Rust GUI 不一定要收敛到**单一**架构。可能最终会是多峰稳态：egui 管调试面板、Iced 管中轻量应用、linebender 栈（Vello + Xilem）管需要顶级 2D 渲染质量与自定义交互的复杂应用。但**底层共享基础设施**（wgpu、文本布局、a11y、字体 shaping）收敛的价值非常大——这是 2020 年 Rust 2021 征文里 Raph 最明确的呼吁。

## 相关

- [[reactive-ui-rust]]
- [[smooth-window-resize]]
- [[raph-linus]]
- [[fearless-simd]]
- [[ecs-for-rust-ui]] — 2018 年 xi-win-ui 的原始架构笔记

## Sources

- [[sources/raphlinus-rust-2021-gui]]
- [[sources/raphlinus-smooth-resize-test]]
