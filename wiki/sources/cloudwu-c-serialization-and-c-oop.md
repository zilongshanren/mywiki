---
tags: [source, 软件设计, C, 序列化, 面向对象]
date: 2026-04-14
sources: 1
---

# 序列化、C OOP 与 protected（云风 / blog.codingnow.com）

[[cloudwu]] 发表于 2010 年 3 月的博客，合并了几篇笔记：一个纯 C 的自描述结构序列化库、一次对 C++ `protected` 的小抱怨、以及他偏爱的用 C 写面向对象的范式；另有一些杂谈（被坏 OA 系统清空面试记录的吐槽、招聘的收尾）本摘要不涉及。

## 摘要

**序列化部分**：云风不喜欢 Boost.serialization 那种靠 template 堆起来的"非侵入"方案，也觉得 C/C++ 缺乏类型元信息从根本上没法直接抄 Java/.NET 的做法。他的思路是**自己定义一个小型结构描述语言**，写个工具生成 meta 头文件，运行期拿这些 meta 驱动一个约 500 行的 C 库做序列化。字段只分两种：值类型（按字节拷贝）和引用（内存为指针、输出为 base-1 偏移量），引用再分为外引用（翻译成 atom）和内引用（递归序列化）。硬性需求是**合并值相同的节点**和**正确处理有向有环图**，因此 protobuf 不可用。算法从朴素 O(N!) 迭代合并改进为**单次遍历**：出边全处理完就把节点 finalize 成 atom 查重；遇到环时当前节点直接变 atom 不再合并（牺牲一些合并机会换线性复杂度）。实现要点是用 arena 堆管理临时对象，用 `longjmp` 处理深层的 buffer 溢出错误。

**C OOP 部分**：云风反对用宏模拟 C++ 对象模型，认为 C++ 继承是过紧耦合。他偏爱的 C OOP 范式：定义一个接口虚表 `i_foo`（函数指针集合）+ 一个 `foo_object` 持有 `iface + data`，派生类通过组合（而非继承）扩展自己的 `data`，用一个包装函数把自己包成 `foo_object`。关键哲学：**生命期管理与对象模型分离**——`foo_object` 不负责释放 `data`。他也顺带讲了 C 函数指针的坑（`void (*)()` 接受任意参数列表）和 C99 指定初始化器对写虚表的好处。

**protected 部分**：小篇幅提到 `foo::a` 对 foobar 是 protected 时，foobar 的成员函数能访问 this 的 a 却不能通过 foo 指针访问另一个 foo 实例的 a——引用《C++ 语言的设计和演化》里 Stroustrup 关于 Interviews 库后来禁用 protected 数据成员的故事，顺嘴感慨 C++ 很难做出稳定设计。

## 关键要点

- C 序列化：自定义结构描述语言 + 离线工具生成 meta。
- 值 / 外引用 / 内引用三分类，引用用 base-1 偏移。
- 合并等值节点 + 处理环：单次遍历 + finalize-to-atom 策略。
- arena 堆管理临时对象；`longjmp` 处理深层错误。
- C OOP：接口虚表 + 组合 `data` 指针，生命期独立管理。
- 反对用 C 宏模拟 C++ 对象模型；C++ 继承是过紧耦合。
- 用 C99 指定初始化器写虚表更稳。
- Mark Linton 后来在 Interviews 里禁用了 protected 数据成员——Stroustrup 亲笔记录。

## 链接到的概念

- [[c-serialization-metadata]]
- [[c-interface-oop]]
- [[c-opaque-struct-modules]]
- [[interface-vs-implementation]]
- [[information-hiding]]
- [[linear-allocator]]
- [[cloudwu]]

## 原文

- 链接：https://blog.codingnow.com/2010/03/
- 本地：`raw/articles/blog.codingnow.com/2010-03-31_yun-feng-de-blog.md`
