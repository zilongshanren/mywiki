---
tags: [source, C++, Rust, 库设计, 编译时间, 协程]
date: 2026-04-14
sources: 1
---

# Oxidizing C++（Max Slater）

[[max-slater|Max Slater]] 2024 年 1 月发布的长文，介绍他为个人图形 / 游戏项目写的 C++20 基础设施 **rpp**，风格以 Rust 为主要灵感来源。目的不是推广，而是记录一套高度个性化的 C++ 子集：只要愿意放弃通用性，就能拿到快编译、显式性与控制力上的巨大回报。

## 摘要

文章按五块展开：

1. **编译时间**：MSVC profile 显示主流 STL 风格代码 80% 时间花在处理头文件与模板实例化上；仅 `std::chrono` 一行包含就能吃掉某 TU 的 75%。rpp 通过全面替换 STL + 把系统头集中到单独 TU，把 10 万行项目编译时间从 20 秒压到 3 秒。
2. **数据结构**：五种指针（`T*`、`Ref`、`Box`、`Rc`、`Arc`）、无 SSO 的 `String`、`Array/Vec/Slice`、Stack/Queue/Heap、Robin Hood `Map`、`Opt`、`Variant`（带 pattern match 的 `match(Overload{...})`）、`Function` 强制 SSO。显式 `clone()` 取代隐式拷贝。
3. **分配器 + Region**：分配器是**类型**不是对象，完全编译期决定。`Mregion<R>` 栈分配器用 brand 做运行时检查——近似 Rust 生命周期。`Mpool` 给中等寿命对象提供固定块 freelist。所有分配 per-frame 追踪，配合 tracing profiler。
4. **反射**：显式 `RPP_RECORD` 宏生成 `Refl` 特化，驱动泛型 printf 与 ImGui UI 自动生成。
5. **协程**：`Async::Task<T>` = 协程 frame 指针 + 状态字；Promise 生命周期用 Raymond Chen 的状态机 + 单次原子完成转移；支持 symmetric transfer 与平台事件 awaitable（GPU fence 直接变 task）。

文末附录解释「为什么不干脆转 Rust」——图形 / 游戏项目对 borrow checker 不友好，真正的 bug 在 GPU 那边；Rust 编译慢（前）；Jai 九年未公开；C/D/Odin/Zig 改善不足。

## 关键要点

- **STL 是 C++ 编译时间的主要来源**，替换比精简更有效。
- **region 分配器 + brand** 是 Rust 生命周期在 C++ 的可落地近似，运行时检查 + 零运行时开销。
- **分配器作为类型**而非 PMR 的 `memory_resource` 对象，避免虚表调用。
- **显式 clone** 是大多数 bug 的预防：所有非平凡复制都在源码里可见。
- **C++20 协程**已足够用作主线异步原语，但编译器实现仍有 bug。
- **反射靠 macro + 手工特化**能撑到真正的语言级反射落地。
- **不是 production-ready 库**——是一篇「个人项目可以怎样重建 C++ 子集」的论证。

## 链接到的概念

- [[rpp-stl-replacement]]
- [[cpp-multi-paradigm-discipline]]
- [[open-addressing-hashtable]]
- [[cpp-runtime-reflection]]
- [[linear-allocator]]
- [[max-slater]]

## 原文

- 链接：https://thenumb.at/rpp/
- 本地：`raw/articles/thenumb.at/2024-01-06_oxidizing-c.md`
