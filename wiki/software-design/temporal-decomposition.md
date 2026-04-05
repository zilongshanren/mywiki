---
tags: [软件设计, 反模式, aposd]
date: 2026-04-05
sources: 1
---

# 时序分解（Temporal Decomposition）

**时序分解**是一种听起来合理但常常有害的设计直觉：

> "In temporal decomposition, the structure of a system corresponds to the time order in which operations will occur. When designing modules, focus on the knowledge that's needed to perform each task, not the order in which tasks occur."

**核心问题**：按照「事情发生的顺序」切割模块，而不是按照「谁拥有哪些知识」切割。这几乎必然制造 [[information-leakage]]。

## 反例：动画配置初始化

流程是「读文件 → 解析状态 → 创建状态机 → 绑定 GameObject」。时序分解的设计：

```csharp
public class AnimConfigReader { ... }   // 步骤1：读文件
public class AnimConfigParser { ... }   // 步骤2：解析
public class AnimStateMachineFactory { ... }  // 步骤3：创建
```

`AnimConfigReader` 要知道配置文件格式才能读，`AnimConfigParser` 也要知道才能解析——「配置文件格式」这份知识在两个类里同时存在。**信息泄漏。**

## 经典案例：HTTP 请求

> "One team used two different classes for receiving HTTP requests; the first class read the request into a string, and the second class parsed the string. Information leakage occurred because an HTTP request can't be read without parsing much of the message; for example, the Content-Length header must be parsed to compute the total request length."

表面上「读」和「解析」是两件事，但 HTTP 协议结构决定了——**你不解析就没法读完**。Content-Length 在头里，必须先解析头才知道 body 多长。在知识层面，这两步是同一件事。

## 资源加载的时序分解陷阱

```csharp
// 错误
public class AssetLoader { ... }        // 加载原始字节
public class AssetDecompressor { ... }  // 解压
public class AssetDeserializer { ... }  // 反序列化

// 正确
public class AssetBundleReader {
    public Asset Load(string path) { ... }  // 内部一条龙处理
}
```

三个类都需要了解资产包内部格式。升级格式，三处都改。

## Ousterhout 的反直觉建议

> "information hiding can often be improved by making a class slightly larger."

把本应合并的类强行拆开，只会制造信息泄漏。**有时候，让一个类「稍微大一点」，是比拆成两个浅类更好的设计。** 这与 Clean Code 的「小类优先」直接冲突——Ousterhout 的判断标准是「深度」，不是「大小」。

## 识别信号

- 类名是流水线结构：`XXXLoader / XXXParser / XXXProcessor`。
- 相邻步骤共享一份格式/协议/结构的知识。
- 「按职责分」的拆法，实际上是按时间顺序分。

## 相关

- 直接后果：[[information-leakage]]
- 正确原则：[[information-hiding]]
- 相关张力：[[classitis]] 也常以时序分解形态出现

## Sources

- [[sources/aposd-day06]]
