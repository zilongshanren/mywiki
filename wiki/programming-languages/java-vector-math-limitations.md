---
tags: [java, c-sharp, 运算符重载, 栈分配, 垃圾回收, 数值计算]
date: 2026-04-14
sources: 1
---

# Java 做向量数学的两个痛点

[[emilio-lopez-ros|Emilio López Ros]] 在 Android 平台手写 `Vector3` 工具类时总结了一个在游戏和图形社区被反复吐槽的事实：**Java 并不适合做矢量/矩阵数学**。不是因为性能必然差（JIT 其实做得不错），而是因为语言层面缺了两个关键特性：**栈分配的值对象**和**运算符重载**。

## 痛点一：没有运算符重载，链式表达式极不可读

C++、C#、Rust 都允许给用户定义类型重载 `+ - * /`，于是可以写出贴近数学符号的表达式：

```csharp
// C#
Vector3 v1 = pOrigin + (pTest2 - pTest1).Normalized() * factor;
```

Java 里只能一路 `.add().subtract().mul()`：

```java
Vector3 v2 = pOrigin.add(pTest2.subtract(pTest1).norm().multiply(factor));
```

对 vector/matrix 这个特定的领域，运算符重载带来的不是炫技，而是**纸面数学能否直接被代码忠实表达**。三两步链式之后，Java 版本就变成了"括号迷宫"，读的人要在心里把 OOP 的方法调用重新翻译回数学。Lopez 认为这是"运算符重载被滥用"之外最经典的一个反例——给出再多 coding style 的理由，也抵不住连续写上百行向量代码时候的认知负担。

## 痛点二：没有栈分配对象，GC 变成 hot loop 杀手

更大的问题是**没有值类型**。Java 所有对象都在堆上分配，`Vector3` 也不例外。向量运算天然大量出现在循环内部——粒子系统、物理 tick、动画骨骼、碰撞检测——每一帧都会在 heap 上制造几百几千个临时 `Vector3`，然后等 GC 一次性回收。这在**桌面 Java** 问题还不严重，到了 2014 年的低端 Android 机上就是灾难：GC 停顿足以打断 60 fps 目标。

唯一的 workaround 是在类里声明一堆 "temp vector" 成员变量，然后把函数改成 **out-parameter 风格**——调用方传入一个预分配的 `tempVector` 让函数把结果写进去：

```java
Vector3 mTempVector = new Vector3();  // 成员变量，一次性分配
// …
tempVector.copy(pOrigin.add(pTest2.subtract(pTest1).norm().multiply(factor)));
interestingMathFunction(param1, param2, tempVector);      // tempVector 是 output
interestingMathFunction2(tempVector, tempVector2, tempVector3); // 哪个 in 哪个 out？
```

这种风格代价很高：**函数签名里看不出哪个参数是输入、哪个是输出**、临时变量共享时容易踩 aliasing、一个类要养好几个 temp 作为 scratch。更糟的是，内层函数之间的返回值再也不能直接串起来——每一步都要先把结果 copy 进一个 temp，再把 temp 交给下一个函数。这和 C++ 里的 RVO、C# 的 `struct` 值语义相比，工程成本完全不是一个量级。

此外，赋值默认是**按引用**——`v = a.add(b)` 得到的是 `a.add(b)` 返回的那个对象的引用，写代码的人常常在不注意的地方和别人共享状态；要真正得到副本必须显式 `new Vector3(...)` 或 `v.copy(...)`。[[garbage-collector|垃圾回收]] 背景下的 aliasing bug 和 GC 压力叠加，就变成了"不可能安全地 hot-loop 向量运算"。

## 为什么 Unity 选了 C\#

文章结尾抛出一个观察：Java 和 C# 语法高度相似，**但 C# 同时提供了运算符重载和 `struct` 值类型**。这两个特性合起来消灭了 Java 在数值计算上的两个根本短板——`Vector3` 可以被声明成 `struct`，在栈上或作为字段内嵌分配，`+` `*` 直接重载——于是游戏引擎的 hot path 既能保持数学可读性，又完全绕开 GC。Lopez 推测这可能是 **Unity 选 C# 而不是 Java** 的多个深层原因之一，即便当时（2005 年前后）Java 在企业市场更主流。

## 相关

- [[garbage-collector]]
- [[closure]] —— 另一个 Java 长期缺席、C# 更早补上的语言特性
- [[cpp-runtime-reflection]] —— C++ 系解决运行时问题的另一种思路

## Sources

- [[sources/elopezr-java-vector-math]]
