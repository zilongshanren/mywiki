---
tags: [source, c++, soa, 数据导向设计, 性能, 内存布局]
date: 2026-04-27
sources: 1
---

# Making SoA Tolerable（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 发表于 2021 年 2 月的文章，聚焦如何在现代 C++ 里以可维护的方式实现结构数组（SoA），兼顾缓存友好性与代码可读性。

## 摘要

文章从 Chandler Caruth 的 CppCon 演讲出发：90–95% 的性能来自数据布局和内存访问模式，而非指令选择。编译器能自动优化指令（整数除法换乘法等），但数据布局几乎全靠程序员手写。Supnik 在 X-Plane 移植到 Vulkan 后，发现驱动开销降低 10x，而自家剔除代码的 BVH 树却成了瓶颈——树节点不连续，VTune 显示全是缓存缺失。替换为深度固定为 2 的扁平数组树之后速度飞升。文章核心是一种 C++ SoA 惯用法：用一个结构体同时充当"拥有内存的数组"和"可自增的迭代器"，每个成员字段是指向各自连续数组起点的裸指针；配合一个 `UTL_block_alloc` 辅助类，把多条成员数组一次性分配到单块连续内存中，既保证字段间物理紧邻又保留封装形式。

## 关键要点

- 大 N 之前别用树：N=100 已经够小，直接 `std::vector` 线性扫描更快
- SoA 的 C++ 惯用法：结构体内每个字段存 `float*`，`operator++` 递增所有指针，一个结构体既是数组又是迭代器
- `UTL_block_alloc` 把所有字段的 malloc 合并为一次，保证字段数组物理相邻（避免跨 VM page）
- SIMD 友好度：将 vec3 拆成独立的 x/y/z 数组，四个对象可完美放入一条 SIMD lane；如果始终整体使用 vec3 则保持 XYZXYZ 交错反而更优
- AoSSoA（Arrays of Structures of Structure of Arrays）：外层对应 SIMD 宽度的小分组，是 AVX/AVX2 场景下的第三条路
- C++ 的根本缺陷：没有 generative meta-programming，无法自动将 OOP 结构改写成 SoA

## 链接到的概念

- [[aos-vs-soa]]
- [[simd-memory-bandwidth-bound]]
- [[cache-friendliness]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2021/02/making-soa-tollerable.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2021-02-27_making-soa-tollerable.md`
