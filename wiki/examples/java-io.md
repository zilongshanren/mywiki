---
tags: [反面案例, 浅模块, classitis, aposd]
date: 2026-04-05
sources: 2
---

# Java I/O —— Classitis 的典型

Java I/O 是 Ousterhout 举的**典型 [[classitis]] 案例**，和 [[unix-io]] 形成完美对照。

## 三层包装的序列化读取

```java
FileInputStream fileStream = new FileInputStream(fileName);
BufferedInputStream bufferedStream = new BufferedInputStream(fileStream);
ObjectInputStream objectStream = new ObjectInputStream(bufferedStream);
```

读一个序列化文件需要三个对象。这三个对象之间有依赖：必须按此顺序创建，前两个之后几乎不单独使用。

## 为什么特别糟糕

> "It is particularly annoying (and error-prone) that buffering must be requested explicitly by creating a separate BufferedInputStream object; if a developer forgets to create this object, there will be no buffering and I/O will be slow."

Ousterhout 用了两个词：**annoying** 和 **error-prone**。因为繁琐（annoying），所以容易出错（error-prone）。

忘记加 `BufferedInputStream`：
- 不会有编译错误
- 不会有运行时错误
- 程序照样跑
- 只是悄悄地 I/O 慢几十倍

这是最危险的那种错误：可能在开发环境永远不被发现，到生产环境真实用户数据压力下才暴露。

## 信息泄漏与虚假抽象的双重罪

- **[[information-leakage]]**：缓冲这个实现细节泄漏给了调用者——调用者必须知道「什么时候需要加 buffer」。
- **[[false-abstraction]]**：接口看起来在做 I/O，但实际上需要懂得很多实现层的知识才能正确使用。

## 设计哲学对比

| | Unix I/O | Java I/O |
|---|---|---|
| 所需对象/调用 | 5 个函数 | 3 个对象 |
| 缓冲是否默认 | 内核默认提供 | 显式包装 |
| 常见情况成本 | 最小 | 高 |
| 忘了缓冲的后果 | 不会出现（已默认） | 悄悄慢几十倍 |

> "Almost every user of file I/O will want buffering, so it should be provided by default."

## 根本教训

把三种能力（文件访问、缓冲、序列化）分成三个类听起来很「正交」——每个类做一件事，自由组合。但问题是：**99% 的情况都需要缓冲**。所以把缓冲单独拆出来不是在提供灵活性，而是在制造陷阱。

## 相关

- 反面标杆：[[unix-io]]
- 体现的反模式：[[classitis]]、[[shallow-modules]]、[[information-leakage]]、[[false-abstraction]]

## Sources

- [[sources/aposd-day04]]
- [[sources/aposd-day05]]
