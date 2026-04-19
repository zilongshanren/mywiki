---
tags: [source, unity, dots, ecs, custom-editor, debug]
date: 2026-04-19
sources: 1
---

# Using Custom Editors to interact with Unity ECS World（Gemserk / Ariel）

[[gemserk]] 2020 年 8 月的实战笔记：Unity ECS 转换工作流下 Entity 无法在 Inspector 里编辑，作者用一层 shadow GameObject + CustomEditor 给关心的 Entity 做可写的调试 UI。

## 摘要

思路是每个要调试的 Entity 关联一个 shadow GameObject（挂 `DebugEntityMonoBehaviour`）。`DebugEntitiesSystem` 用 `ISystemStateSharedComponentData` 管生命周期：Entity 出现就建 shadow GO + shared component、每帧把 ECS 字段镜像到 MonoBehaviour、Entity 销毁时再销毁 shadow GO。对应的 `DebugEntityInspector` 是 `CustomEditor`：监听 `EndChangeCheck` 写回 `EntityManager.SetComponentData`，按钮按下时不是直接改值而是创建 `Damage` 消息 Entity 让游戏逻辑自己处理、维持不变量。扩展例：同步 `AttackComponent.range` 和 `Translation.Value` 到 shadow，`OnDrawGizmos` 画攻击范围 wireframe。作者坦白缺点：手写不自动、只在 Editor 内可用、不 scale；但对开发中的定点调试非常够用。文末提到进一步方向：用 Unity UI Toolkit 做游戏内调试 UI，摆脱 Editor-only 限制。配套仓库 `DebugToolsEcsExample`。

## 关键要点

- `ISystemStateSharedComponentData` 不会随 Entity 销毁自动移除，正适合"需要清理副作用"的场景。
- 三段查询：`WithNone<DebugComponent>` 创建、`WithAll` 同步、`WithNone<UnitComponent>` 销毁。
- CustomEditor 的按钮不要直接改值，应当创建消息 Entity 走游戏逻辑路径。
- Gizmos 依赖 shadow GO 的 Transform，所以要同步 `Translation` 值。
- 自动反射方案会暴露太多无关字段——白名单式的手写 Editor 反而更可用。

## 链接到的概念

- [[unity-ecs-custom-editor-debug]]
- [[ecs]]
- [[dots-ecs-programming-patterns]]

## 原文

- 链接：<https://blog.gemserk.com/2020/08/13/using-custom-editors-to-interact-with-ecs/>
- 本地：`raw/articles/blog.gemserk.com/2020-08-13_using-custom-editors-to-interact-with-unity-ecs-world.md`
