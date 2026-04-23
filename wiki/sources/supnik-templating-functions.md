---
tags: [source, cpp, templates, compile-time]
date: 2026-04-19
sources: 1
---

# Templating Functions（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2010 年 1 月的 C++ 模板小品。对比「按类型参数化」与「按值参数化」两种模板写法对函数内联的影响。

## 摘要

C++ 模板参数可按类型（`typename T`）也可按非类型值（`int`、函数指针等）参数化。如果要把算子 `op` 传给泛型函数 `do_op` 并期望完全内联，**必须走非类型版本** `template<int(*OP)(int,int)> int do_op(int a, int b) { return OP(a,b); }`——此时每个实例化（`do_op<add>`、`do_op<sub>`）固化一个编译期已知的函数符号，展开后就是直接运算。反之 `template<class OP> int do_op(int a, int b, OP op)` 只会为「函数指针类型」生成一次实例化，`op` 在函数体里是运行时的函数指针；甚至把普通 `int(*)(int,int)` 变量传进去都合法，内联无从谈起。但按类型版本仍有其用：当你传入**签名不同**的函数（如 `float fadd(float,float)`）时，每次实例化会生成一份带类型强制转换的 wrapper，这是它真正的用武之地。文中代码被 Blogger HTML 转义吃掉了不少尖括号，留言区有读者吐槽——概念本身清晰，示例需配合上下文理解。

## 关键要点

- 按类型参数化：`template<class OP>` → 函数指针类型共享，不能内联具体函数
- 按值参数化：`template<int(*OP)(int,int)>` → 每个实例化固化具体符号，可完全内联
- 验证：把 `add` 换成 `int(*fp)(int,int) = add; do_op<fp>(...)` 编译失败，因为 `fp` 不是 constant-expression
- 按类型版本的真正价值：跨签名的类型强制转换 wrapper
- Lisp 程序员的微笑：这一切在 Lisp 里都是理所当然的

## 链接到的概念

- [[cpp-template-value-vs-type-parameter]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/01/templating-functions.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-01-28_templating-functions.md`
