---
tags: [软件设计, aposd, 核心概念]
date: 2026-04-05
sources: 1
---

# 抽象（Abstraction）

Ousterhout 对抽象的精确定义：

> "An abstraction is a simplified view of an entity, which omits unimportant details."
> 抽象是一个实体的简化视图，省略了不重要的细节。

关键词是**「不重要的细节」**。抽象不是任意的简化，而是**有选择地省略不重要的细节**。

## 两种抽象失败

**第一种：包含了不重要的细节**

接口比必要的更复杂。例如哈希表接口暴露了「当前哈希算法」——大多数调用者根本不需要知道，却增加了认知负担。这会让模块变浅（参见 [[shallow-modules]]）。

**第二种：省略了重要的细节（[[false-abstraction|虚假抽象]]）**

> "An abstraction that omits important details is a false abstraction: it might appear simple, but in reality it isn't."

看起来简单，实际上是陷阱。经典例子：文件系统缓存对外看似简单，但数据库开发者必须知道「数据什么时候真正写到磁盘」——这个细节很重要，隐藏它就是虚假抽象。

游戏开发中的常见陷阱：

```csharp
// 看起来简单
GameObject obj = ResourceManager.Load("prefabs/bullet");
```

但调用者需要知道：obj 的生命周期由谁管？引用计数还是 GC？场景切换会不会被卸载？如果接口里看不到这些信息，就是虚假抽象——简单外表下藏着定时炸弹。

## 与深模块的关系

一个 [[deep-modules|深模块]] 正是通过好的抽象来隐藏不重要细节、保留重要接口。抽象是深度的实现机制。

## 相关
- 载体：[[deep-modules]]
- 反面：[[false-abstraction]]
- 目标：隐藏 [[obscurity]] 意义下的「不重要细节」
- [[identity-problem-naming]] — 抽象的本质是划分 1,000 维空间
- [[stl-not-abstraction-prescription]] — 反面案例：STL 明确地不隐藏实现复杂度

## Sources

- [[sources/aposd-day04]]
