---
tags: [软件设计, 模块化, aposd, 核心概念]
date: 2026-04-05
sources: 1
---

# 信息隐藏（Information Hiding）

**信息隐藏**是实现 [[deep-modules]] 的核心技术：

> "The most important technique for achieving deep modules is information hiding. The basic idea is that each module should encapsulate a few pieces of knowledge, which represent design decisions. The knowledge is embedded in the module's implementation but does not appear in its interface."

翻译：**每个模块应该封装一些代表设计决策的知识。这些知识活在实现里，不出现在接口上。**

## 「知识」这个词

Ousterhout 用 knowledge 而不是「数据」「变量」「算法」，因为他要强调的是**设计决策本身**。

存档格式用 JSON——这是一种知识。文件布局、序列化策略——全都是知识。如果这份知识只藏在 `SaveSystem` 类里，外面不在乎是 JSON 还是 Protocol Buffers，那就是信息隐藏。有一天换成 protobuf，只改 SaveSystem，其他系统不受影响。

## 两大好处

> "Information hiding reduces complexity in two ways. First, it simplifies the interface. Second, information hiding makes it easier to evolve the system. If a piece of information is hidden, there are no dependencies on that information outside the module, so a design change will affect only the one module."

1. **简化接口**。
2. **更容易演进系统**——修改成本 O(1)。

## `private` ≠ 信息隐藏

这是最容易踩的坑：

> "Hiding variables and methods by declaring them private isn't the same thing as information hiding. Information about the private items can still be exposed through public methods such as getter and setter methods."

**`private` 是访问控制（语言机制）。信息隐藏是设计哲学。**

反例：有 private，没有信息隐藏：

```csharp
public class CharacterStats {
    private Dictionary<string, float> _stats;
    public Dictionary<string, float> GetStats() => _stats;  // 返回内部字典引用
}
```

调用者现在知道内部用字典存属性，可以直接破坏不变量。

正例：真正的信息隐藏：

```csharp
public class CharacterStats {
    private Dictionary<string, float> _stats;
    public float GetStat(string name) { ... }
    public void SetStat(string name, float value) { ... }  // 在这里加业务约束
}
```

调用者不知道内部是字典还是数组。改实现接口不变。

HTTPRequest 的对照：
- `getParams()` 返回 `Map<String, String>` → 浅模块，暴露实现。
- `getParameter(String name)` 返回 `String` → 深模块，隐藏实现。

## 优秀工程师的品味

**真正的信息隐藏是设计决策的结果，不是语言约束的副产品。** 一个优秀工程师能用 public 字段实现完美的信息隐藏（只要外部不需要知道该字段如何产生和使用）；一个糟糕工程师用满 private 也会把内部实现通过 getter 漏个干净。

## 关联的反面

信息隐藏的反面是 [[information-leakage]]。[[temporal-decomposition]] 是制造信息泄漏的常见方式。

## 相关

- 反面：[[information-leakage]]
- 结果：[[deep-modules]]
- 常见陷阱：[[temporal-decomposition]]
- 语言机制 vs 设计哲学的区分
- C 语言实践：[[c-opaque-struct-modules]]、[[malloc-wrapper-debug]]

## Sources

- [[sources/aposd-day06]]
