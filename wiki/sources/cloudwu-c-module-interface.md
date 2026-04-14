---
tags: [source, 软件设计, 模块化, C]
date: 2026-04-14
sources: 1
---

# 关于 C 语言模块化设计的笔记（云风 / blog.codingnow.com）

[[cloudwu]] 发表于 2010 年 1 月的博客，是他"模块化随想系列"的一篇，谈如何在 C 语言下保持清晰的模块层次和接口约定。

## 摘要

云风主张用不透明结构 `struct A` + 统一前缀 `A_xxx` 的 API 来组织 C 模块，每个模块对应一个 `.c` 文件、围绕一类对象展开。他反对 `typedef` 掉 `struct` 前缀、反对越层调用、反对在 `a.h` 里 `#include "b.h"` 而偏好 `struct B;` 前向声明，以此防止模块层次通过头文件传染。对于 C 没有 `friend` 的痛点，他给出一个朴素的解法：在 `b.h` 暴露一个伪类型 `struct i_A *`，只有 `a.c` 内部能通过 `static inline` 函数把 `struct A *` 转换成它，使 `B_set_A` 这个本该只给 A 用的接口对其他模块**不可用**。他强调：草率暴露接口是日后系统脆弱的根源——分层是原则性的，不是技巧性的。

## 关键要点

- C 模块的接口：前缀命名 + 不透明 `struct` + 头文件仅前向声明。
- 两类 API：`self`-first（成员方法）与全局（静态方法）。
- 下层对上层一无所知；即便被迫持有引用，也只是裸指针。
- 循环引用时的"C friend"：用只能在 `a.c` 里构造的 `struct i_A *` 藏起 `B_set_A`。
- 内存管理 / log / 字符串等基础设施可以被多层直接用，但超过一定层次后仍应再隐藏。

## 链接到的概念

- [[c-opaque-struct-modules]]
- [[modular-design]]
- [[information-hiding]]
- [[interface-vs-implementation]]
- [[dependencies]]
- [[cloudwu]]

## 原文

- 链接：https://blog.codingnow.com/2010/01/
- 本地：`raw/articles/blog.codingnow.com/2010-01-28_yun-feng-de-blog.md`
