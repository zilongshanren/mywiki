---
tags: [source, c, 接口设计, 类型安全, 中文博客]
date: 2026-04-14
sources: 1
---

# C 语言里类型安全的多变体接口（云风 / blog.codingnow.com）

[[cloudwu]] 发表于 2010 年 7 月的短文，谈在 C 语言下如何把多个"参数形态各异"的下游模块粘合到一个统一接口上，又不丢掉编译器的类型检查。

## 摘要

云风先回顾了 C 语言里一些容易被忽略的细节：`void foo();` 是参数未定（弱类型），不是无参；要严格无参数得写 `void foo(void)`；可变参数靠 `...` 和 `va_list`，所以才有 `printf` 之外被迫成对提供的 `vprintf`。C++ 的解法是 functor 或类继承。然后他给出 X-Window 的另一种朴素做法：定义一个 `XEvent` union，把所有可能的事件类型作为不同的 struct 列入这个 union，每个 struct 头部留一个 `type` 字段以便分发。事件循环只接收 `XEvent *`，访问时按 `event.xkey.keycode` 或 `event.xbutton.x` 取字段。比起 Win32 用 `WPARAM` / `LPARAM` 把一切压扁成两个 32 位整数，这种 tagged union 既统一了接口形态，又保留了类型安全。本质上是把"由编译器在调用现场逐个压栈参数"这件事改由程序员主动填一个结构体——靠 struct 兜住每组参数的类型，再靠 union 把多组合并成同一个顶层类型。这种"传 struct 指针而非逐个参数"的做法在 BSD socket `connect(struct sockaddr *)` 等 C API 里也很常见。

## 关键要点

- C 的 `void foo();` 是参数未定，不是 `void`
- `va_list` 是 C 处理可变参数的常规手段，但破坏了类型安全
- XEvent = union of struct，每个 struct 头部带 `type`
- 与 Win32 的 `WPARAM/LPARAM` 形成鲜明对比：tagged union 保留类型信息
- 推广：在粘合层定义 union，让多模块共用一个类型安全的统一接口
- 同源思路在 BSD sockets 的 `sockaddr` 家族里也能看到

## 链接到的概念

- [[c-tagged-union-dispatch]]
- [[c-opaque-struct-modules]]
- [[c-interface-oop]]
- [[interface-vs-implementation]]
- [[cloudwu]]

## 原文

- 链接：https://blog.codingnow.com/2010/07/
- 本地：`raw/articles/blog.codingnow.com/2010-07-28_yun-feng-de-blog.md`
