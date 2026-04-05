---
tags: [软件设计, 复杂性根源, aposd]
date: 2026-04-05
sources: 1
---

# 模糊性（Obscurity）

**模糊性**是复杂性的第二个根源（和 [[dependencies]] 并列）：

> "Obscurity occurs when important information is not obvious."
> 当重要信息不显而易见时，就产生了模糊性。

模糊性直接制造 [[unknown-unknowns]]。当系统的重要信息被藏起来时，调用者无法知道自己需要关心它，于是 bug 悄然泄漏。

## 典型来源

1. **命名不精确**。`time` 是秒还是毫秒？UTC 还是本地？帧时间还是墙钟？`count`、`flag`、`temp`、`data`——不加修饰时都是红旗。
2. **不一致性**。同一个概念一处叫 `Character`，一处叫 `Actor`，又一处叫 `Entity`。读者永远不确定它们是不是同一个东西。
3. **隐式约定**。带副作用但没文档的函数。看不见的初始化顺序要求。「必须先调 X 再调 Y」这类只活在口头知识里的假设。
4. **过时的文档**。注释描述的是旧版本的行为，不仅无用而且主动误导。

## 文档是补丁，不是解药

> "The need for extensive documentation is often a red flag that the design isn't quite right. The best way to reduce obscurity is by simplifying the system design."

如果一个函数需要 30 行注释才能被安全使用，真正的问题通常是设计本身不清楚——注释是在掩盖结构性问题。更好的方案是重新设计函数，让签名和类型直接表达约束：改名以精确、消除副作用、把约束挤进类型。自解释的代码比任何注释都长寿。

## 一种微妙的变体：泄漏的抽象

模糊性还会以相反方式出现：当一个「简洁」的抽象隐藏了调用者其实需要知道的细节时，它就变成了 [[false-abstraction|虚假抽象]]。一个不告诉你「写入什么时候真正落盘」的文件缓存 API 在此类——表面简单，实际是陷阱。

## 相关

- 姊妹根源：[[dependencies]]
- 直接后果：[[unknown-unknowns]]
- 对策：[[abstraction]]、[[information-hiding]]

## Sources

- [[sources/aposd-day02]]
