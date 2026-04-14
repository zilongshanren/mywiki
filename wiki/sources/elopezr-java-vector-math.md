---
tags: [source, java, c-sharp, 运算符重载, 值类型, 垃圾回收]
date: 2026-04-14
sources: 1
---

# Java and Vector Math（Emilio López Ros）

[[emilio-lopez-ros|Emilio López Ros]] 2014 年的一篇语言对比短文，记录他在 Android 平台写 `Vector3` 工具类时被 Java 两个结构性缺陷反复折磨的过程：**没有运算符重载**和**没有栈分配（值类型）对象**。结尾顺带推测了 Unity 选择 C# 而非 Java 的语言动机。

## 摘要

作者从"向量数学该长什么样"出发，给出几个对比。对数学上写作 `v1 = pOrigin + (pTest2 − pTest1).norm() * factor` 的一行表达式，Java 必须写成 `pOrigin.add(pTest2.subtract(pTest1).norm().multiply(factor))` 这种括号迷宫。更糟糕的是 Java 里 `Vector3` 必然是堆对象，赋值默认传引用（容易 aliasing bug），返回值需要显式 `new Vector3(...)` 拷贝；在粒子、物理、动画循环里频繁 new 就意味着频繁 GC 停顿。workaround 只有一条：在类里养一堆 `tempVector` 成员变量，把函数签名改成"传入一个 out 参数让我写进去"的 C 风格——读代码的人根本分不清哪个参数是输入哪个是输出。作者得出的结论是：C# 的 `struct` 值类型 + 运算符重载合起来正好弥补了这两个短板，这"大概是 Unity 选 C# 而不是 Java 的多个深层原因之一"。

## 关键要点

- **无运算符重载**：链式 `.add().subtract().mul()` 让数学代码可读性崩塌；
- **无栈分配对象**：向量运算 hot loop 把 heap 变成 GC 噩梦；
- 唯一 workaround：预分配 `tempVector` 成员变量 + 改函数签名为 out-parameter 风格；
- 代价：签名看不出 in/out、多 temp 之间 aliasing 风险、返回值不能自然链式；
- Java 引用赋值的默认行为（`v = a.add(b)` 不是 copy）埋下隐蔽 bug；
- 作者猜测 Unity 选 C# 的原因之一就是 C# 有 `struct` 值语义和运算符重载；
- 替代方案里他顺带提到 Android NDK（绕过 Java）和中间件（如 Unity）——这也和他自己从自研 Java 引擎迁 [[sources/elopezr-will-of-flame|Will of Flame]] 到 Unity 的经历呼应。

## 链接到的概念

- [[java-vector-math-limitations]]
- [[garbage-collector]]
- [[unity-vs-unreal]]

## 原文

- 链接：https://www.elopezr.com/java-and-vector-math/
- 本地：`raw/articles/elopezr.com/2014-06-15_java-and-vector-math.md`
