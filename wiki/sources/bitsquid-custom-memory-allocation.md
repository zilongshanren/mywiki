---
tags: [source, bitsquid, 内存管理, 分配器, cpp]
date: 2026-04-19
sources: 1
---

# Custom Memory Allocation in C++（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2010 年 9 月的文章，讲 Bitsquid 的自定义分配器体系——为什么不走 STL allocator、不重载 global new，也不让任何人再去 `malloc`。

## 摘要

C++ 标准给的三种"自定义分配"都不够用：override global new 没法区分子系统；每类重载 new 只能做全局对象池；STL allocator 要求所有实例等价、必须模板化、还要 `rebind()` —— 对真正想做 per-system / per-frame 内存控制的引擎毫无意义。Bitsquid 的做法是一条**抽象接口 `Allocator`**：三个虚函数 `allocate / deallocate / allocated_size`，所有分配都走它。调 `malloc` 或 `new` 直接 `assert(false)`。在这条接口上派生出 `HeapAllocator`（包装 dlmalloc）、`PoolAllocator`、`FrameAllocator`（bump）、`PageAllocator`（VirtualAlloc）、`ProxyAllocator`（转发并按子系统计数）、`TraceAllocator`（存 stack trace）。每个 allocator 析构时 `assert(_size == 0 && _allocations == 0)`——**引擎无法退出而不内存干净**。引导靠一块静态 `char _buffer[]` 做 bootstrap heap，placement-new 出第一个 `HeapAllocator`。

## 关键要点

- **唯一接口 = `Allocator &`**，所有容器构造函数都吃一个引用，[[handle-based-resource-manager|资源管理器]]、子系统各自造自己的；
- **virtual 可以忍**——分配本来就贵，一次 vcall 不值得为它去模板化所有类型；
- `allocated_size()` 强制所有 allocator 回答大小——即使 frame allocator 要多存几字节 header 才行；内存监控更重要；
- **Proxy allocator**：零成本的子系统级计数，`"sound"` / `"physics"` / `"anim"` 各一个，报表里一目了然；
- **Trace allocator**：按需开，记录 stack trace（在 debug allocator 里分配，不污染真实预算）。作者更偏好它而不是 `__FILE__`/`__LINE__`——后者在 Vector 一级都被归到同一行；
- **assert-on-leak** 比日志式检测更狠：一旦引入泄漏，shutdown 立刻炸，永远不会带进 release；
- **Bootstrap 分配器**：`char _buffer[BUFFER_SIZE]` → placement-new 首个 `HeapAllocator` → 再它创建 `PageAllocator` / `HeapAllocator`；析构顺序完全可控，不依赖 `_exit()` 回调；
- **make_new / make_delete 模板**替换 placement-new 语法噪声；后来改用 variadic macro 以省编译时间；
- **不用外部库的 `new`**——所有第三方库必须允许注入 allocator，否则不 pick；
- dlmalloc 作为 HeapAllocator 的底层，用 `create_mspace_with_base()` 让它在给定内存块上建堆；`mmap` 被重定向到 `PageAllocator`；
- `realloc` **故意不提供**——它是"不确定性的优化"，需要 grow buffer 时用 linked chain of fixed size buffers，可控、可合并。

## 链接到的概念

- [[custom-allocator-interface]]
- [[virtual-memory]]
- [[linear-allocator]]
- [[malloc-wrapper-debug]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2010/09/custom-memory-allocation-in-c.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2010-09-21_custom-memory-allocation-in-c.md`
