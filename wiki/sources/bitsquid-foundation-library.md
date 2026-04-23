---
tags: [source, cpp, foundation-library, allocator, collections, bitsquid, open-source]
date: 2026-04-19
sources: 1
---

# Bitsquid Foundation Library（Niklas Frykholm / Bitsquid）

[[niklas-frykholm]] 2012 年 11 月的发布公告。Bitsquid 把内部的 foundation 层——内存管理 + 集合类——以 MIT 协议在 Bitbucket 开源，作为其他独立项目的起点。文章本身偏"导览"而非"深入"，但这是 Bitsquid 把 [[types-h-data-code-separation]] 和自定义 allocator 两条主张**工程化落地并公开示范**的节点，具备史料价值。

## 摘要

foundation 库的设计有三条 distinct 主张。**数据与代码分离**：`_types.h` 家族里只有开放结构体（`Array<T>` 就只有 allocator 指针、size、capacity、data 四个成员与 C++ 强制的运算符），所有操作函数放到 `array.h` 的 `array` namespace 里，外部代码可以直接写 `array_extensions.h` 给相同 `Array<T>` 加 `shift` / `binary_search`，与官方函数地位对等——`string_stream` 干脆直接操作 `Array<char>`，`hash` 与 `multi_hash` 共用同一个 `Hash<T>` 底层。**Allocator 作为一等参数**：抽象基类 `Allocator` 通过虚函数暴露 `allocate/deallocate/allocated_size`，所有容器构造时显式收一个 `Allocator &`，这与 [[custom-allocator-interface]] 的主张完全一致。**临时内存双层**：`ScratchAllocator` 是一圈环形缓冲，一对 allocate/free 指针仅做指针算术；溢出时回落到 `MallocAllocator` 保不崩。`TempAllocator<BYTES>` 是 scoped、在栈上预留 `BYTES` 字节，先吃栈、栈满再走 scratch、scratch 再满才走 malloc——三级级联让函数局部的小数组几乎零成本。

集合类刻意"反 STL"：不调 ctor/dtor、`memmove` 搬数据，默认存 POD；`Hash<T>` 固定用 `uint64_t` key，key 不够大自己先 hash。是明显的**游戏引擎基础设施偏好**：少、快、可预测、可扩展高于"正交抽象"。

## 关键要点

- **公开发布**：MIT 协议，Bitbucket 上作为其他开源项目起点
- **数据/代码分离**落地：`_types.h` 只放结构，函数进 namespace；第三方扩展与官方对等
- **Allocator as constructor arg**：所有容器显式收 Allocator，和 STL "allocator 是模板鉴别标签"形成对照
- **三级临时内存**：`TempAllocator` 栈 → `ScratchAllocator` 环 → `MallocAllocator` 兜底
- **ScratchAllocator 陷阱**：长寿命分配混入会卡住 free 指针，需要肉眼防守
- **反 STL 集合**：POD-only，`memmove` 搬数据，`Hash` 固定 `uint64_t` key——简单 > 正交
- 尚未实现：线程安全、`PageAllocator`、数学模块——文章以 "what would you want next" 结尾

## 链接到的概念

- [[types-h-data-code-separation]]
- [[custom-allocator-interface]]
- [[bitsquid-foundation-library-concept]]
- [[aos-vs-soa]]

## 原文

- 链接：https://bitsquid.blogspot.com/2012/11/bitsquid-foundation-library.html
- 本地：`raw/articles/bitsquid.blogspot.com/2012-11-01_bitsquid-foundation-library.md`
