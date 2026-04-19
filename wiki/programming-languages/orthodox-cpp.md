---
tags: [cpp, 编程风格, 简化, 游戏引擎]
date: 2026-04-19
sources: 1
---

# Orthodox C++（C+）

Orthodox C++（亦称 C+）是 [[branimir-karadzic]] 2016 年在一则 gist 里提出的 C++ 子集主张：**只用那些真正改进 C 的 C++ 特性，拒绝所谓"现代 C++"的大多数新玩具**。它是 "Modern C++" 的反面——不是要追上 C++11/14/17/20 的潮流，而是退回到一个更小、更干净、更容易被别人接手的语言核心。

## 背后的判断

Karadžić 自述他们在 1990 年代末也曾是"追新派"的 C++ hipster，鼓吹过 RTTI、异常、流式 IO、模板元编程这些当年的新玩意。但在多年游戏引擎实战之后，他们发现：

- 有些特性一旦启用就再也关不掉（[[cpp-exceptions]] 有全局运行时代价，哪怕你从不 `throw`）；
- 有些特性造成的代码复杂度远超其收益（metaprogramming、复杂模板设计）；
- 有些特性让 C++ 和底层 C 库互操作困难（exceptions 与 C 错误码风格格格不入）；
- 有些特性产生的二进制不便携（modules）。

这与 Bjarne Stroustrup 自己的名言相呼应：*"Within C++, there is a much smaller and cleaner language struggling to get out."*

## 规矩清单

Orthodox C++ 的"不要"清单大致是：

- **不要用异常**——异常是唯一需要复杂运行时支持、且启用后影响所有代码（对象构造、析构、try/catch）的 C++ 特性，还会限制优化器。同时异常规格不在编译期强制，与 C 错误码风格也不兼容。
- **不要用 RTTI**。
- **不要用 `<iostream>` / `<stringstream>`**，用 `printf` 风格 API。
- **不要用 `<cstdio>` / `<cmath>` 这类 C++ 包装头**，直接用 `<stdio.h>` / `<math.h>`。
- **不要用会分配内存的 STL 容器**，除非你完全不在乎内存管理。参考 Alexandrescu 的 `std::allocator` talk 和"AAA 工作室为何普遍 opt out STL"的讨论——这也是 [[rpp-stl-replacement]] 这类替代库存在的理由。
- **不要滥用元编程**来做"学术自慰"，仅在真正降低复杂度时适度使用。
- **不要用 modules**——重写成本、平台可移植性、工具链兼容都在倒退，而好处几乎是零。
- **对标准刚出的新特性保持警惕**。经验法则：`当前年份 ≥ 标准年份 + 5` 才"选择性"开用。例如 `constexpr` 在 C++11 引入，真正变得好用要等到 C++14。
- **C 风格优先**——如果一段代码不需要更多复杂度，就别强塞 C++ 特性。理想情况下任何熟悉 C 的人都能读懂它。

2025 年的 revision 里，Orthodox C++ "委员会"才算"选择性批准" C++20 的使用。

## 为什么这套规矩有价值

- **代码库容易被他人接受**——每个工程组都有自己的 C++ 子集偏好，Orthodox 这个子集小到几乎不会踩到别人的雷。
- **老编译器也能编**——在需要支持多平台、老主机 SDK 时这一点非常实在。
- **构建快、二进制小、行为可预测**——没有隐藏的异常表、没有 RTTI 元数据、没有模板实例化爆炸。

## "同路人"的代码范本

Karadžić 列出的、符合或接近 Orthodox C++ 精神的代码库包括：

- **DOOM 3 BFG** —— id Software 的开源释出，典型的 "C-with-classes" 风格。
- **Qt**——当用 `-no-rtti -no-exceptions` 编译时属于这一类。
- **dear imgui** (ocornut) —— 即时模式 UI 库，[[dear-imgui-docking]] 的根基。
- **Network Next SDK**。
- **任何能被 C++ 编译器直接编译的 C 代码**。

概念上相近的主张还有 Embedded C++、Nominal C++、Defold 引擎的 code style、Alexander Radchenko 的 "Keep It C-mple" 等。

## 与本 wiki 的其他节点

- 与 [[cpp-multi-paradigm-discipline]] 共享同一种"自律减法"的取向——C++ 给你的工具太多，工程师的责任是选择不用哪些。
- 与 [[rpp-stl-replacement]]、AAA 工作室普遍绕过 STL 的做法是互为注脚的。
- 与 [[graphics-programmer-constraints]] 的"约束是生产力"观念一脉相承：限制语言子集，省下的认知负担可以转投问题本身。

## Sources

- [[sources/bkaradzic-orthodox-cpp]]
