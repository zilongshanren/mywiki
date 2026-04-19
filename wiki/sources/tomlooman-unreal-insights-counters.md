---
tags: [source, unreal-engine, profiling, unreal-insights, stats-system]
date: 2026-04-19
sources: 1
---

# Adding Counters & Traces to Unreal Insights & Stats System（Tom Looman）

[[tom-looman]] 2026 年 3 月的文章，系统梳理 UE 的两套剖析接入方式——老的 Stats System（`stat XXX` 命令）和新的 Unreal Insights——以及两边的埋点宏。

## 摘要

UE 里埋指标有两条路径：Stats System 挂在 StatGroup 下、游戏视口上用 `stat <group>` 打开；Unreal Insights 用独立宏声明、采集后在离线 UI 查看。两类指标：**Counter** 记频次/实例数，**Cycle Counter** 记函数或 scope 的 CPU 时间。Insights 侧宏最简——`TRACE_DECLARE_INT_COUNTER` 声明，`TRACE_COUNTER_SET/ADD/SUBTRACT` 读写，采集时带 `-trace=counters`。Stats System 侧要先 `DECLARE_STATS_GROUP` 建组，然后 `DECLARE_DWORD_ACCUMULATOR_STAT` + `INC_DWORD_STAT` 或 `DECLARE_CYCLE_STAT` + `SCOPE_CYCLE_COUNTER`。进一步还介绍 Named Events——带具体 Actor/Class 名字的精细化追踪，用 `SCOPED_NAMED_EVENT` / `SCOPED_NAMED_EVENT_FSTRING` 开启，代价较大（听说过 20% 开销），只适合定点调查不适合测整体帧性能。最后给出实务建议：提前埋、只埋有用的、用 `stat none` 一键清屏。所有示例代码都能在 [[project-orion-action-roguelike]] 的源码里找到对照。

## 关键要点

- 两套剖析宏入口：`CountersTrace.h`（Insights Counter）、`CpuProfilerTrace.h`（Insights Cycle Counter）、`Stats.h`（Stats System）
- Insights Counters 需要 `-trace=counters` 通道才能采到
- Cycle Counter 可以用 `{}` 限定测量范围到函数中的一小段
- Named Events 带上下文但开销大，有时需 `-statnamedevents` 或 `stat namedevents`
- `TRACE_BOOKMARK` 可在 Insights 时间线打书签，便于定位事件

## 链接到的概念

- [[unreal-insights-counters-traces]]
- [[project-orion-action-roguelike]]
- [[tom-looman]]

## 原文

- 链接：<https://tomlooman.com/unreal-engine-profiling-stat-commands/>
- 本地：`raw/articles/tomlooman.com/2026-03-19_adding-counters-traces-to-unreal-insights-stats-system.md`
