---
tags: [source, cpp, header-organization, compile-time, bitsquid]
date: 2026-04-19
sources: 1
---

# A new way of organizing header files（Niklas Frykholm / Bitsquid）

[[niklas-frykholm]] 2012 年 9 月的博客，提出一种和标准 C++ "一类一对 `.h/.cpp`" 完全不同的 header 组织方式：**把所有 struct / class 的数据定义集中到一个 `types.h`，再把函数按功能而不是类型分到不同 `.h/.cpp` 文件里**。这套想法后来直接落到 [[bitsquid-foundation-library]]，也是 Bitsquid 工程风格从 OOP 偏向 C-with-namespaces 的根源。

## 摘要

Frykholm 的不满有两点。工程上：C++ 的"每类一对 header"必然长出臃肿的 include 图，只要一个底层类型（`array.h` / `vector3.h`）被中层 header 引用，就会传染给所有上游的 TU，编译时间持续恶化，回头砍 include 是痛苦又收益稀薄的活。设计上：OOP 把"数据和操作数据的函数"绑在一个 class 里，导致 class 被序列化、字节序、脚本绑定、网络同步等副业务污染，且成员函数天然比外部函数更"一等"，生态很难真正对等扩展。

他的提案是：**`types.h` 只放 struct 裸数据和引用型类的前向声明**，任何需要按值使用类型的 header 只 include `types.h` 一个文件，从根上切断 include 传染；函数签名和 inline 实现放到按功能组织的 `vector3.h` / `array.h` / `serialization.h` / `path.h` 里，只被真正用到的 `.cpp` include。class 语义主要靠命名约定护栏——以 `class` 声明且成员加下划线的视为内部，以 `struct` 声明且成员无前缀的视为"可以直接摸"，纯虚接口类通过 factory 函数构造。他承认的代价是：`types.h` 改动会触发大范围重编译，但他判断基础类型改动本来就稀少、而现代的 SSD + 多线程编译让 rebuild 成本可控。

## 关键要点

- 问题分两层：**编译时间**（include 图传染）与**设计哲学**（OOP 方法绑定导致 class 膨胀）
- 做法：**数据集中到 `types.h`**，函数按功能而非类型组织，外部函数与成员函数地位对等
- "零状态即合法空状态"是一条隐含约束——这样构造函数退化成 `memset` 就能用
- 护栏靠命名约定：`class + _member` = 内部；`struct + member` = 公开裸数据
- 承认的代价：`types.h` 改动带来大规模重编译；作者认为现代构建环境下可接受
- 评论区有重要反驳：**违反 DRY（函数原型要声明两次）**、替代方案是传统 `.h/.inl/.cpp` 三段分离

## 链接到的概念

- [[types-h-data-code-separation]]
- [[header-hero-compile-analysis]]
- [[c-opaque-struct-modules]]
- [[orthodox-cpp]]

## 原文

- 链接：https://bitsquid.blogspot.com/2012/09/a-new-way-of-organizing-header-files.html
- 本地：`raw/articles/bitsquid.blogspot.com/2012-09-03_a-new-way-of-organizing-header-files.md`
