---
tags: [source, software-design, build-systems, gui]
date: 2026-04-19
sources: 1
---

# dcmake: a GUI debugger for CMake（Chris Wellons / nullprogram）

[[chris-wellons]] 发表于 2026 年 4 月的文章，介绍基于 CMake 3.27 `--debugger` 模式和 DAP 协议构建的多平台 GUI 调试器 dcmake。

## 摘要

CMake 自 3.27（2023 年 7 月）起支持 `--debugger` 模式，通过 Debugger Adapter Protocol（HTTP-like JSON 消息）供前端启停、步进、断点、查变量。作者借助 AI 协作（呼应其 3 月的 [[sources/nullprogram-ai-programming-quiltcpp|上一篇]]）在 30 分钟内做出原型、一天内做出完整的多平台 GUI 应用 [[dcmake]]。界面用 Dear ImGui（docking 分支），Visual Studio 风格的键位（F10 步过、F11 步入、F5 继续、右键 run-to-line、悬停看变量、行号点击下断点）。macOS/Linux 走 GLFW + OpenGL 3；Windows 用原生 Win32 + DirectX 11。支持 Windows Unicode 路径，刻意避开 C++ 标准库 I/O——这点作者指出“当前前沿 AI 无法独立处理”。除了调试常规 `-B build` 配置，还能调试 `-P` 脚本模式。dcmake 将随下个 w64devkit 一起发布。

## 关键要点

- CMake DAP 模式是一个意外好用的扩展点
- Dear ImGui docking 分支几乎就是“调试器 UI 工具箱”，节省大量工作
- AI 做 UI 效果“惊人”：描述粗略、能自动补细节、甚至预测下一步需求
- Windows Unicode 全链路仍是 AI 的盲点，需要人工干预避开 C++ stdlib I/O
- 复用 Visual Studio 键位降低学习成本
- 估计没有 AI 作者要花一个月，现在只用一天

## 链接到的概念

- [[dcmake]]
- [[cmake-dap-debugger]]
- [[dear-imgui-docking]]

## 原文

- 链接：https://nullprogram.com/blog/2026/04/07/
- 本地：`raw/articles/nullprogram.com/2026-04-07_null-program.md`
