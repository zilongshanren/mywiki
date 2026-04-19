---
tags: [source, ue, unreal, 物理, 观测性, 工具, 2024]
date: 2026-04-19
sources: 1
---

# The tools we use to develop our physics game in UE5（Thomas Poulet / 2024）

[[thomas-poulet]] 2024 年 7 月写的 UE5 工程实践文。他们公司除了 AAA 咨询还在做一款自家的物理驱动游戏——物理角色控制器是一类著名的「Jenga 式复杂系统」，每调一参就破另一处。Poulet 把他们一路淘出来的**可观测性工具栈**按适用层级排了一遍。

## 摘要

核心主张是 **observability 决定迭代速度**：一个物理模型要好调，前提是「系统内部状态能以方便的形式摆在设计师面前」。文章梳理了 UE 里五档工具：On-screen log → Gameplay Debugger → Visual Logger → ImGui → 自研 Ariadne。每一档都写了最小可跑的 C++ / BP 接入片段，踩过的坑（比如 GDT 要在 `PreDefault` 阶段加载的模块里注册、Visual Logger 没有 `UE_VLOG` 就抓不到快照），以及为什么升下一档。终点站 Ariadne 把「每个变量自动被反射到 server、设计师自己在 Grafana 里拼 dashboard」作为设计原则，让工程师退出观测性回路。表格给出五档的 pros/cons/接入层/时序性。

## 关键要点

- 物理角色控制器的苦来自**可见性不足**，不是算法不够聪明。
- **On-screen log 的关键是 unique key**：`(ModuleKey << 32) | ValueKey`，一个模块一个 ModuleKey 避免消息互盖。
- **Gameplay Debugger** 留了 93 个自定义 category；接入需要单独的 debug 模块（因为要 `PreDefault` 阶段加载）、在 `Build.cs` 里 `SetupGameplayDebuggerSupport`；`FGameplayDebuggerCategory` 的 `CollectData` + `DrawData`；可以挂 `FDebugRenderSceneProxy` 画 3D 可视化。
- **Visual Logger** 走 `IVisualLoggerDebugSnapshotInterface::GrabDebugSnapshot`，配 `UE_VLOG` / `UE_VLOG_ARROW` / `UE_VLOG_HISTOGRAM`；痛点：图表时间窗只有 0.5s，只能在主 viewport 显示，C++ only。
- **ImGui** 自由但要工程师手工接每一个变量，设计师受制于 check-in 节奏。用了 [Network ImGui plugin] 做远程调试（目标机推回 PC）。
- **Ariadne**（自研）：以 server 为中心，**actor 打 tag → 所有 property 自动上报** 是设计破口；前端接 Grafana，设计师 WYSIWYG 拖面板。作者甚至拿来分析自己在 Forza 的赛道表现。
- 选工具的四个参数：**rate of change / data type / update frequency / live-or-historical**。

## 链接到的概念

- [[thomas-poulet]]
- [[ue-observability-stack]]
- [[unreal-insights-counters-traces]]
- [[runtime-editor-console-connection]]

## 原文

- 链接：<https://blog.thomaspoulet.fr/posts/the-tools-we-use-to-develop-our-physics-game-in-unreal-engine-5/>
- 本地：`raw/articles/blog.thomaspoulet.fr/2024-07-22_the-tools-we-use-to-develop-our-physics-game-in-unreal-engin.md`
