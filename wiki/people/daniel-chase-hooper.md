---
tags: [人物, 作者]
date: 2026-04-19
sources: 5
---

# Daniel Chase Hooper

独立软件开发者，前 Apple 工程师，设计工具 [Principle](https://principle.app) 的作者。主博客 `danielchasehooper.com` 以 C 语言、macOS / Swift、图形着色、编译与构建工具为主，风格是**动手做一个小工具把抽象概念变成可摸的东西**——例如用 DLL swap 给 Swift 搞 hot reloading、用 `fork/exec` 监听做跨平台构建可视化工具 *What The Fork*、以及用 `__builtin_clzll` 把 Segment Array 的寻址压到 10 条 x86 指令。2025-26 年也在博客里写了对 AI coding agent（Claude Code / Opus 4.5）在 C 项目里的实测，态度是「给具体指令用它当键盘替代，不要当大脑替代」。

## 相关

- [[segment-array]] — 稳定指针 + 对数段数 + 常数时间寻址的增长数组
- [[build-process-visualization]] — 用 `fork / exec / exit` 系统调用还原构建时间轴
- [[swift-dylib-hot-reloading]] — 不用 Xcode Previews，用 `dlopen` 做 SwiftUI 热重载
- [[ai-code-agent-workflow]] — 老 C 程序员眼里的 code agent 使用法
- [[binary-hot-reload]] — 游戏引擎 DLL 热重载（同思路的 C++ 对照）
- [[vibe-coding-workflow]] — 另一份 AI 代理编程工作流实录

## Sources

- [[sources/hooper-segment-array]]
- [[sources/hooper-build-visualizer]]
- [[sources/hooper-swiftui-hot-reloading]]
- [[sources/hooper-what-the-fork]]
- [[sources/hooper-testing-ai-c]]
