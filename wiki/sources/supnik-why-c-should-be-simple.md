---
tags: [source, cpp, software-design, programming-languages, complexity]
date: 2026-04-27
sources: 1
---

# Why Your C++ Should Be Simple（Ben Supnik / The Hacks of Life）

[[people/ben-supnik]] 发表于 2017 年 3 月的文章，以"大脑带宽有限"为核心论点，主张 C++ 代码应刻意写得比你实际能力更简单。

## 摘要

文章引用 Kernighan 的名言作为起点："调试的难度是写代码的两倍，所以如果你写代码时竭尽所能，你怎么调试它？"Supnik 将这一论点延伸到大脑带宽的分配：写复杂 C++ 本身消耗认知资源，挤占了解决业务问题、算法问题、调试和架构设计所需的注意力。文章列举四类 C++ 特性作为"复杂度不值回报"的例子：（1）过度运算符重载；（2）模板元编程（TMP）——智力消耗极高但产出可用 codegen 替代；（3）深层模板嵌套——存在一个拐点，超过后调试代价超过收益；（4）过度抽象的类层次——增加 purity 的代价是给其他代码制造障碍。最后的不对称性结论：代码太简单时升级容易，代码太复杂时降级极其耗时，因此默认应偏向简单。

## 关键要点

- 核心论点：大脑带宽是零和的，"会用高级 C++"不等于"应该用"
- 复杂 C++ 使代码不可调试，调试难度是写作难度的两倍
- 运算符重载、TMP、深层模板、过度类层次均属"复杂度大于回报"的典型
- 不对称性原则：从简单到复杂的升级代价低，从复杂到简单的重构代价高
- 结论：写比你能力更简单的 C++，将省出的认知资源投入真正的价值点

## 链接到的概念

- [[programming-languages/orthodox-cpp]]
- [[software-design/cpp-multi-paradigm-discipline]]
- [[software-design/cognitive-load]]
- [[software-design/complexity]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2017/03/why-your-c-should-be-simple.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2017-03-18_why-your-c-should-be-simple.md`
