---
tags: [source, c++, 闭包, 模板, 语言设计]
date: 2026-04-19
sources: 1
---

# Confessions of a Lisp Hater（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2012-02-27 的一则短文——写完一段 `CollectionVisitor<Pmwx, Face_handle, UnlinkedFace_p>` 模板实例化和对应的 `UnlinkedFace_p` predicate 样板 struct 之后，他罕见地"羡慕 Python/Lisp"了一次：**C++ 没有真正的闭包，function object 的 boilerplate 主宰了代码密度**。

## 摘要

Supnik 拆了自己的一段 X-Plane scenery tools 代码：为了给一个泛型 visitor 传谓词，必须手写一个 struct——存引用、ctor 捕获、`operator()` 返回一行判断，总共四五行样板换"一行真正有用的 C++"。而且受限于 C++03，这个 struct 不能就近放在使用处的函数里（GCC 当时对 local struct 做 template 参数不满意）。他把同等逻辑的 Python 版本写下来：没类型声明、闭包捕获自动、整条链能写成一串嵌套调用。随后他抛了一段经典类比：**"Coding in C is like going out to dinner with someone who's really cheap and insists on discussing the price of everything on the menu"**——每次指针解引、虚调用、条件分支都要算周期；而 Python 像是"用朋友信用卡购物"——迭代嵌套、中间 list 插入，"感觉对就干"。

评论区里读者指出两条解药：Boost.Lambda（Supnik 反对——"治病比病还重"）和 C++11 lambda + `std::function` + `auto`。后者正好赶上他写这篇的时间点，几年内就消除了他这次抱怨的主要来源。

## 关键要点

- **C++ 谓词 boilerplate 是模板泛型的隐税**——visitor / algorithm 越泛，函数对象就越多、越啰嗦。
- **C++03 里 local struct 不能当 template 参数**——样板被迫挪出 function 体，上下文割裂。
- **"知道每样菜价钱" vs "刷别人的信用卡"** 是 Supnik 式的 C++ vs Python 工程心态对比——C++ 程序员习惯内化运行期代价。
- **C++11 lambda 是历史性救赎**——评论者几乎一致认为 `auto` + lambda + `std::function` 改变了样板局面；这条线在 Supnik 后续博客（coroutine、sequences）里反复复用。
- 本文没给新技术，只是语言设计上的一次"诚实一刻"。

## 链接到的概念

- [[closure]]
- [[higher-order-functions]]
- [[cpp-template-value-vs-type-parameter]]
- [[stl-not-abstraction-prescription]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2012/02/i-hate-to-admit-this-but-sometimes-i.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2012-02-27_confessions-of-a-lisp-hater.md`
