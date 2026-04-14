---
tags: [source, 软件设计, C++, 垃圾回收]
date: 2026-04-14
sources: 1
---

# 200 行的 C++ 标记清除 GC（云风 / blog.codingnow.com）

[[cloudwu]] 发表于 2010 年 2 月的博客，春节假期写的一个小玩具：用不到 200 行 C++ 实现一个标记清除 GC 框架，用来给他的引擎 C++ 中间层（和 Qt 结合）补一条对象生命期管理的出路。

## 摘要

动机是：引擎本身是纯 C + Lua，原本依赖 Lua GC 管理 C 对象生命期；当需要把中间层搬到 C++ 时没有原生 GC，而引用计数又解决不了循环引用，所以他写了一个标记清除版本。接口围绕两个纯虚结构：`i_gcobject`（`touch / mark / grab / release / collect`）和 `i_gcholder`（作为 root 的 `hold / unhold`）。默认实现 `gcobject` 用一个 bool 标记位和全局 `gc_pool` 登记所有对象，采用"乒乓开关"避免标记前清零。派生类只要虚继承 `gcobject` 并在 `touch()` 里对子引用 `mark()`——示例用 `std::multiset` 写了个 tree 验证双向引用正确回收。云风刻意不用模板、不追求语法糖，强调接口和实现分离、使用简单、易读易扩展；整个取舍表达了他"生命期应独立管理"的长期主张。

## 关键要点

- 目标是最低可用 GC：没有分代，没有并发，也没有模板魔术。
- 标记位乒乓切换避免 pre-pass 清零。
- root 的 `hold_set / unhold_set` 延迟合并避免每次操作都排序。
- `touch()` 是唯一需要派生类实现的钩子——遍历并 `mark` 所有子引用。
- 析构函数可作为 finalize 使用，但**不要**在析构里主动释放关联的 gc 对象。
- 多级 holder 理论上支持，但在有主循环的程序里没必要。

## 链接到的概念

- [[simple-cpp-mark-sweep-gc]]
- [[garbage-collector]]
- [[information-hiding]]
- [[interface-vs-implementation]]
- [[cloudwu]]

## 原文

- 链接：https://blog.codingnow.com/2010/02/
- 本地：`raw/articles/blog.codingnow.com/2010-02-28_yun-feng-de-blog.md`
