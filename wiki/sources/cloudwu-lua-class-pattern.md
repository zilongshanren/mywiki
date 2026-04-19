---
tags: [source, lua, oop, 元表, 封装]
date: 2026-04-19
sources: 1
---

# 在 Lua 中定义类型的简单方法（云风 / blog.codingnow.com）

[[cloudwu]] 发表于 2025 年 8 月的一篇设计笔记，整理了他自己常用的几种用 Lua 定义类型（尤其是容器类型）的写法，核心是"用元表就够了、别给 Lua 再套一层 class 系统"。

## 摘要

文章先给出最朴素的做法：一张方法表把 `__index` 指向自身，再写一个 `new_object` 用 `setmetatable` 构造实例。接着给出一个可选的 `class` 模块封装，解决"想通过类名找到所有类型"的场景，额外支持 `class.set { ... }` 与 `class "set"` 两种语法。重头戏是容器类型的四种实现：元数据放在 `self.container` 旁、元数据以 `_n` 前缀混入 `self`、元数据外置到 ephemeron 弱表、以及最新发现的小技巧——**用 `[false]` 作为元数据 key**。这四种写法的取舍点在于"集合是否表现得像一个纯 table"、"迭代时是否需要剔除元数据"、"是否愿意为此引入弱表或下划线约定"。最后演示如何给容器类一层 `__pairs` 过滤掉 `false`，并支持覆盖默认构造函数，使得外部使用者看到的就是一个普通 table，但拿到了 `#obj` 和干净 `pairs` 的好处。

## 关键要点

- Lua 里"定义类型"本质就是元表 + `__index`，不必模仿其他语言的 class
- `class` 模块的封装边界要克制——只管注册与默认构造，不做继承/类型检查
- 容器元数据隐藏度有一个连续谱，从直接暴露 `self.container` 到 ephemeron 弱表
- `[false]` 作为 key 是新技巧：天然不冲突、不引入弱表、不引入命名约定
- 可以再配 `__pairs` 过滤 `false`，让容器对外完全像 table 一样工作
- 写法选择看"调用方用得舒不舒服"而非"哪种更 OO"

## 链接到的概念

- [[lua-class-pattern]]
- [[lua-design-philosophy]]
- [[information-hiding]]
- [[interface-vs-implementation]]
- [[cloudwu]]

## 原文

- 链接：https://blog.codingnow.com/2025/08/
- 本地：`raw/articles/blog.codingnow.com/2025-08-26_yun-feng-de-blog.md`
