---
tags: [source, 编程语言, C++, 反射, 元编程]
date: 2026-04-14
sources: 1
---

# Exile: Reflection（Max Slater）

[[max-slater|Max Slater]] 2018 年 8 月发表（2019 年 7 月更新元程序部分），介绍他在自研引擎 **Exile** 里通过 **libclang 元程序** 实现的 C++ 运行时类型反射系统。目标是在不借助任何现代 C++ 反射库 / macro 样板的前提下，支持自动序列化、自动 ImGui 编辑器等功能。

## 摘要

C++ 缺少运行时 reflection，标准提案遥遥无期；Slater 借鉴了 Jai 的类型内省模型，在 Exile 里自己搭了一套。核心是一张全局（thread-local）的 `type_id → _type_info` 哈希表。`_type_info` 是一个带标签的 union，根据类型种类（void / int / float / ptr / struct / ...）各自保存元数据——struct 情况下存成员名字、成员 type hash、成员 offset 和成员数量。

入口是 `TYPEINFO(T)` 宏：通过 `typeid(T).hash_code()` 得到 key，查表。指针类型用 SFINAE 做**按需懒加载**——第一次请求 `int**` 时递归地创建 `int*` 和 `int` 的节点。RTTI 是关闭的，因为 `typeid` 对编译时已知类型不需要 RTTI 支持。

type table 的填充不靠运行时 macro 一个个注册，而是**构建前跑一个用 libclang 写的元程序**：解析所有 C++ 源、遍历 AST、对每个 struct 定义输出一段 C++ 代码把 `_type_info` 填进表——构建系统把这段代码连同游戏一起编译。展示的 `print_struct<T>`、`ImGui::EditAny(&cam)` 等例子说明基本功能一旦搭好，就能覆盖多数数据驱动场景。

## 关键要点

- **C++ 没有运行时反射**是真正的痛点，不是理论偏好——序列化、编辑器、网络打包都需要。
- **libclang 元程序路线**在 Unreal UHT / Qt moc 传统之内——用工具补齐语言特性，而不是等语言升级。
- **type table 作为单一 source of truth**：运行时所有反射操作都从这个 hash map 出发。
- **SFINAE 做 lazy pointer type 注册**：`int** → int* → int` 的递归插入，让「任何已知基础类型的任意指针层数」都能用。
- **关闭 RTTI 仍然可用 `typeid`**：因为它对静态类型信息不依赖 RTTI。
- **2019 年重写**解决了循环依赖和嵌套模板的类型依赖图问题——原始实现没法正确处理相互引用的 struct。
- **局限**：不反射 OOP 特性（方法、构造、继承）——只覆盖 Slater 引擎里 C 风格 POD 的需求。

## 链接到的概念

- [[cpp-runtime-reflection]]
- [[max-slater]]

## 原文

- 链接：https://thenumb.at/Reflection-in-Exile/
- 仓库：https://github.com/TheNumbat/exile
- 本地：`raw/articles/thenumb.at/2018-08-14_exile-reflection.md`
