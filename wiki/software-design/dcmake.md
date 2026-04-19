---
tags: [cmake, debugger, imgui, ai-assisted]
date: 2026-04-19
sources: 1
---

# dcmake：CMake 的 GUI 调试器

dcmake 是 [[chris-wellons]] 2026 年 4 月用一天时间完成的多平台 CMake GUI 调试器，充分利用 CMake 自 3.27（2023 年 7 月）起提供的 [[cmake-dap-debugger|--debugger 模式]]。

功能与 UX：

- [Dear ImGui](https://github.com/ocornut/imgui) docking 分支——所有“窗口”可自由拖出浮动或吸附
- Visual Studio 风格键位：F10 step over、F11 step in、F5 continue、Shift+F5 stop、行号点击打断点、右键 run-to-line、hover 看变量
- UI 状态持久化，秒开

支持的目标：

- `cmake -B build` 配置过程
- `cmake -P` 脚本模式（CMake 在这种模式下相当于一个平台无关的 shell 脚本语言）
- 不支持 `--build`（那阶段没有 CMake 可调试）

跨平台后端：

- **macOS / Linux**：GLFW + OpenGL 3
- **Windows**：原生 Win32 窗口 + DirectX 11

Windows Unicode 全链路支持需要特别注意 **不要用 C++ 标准库的 I/O**——这一点 [[chris-wellons]] 指出“当前前沿 AI 尚无法独立处理”，必须人工引导。macOS 平台层需要一点 Objective-C，这部分也主要交给 AI 完成。

意义：它是作者 [[ai-driven-conformance-clone|AI 协作编码方法论]]的自我示范——作者预估 2026 年前自己要花一个月才能做出 dcmake。

## 相关

- [[cmake-dap-debugger]]
- [[dear-imgui-docking]]
- [[chris-wellons]]

## Sources

- [[sources/nullprogram-dcmake]]
