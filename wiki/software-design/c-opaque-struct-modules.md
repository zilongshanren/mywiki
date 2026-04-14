---
tags: [软件设计, 模块化, C, 接口设计]
date: 2026-04-14
sources: 1
---

# C 语言下的不透明结构模块

在没有 `namespace`、`class`、`friend` 等语言机制的 C 里，[[modular-design]] 依然可以做得很干净。云风在 2010 年初的系列笔记里把他在网易引擎里常年实践的写法总结了一套朴素的范式，本页把它整理成可照搬的模板。

## 前缀命名 + 不透明类型

C 没有命名空间，工程上的惯例是给模块 `A` 的所有 API 加统一前缀 `A_xxx`。一个模块对应一个 `.c` 文件，围绕**一种对象**展开。对象有两种常见形态：整数 handle，或不透明指针 `struct A *`。云风偏好后者。

在头文件 `a.h` 中，`struct A` **只声明不定义**，具体字段全部藏在 `a.c`：

```c
/* a.h */
struct A;                             /* forward declaration only */
struct B;                             /* 如果方法需要，也 forward */
struct A* A_create(void);
void      A_release(struct A *self);
void      A_bind   (struct A *self, struct B *b);
void      A_commit (struct A *self);
void      A_update (void);            /* 类似"静态成员" */
int       A_init   (void);
```

这正是 [[information-hiding]] 的 C 语言版本——头文件是**契约**，结构布局是**秘密**。云风还强调一个细节：不要 `typedef` 或宏掉 `struct` 前缀，把它写出来对底层模块是更诚实的表达。

## 接口约定两类

- 第一个参数是 `self` 指针的，相当于 C++ 的 `this`（如 `A_commit`）。
- 不带 `self`、对模块全体做处理的，相当于 C++ 的静态成员函数（如 `A_update`）。

这是一种**范式**而不是在用 C 模拟 C++。对"基于某类数据做一组处理"的场景，这样划分就是自然的。

## 层次与前向声明

如果模块 `A` 的实现里要用到模块 `B`，`a.h` 中**不应该** `#include "b.h"`——只需要 `struct B;` 前向声明一下。这样包含 `a.h` 的调用者不会被迫拿到 `B` 的接口，模块层次就不会被头文件传递出去。

越层调用（`A → B → C` 中 `A` 直接调 `C`）是设计污点，应尽力避免。个别例外（内存管理、日志、字符串基础库）可以作为"基础设施"被任意层直接使用，但超过一定层次之后还是应当再隐藏一次。

## 循环引用与 friend 的 C 版

最棘手的情形：`A` 和 `B` 之间需要相互持有引用。原则上谁在上层，这个 bind 就是谁的方法——由 `A_bind(self, b)` 发起。但为了让 `B` 内部能保存 `A *`，`B` 模块必须暴露一个 `B_set_A` 出来，而这个接口**只应当给 A 用**。

C 里没有 `friend`，云风给出的办法是"藏类型"：

```c
/* b.h */
struct i_A;
void B_set_A(struct B *self, struct i_A *a);

/* a.c 内部 */
static inline struct i_A* toI(struct A *a) { return (struct i_A *)a; }

/* b.c 内部 */
static inline struct A* A(struct i_A *a) { return (struct A *)a; }
```

`struct i_A` 是一个"无处可得的类型"——只有 `a.c` 里的转换函数能造出它。其他模块既拿不到这个指针，也就无法误用 `B_set_A`。本质上是一次受控的 [[interface-vs-implementation]] 约束：接口签名里的类型即访问控制。

## 要点

- 模块接口是一种**设计压力**，草率暴露接口是系统日后脆弱的根源。
- 下层模块应当对上层**一无所知**；即便被迫持有上层引用，也只能是裸指针，绝不在下层调用上层接口。
- 不要用"聪明的"语法糖绕开循环依赖——这是原则性的分层问题，不是技巧问题。

## 相关

- [[modular-design]]
- [[information-hiding]]
- [[interface-vs-implementation]]
- [[dependencies]]
- [[c-interface-oop]]
- [[cloudwu]]

## Sources

- [[sources/cloudwu-c-module-interface]]
