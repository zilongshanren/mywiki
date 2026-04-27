---
tags: [concurrency, tsan, threading, race-condition, debugging, clang]
date: 2026-04-27
sources: 1
---

# ThreadSanitizer（tsan）：游戏引擎级竞态检测

ThreadSanitizer（tsan）是 Clang/GCC 的一项动态分析工具，通过影子内存（shadow memory）记录每个内存位置的线程访问历史，在内存操作被修改为与影子内存交互的版本时，实时检测未同步的并发读写。与 [[undefined-behavior-c-cpp|UB]] 相关的竞态条件不只在发生 "Really Bad Data" 时才被捕捉——只要访问缺少同步，tsan 就会报告，这使它能在每次启动时稳定复现那些在生产环境里极少触发的 bug。

## 关键特性

tsan 在**同步点之间**寻找竞态，而不依赖实际执行顺序。这意味着：
- 即便正常运行从不触发问题，tsan 也能在 instrumented 构建中发现它
- 与 [[undefined-behavior-c-cpp|UB]] 的编译器重排问题不同，tsan 针对的是运行时访问模式

代价是精度有限：同时跟踪超过四个线程时，影子内存可能发生驱逐（eviction），历史被清除，导致某些竞态漏报。

## X-Plane 案例集

Supnik 在为 X-Plane 引入 tsan 的第一次会话中依次命中了三类竞态：

**1. 良性竞态（Benign Race）**：主线程读取纹理质量 preference，同时后台线程已开始加载纹理。代码重构使后台线程在不需要 preference 值时完全跳过读取，消除竞态而不改变逻辑。

**2. 真实 Bug（"bounce between threads"惯用法的误用）**：机场挤出任务向共享 shader-layer vector 添加元素，多个任务在不同线程各自"跳回"主线程修改同一 vector，导致偶发 vector 扩容时的 use-after-free。此 bug 的崩溃报告已积累一段时间，但开发者本机从未复现。tsan 使其在每次启动时稳定触发。

**3. 双缓冲方案设计缺陷**：天气引擎用双缓冲让主线程和 worker 并行，但没有保证 worker 在同一帧内完成并同步。当 worker 较快时，它在主线程换缓冲之前同步完毕，tsan 认为无问题；只有 worker 较慢时才暴露竞态。这个 bug 需要 tsan 运行约 30 分钟才被捕捉到。

## 与"良性竞态"的哲学

[[undefined-behavior-c-cpp|UB]] 时代已经关闭了"我知道这个竞态是安全的"的大门——要确认良性，至少需要：原子访问在目标架构上天然对齐、所有可能执行顺序下语义不变、以及 Clang 没有把未同步代码重排成危险形式（而 Clang 有这个权利）。现实中第三条几乎无法静态证明，因此 Supnik 的结论是：不管竞态看起来多无害，都应该消除。

## Sources

- [[sources/supnik-race-condition-vroom]]
