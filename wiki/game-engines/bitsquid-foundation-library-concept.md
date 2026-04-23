---
tags: [foundation-library, cpp, allocator, collections, bitsquid, open-source]
date: 2026-04-19
sources: 1
---

# Bitsquid Foundation Library：最小可用的引擎基座

2012 年 11 月 [[niklas-frykholm|Niklas Frykholm]] 在 Bitbucket 以 MIT 协议开源的**引擎基座库**，用意不是"给 Bitsquid 的人用"——Bitsquid 自己内部早就有一份类似代码——而是给社区里"想从零搭引擎"的独立开发者一个起点。它本身代码量极小，历史地位更大：**它是 Bitsquid Blog 先前几篇主张（[[types-h-data-code-separation]]、[[custom-allocator-interface]]）的第一份公开完整示范代码**，让这些主张从 blog post 的讨论变成可以 `hg clone` 下来上手的实物。

## 三条主张合体

foundation 库几乎每个文件都在实践 Bitsquid Blog 先前文章里的某一条想法：

- **数据/代码分离**：`collection_types.h` 只放 `Array<T>` / `Hash<T>` / `Queue<T>` 的骨架（成员 + C++ 强制的运算符，仅此而已），所有操作函数在 `array.h` / `hash.h` / `queue.h` 的 namespace 里。想 patch `Array` 加 `shift` / `binary_search`？开一个 `array_extensions.h` 往同 namespace 里加函数，与官方函数**完全对等**——这是 [[types-h-data-code-separation]] 的落地点。
- **Allocator as first-class**：抽象基类 `Allocator` 带 `allocate/deallocate/allocated_size` 三个虚函数；所有容器**构造函数显式收 `Allocator &`**。没有 `malloc`、没有 `new`、没有隐藏全局 allocator。具体实现有 `MallocAllocator` / `ScratchAllocator` / `TempAllocator<BYTES>`。详情见 [[custom-allocator-interface]]。
- **反 STL 集合**：POD-only，不调 ctor/dtor，`memmove` 搬数据。Frykholm 的理由："存非 POD 就用指针"——把构造/析构的时机和位置交还给调用方。

## 临时内存三级级联（本库独有）

foundation 最值得单独看的设计是 `ScratchAllocator` + `TempAllocator` 的两层组合：

**`ScratchAllocator`** 是一圈**环形缓冲**。两个指针：`allocate` 向前走分配、`free` 跟在后面释放。只做指针算术，不碰 `malloc`。环满时**不崩**——fall back 到底层 `MallocAllocator`，只是慢了。一个"陷阱"要注意：长寿命分配混进 scratch 会卡住 `free` 指针无法追上 `allocate` 指针，scratch 越用越窄，直到全部退化到 `malloc`；这是工程纪律问题不是 bug。

**`TempAllocator<BYTES>`** 是 scoped allocator，在栈上预留 `char buffer[BYTES]`；落出作用域时自动释放。请求先从栈 buffer 出，栈不够走 scratch，scratch 不够走 `malloc`——三级级联。典型用法：

```cpp
void test() {
    TempAllocator1024 ta;
    Array<char> message(ta);   // 绝大多数情况直接命中栈
    ...
}   // ta 析构 → message 的内存自动回收
```

这是一个被后来很多引擎（Our Machinery、The Machinery、以及 Bitsquid 的后继 Stingray）继承并细化的模式。它的要害不是"环形缓冲"（很普通）而是**让整个集合类家族天然配合这种临时内存**——因为集合类已经显式接收 `Allocator`，同一个 `Array<T>` 既能用 `MallocAllocator` 长期存在，也能用 `TempAllocator` 活一个函数作用域。

## 反 STL 的集合设计

除了 allocator，foundation 的集合类还有几处**有意的简化**：

- **`Hash<T>` 固定用 `uint64_t` 作为 key**；key 放不下 64 bit 自己先 hash。没有"generic Hashable" trait。
- **`string_stream` 不是类**，就是一组在 `Array<char>` 上操作的函数，放在 `string_stream` namespace。这是"函数按功能组织"最干脆的例子——StringStream 和 Array 本是同一块内存，只是**两套不同的函数视角**。
- **`hash` 与 `multi_hash` 共享 `Hash<T>`**：单键和多键两套语义，共用同一个底层存储。传统 OOP 思维里这会是两个 class + 代码重复。

## 历史意义与局限

**承上**：它把 Bitsquid Blog 2010 年起讨论的 [[custom-allocator-interface]]、2012 年 9 月的 [[types-h-data-code-separation]] 一次性集成成可运行代码。Stingray、Our Machinery 的底层风格都可以追回这里。

**启下**：对之后一批"自研极简 C++ 引擎"——[[ant-engine]]、[[mach-engine]]、The Machinery——是可直接 cargo cult 的参考。

**局限**（文章自己承认）：

- 线程安全没做；allocator 不是 thread-safe（评论区讨论后打算给一个可选的 critical section 接口）
- `PageAllocator` 没写（要跨平台）；最底层直接用 `MallocAllocator`
- 数学模块没做（planned）
- 不做 exception、不做 RTTI、不兼容 STL——这些都**不是 bug 是特性**（合 [[orthodox-cpp]]）

## 为什么它在 2026 年还值得读

2012 年的大多数 C++ 库代码今天读起来会觉得"那时候的人怎么这么原始"。foundation 库的反面：**它今天读起来依然很像现在顶级独立引擎的基座代码**。原因是 Frykholm 当年要解决的问题（allocator 控制、compile time、模块化扩展、最小 POD 容器）至今没变——C++ 的 STL 也没真的解决它们——所以这份代码变成了跨越十几年的活教材。

## 相关

- [[niklas-frykholm]]
- [[types-h-data-code-separation]] —— foundation 最重要的头层模式
- [[custom-allocator-interface]] —— foundation 的 allocator 抽象来源
- [[header-hero-compile-analysis]] —— 这种 header 组织方式能把 blowup 压到多少的测量工具
- [[orthodox-cpp]]
- [[aos-vs-soa]]
- [[ant-engine]]
- [[mach-engine]]

## Sources

- [[sources/bitsquid-foundation-library]]
