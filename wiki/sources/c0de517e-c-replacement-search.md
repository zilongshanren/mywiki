---
tags: [source, 编程语言, 游戏开发, c++, 语言生态]
date: 2026-04-27
sources: 1
---

# Where is my C++ replacement?（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2014 年 6 月的文章，系统探讨为何游戏/渲染领域至今没有出现可行的 C++ 替代语言。

## 摘要

Pesce 以「收益/成本」框架评估 D、Rust、Go 三门语言对游戏/渲染程序员的吸引力。他的核心论点是：**一门新语言要在这个领域成功，必须满足两个条件之一：近乎零成本的迁移（超集/子集化），或者提供数量级的生产力提升**。漂亮的语言特性——更好的类型系统、内存安全、更整洁的模板——远远不够。Web 领域夺走了大多数新语言的注意力，游戏领域的特殊需求（C 互操作、跨平台确定性、低延迟迭代）反而成了孤岛。他最后押注「**可交互编程/热重载**」才是唯一能让人放弃 C++ 的杀手级特性——Lua 的成功恰好证明了这一点：游戏人宁可牺牲运行时性能换取实时交互。

## 关键要点

- D 的问题不是语言本身不好，而是「更好的 C++」这个价值主张不够颠覆性；没有聚焦的细分场景，也没有大公司背书的营销推力
- Rust 的并发/安全目标对游戏渲染来说并不痛——渲染的并发已经用大 parallel_for 解决了，安全靠工具链也够用
- Go 有快迭代的目标，但 C 互操作慢、语言特性对游戏几乎无益
- Lua 之所以成功：零平台风险（纯 C 可移植）+ 可交互（REPL/热重载），语法反而无关紧要
- 工程师常低估非技术阻力：社区、教育、招聘、旧代码库、证明 ROI——每一项都是大山
- LLVM 是最有希望的公共基础：让新语言低成本支持各平台，类比 JVM 之于服务器端

## 链接到的概念

- [[cpp-multi-paradigm-discipline]]
- [[orthodox-cpp]]
- [[lua-design-philosophy]]
- [[gamedev-language-adoption]]

## 原文

- 链接：https://c0de517e.blogspot.com/2014/06/where-is-my-c-replacement.html
- 本地：`raw/articles/c0de517e.blogspot.com/2014-06-14_where-is-my-c-replacement.md`
