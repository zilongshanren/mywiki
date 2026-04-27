---
tags: [软件设计, C++, 接口设计, 样板代码, bitsquid]
date: 2026-04-19
sources: 1
---

# PIMPL vs 纯虚接口：三种隔离实现的方式

在 C++ 里把**公共接口**和**私有实现**分开，通常出于三个动机：头文件整洁、减少编译依赖、便于日后重写实现不破坏调用方。Niklas Frykholm 在 2012 年的这篇博客把三条可行路径摆到同一张桌子上对比，结论直白——**他更偏好在头文件里写纯虚抽象类**，因为样板最少、灵活度最高。

## 三条路径

**C 风格的不透明指针**。头文件里只 `struct SoundWorld;` 前向声明，字段全在 `.cpp`。配一组 `make_sound_world / destroy_sound_world / play / stop` 的自由函数。这正是 [[c-opaque-struct-modules]] 的做法——简洁、无虚函数开销、无转发代码，Niklas 自己评价「每年越来越欣赏 C，越来越被 C++ 打击」。

**PIMPL（pointer-to-implementation）**。公共类里藏一个 `_impl` 指针，每个公共方法都手写一段转发 stub 到 `_impl->method(...)`。优点是可 `new` 可栈分配可继承，缺点是**每一个方法都要写两遍**——头文件声明一遍、`.cpp` 里写转发一遍——并且多一次 `_impl` 解引用。

**纯虚抽象基类 + 工厂**。头文件里把 `SoundWorld` 写成全 `virtual` 的抽象类，加两个静态工厂 `make(Allocator&)` / `destroy(Allocator&, SoundWorld*)`；`.cpp` 里派生一个 `SoundWorldImplementation` 实现所有虚方法。没有转发 stub、没有头/cpp 同步的义务——`.cpp` 里新增私有 helper 直接写就行，不用先去头文件补一行声明。

## 为什么 Niklas 偏向第三条

PIMPL 的"能 new、能栈分配、能继承"这几个所谓优势，在 Bitsquid 这种**只对大型系统对象（World、Manager）做接口隔离**的场景里全都用不上：分配走自定义 [[custom-allocator-interface|Allocator]]，对象都在堆上，也刻意不用实现继承——[[interface-vs-implementation]] 的原则是**接口继承可以、实现继承几乎总是设计事故**。

虚函数开销同样不是问题。Niklas 的做法是在接口设计上贯彻 Mike Acton 的 *Where there's one, there's more than one*——API 从来不是 `set_sound_position(id, pos)`，而是 `set_sound_positions(count, ids[], positions[])`。单次虚调用分摊到一批数据上，既省了虚函数成本，也给批量优化、DMA、并行留出空间。

更核心的是 Niklas 的一条价值观：**每一行代码都是债务**——写、读、debug、优化、重构的时候都要反复付代价。样板多 150 行不是"只是多打点字"，是让"加一个 helper 方法"的心理门槛变高，进而让代码结构变差。这是 Sapir–Whorf 效应在编程语言里的体现：语法鼓励什么，人就会多做什么。

## 适用范围的小字

这套对比只适用于**大型 heap 对象**：世界、管理器、子系统。小的值类型、POD、算术类型不该走任何一种隔离——直接把结构暴露出去、让编译器 inline 就是。所以真正的选择不是"三选一"而是"先判断这个类型是否值得隔离，再选怎么隔离"。

## 相关

- [[c-opaque-struct-modules]] — 纯 C 下的等价做法，这里被 Niklas 单独提名推崇
- [[interface-vs-implementation]] — APoSD 同主题的抽象视角
- [[c-interface-oop]] — C 函数表加 self 指针的 OOP 模拟
- [[information-hiding]]
- [[api-fast-path-design]] — 批量化 API 是降低虚调用开销的前置设计
- [[custom-allocator-interface]] — 工厂函数上的 Allocator 参数
- [[niklas-frykholm]]

## Sources

- [[sources/bitsquid-pimpl-vs-pure-virtual]]
- [[sources/c0de517e-cpp-style-pain]] —— Pesce 2012：C-style 不透明指针在实战中天然实现 PIMPL 隔离
