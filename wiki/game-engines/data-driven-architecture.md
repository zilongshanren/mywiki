---
tags: [游戏引擎, gea, 架构]
date: 2026-04-05
sources: 1
---

# 数据驱动架构（Data-Driven Architecture）

Jason Gregory 认为**数据驱动是真正引擎 vs 游戏专用软件的分水岭**。

## 定义

**行为由配置/组件定义，而不是由硬编码逻辑定义**。同一段代码通过不同数据文件、不同 component 组合，能产出完全不同的行为。

## 具体对照

**硬编码（游戏专用）**：
```csharp
void RenderOrc(Orc orc) { /* orc-specific logic */ }
```

**数据驱动（引擎）**：
```csharp
void Render(Entity entity) {
    if (entity.HasComponent<MeshRenderer>()) {
        Draw(entity.GetComponent<MeshRenderer>());
    }
}
```

## 体现形态

- **ECS/Component Composition**：Unity GameObject+Component、Unreal Actor+Component。
- **Blueprint / Visual Scripting**：让非程序员也能定义行为。
- **ScriptableObject** / **Data Asset**：把配置外置到资源文件。
- **Behavior Tree / State Machine** 可视化编辑。

## 好处

- 美术/策划独立迭代，不需要程序介入。
- 同引擎能支持多种风格游戏。
- 数据可被工具链处理（批量编辑、自动化测试、procedural generation）。

## 权衡

- 抽象层引入 overhead（`GetComponent()`、反射）。
- 调试更难（行为分散在数据文件里）。
- 性能问题常在运行时才暴露。

Unity DOTS 的目标之一是**在保持数据驱动灵活性的同时恢复性能**——通过 SoA 布局。

## 相关

- [[game-engine]]
- [[engine-layering]]
- [[ecs]]
- [[aos-vs-soa]]

## Sources

- [[sources/gea-day01]]
