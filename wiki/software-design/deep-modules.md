---
tags: [软件设计, 模块化, aposd, 核心概念]
date: 2026-04-05
sources: 2
---

# 深模块（Deep Modules）

**深模块**是 Ousterhout 的核心正面构造——设计理想：

> "The best modules are those that provide powerful functionality yet have simple interfaces. I use the term *deep* to describe such modules."
> 最好的模块是那些提供强大功能但接口简单的模块。我用「深」来描述它们。

可视化成矩形：面积代表功能，宽度（顶边）代表接口复杂度。**深模块**高而窄——大面积，小顶边。[[shallow-modules|浅模块]]矮而宽——小面积，大顶边。

## 接口即成本的视角

> "The benefit provided by a module is its functionality. The cost of a module (in terms of system complexity) is its interface."
> 模块提供的收益是它的功能。从系统复杂性角度看，模块的成本是它的接口。

这个视角重新定义了接口。一个方法不是「提供的服务」——它是**强加给每个调用者的负担**。每个参数、每个副作用、每条使用约定，都是所有使用者必须装在脑子里的东西。减少接口面积不是整洁——而是慷慨。

接口有两部分：

- **形式化（Formal）**——签名、类型、异常。编译器可检查。
- **非形式化（Informal）**——行为、前置条件、顺序、线程安全、副作用。编译器不可检查。

> "For most interfaces the informal aspects are larger and more complex than the formal aspects."

一行签名可能藏一页使用约束。深模块设计很大程度上就是缩小非形式化的表面。

## 经典例子：Unix I/O

五个系统调用：

```
open, read, write, lseek, close
```

背后是几十万行的文件系统、缓存、调度、设备驱动、权限。详见 [[unix-io]]。接口几十年没变，实现却经历了激进重写——深度的第二重收益：**实现可以演进，调用者不受影响**。

## 更深的模块：垃圾回收器

> "Another example of a deep module is the garbage collector in a language such as Go or Java. This module has no interface at all; it works invisibly behind the scenes to reclaim unused memory."

GC 是极限案例：**接口为零**的模块。详见 [[garbage-collector]]。加上 GC 不仅让系统更深，还**缩小**了系统总接口——因为它消除了 `free`/`delete` 的全局词汇。

## 深度的启发式判断

判断模块是否足够深的实操测试：

1. **文档比率**。接口文档长度接近或超过实现长度——可能太浅。
2. **调用者知识测试**。新用户能否不读源码就正确使用？必须看内部的话，接口在泄漏。
3. **常见情况的简洁度**。80% 的使用场景长什么样？Unix I/O 默认顺序+缓冲；Java 的流三件套（见 [[java-io]]）需要三个对象。前者为常见情况优化。
4. **实现变更测试**。改内部需要改调用者吗？需要的话，细节在泄漏。

一个粗略的量化：`深度 ≈ 实现行数 / 文档化接口行数`。越大越深。

## 不是庞然大物的许可证

深不代表「一个做所有事的巨类」。深模块依然有一个连贯的单一职责——它只是通过一个窄接口去履行。判断标准不是大小，而是**是否隐藏了知识**。参见 [[information-hiding]]。

## 相关

- 反面：[[shallow-modules]] 及其病态形态 [[classitis]]
- 引擎：[[information-hiding]]
- 机制：[[abstraction]]、[[interface-vs-implementation]]
- 经典例证：[[unix-io]]、[[garbage-collector]]

## Sources

- [[sources/aposd-day04]]
- [[sources/aposd-day05]]
