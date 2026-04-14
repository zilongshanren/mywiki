---
tags: [source, rendering, profiling, playcanvas, webgl]
date: 2026-04-14
sources: 1
---

# Performance Matters：PlayCanvas Profiler 发布（Will Eastcott / PlayCanvas Blog）

PlayCanvas CEO Will Eastcott 于 2015 年 11 月发布的短文，介绍了引擎内置的 Profiler 浮层的首个 beta 版本。

## 摘要

PlayCanvas Profiler 是一块叠加在运行应用上的调试面板，开发者按 Ctrl+Alt+T 即可切换显示。左侧列出场景的核心指标——帧率、启用相机数、着色器/材质/三角形计数——以及一帧耗时在 update、physics、render 三段的分解，用于快速定位掉帧根因。右侧是启动时间轴，标出 DOM interactive、preload 开始、main loop 启动等关键事件，并用绿色条带表示异步资源加载、橙色条带表示阻塞式着色器编译。后者对 Web 游戏尤为关键：首帧前的 shader 编译常常是隐性的体验杀手，时间轴把它们可视化出来后开发者才有对症下药的依据。这是 Profiler 的初始版本，定位是引擎内置、即用即看的性能观测工具。

## 关键要点

- 帧内剖析浮层是一种"即开即看"的性能观测范式，和离线 CPU profiler 互补
- 一帧耗时拆为 update / physics / render 三段是 Web 游戏引擎里的典型分法
- 启动时间轴把异步资源加载和 shader 编译可视化出来，避免稳态 FPS 数据掩盖启动瓶颈
- 浮层可切换开关（热键 Ctrl/Cmd+Alt+T），不干扰日常开发

## 链接到的概念

- [[frame-profiler-overlay]]
- [[bottleneck-analysis]]
- [[draw-call]]

## 原文

- 链接：https://blog.playcanvas.com/performance-matters-introducing-the-playcanvas-profiler
- 本地：`raw/articles/blog.playcanvas.com/2015-11-17_performance-matters-introducing-the-playcanvas-profiler-play.md`
