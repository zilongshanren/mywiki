---
tags: [source, c++, 未定义行为, 编译器, clang, cgal]
date: 2026-04-19
sources: 1
---

# The Dangers of Super Smart Compilers（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2015 年 12 月的生产事故报告：X-Plane 的 RenderFarm 换用 Clang 优化构建时段错误，根因是 Clang 把 CGAL `CC_iterator` 的 `operator==(handle, nullptr_t)` 里那行 `&*rhs == NULL` 整体优化成 `return false`——因为从标准角度看，`*rhs` 在 `rhs` 为 null 时是在构造一个「空引用」，而空引用属于 UB，编译器可以任意处理。

## 摘要

`handle == NULL` 这种 C++ 惯用法用的是「`operator*` 取引用，再 `&` 取回裸指针」的旧 idiom。Clang 的静态推理：要让 `&*rhs` 等于 NULL，意味着 `*rhs` 构造了一个合法的「空引用」——标准里**没有**这个东西，所以程序必然已进 UB；在 UB 分支上编译器选最简化的行为，即永远 return false。结果是 `if(pts->buddy == NULL) { ... }` 整块被删。GCC 不做这个推理，所以 GCC 优化构建没事；Clang `-O0` 不应用这个 pass，debug 构建也没事。短期修复：改成双 handle 的 `operator==`，Clang 编译期看不出是 null，被迫保守生成一次真实比较。长期修复：CGAL 新版本用 `operator->()` 取裸指针绕开引用语义。真正的教训：**`&*ptr` 在 null 场景下是 UB，`std::addressof` 也救不了，因为 `*ptr` 那一步已经 UB 完了**。

## 关键要点

- Clang 对「不可能是真的」的 UB 分支做激进化简：整条 true 分支变成 `return false`
- 经典 `&* ` idiom 在 post-classical 编译器下随时可能爆炸
- debug / GCC / Clang 三路表现不一致是 UB 的典型信号
- `std::addressof` 换不了——UB 发生在 `*ptr` 那一步
- 评论区援引 Raymond Chen 的 post-classical compiler 说法、LLVM 官方 UB 博文、Regehr 关于 GCC 的同类案例

## 链接到的概念

- [[clang-null-reference-ub-optimization]]
- [[undefined-behavior-c-cpp]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2015/12/the-dangers-of-super-smart-compilers.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2015-12-19_the-dangers-of-super-smart-compilers.md`
