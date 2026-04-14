---
tags: [source, rust, gui, druid, 生态]
date: 2026-04-14
sources: 1
---

# Rust 2021: GUI（Raph Levien / raphlinus.github.io）

[[raph-linus]] 回应 Rust 社区「2021 路线图征文」的帖子，盘点 Rust GUI 生态的现状、Druid 的定位，以及他对整合路径的判断。

## 摘要

Raph 承认 Rust GUI 还没有共识：每隔两三个月就有一个新工具包冒出来。但他坚信 Rust 的强项——宽动态范围（可以既写高抽象应用逻辑又写低层细节）、跨平台一致性、内存安全——特别适合写 GUI。文章给出 Druid 在 2020 年的进展：富文本排版、接近浏览器质量的键盘事件、基于脏区的增量绘制、多窗口、HiDPI 动态切换、焦点在 TextBox 间跳转。他明确说 Druid 还不能用于生产，主力测试应用是字体编辑器 Runebender。在「愿景收敛」一节里，他把 Rust GUI 的发散状态类比 async Rust 早年（poll vs callback、`.await` vs `await!()`），认为整合比 async 更难，因为人们想构建的东西本来就不同（文档编辑器 / 3D / 视频 / 行业内嵌）。他也表扬 Iced 的 Elm-like 反应式架构比 Druid 的 lens 模型更易懂，并把 Druid 的首要使命重新定义为**「教学和知识梳理」**——存档那些分散在 Chromium / Gecko 代码库里的 GUI 细节。文章末尾的 wishlist 包括：wgpu 成熟、macOS Obj-C 绑定改善、OpenType shaping 有纯 Rust 方案（Allsorts / rustybuzz）、以及语言层面的关键字参数。

## 关键要点

- **Rust 适合 GUI 的三个理由**：动态范围（高低层统一）、跨平台、安全（C++ 对象生命周期易崩）
- **Druid 不是产品，是研究载体**：首要使命是梳理并文档化 GUI 工程的暗知识，而不是争抢「Rust 最好的 GUI 库」
- **Elm-like 反应式** vs **lens 模型**：Iced 更易上手；Druid 的 lens 概念强大但对 app data 设计有负担；Crochet 是探索更易用反应式的原型
- **Runebender 作为 hero app**：字体编辑器作为真实驱动力，帮助设定优先级与排除 scope creep
- **"cycles" 项目管理技巧**：显式地把能无限膨胀的子问题（BiDi、accessibility）推到下一个 cycle
- **GUI 需要的 2D 基础设施本身也是大工程**：GPU 加速绘制、text layout、accessibility 都是独立大项目
- **语言愿望清单**：wgpu 成熟、Rust 关键字参数（替代 builder / struct default 模式）
- **Rust 生态的稀缺信号**：纯 Rust 的 OpenType shaping（Allsorts、rustybuzz）在当时是"其他语言都还没做到"的事

## 链接到的概念

- [[rust-gui-ecosystem]]
- [[reactive-ui-rust]]
- [[smooth-window-resize]]

## 原文

- 链接：https://raphlinus.github.io/rust/druid/2020/09/28/rust-2021.html
- 本地：`raw/articles/raphlinus.github.io/2020-09-28_rust-2021-gui.md`
