---
tags: [软件设计, 模块化, aposd, 反模式]
date: 2026-04-05
sources: 2
---

# 浅模块（Shallow Modules）

**浅模块**是 [[deep-modules|深模块]] 的反面——接口复杂度相对于它提供的功能过于复杂：

> "a shallow module is one whose interface is relatively complex in comparison to the functionality that it provides... It doesn't take much code to manipulate a linked list (inserting or deleting an element takes only a few lines), so the linked list abstraction doesn't hide very many details."

这里的「复杂」不是指接口有多少方法，而是**使用这个模块需要理解的东西**：它的存在、命名、参数语义、合用场景、副作用。总和就是「认知税」。如果税高于省下的工作量，这个模块就是浅的、有害的。

## 极端案例

```java
private void addNullValueForAttribute(String attribute) {
    data.put(attribute, null);
}
```

Ousterhout 的判断：

> "From the standpoint of managing complexity, this method makes things worse, not better. The method offers no abstraction, since all of its functionality is visible through its interface."

这个方法提供的抽象**为零**。接口复杂度和实现复杂度完全等价，接口端还多了发现成本和记忆成本。调用者学习它换来的信息量是零，付出的认知成本是正的。

甚至打字数上——`data.put(attribute, null)` 比调用这个方法更短。所谓「封装」是纯粹的负担。

## 核心认知

好的抽象不是把代码切成更小块，而是**让调用者理解更少的东西**。分割是手段，不是目的。当分割之后调用者需要理解的东西变多了，这种分割就是净亏损。

## 病态扩展：Classitis

当浅模块成为系统性的设计倾向，就产生了 [[classitis]]——「类应该小，所以类越多越好」的教条式应用。

## 合理存在的场景

并非所有浅模块都是失败：

- **边界层的 pass-through**：不同抽象层次之间的薄适配层，职责就是翻译。
- **框架强制的结构**：Unity 的 MonoBehaviour 生命周期有时强制把逻辑分散到不同类里。
- **测试隔离**：为了可测试性而提取的小接口，是有意识的权衡。

关键词是**有意识**。如果你创建一个浅模块，应该清楚为什么、代价是什么、代价是否值得。[[classitis]] 的危害在于它通常是**无意识的**。

## 相关

- 反面：[[deep-modules]]
- 病态形态：[[classitis]]
- 例证：[[java-io]]
- 原因：[[information-leakage]]、[[false-abstraction]]

## Sources

- [[sources/aposd-day04]]
- [[sources/aposd-day05]]
