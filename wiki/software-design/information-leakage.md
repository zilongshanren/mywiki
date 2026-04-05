---
tags: [软件设计, 反模式, aposd]
date: 2026-04-05
sources: 1
---

# 信息泄漏（Information Leakage）

**信息泄漏**是 [[information-hiding]] 的反面——Ousterhout 认为是最重要的设计红旗之一：

> "Information leakage is one of the most important red flags in software design. If you encounter information leakage between classes, ask yourself 'How can I reorganize these classes so that this particular piece of knowledge only affects a single class?'"

**信息泄漏发生在：一份知识（一个设计决策）同时存在于多个模块里。** 当它的实现改变时，所有拥有这份知识的模块都必须跟着改——这是 [[change-amplification]] 的直接原因。

## 显式泄漏

网络位置序列化的典型案例：

```csharp
public class NetworkSender {
    public void SendPosition(Vector3 pos) {
        // 知道：x/y/z 各 4 字节，紧凑排列
        BitConverter.GetBytes(pos.x).CopyTo(data, 0);
        BitConverter.GetBytes(pos.y).CopyTo(data, 4);
        BitConverter.GetBytes(pos.z).CopyTo(data, 8);
    }
}

public class NetworkReceiver {
    public Vector3 ReceivePosition(byte[] data) {
        // 同一份序列化格式的知识
        float x = BitConverter.ToSingle(data, 0);
        ...
    }
}
```

「位置序列化格式」这份知识同时藏在两个类里。改成 half 精度？两个类都要改。加 timestamp？两个类都要改。

解法：把序列化知识集中到一个 `PositionSerializer`。

## 后门泄漏（Back-door Leakage）——更可怕

> "Suppose two classes both have knowledge of a particular file format (perhaps one reads files in that format and the other writes them). Even if neither class exposes that information in its interface, they both depend on the file format: if the format changes, both classes will need to be modified. Back-door leakage like this is more pernicious than leakage through an interface, because it isn't obvious."

**后门泄漏不出现在任何接口里，但实实在在地存在。**

地图编辑器例子：`MapExporter.Export()` 和 `MapImporter.Import()` 的接口都干净，但两者实现里都持有地图文件格式的知识。升级地图格式，两个类都得改。

## 如何发现

经典诊断问题：

> **「如果 X 改了，有多少个地方需要修改？」** 如果答案大于 1，那个 X 对应的知识就泄漏了。

其他信号：
- 接口暴露了 `Map`、`List`、`byte[]` 这种具体数据结构。
- 命名暴露了实现（`parseJsonConfig()`）。
- 改 A 必须改 B。
- 类名是 `XXXLoader / XXXParser / XXXProcessor` 这种流水线结构——警惕 [[temporal-decomposition]]。

## 游戏开发中的高危区域

- **存档系统**：序列化格式的知识不要泄漏到存档系统之外。
- **资源管理**：资源包格式的知识只应该存在于加载器里。
- **网络协议**：包格式的知识不应泄漏到游戏逻辑层。
- **配置系统**：Config 文件格式（CSV/JSON/SO）不要泄漏到使用方。
- **渲染管线**：Shader property binding 不要泄漏到上层 Material 代码。

## 相关

- 反面：[[information-hiding]]
- 典型制造机：[[temporal-decomposition]]
- 效果：[[change-amplification]]
- 修复指引：把共享知识收归一处，让一个类「稍微大一点」

## Sources

- [[sources/aposd-day06]]
