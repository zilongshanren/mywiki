---
tags: [内存管理, 分配器, cpp, 游戏引擎, bitsquid]
date: 2026-04-19
sources: 1
---

# 自定义 Allocator 抽象接口

C++ 给出的"自定义分配"机制都有明显的设计错位：

- **override global `new`**：只能一套策略走到底，拆不开 per-system / per-frame 需求。
- **per-class `new`**：只适合全局对象池，做不了 per-thread、per-streaming-chunk 的划分。
- **STL allocator**：要求模板化、要求所有实例等价、要 `rebind()`——反映的是 1990 年代支持 Win16 分段内存的设计目的，不是"我想一个子系统一个预算"的实际需求。

[[niklas-frykholm|Niklas Frykholm]] 在 Bitsquid 里走了另一条路：**一条抽象基类 `Allocator`**，三个虚函数。所有容器、所有系统都持有 `Allocator &`；调 `malloc` / 全局 `new` 直接 `assert(false)`。

```cpp
class Allocator {
public:
    virtual void  *allocate(size_t size, size_t align) = 0;
    virtual void   deallocate(void *p) = 0;
    virtual size_t allocated_size(void *p) = 0;
};
```

## 派生层级

- **`HeapAllocator`**：包装 dlmalloc。用 `create_mspace_with_base()` 让 dlmalloc 在给定内存块上建堆；`mmap` 重定向到 `PageAllocator`。
- **`PageAllocator`**：调 `VirtualAlloc` / `mmap`，以页为粒度向 OS 要内存；作为其他 allocator 的 backing。
- **`PoolAllocator`**：固定大小 slot 的对象池，无 header、零碎片。
- **`FrameAllocator`** = [[linear-allocator|bump / linear allocator]]：一帧内只推进指针，帧末整块 reset。作者仍要求它回答 `allocated_size()`——即使要多存几字节。
- **`ProxyAllocator(name, backing)`**：透传给 backing，但**按 name 计数与字节数**。`ProxyAllocator("sound", default)`、`"physics"`、`"anim"` —— 内存报表立刻按子系统切好。
- **`TraceAllocator`**：debug 用，记录 stack trace（trace 本身的存储走一个独立的 debug allocator，不影响真实预算）。

## 纪律

- **assert-on-leak**：每个 allocator 析构 `assert(_size == 0 && _allocations == 0)`，进程退出时由 global allocator 反向析构。**只要引入内存泄漏，build 当天就会炸**——根本不会带到 release。
- **子系统显式绑定**：容器构造函数都吃 `Allocator &`；高层要么 new 自己的 allocator，要么用 `memory_globals::default_allocator()`。
- **`allocated_size()` 强制实现**：为 memory tracking 付 per-allocation header 是值得的。
- **不用外部依赖的 `new`**：UnitTest++ 等库一律不用——"高性能库本就应该允许注入 allocator"。

## Bootstrap 问题

第一个 allocator 怎么来？不能 static init（析构时机不可控），不能 `new`（被禁了）。作者的做法：

```cpp
char _buffer[BUFFER_SIZE];
HeapAllocator *_static_heap = new (_buffer) HeapAllocator(
    NULL, _buffer + sizeof(HeapAllocator),
    BUFFER_SIZE - sizeof(HeapAllocator));
_page_allocator = _static_heap->make_new<PageAllocator>("page_allocator");
_heap_allocator = _static_heap->make_new<HeapAllocator>("heap_allocator", *_page_allocator);
```

`char _buffer[]` 是 BSS 段零初始化，不调用构造/析构；在它上面 placement-new 一个"静态 heap"，再从这个 heap 里派生出真正的 page/heap allocator。shutdown 逆序析构。

## make_new / make_delete

Placement-new 的语法太丑，作者写了一组模板（后来改成 variadic macro 省编译时间）：

```cpp
MyClass *m = allocator.make_new<MyClass>(arg);
allocator.make_delete(m);
```

## 和其他设计的关系
- 和 [[malloc-wrapper-debug|malloc 加壳（云风）]]对照：两者都是"给 C/C++ 分配机制套一层壳以便断言和监控"，云风偏 cookie + filename tracking，Bitsquid 偏 subsystem proxy + assert-on-leak。
- 和 [[virtual-memory|VirtualAlloc]] 的直接结合：page allocator 是 dlmalloc 的 backing，引擎可以切整段 VM 给 RSX、给 debug 数据、给 lua 堆，各自独立计数。
- **不提供 `realloc`**：作者认为它是"非确定性优化"；要 grow 就用"定长块链"自己 merge，可控、可预测。
- [[alloc-order-matches-draw-order]] —— 在 X-Plane 的 custom allocator 上做「精心聚拢」反而更慢的案例

## Sources
- [[sources/bitsquid-custom-memory-allocation]]
- [[sources/bitsquid-gc-and-allocation-sizes]] — 把全局分配压到页粒度的推理过程
