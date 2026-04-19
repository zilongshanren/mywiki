---
tags: [source, 构建系统, 可观测性, 工具]
date: 2026-04-19
sources: 1
---

# I Made A Real-Time Build Visualizer（Daniel Hooper）

[[daniel-chase-hooper]] 2025 年 8 月介绍他做的跨平台构建可视化工具 *What The Fork*（`wtf`）——在任意构建命令前加 `wtf` 前缀，就能看到所有进程的时间轴甘特图；和构建系统 / 语言无关，因为它只监听 OS 的 fork/exec/exit 系统调用。

## 摘要

大多数构建慢不是因为代码多，而是**做了可以被看见就能修掉的蠢事**——串行编译、启动空转、重复探测环境——但没有可视化就看不见。作者为此写了 *What The Fork*：通过 macOS 的 EndpointSecurity、Linux 的 ptrace、Windows 的 ETW 抓进程生命周期事件，还原完整构建时间轴。文章展示了几个真实案例：某 cargo 项目 10 核机器上依赖 crate 单线程编译（可提速 10×）；CMake 为探测环境反复递归 `cmake→make→make→clang`，整个构建重复了 85 次；xcodebuild 启动空转 6 秒、尾段只剩 1–2 个 clang；ninja 构建 LLVM 则是 0.4 秒就 busy。工具作为「事实上的构建速度上限标杆」功能，对优化 CI clean build 特别有用。

## 关键要点

- 三平台 API：macOS EndpointSecurity、Linux ptrace、Windows ETW——都痛苦但能拼出 `(pid, parent_pid, timestamp, cmdline, cwd)` 事件流
- 构建终端输出只能看到顶层命令，**看不到孙子进程**（clang 调 ld、CMake 的环境探测链）——必须走 syscall 层
- 可视化直接暴露四类问题：无并行、冗余重做、启动空转、随机依赖顺序
- Ninja 作为 baseline：2.47M 行 LLVM 0.4 秒开始编译，xcodebuild 6 秒启动
- CI clean build 是首要场景：某用户 35s → 3.3s
- 副产品：技术也能 profile 任意派生子进程的程序，不止构建

## 链接到的概念

- [[build-process-visualization]]
- [[segment-array]] — wtf 内部用来存事件流
- [[ci-cost-optimization-asg]]

## 原文

- 链接：<https://danielchasehooper.com/posts/syscall-build-snooping/>
- 本地：`raw/articles/danielchasehooper.com/2025-08-13_i-made-a-real-time-build-visualizer.md`
