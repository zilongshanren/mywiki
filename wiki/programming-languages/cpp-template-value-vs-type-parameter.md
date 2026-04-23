---
tags: [cpp, templates, inlining, compile-time]
date: 2026-04-19
sources: 1
---

# C++ 模板按类型参数化 vs 按值参数化

C++ 模板参数分两种：类型参数（`typename T`）与**非类型**参数（`int X`、函数指针、成员指针等具体值）。对于要把函数作为参数传给泛型算子的场景，这两种写法的语义天差地别。

「传统」按类型参数化的写法，用 functor——把算子做成一个类，类本身就是唯一的类型，于是 `template<class F> T do_op(T a, T b, F op)` 每一次实例化都对应一个具体 functor 类型，编译器可以放心内联 `op(a,b)`。

但如果你把函数指针作为普通参数传进去，比如：

```cpp
template<class OP>
int do_op(int a, int b, OP op) { return op(a, b); }
int add(int a, int b) { return a + b; }
int c = do_op(4, 5, add);
```

看起来好像差不多——但 `OP` 被推导成 `int(*)(int,int)`，这是**所有**同签名函数共享的一个类型。换句话说 `do_op` 只实例化了一次，`op` 在函数体里就是一个运行时的函数指针。要强证据的话：

```cpp
int (*func_ptr)(int,int) = add;
int c = do_op(4, 5, func_ptr);  // 合法
```

把 `add` 替换成变量也能编译，说明编译器没有把具体哪个函数固化到 `do_op` 的实例化里。想要真正内联，必须让那个函数本身作为**值**参与模板实例化——把函数指针当作非类型模板参数：

```cpp
template<int (*OP)(int,int)>
int do_op(int a, int b) { return OP(a, b); }
int c = do_op<add>(4, 5);  // OK，每个 <add>、<sub> 生成独立 do_op
int (*fp)(int,int) = add;
int c = do_op<fp>(4, 5);   // 编译错：fp 不是 constant-expression
```

此时每个实例化里 `OP` 是一个编译期已知的函数符号，`do_op<add>` 展开后就是 `return a + b;` 的形态。

回过头看第一种写法——既然不内联，它还有什么价值？Supnik 给出的答案是**类型强制转换（type coercion）**：`template<class OP>` 版本可以接受签名不同的函数（比如 `float fadd(float, float)`），每次实例化会为不同签名生成一份把参数从 `int` 转到 `float`、再把结果转回来的外壳代码。这在设计上未必优雅，但说明了「按类型」版本真正的适用场景是**签名异质**时的 wrapper 生成，而不是算子内联。

## 相关

- [[cpp-multi-paradigm-discipline]]

## Sources

- [[sources/supnik-templating-functions]]
