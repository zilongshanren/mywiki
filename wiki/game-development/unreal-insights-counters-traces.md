---
tags: [unreal-engine, profiling, unreal-insights, stats-system, cpp]
date: 2026-04-19
sources: 1
---

# 给 Unreal Insights 与 Stats System 加 Counters / Traces

UE 的剖析体系实际上有两条路径并存：**老的 Stats System**（`stat XXX` 命令，显示在游戏视口里）和 **Unreal Insights**（离线 trace 后用专门 UI 查看）。它们有相同的动机——在代码里埋点拿运行时指标——但宏不一样，API 位置也不一样，[[tom-looman]] 的这篇文章把两边的用法对齐着讲了一遍。相关宏的头文件入口记一下：

- `Runtime/Core/Public/ProfilingDebugging/CountersTrace.h` —— Insights 的 Counters
- `Runtime/Core/Public/ProfilingDebugging/CpuProfilerTrace.h` —— Insights 的 Cycle Counters
- `Runtime/Core/Public/Stats/Stats.h` —— 老的 Stats System（部分项需要 `-statnamedevents`）

## 两类指标

- **Cycle Counter** —— 测某个函数或 scope 花的 CPU 时间。
- **Counter** —— 只是计数，适合记发生频率或当前实例数，例如 "活跃金币数"、"本局累计 Spawn 的 Actor 数"。

## Counters

Insights 侧的 Counter 最简，cpp 顶部声明，之后任意处 set/add/sub：

```cpp
TRACE_DECLARE_INT_COUNTER(CoinPickupCount, TEXT("Game/ActiveCoins"));
// 或 TRACE_DECLARE_FLOAT_COUNTER

TRACE_COUNTER_SET(CoinPickupCount, CoinLocations.Num());
TRACE_COUNTER_ADD(CoinPickupCount, N);
TRACE_COUNTER_SUBTRACT(CoinPickupCount, N);
```

采集时要带 `-trace=counters` 通道，才能在 Insights 的 Counters tab 看到。

Stats System 侧则要求先有 StatGroup，所有 stat 都挂在某个 group 下，视口上用 `stat game`、`stat anim` 之类命令按 group 显示。定义自己的 group：

```cpp
DECLARE_STATS_GROUP(TEXT("My Group Name"), STATGROUP_MyGroupName, STATCAT_Advanced);
```

声明一个计数型 stat 并在事件点累加：

```cpp
DECLARE_DWORD_ACCUMULATOR_STAT(TEXT("Actors Spawned"), STAT_ACTORSPAWN, STATGROUP_Game);
INC_DWORD_STAT(STAT_ACTORSPAWN);
```

## Cycle Counters

测执行耗时用 Scope Cycle Counter，在函数开头声明即可：

```cpp
DECLARE_CYCLE_STAT(TEXT("GetModuleByClass"), STAT_GetSingleModuleByClass, STATGROUP_LODZERO);

AWSShipModule* AWSShip::GetModuleByClass(TSubclassOf<AWSShipModule> ModuleClass) const
{
    SCOPE_CYCLE_COUNTER(STAT_GetSingleModuleByClass);
    // ...
}
```

用花括号可以把测量范围限制在一小段逻辑里，而不是整个函数。

## Named Events：带上下文的追踪

Named Events 是 Insights 的精细化追踪选项，能带出 "是哪个具体 Actor/Class 在跑这段逻辑"——不再只是 "有某个对象在 tick CharacterMovementComponent"，而是明确到 `BP_PlayerCharacter`。代价是开销显著（Tom 提到听过 20% 的数字），**不应该拿来衡量整体帧性能**，只用来做定点调查。

启用方式：命令行加 `-statnamedevents`，或者运行时 `stat namedevents`。宏用法：

```cpp
SCOPED_NAMED_EVENT(StartActionName, FColor::Green);
SCOPED_NAMED_EVENT_FSTRING(GetClass()->GetName(), FColor::White);
// TRACE_BOOKMARK(TEXT("StartAction::%s"), *GetNameSafe(Action));
```

`_FSTRING` 变体允许运行时字符串作为名字，但每次取 class name 本身也会增开销，需要谨慎使用。

## 实务建议

- **提前埋点** —— 功能刚做完时性能可能很好，随着内容和代码演进会劣化，预先埋好 stat 才能立刻定位。
- **只埋有用的** —— stat 本身有微小开销（仅 non-shipping 构建），更重要的是无效 stat 会污染视图、增加代码噪音。
- **stat none** —— 视口上一键清掉所有已打开的 stat 显示。

## 相关

- [[project-orion-action-roguelike]] —— Project Orion 里有大量 trace 实装示例

## Sources
- [[sources/tomlooman-unreal-insights-counters]]
- 相关：[[ue-observability-stack]] — Thomas Poulet 的五档调试工具栈；[[ue-asset-validator-blueprint]] — 蓝图内容验证
