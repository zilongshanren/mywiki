---
tags: [软件设计, 复杂性根源, aposd]
date: 2026-04-05
sources: 1
---

# 依赖（Dependencies）

**依赖**是复杂性的两大根源之一（另一个是 [[obscurity]]）：

> "A dependency exists when a given piece of code cannot be understood and modified in isolation; the code relates in some way to other code, and the other code must be considered and/or modified if the given code is changed."
> 当一段代码不能独立被理解和修改时，就存在依赖；代码与其他代码相关，修改前者时必须考虑或修改后者。

依赖是不可避免的——你不可能写完全没有依赖的代码。设计问题不是「是否有依赖」，而是依赖是否**必要、显式、方向清晰**。

## 依赖如何制造复杂性

依赖喂养了三种症状中的两种：

- **[[change-amplification]]**：改 A 必须改 B、C、D。
- **[[cognitive-load]]**：理解 A 必须先理解 B、C、D。
- **[[unknown-unknowns]]**：隐藏的依赖变成待引爆的 bug。

## 好依赖 vs 坏依赖

**好依赖**的特征：
- 显式——出现在函数签名或类型里，不走全局变量偷运。
- 简单——少数几个清晰的接触点，而不是几十个入口。
- 方向明确——A 依赖 B，不反过来。

**坏依赖**的特征：
- 藏在全局可变状态里。
- 双向或循环依赖。
- 跨层穿透多个不相关的模块。

## 循环依赖：游戏引擎典型案例

经典失败：渲染模块依赖物理模块提供碰撞体位置；物理模块依赖渲染模块提供几何数据做碰撞检测。两者无法先后初始化。解法是引入一个共享的中间层（比如 Transform 数据存储），让两个模块都依赖它，断开循环。

## 事件系统的伪装

事件总线常被当作「解耦」，但实际上常常**隐藏**依赖而非消除。事件发送方和订阅方在语义上依然相互依赖（顺序、载荷结构、副作用假设），只是代码级搜索找不到连接了。这是把显式依赖换成了隐式依赖——游戏开发中 [[classitis]] 的主要形式之一。

## 相关

- 姊妹根源：[[obscurity]]
- 后果：[[change-amplification]]、[[cognitive-load]]、[[unknown-unknowns]]
- 对策：[[information-hiding]]、[[deep-modules]]

## Sources

- [[sources/aposd-day02]]
