---
tags: [cmake, debugger, build-systems]
date: 2026-04-19
sources: 1
---

# CMake 的 DAP 调试模式

CMake 自 3.27（2023 年 7 月）起内建 `--debugger` 选项，实现了 Microsoft 的 [Debugger Adapter Protocol (DAP)](https://microsoft.github.io/debug-adapter-protocol/)。DAP 是一个 HTTP-like 的 JSON 消息协议，原本为 VS Code 等前端与调试器后端的通用对接设计。

这样一来 CMake 自己成为一个可被前端调试的程序：客户端可以启动、暂停、断点、step over/in、查变量、watch 表达式，直接操纵一次 CMake 配置过程。

适用场景：

- 调试复杂的 `CMakeLists.txt` 配置逻辑、深入 `include()` 链
- 调试 `cmake -P script.cmake`——CMake 在这种模式下作为平台无关的脚本语言运行
- **不适合** `cmake --build`——那阶段 CMake 已经把控制权交给具体构建工具

[[chris-wellons]] 基于这个接口做出了 [[dcmake]]，按自己的话说：“CMake 到了 2023 年才提供这个能力，这是个意外好用的扩展点。”

## 相关

- [[dcmake]]

## Sources

- [[sources/nullprogram-dcmake]]
