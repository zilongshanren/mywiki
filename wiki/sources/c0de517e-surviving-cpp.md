---
tags: [source, c++, 软件设计, 解耦, 代码评审]
date: 2026-04-19
sources: 1
---

# Surviving C++（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 2011 年 2 月发表的一篇长文，把他对 C++ 的长期吐槽换成正向姿态：**既然不能消灭它就研究怎么活下来**；结论是「唯一真正重要的是解耦」。

## 摘要

文章分三段：(1) 为什么 C++ 是一堆补丁语言、为什么每个工作室都要自己切子集；(2) 项目里唯一真正重要的质量是「可被修改的能力」，换言之就是**模块间的解耦**——其它风格规则顶多影响 WTF/minute，不影响项目寿命；(3) 一组视觉 flashcard：看到 header / `#include` / 返回裸指针 / 非接口继承 / 成员函数 / 全局 `static`，脑子里应该闪过哪些质疑。

Pesce 在 [[sources/c0de517e-survive-cpp-guidelines-experiment|一个月前的 etherpad 实验]]里收集了一堆众包 C++ 规则，看完之后反而失望——因为大多数条款只管表面。本文是对那次实验的**思辨归零**：绕开条款，直接说**真正值得在代码评审里警觉的就是依赖面**。附言进一步推论：**如果你的代码好解耦，未来完全可以换到别的语言；反之再多 C++ 最佳实践也救不了**。

## 关键要点

- **软件项目最重要的单一质量是可修改性**——这一条本身值得单独成页，见 [[cpp-decoupling-over-details]]。
- **没有人用纯标准 C++**——工作室方言 + lint 强制执行。游戏圈的 C++ 是一门事实上的方言语言。
- **没有两三个真实使用点就不要泛化**；没有两三个真实依赖就不要抽象。
- **Header 里的每一个声明都在传播依赖**——PIMPL / 抽象接口 / 前向声明 / 双层 include 目录是减少这种传播的主要手段。
- **静态依赖 vs 动态依赖**——核心库（内存 / 数学）可静态依赖，跨模块最好动态依赖。
- **Pesce 对 OOP 的一贯怀疑**在这里再次出现——非接口继承、成员函数滥用、static 滥用都在 flashcard 清单里。
- **落地练习**：挑一个小模块试着拆进 DLL 或换别的语言重写。拆得动 → 项目健康；拆不动 → 必有耦合问题。

## 链接到的概念

- [[cpp-decoupling-over-details]]
- [[cpp-multi-paradigm-discipline]]
- [[system-decoupling-patterns]]
- [[header-as-user-manual]]
- [[pimpl-vs-pure-virtual]]
- [[angelo-pesce]]

## 原文

- 链接：https://c0de517e.blogspot.com/2011/02/surviving-c.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-02-26_surviving-c.md`
