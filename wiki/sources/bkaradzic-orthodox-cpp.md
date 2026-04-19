---
tags: [source, cpp, 编程风格]
date: 2026-04-19
sources: 1
---

# Orthodox C++（Branimir Karadžić）

[[branimir-karadzic]] 2016 年 1 月发布的 gist / 博客短文，提出 [[orthodox-cpp]]（又称 C+）——一个反 "Modern C++" 的 C++ 子集主张：只用那些真正改进 C 的特性，拒绝 RTTI、异常、iostream、metaprogramming、modules 等大多数现代玩具。

## 摘要

Karadžić 自述从 1990 年代的"追新派"变为"减法派"的路径，给出一份具体的"不要"清单：禁用异常（运行时代价 + 限制优化器 + 与 C 错误码风格不兼容）、禁用 RTTI、不用 `<cstdio>` 改用 `<stdio.h>`、不用 iostream 改用 printf、不用会分配内存的 STL 容器、慎用 metaprogramming、慎用 modules、对刚出的标准特性保持警惕（经验法则：`当前年份 ≥ 标准年 + 5` 才"选择性"使用）。他举出 DOOM 3 BFG、dear imgui、Qt（no-rtti/no-exceptions）、Network Next 为符合此风格的代码范本。2025 年的更新里才"选择性批准" C++20。这篇短文已成为游戏引擎圈关于 C++ 使用风格最被频繁引用的论述之一。

## 关键要点

- Orthodox C++ 的核心不是"回到 C"，而是"**小而干净的 C++ 子集**"。
- 它解决的真问题是代码库**能被别人接受**——每个工程组都有自己的 C++ 偏好，Orthodox 子集小到几乎不与别人冲突。
- 清单里最硬的两条是 **no exceptions** 和 **no RTTI**——前者因为有全局不可关掉的代价，后者因为大多数游戏引擎有自己的反射方案（对比 [[cpp-runtime-reflection]]）。
- "**Simple always wins**" 的味道与 [[orthodox-cpp]] 对依赖的筛选守则（见 [[middleware-vs-open-source]]）是同一种工程审美。
- 对 C++ modules 的明确 "don't"：重写成本 + 平台可移植性差 + 工具链割裂 = 收益几乎为零。

## 链接到的概念

- [[orthodox-cpp]]
- [[cpp-multi-paradigm-discipline]]
- [[rpp-stl-replacement]]

## 原文

- 链接：https://bkaradzic.github.io/posts/orthodoxc++/
- 本地：`raw/articles/bkaradzic.github.io/2016-01-16_orthodox-c.md`
