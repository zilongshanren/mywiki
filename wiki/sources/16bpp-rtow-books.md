---
tags: [source, ray-tracing, cpp, performance, optimization]
date: 2026-04-27
sources: 1
---

# Books 1 & 2: Ray Tracing in One Weekend, and The Next Week（16BPP.net）

[[people/16bpp]] 发表于 2021 年 2 月的文章，记录了重写 Peter Shirley *Ray Tracing in One Weekend* 系列的完整过程，以及在 [[psraytracing]] 项目各版本中积累的 C++ 性能优化经验。

## 摘要

作者带着「用 C++17 重写并在性能上超过原书代码」的目标重做了这套书。文章按六个版本（r1–r6）逐步记录了主要优化手段和踩坑：r1 是主体工作，核心方法是把分支结构合并以便编译器自动向量化（`XYRect::hit()` 和 `AABB::hit()` 的去分支改写），以及使用 Compiler Explorer 验证汇编输出。r2 将 Box 对象从「6 个矩形组成的 HittableList」改成单一 SIMD 友好的 `hit()` 函数，渲染耗时减少约 40%。r3 实验了「每线程深拷贝场景图」（4 线程下快 20–30%，原因是消除共享指针的引用计数竞争），以及「BVH 树展开为线性数组」（只快 1–2%，未推广）。r4 将 `HitRecord` 的材质指针从 `shared_ptr` 改为裸指针，净得 10–30% 提升。r5–r6 处理 Book 3 的 PDF 采样重构，用 `std::variant` 把 PDF 对象移到栈上，消除 `shared_ptr` 的动态分配开销。全文反复强调：RNG 种子改变会改变场景布局从而影响渲染时间，因此性能测试必须用相同种子；三角函数近似（`asin`/`atan2`）可以在视觉无差的前提下带来实测可感的加速。

## 关键要点

- **减少分支并聚拢同类运算**：给编译器更好的自动向量化提示，`AABB::hit()` 去分支后效果显著
- **shared_ptr 在热路径上是性能杀手**：材质指针改裸指针一行代码换来 10–30% 提升
- **每线程深拷贝**：消除多线程共享场景图的引用计数开销，4 线程下 20–30% 加速
- **RNG 控制场景布局**：必须固定 RNG 种子后再对比渲染时间，否则对比无效
- **BVH 线性化收益有限**（1–2%），代码复杂度不值当——这是反面案例
- **`std::variant` 替代虚函数多态**：把 PDF 对象从堆移到栈，在 Book 3 场景中有实测收益

## 链接到的概念

- [[psraytracing]]
- [[asin-cg-approximation]]

## 原文

- 链接：https://16bpp.net/blog/post/psraytracing-a-revisit-of-the-peter-shirley-minibooks-4-years-later/
- 本地：`raw/articles/16bpp.net/2021-02-22_books-1-2-ray-tracing-in-one-weekend-and-the-next-week.md`
