---
tags: [游戏引擎, gea, 架构]
date: 2026-04-05
sources: 1
---

# 引擎分层（Engine Layering）

**上层依赖下层，下层不依赖上层**——引擎架构的第一纪律。

## Gregory 的典型分层

```
Game                    ← 游戏逻辑
─────────────────────
Gameplay Foundations    ← 脚本、AI、行为树
─────────────────────
Rendering / Physics / Animation / Audio / Input / UI ...
─────────────────────
Core Systems            ← 资源管理、场景管理、事件
─────────────────────
Platform Independence   ← 平台抽象
─────────────────────
OS / Hardware
```

## 为什么单向依赖

- **可测试性**：下层可独立测试。
- **可替换性**：换 OpenGL 为 Vulkan 只需改 Platform 层。
- **复用性**：核心系统可在不同游戏类型间复用。

## 循环依赖 = 死刑

Gregory 说得直白：**循环依赖是引擎设计的死刑**。一旦出现：
- 无法单独测试其中任何一层。
- 构建依赖变成纠结的图。
- 重构接口必须同时改两处。

这与 APoSD 的 [[dependencies]] 分析吻合——**依赖方向清晰**是可维护性的关键。

## 破循环的典型手段

- **引入中间层**：两个相互依赖的模块依赖一个共同的数据/接口。
- **事件系统**：下层发出事件，上层订阅（但注意 [[classitis-in-games|事件系统滥用]]）。
- **依赖倒置**：高层定义接口，低层实现。

## 相关

- [[game-engine]]
- [[dependencies]]
- [[classitis-in-games]]

## Sources

- [[sources/gea-day01]]
