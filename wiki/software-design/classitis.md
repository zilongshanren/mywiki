---
tags: [软件设计, 反模式, aposd]
date: 2026-04-05
sources: 3
---

# Classitis（类炎症）

Ousterhout 发明的词，描述「类越多越好」这种系统性错误倾向：

> "The extreme of the 'classes should be small' approach is a syndrome I call *classitis*, which stems from the mistaken view that 'classes are good, so more classes are better.'"

Classitis 是对单一职责原则（SRP）的机械化理解产物。「单一职责」没有客观粒度——如果把职责定义得足够窄，任何类都可以被拆成十个「更专注」的类。

## 核心危害

> "Small classes don't contribute much functionality, so there have to be a lot of them, each with its own interface. These interfaces accumulate to create tremendous complexity at the system level."

不能只看单个类的复杂度，要看系统整体的接口复杂度。十个小类的接口总和，可能比一个功能完整的深类的接口复杂得多——而且这种复杂度是**分布式的、隐性的**，更难理解和维护。

## 标准病例：Java I/O

```java
FileInputStream fileStream = new FileInputStream(fileName);
BufferedInputStream bufferedStream = new BufferedInputStream(fileStream);
ObjectInputStream objectStream = new ObjectInputStream(bufferedStream);
```

三个对象读一个序列化文件。忘记 `BufferedInputStream` 不会报错，只会悄悄慢几十倍——**annoying 导致 error-prone**。把缓冲这种 99% 场景都需要的能力拆成单独的类，不是灵活性，是陷阱。详见 [[java-io]]。

## 游戏开发中的 Manager 癌

经典案例：

```
PlayerMovementManager.cs
PlayerAnimationManager.cs
PlayerInputHandler.cs
PlayerStateManager.cs
PlayerHealthManager.cs
PlayerAbilityManager.cs
PlayerAudioManager.cs
PlayerVFXManager.cs
PlayerUIManager.cs
```

十个 Manager 挂在同一个 Player 上。每个只做「一件事」，看起来职责清晰。但实际使用时：理解「玩家受伤时发生什么」需要同时打开五个文件；加「受伤摄像机震动」不明确该改哪个 Manager。这就是系统级接口复杂度远高于模块级表面简洁的体现。

一个更深的 `PlayerController` 可能有 800 行——**但行数是假指标，认知负担才是真指标**。一个接口简洁、逻辑内聚的 800 行类，比十个接口复杂、依赖分散的 80 行 Manager，更容易理解、修改、测试。

## 事件系统的变体

Classitis 的隐性变体：每个 Manager 发若干事件、听若干事件。每个 Manager 的接口看起来简洁，但**系统整体的接口**是一张庞大且隐形的事件网络图。想知道「玩家死亡时发生什么」，需要追查所有 `OnPlayerDeath` 的订阅者——可能散布在十五个文件里，且执行顺序无文档化。

**显式耦合比隐式耦合好管理——因为显式耦合可以在代码里看到、追踪、测试。**

## 与 Clean Code 的张力

Clean Code 主张「函数不超过 N 行」「类要小」。Ousterhout 反驳：**拆分的标准应该是「是否增加了深度」，而不是「是否超过了 N 行」**。一个 50 行的线性函数，可能比拆成 5 个 10 行的函数更好理解，因为 5 个函数意味着 5 个接口、5 次跳转。

## 相关
- 根源：[[shallow-modules]]
- 反面：[[deep-modules]]
- 游戏开发视角：[[classitis-in-games]]
- 经典案例：[[java-io]] vs [[unix-io]]
- [[cpp-multi-paradigm-discipline]] —— 云风评注 Effective C++ 3rd 的 Item 1：把 C++ 当成语言联邦、定义团队子集
- 图形/引擎实例：[[sources/aras-syntonic-dentiforms-redux]] —— Aras 回头看自己 2004 年的 demo，把 `IAnimChannel`/`CAnimChannel<T>`/`IAnimStream<T>`/`CAbstractTimedAnimStream<T>`……14 个模板接口压成 3 个具体类型，整个项目 216 文件 24k 行 → 49 文件 6k 行
- [[encapsulation-over-polymorphism]] —— Supnik 的 90/10/0 原则，classitis 正是把「类多 = 抽象多 = 好设计」的幻觉推向极致的症状

## Sources

- [[sources/aposd-day04]]
- [[sources/aposd-day05]]
- [[sources/aras-syntonic-dentiforms-redux]]
- [[sources/c0de517e-cpp-style-pain]] —— Pesce 2012：C-style 不透明指针模块「免费」解决了 singleton / 依赖注入 / PIMPL，证明许多 C++ 包裹是无谓的复杂度
