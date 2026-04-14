---
tags: [source, 编程语言, lua, 访谈, 中文博客]
date: 2026-04-14
sources: 1
---

# 《编程之魂》第七章 Lua 校译稿（云风 / blog.codingnow.com）

[[cloudwu]] 发表于 2010 年 6 月的博客，公开了他为博文出版的《Masterminds of Programming》中文版（《编程之魂》）所校译的第七章片段——Roberto Ierusalimschy 与 Luiz Henrique de Figueiredo 关于 Lua 设计哲学的访谈。云风对原译本不满意，干脆放弃 3/4 译文亲自重译，并贴出了一大段译稿。

## 摘要

这是一段长访谈的中译，覆盖 Lua 的几乎全部设计要点：脚本语言的原始定义（控制其它语言写的组件）、`table` 作为唯一聚合结构的来由（VDM + AWK）、first-class 函数与闭包、协程式并发（不信任抢占式共享内存的多线程）、垃圾收集而非引用计数、以 ANSI C89 实现并坚持极致可移植性、基于寄存器的 VM 架构动机、从 lex/yacc 切到手写递归下降的理由、"机制而非法策"的语言设计风格、以及"几乎所有特性都成本太高"的特性评估方法。访谈还谈到了优秀程序员的判别（写程序时是否享受其中）、调试的可教与不可教、注释在好代码中的尴尬定位、以及 ANSI C 在 2010 年仍然是他们眼中可移植性最好语言的判断。

## 关键要点

- "脚本语言" = 用来粘合 / 控制其它语言写的组件，不是动态语言的同义词
- table 来源于 VDM 把 set / sequence / map 都收敛到 map
- 协程是非对称、有栈的，可以在嵌套调用中 yield，比 Python 生成器强大
- 不信任抢占式共享内存多线程；多核场景用"每线程一份独立 lua_State"
- 几乎所有新特性"成本都太高"；新特性能不能让作者"惊喜"是关键判据
- "机制而非法策"——不内置 OO，但提供 metatable 让用户长出 OO
- ANSI C89 实现是 Lua 跑遍机器人 / 路由器 / 打印机的根本原因
- Roberto / Luiz 都不爱注释——清晰的代码比加注释的代码可读
- 手写 LL parser 是因为 yacc 主干代码可移植性差且不可重入

## 链接到的概念

- [[lua-design-philosophy]]
- [[lua-cpp-binding]]
- [[closure]]
- [[garbage-collector]]
- [[cloudwu]]

## 原文

- 链接：https://blog.codingnow.com/2010/06/
- 本地：`raw/articles/blog.codingnow.com/2010-06-29_yun-feng-de-blog.md`
