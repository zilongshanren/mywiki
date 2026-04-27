---
tags: [profiling, performance, game-engines, instruments, frame-hitch]
date: 2026-04-27
sources: 1
---

# 用时间轴标记隔离帧卡顿（Frame Hitch）

自适应采样 profiler（如 Instruments、VTune）的采样概率与代码执行时间成正比，这对稳定性能场景非常有效。但在"海量正常帧中混入极少数慢帧"的场景（即 **hitch**）面前，采样 profiler 会失效：假设 300 帧各 15 ms，混入 1 帧 60 ms，慢帧只占总采样时间的 1.3%，任何造成 hitch 的函数都会淹没在噪声里。

## Points of Interest：时间轴标记

解法是给时间轴加**用户自定义标记**，直观标出哪一帧是慢帧。Instruments 8.0 引入了 "Points of Interest" track，可以在代码里调用低级 syscall 插入单点标记或带起止的区间标记：

```c
// 单点标记（帧边界）
syscall(SYS_kdebug_trace, APPSDBG_CODE(DBG_MACH_CHUD, 0) | DBG_FUNC_NONE, 0,0,0,0);

// 区间标记（慢操作）
syscall(SYS_kdebug_trace, APPSDBG_CODE(DBG_MACH_CHUD, 1) | DBG_FUNC_START, 0,0,0,0);
/* ... */
syscall(SYS_kdebug_trace, APPSDBG_CODE(DBG_MACH_CHUD, 1) | DBG_FUNC_END, 0,0,0,0);
```

这样在 System Trace 的时间轴上，帧边界变为可见节点，慢帧区间一目了然，可以精确定位到导致卡顿的区域。

## 案例：X-Plane 的飞行中 GLSL 编译

Supnik 用此技术发现 X-Plane 的帧卡顿根因是**运行时 GLSL shader 编译**：当场景变化触发之前未缓存的 shader 变体时，driver 在帧中途同步编译，产生 45ms+ 的尖刺。这类问题在普通采样 profiler 下完全不可见，只有时间轴标记才能把"慢帧"和"慢帧里的慢操作"关联起来。

## 与 System Trace 的配合

标记需要在 Windowed 模式下配合 System Trace 使用（可看到每个 CPU 核的调度情况、VM 活动等），代价是分析工具本身会有一定性能开销。Instruments 8.0 还新增了 CPU 核视图中的橙色高亮，表示"可运行线程数超过核数"（调度饱和），这对诊断多核争抢导致的帧卡顿也很有用。

## Sources

- [[sources/supnik-instruments-slow-frames]]
