---
tags: [C++, Rust, 库设计, 编译时间, 分配器, 协程]
date: 2026-04-14
sources: 1
---

# rpp：Rust 风味的 C++ STL 替代库

**rpp** 是 [[max-slater|Max Slater]] 个人项目用的一套 C++20 基础设施，定位是 STL 的完整替代品，灵感大量来自 Rust（连名字都是）。它同时也是一篇更务实的陈述：**如果你愿意接受一个小的、非通用、只为自己服务的库，C++ 的很多历史包袱其实是可以丢的。**

## 设计目标（按优先级）

1. **快编译**：include rpp 不应让编译时间增加 >250ms；任何 STL 或系统头文件（`windows.h`、`std::chrono`）都不得泄漏到用户侧。
2. **好调试**：debug build 要跑得动，断言密集，禁用 exceptions / RTTI，使用 concepts 产生可读的编译错误。
3. **显式性**：所有非平凡操作必须在源码中可见——禁用隐式拷贝、隐式转换、隐式分配。
4. **性能**：region allocator、协程调度器、针对内存布局的数据结构默认值。
5. **元编程**：集中在 `constexpr` + concepts，再加一套反射。

## 为什么 STL 是编译时间杀手

Slater 用 MSVC profile 跑了一份主流风格的 C++17 项目（10 万行含依赖，20 秒编译）。绝大部分时间花在**处理头文件**上：仅包含 `std::chrono` 一项就吃掉某个 TU 的 75% 时间；最慢的 TU 在前端里 spent 10 秒解 constraint、实例化模板。rpp 里同样 10 万行的渲染项目编译只要 3 秒——秘诀不是「rpp 实现得有多快」，而是**STL 根本没被 include 进来**：

- 与 libc、Windows/Linux API 的交互集中到单独的 TU，用 opaque handle 暴露。
- rpp 自己重新实现了他实际用到的 STL 容器与算法；避不开的只剩 `std::initializer_list` 与 `std::coroutine_handle`（语言内建），它们被手工 extern 到一个不 include 任何东西的头文件里。

## 数据结构总览

五种指针语义各不相同：`T*`（极少用）/ `Ref<T>`（非空、非所有）/ `Box<T,A>` / `Rc<T,A>` / `Arc<T,A>`。

容器族：`String<A>` / `String_View`（无 SSO，长度显式分配）、`Array<T,N>`（固定长）、`Vec<T,A>` / `Slice<T>`、`Stack/Queue/Heap<T,A>`、`Map<K,V,A>`（Robin Hood 开放寻址，见 [[open-addressing-hashtable]]）。`Opt<T>` 和 `Variant<A,B,...>` 作为值类型错误处理与和类型——后者通过 `match(Overload{...})` 做 pattern matching。`Function<R(Args...)>` 强制 SSO，永不分配；需要更大容量时用 `FunctionN`。

所有非平凡类型**必须**显式 `clone()` 才能复制。`Clone` 是 concept，允许泛型代码在 trivially-copyable / Clone / Copy-Constructible 三档里选最快的实现。构造函数几乎都是 `explicit`，代价是模板参数推导变弱——常常得显式标注类型。

## Region 分配器：Rust brand 的穷人版

rpp 的分配器是**类型**，不是运行时对象——与 STL 的 PMR 不同，它没有虚表开销。最有意思的是 `Mregion<R>`：一个全局、thread-local、chunked 的栈分配器，传入 `R` 作为 **brand**。

```cpp
Region(R) {
    Vec<u64, Mregion<R>> local_vector;
    local_vector.push(1);
} // R 结束，所有分配自动回收
```

Region 地域安全在 Rust / OCaml 里能靠生命周期静态检查，但 C++ 没有——于是 rpp 用**运行时 brand 检查**兜底：分配或释放时对比当前 region brand 与数据结构 brand 是否一致，不一致就 assert。Brand 是从 source location 推导的编译期常量，零运行时开销。

另一种折中：`Mpool` 是固定块大小的 freelist，为 `Box/Rc/Arc` 提供中等寿命对象的几近零开销分配。每个 size 的 pool 独立统计。

## Tracing 与反射

所有分配事件按帧记录，方便追「平均零分配/帧」这种目标；同款机制也用来做 `Trace("Name") { ... }` 的 tracing profiler，由用户代码遍历结果时间树。

反射系统用显式 `RPP_RECORD(Data, RPP_FIELD(ints), ...)` 生成 `Refl` 特化，不依赖编译器补丁。内建 `Format::Write` 模板偏特化给出一个泛型 printf，而且作者扩展了一个类似的系统给 Dear ImGui 自动生成任意类型的 UI——反射 + 模板组合的典型工业用法。

## 协程与异步 I/O

C++20 协程被 rpp 当作主线异步原语。`Async::Task<T>` 内部只是协程 frame 指针 + 一个状态字；借助 [Raymond Chen 的状态机设计](https://devblogs.microsoft.com/oldnewthing/20210416-00/?p=105115)，Promise 的生命周期不需要引用计数，所有状态转移都用单次原子写完成。scheduler 支持 symmetric transfer 直接 resume 后继任务。同一机制还能 `co_await` 平台事件（`HANDLE`、eventfd），让 GPU fence 变成可 awaitable 的 task：

```cpp
co_await vk.async(pool, [](Vk::Commands& cmds) { /* 填 command buffer */ });
```

## 取舍与教训

- **不是 production-ready 库**，也不打算推广给团队使用。
- **显式性带来的推导缺失**：模板参数经常要手写。
- **协程仍踩编译器 bug**：MSVC 19.37 的 symmetric transfer 崩溃；Clang 早期也有。实用性比理论上差一点。
- **没转 Rust** 的理由很具体：图形/游戏工作流对 borrow checker 不友好，痛的 bug 来自 GPU 而非内存/并发；Rust 编译速度（之前）不够快；Jai 九年没等到编译器。

这篇文章的更高一层意义在于——它示范了「写自己的 STL」的可行性与边界：对个人或小团队项目，**放弃通用性以换显式 / 快编译 / 控制流清晰** 是一桩合算的生意。

## 相关

- [[cpp-multi-paradigm-discipline]] — C++ 的多范式诅咒：团队要先选子集
- [[cpp-runtime-reflection]] — 另一种 C++ 反射路线（libclang 生成）
- [[open-addressing-hashtable]] — rpp `Map` 的理论基础
- [[linear-allocator]] — region 的最小内核
- [[max-slater]]

## Sources

- [[sources/slater-oxidizing-cpp]]
