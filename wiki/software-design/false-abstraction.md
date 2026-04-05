---
tags: [软件设计, 反模式, aposd]
date: 2026-04-05
sources: 1
---

# 虚假抽象（False Abstraction）

Ousterhout 对省略了重要细节的抽象的诊断：

> "An abstraction that omits important details is a false abstraction: it might appear simple, but in reality it isn't."

虚假抽象**看起来简单**，但调用者实际上必须理解被隐藏的细节才能安全使用。它是一种特别危险的复杂性，因为它伪装成清晰。

## 经典例子：文件系统缓存

文件系统 API 对外看似简洁，但对数据库开发者来说，「数据什么时候真正落盘」是关键信息。如果接口没有暴露这个信息或提供控制手段，数据库的耐久性保证就被悄悄破坏了——接口看起来简单，实际设计失败。

## 游戏开发中的案例

```csharp
GameObject obj = ResourceManager.Load("prefabs/bullet");
```

看似简单的资源加载接口。但：
- `obj` 的生命周期由谁管？
- 是引用计数还是 GC？
- `Load` 后资源会不会在下次场景切换时被卸载？
- 再次 `Load` 同一路径是返回缓存还是重新加载？

这些信息在接口里不可见，但调用者必须知道才能正确使用。一个典型的虚假抽象——简单外表下的陷阱。

## 如何识别

- 接口命名/签名承诺了简单，但实际使用中需要反复查源码。
- 使用者经常问「这个函数会不会……」这种关于内部行为的问题。
- 有一些「隐藏规则」只有老成员才知道。
- 文档里一堆「警告/注意」条目——文档在补丁式地补回被错误隐藏的信息。

## 解药

要么让隐藏的信息真正不相关（重新设计让它不再重要），要么把它纳入接口（让它变得显式）。不要假装它不存在。

## 相关

- 反面：[[abstraction]] 的正确形态
- 效果：[[obscurity]] 的载体
- 对比：一个成功的隐藏案例是 [[garbage-collector]]——GC 把内存管理变得真正不相关

## Sources

- [[sources/aposd-day04]]
