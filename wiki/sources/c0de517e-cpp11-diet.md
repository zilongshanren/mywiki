---
tags: [source, 编程语言, cpp, cpp11, 游戏引擎]
date: 2026-04-27
sources: 1
---

# Integrating C++11 in Your Diet（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2013 年 5 月的实践文章，以「饮食管理」为比喻，梳理了在游戏引擎日常开发中哪些 C++11 特性值得立即采用、哪些暂时不成熟、哪些应该避开，末尾附有对整个 C++11 标准的批判性评价。

## 摘要

文章的核心判断是：C++11 并未解决 C++ 的根本问题（语言规则太复杂、默认行为危险、模板系统先天残缺），主要是在追赶其他语言的功能列表，且很多功能做得不彻底（例如 rvalue references 的复杂度高于收益）。但其中有几个特性确实值得立即使用，原因是它们改善了可读性或消除了隐式陷阱，而不是增加了新的复杂度。整体建议与 [[orthodox-cpp]] 精神一致：挑有用的用，拒绝「聪明」用法。

## 关键要点

**立即采用：**
- `auto`：消除隐式类型转换，减少冗余类型声明，对 STL 迭代器和 lambda 配合尤为有用
- Lambda：比函数指针好用，显式捕获语法强迫程序员思考生命周期；无捕获版本可隐式转为函数指针
- Type traits + `static_assert`：可以把原来靠注释或约定的类型约束变成编译期断言
- Range-based for：小改进，减少样板代码
- `override`/`final`：虚函数重写的编译期验证

**谨慎使用：**
- Rvalue references：在不依赖大量 STL 或复杂对象的游戏引擎代码里收益有限，规则复杂度高
- Variadic templates：只适合「库」级代码（如 `std::tuple`），不适合业务代码
- Initializer lists：给构造函数重载决议增加新规则，应限制在容器初始化场景
- Typed enums：虽好但增加记忆负担，作者尚未决定

**避开：**
- 不要用 `noexcept`——本来就不该用异常
- Extern templates——是模板滥用的打补丁，治标不治本

**标准库新增（现实：替代品更好）：**
- 新智能指针、并发原语、容器等总体有用，但落后于游戏引擎的实际需求（无 `fixed_vector`、无真正的 job system、无 SIMD 支持），AAA 工作室通常仍用内部实现

## 链接到的概念

- [[cpp11-diet-features]]
- [[orthodox-cpp]]

## 原文

- 链接：https://c0de517e.blogspot.com/2013/05/integrating-c11-in-your-diet.html
- 本地：`raw/articles/c0de517e.blogspot.com/2013-05-13_integrating-c-11-in-your-diet.md`
