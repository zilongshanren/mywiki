---
tags: [source, programming, cpp, c-style, 软件设计]
date: 2026-04-27
sources: 1
---

# Doing some homework. C-Style and pain.（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2012 年 9 月的文章，通过一个 DX9 渲染小测试台的编写经历，反思 C-style 与 C++ OOP 的适用边界，并论证「不使用某个语言特性，其实已经解决了 C++ 包裹出来的许多问题」。

## 摘要

Pesce 描述了一次在家写 DX9 渲染测试台的经历。与工作中受制于已有框架不同，这次他可以自由选择代码风格。结果图形 API 层自然地写成了 C-style：不透明的 `gContext` 指针 + 显式初始化/释放 + 函数接受 context 作为第一参数。他发现这种写法「免费」解决了 C++ 中需要设计模式才能解决的一系列问题：singleton 问题（显式 new/delete 语义）、依赖注入（context 必须显式传递，不可「全局取用」）、PIMPL/接口隔离（实现细节天然隐藏在不透明指针后面）、拷贝构造（不存在 class，不存在需要声明 private 的拷贝构造）。

他并非在否定 C++，而是观察到：当功能需要时（复杂对象生命期、虚接口、operator overloading），C++ 特性有其价值；但对于「只有一两个实例的系统级 API」而言，C-style 默认已经满足设计目标，额外的 C++ 包裹只是噪声。核心判断标准是「懒」（laziness）——只在某个特性真正节省了代价时才使用它，而不是因为「高级」「可能未来用得上」。

## 关键要点

- C-style 不透明指针模块默认实现了：singleton 语义、依赖注入、PIMPL 隔离、无拷贝
- 「单例 = 对全局子系统生命期的控制」——显式 new/delete 指针比 Singleton 类更直接
- C++ 特性的正确使用时机：复杂对象生命期（构造/析构）、虚接口、data structure 模板
- 「懒」是最有效的代码复杂度过滤器——预测性抽象基本无效
- 行业系统性地对过度工程化进行了规范化——OO、设计模式、functional、data-oriented 依次成为「正确做法」的话语权，但复杂度本身从未被认真清算
- `std::sort` 是值得用的 STL——不是因为时髦，而是因为它真的好

## 链接到的概念

- [[classitis]]
- [[cpp-multi-paradigm-discipline]]
- [[pimpl-vs-pure-virtual]]
- [[c-opaque-struct-modules]]

## 原文

- 链接：https://c0de517e.blogspot.com/2012/09/doing-some-homework-c-style-and-pain.html
- 本地：`raw/articles/c0de517e.blogspot.com/2012-09-02_doing-some-homework-c-style-and-pain.md`
