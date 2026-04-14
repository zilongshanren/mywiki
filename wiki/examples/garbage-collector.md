---
tags: [经典案例, 深模块, aposd]
date: 2026-04-05
sources: 1
---

# 垃圾回收器 —— 零接口的深模块

Ousterhout 举的**比 Unix I/O 更极端的 [[deep-modules|深模块]]** 案例：

> "Another example of a deep module is the garbage collector in a language such as Go or Java. This module has no interface at all; it works invisibly behind the scenes to reclaim unused memory. Adding garbage collection to a system actually shrinks its overall interface, since it eliminates the interface for freeing objects."

**垃圾回收器是接口为零的深模块。**

## 反直觉的洞察

GC 的实现极其复杂（标记清除、分代回收、并发 GC、暂停时间优化……），但复杂性对调用者完全不可见。

对比 C/C++ 的手动内存管理：`malloc/free`、`new/delete`、智能指针的 `release`——这些都是接口。调用者需要理解所有权语义、什么时候该释放、谁负责释放、忘了会怎样。

Java 的 GC **消灭了所有这些接口**。你不需要调用任何东西、不需要记任何约定、不需要追踪对象生命周期。

## 深度的一般规律

> 有时候让模块更深的最好方式，是**让它完全没有接口**。

添加 GC 不仅让该模块深度无限，还**缩小了整个系统的接口**——因为它从所有调用者的词汇表里删除了 `free`/`delete`。

## 与虚假抽象的区别

[[false-abstraction|虚假抽象]]隐藏了调用者必须知道的细节——表面简洁，实际危险。GC 隐藏了调用者**真正不需要知道的细节**——在大多数应用场景下，对象何时被回收、用什么算法回收，都与代码正确性无关。

GC 不是在假装「内存管理不存在」，而是真的把它变成了调用者无需关心的事实。

## 局限

GC 的深度有例外场景：对暂停时间敏感的应用（游戏、实时系统）、对内存占用敏感的场景，GC 的内部行为重新变得「需要被知道」。在这些边界情况下，原本的深模块需要暴露调节旋钮（堆大小、GC 模式、代参数），这些旋钮本质上就是把部分实现细节暴露出来。

## 相关

- 体现的原则：[[deep-modules]]、[[information-hiding]]
- 类似经典：[[unix-io]]
- 反面：[[false-abstraction]]
- [[lua-incremental-gc]] —— Lua 5.1 的增量 GC：五阶段状态机 + 双白色乒乓 + FIXEDBIT 保护字符串

## Sources

- [[sources/aposd-day04]]
