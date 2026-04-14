---
tags: [source, gui, rust, desktop, 窗口系统]
date: 2026-04-14
sources: 1
---

# The smooth resize test（Raph Levien / raphlinus.github.io）

[[raph-linus]] 发表于 2019 年 6 月的短文，把「拖动窗口左边时右边是否稳定」这件小事，提炼为评估桌面 GUI 工具包的一项基础体检。

## 摘要

Raph 把平滑窗口缩放当作一项诊断：打开待测应用，抓住窗口**左边缘**来回拖动，观察右边缘是否稳定、滚动条有没有抖动。这个动作横跨了 GUI 工具包的多层架构——从与窗口管理器的同步、到事件循环的线程与时序、再到布局与绘制的分阶段策划。文章指出，3D 图形管线天生是异步的（命令提交后由 GPU 稍后渲染再呈现），在稳定窗口下问题不大，但一旦窗口帧在被拖动，内容与边框就会互相错位，产生肉眼可见的抖动。作者给出 macOS 和 Windows 两套工程解法：macOS 用 `CAMetalLayer` + `presentsWithTransaction` 把呈现纳入 CA 事务；Windows 则在 `WM_ENTERSIZEMOVE` 期间切回「redirection buffer」路径（或 `DXGI_SWAP_EFFECT_SEQUENTIAL`），结束后再切回高性能 flip 模式。作者的结论是，winit 的双线程事件循环模型让同步版 resize 处理异常困难，这也是他在 Druid 里选择自己写 window creation 的主要原因。

## 关键要点

- **resize 拖动是 GUI 体系结构的照妖镜**：同时暴露 swapchain 呈现模型、事件循环异步性、布局与绘制的先后次序
- **两条不同步的级联**：窗口边框由 WM 更新、内容由 GPU 管线更新，没有显式同步就会抖
- **macOS 药方**：`CAMetalLayer` + `presentsWithTransaction`，把当前帧并入 CoreAnimation 的事务提交（Tristan Hume 给出的配方）
- **Windows 药方**：旧的 `DXGI_SWAP_EFFECT_SEQUENTIAL` 走 redirection buffer 自带同步；flip model 性能高但与 WM 异步，需要在 `WM_ENTERSIZEMOVE`/`WM_EXITSIZEMOVE` 之间切换路径
- **winit 双线程模型**的代价：application 线程与 event loop 线程通过 channel 异步耦合，resize 时没有同步 draw 完成的机制，促使 Druid 自绘窗口
- **imgui 的一帧延迟**：layout 与 draw 在同一次调用里完成时，常用「基于上一帧 layout 绘制」来简化，resize 时表现为内容落后一帧
- **布局 → 绘制必须分阶段**：任何工具包都需要先计算尺寸再开始绘制，否则 resize 时无法做到「这一帧内就与新尺寸一致」

## 链接到的概念

- [[smooth-window-resize]]
- [[rust-gui-ecosystem]]
- [[reactive-ui-rust]]

## 原文

- 链接：https://raphlinus.github.io/rust/gui/2019/06/21/smooth-resize-test.html
- 本地：`raw/articles/raphlinus.github.io/2019-06-21_the-smooth-resize-test.md`
