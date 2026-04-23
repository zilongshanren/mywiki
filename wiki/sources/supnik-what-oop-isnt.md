---
tags: [source, oop, 软件设计, 教学, 封装, 继承]
date: 2026-04-19
sources: 1
---

# What OOP Isn't（Ben Supnik / The Hacks of Life）

[[ben-supnik|Ben Supnik]] 发表于 2010 年 12 月的 OOP 反思——起点是作者在康奈尔大学 CS100 的教学经历（用 C++ 教数据结构，让大一学生同时学会递归和链表，结果「性能像 LISP、优雅像 C++」）。

## 摘要

Supnik 给新程序员的粗暴启发：OOP 三要素（封装、多态、继承）的相对重要性大约是 **90 / 10 / 0**。封装值 90 分——它是唯一能在大型项目里阻止代码互相污染的机制，本科生几乎没机会写到这个规模所以很难体会；多态值 10 分——它在 GUI、工具链之类同构接口领域有用，但 X-Plane 本身几乎没有多态层次；继承值 0 分——至少在纯代码复用意义上；他自己更早写过 *Inheritance of Implementation is Evil*。他把 (OOP − hype) 最终定义成「语言层面为封装和偶尔的多态接口提供的语法糖」，并直言：OOP 不会让坏程序员变好、不会让代码少 bug，但它确实能帮好程序员少按几次 Ctrl-V。评论区有三条有价值的展开：David 为实现继承辩护（抽象数据库基类）；LogicalError 讲他从「信 OOP → 最小 OOP → 数据导向 + 写当下够用的代码」的演化；Paul Homer 提供「顶层 OOP、底层合并」的经验判断。Supnik 在回帖里进一步把继承细化成：接口继承 OK、实现继承难管、实现继承不必然带来复用——决策标准应该是「你对未来重构的预期」。

## 关键要点

- **90/10/0 原则**：封装、多态、继承的相对重要性（承认是夸张但方向对）。
- 本科教学里 OOP 难教的根源：学生从未写过大到封装开始救命的代码。
- 「多态性」是**问题域属性**：不是所有产品都需要多态层次。
- 继承的三条细分：接口继承可用、实现继承难管、实现继承不必然提升复用。
- **不要为还未写的代码做预设计**——专家身份来自写过，不是读过。
- (OOP − hype) = 语法糖，能减少样板但不改变方法论本质。

## 链接到的概念

- [[encapsulation-over-polymorphism]]
- [[classitis]]
- [[cpp-multi-paradigm-discipline]]
- [[strategic-programming]]
- [[tactical-programming]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/12/what-oop-isnt.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-12-09_what-oop-isnt.md`
