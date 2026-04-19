---
tags: [unity, dots, ecs, editor-tool, debug]
date: 2026-04-19
sources: 1
---

# 给 Unity ECS 世界写自定义 Inspector 调试工具

Unity DOTS 转换工作流下，设计期用 GameObject、运行期转成 Entity。转换后 Inspector 和 Entity Debugger 只能**只读**查看组件值，改不了。[[gemserk]] 给出一种轻量做法：**每个关心的 Entity 配一个"影子 GameObject"**，再给它写 CustomEditor，把 ECS 值暴露出来、可编辑、可触发动作。

## 总体思路

三件东西一起工作：

1. **影子 MonoBehaviour**（`DebugEntityMonoBehaviour`）：仅仅持有 `Entity` 引用 + 一组要显示的镜像字段（`current`、`total`、`attackRange` …）。
2. **同步 System**（`DebugEntitiesSystem`）：用 `ISystemStateSharedComponentData` 把 Entity 与 shadow GameObject 绑定，创建/更新/销毁成对发生。
3. **CustomEditor**（`DebugEntityInspector`）：override `OnInspectorGUI`，渲染字段、监听 `EndChangeCheck`，把用户改的值通过 `EntityManager.SetComponentData` 写回 ECS 世界；再加几个按钮触发游戏动作（`Perform Damage`、`Destroy`）。

## 关键细节：用 ISystemStateSharedComponentData 管生命周期

`ISystemStateSharedComponentData` 的好处是它**不会随 Entity 被销毁而自动清**——当玩家代码 `DestroyEntity` 了目标 Entity，这个组件还会留一帧，给同步 System 一个机会销毁对应的 shadow GameObject、再 `RemoveComponent` 自己。三段式查询：

- `WithAll<UnitComponent>().WithNone<DebugEntitySystemComponent>()` → 新 Entity 来了，造一个 shadow GO，`AddSharedComponent`。
- `WithAll<UnitComponent, DebugEntitySystemComponent, HealthComponent>()` → 每帧把 ECS 字段拷到 MonoBehaviour 字段。
- `WithAll<DebugEntitySystemComponent>().WithNone<UnitComponent>()` → Entity 被销毁或标签被移除，清掉 shadow GO 并移除 system state。

## 写回路径

CustomEditor 里的关键几行：

```csharp
if (EditorGUI.EndChangeCheck()) {
    entityManager.SetComponentData(debug.entity, new HealthComponent {
        current = newCurrent, total = newTotal
    });
}
if (GUILayout.Button("Perform Damage")) {
    var damageEntity = entityManager.CreateEntity(ComponentType.ReadWrite<Damage>());
    entityManager.SetComponentData(damageEntity, new Damage {
        target = debug.entity, damage = 5
    });
}
```

作者强调这是"**复用游戏逻辑做改值**"——真正的伤害由 DamageSystem 处理，Editor 只是注入一条 `Damage` 消息；避免直接改值破坏不变量（例如血量小于等于零但没触发死亡系统）。

## Gizmos 扩展

shadow MonoBehaviour 可以画 Gizmos。例子：同步 Entity 的 `AttackComponent.range` 和 `Translation.Value` 到 MonoBehaviour，在 `OnDrawGizmos` 里画出攻击范围 wireframe。不需要额外代码维护可视化状态——ECS 已经是真源，shadow 只是镜像。

## 作者的权衡

Pros：
- 能把整个 Unity Editor 工具链（Handles、Scene view、Undo）借过来；
- 按需暴露字段，不必像反射自动生成方案那样暴露一堆无关东西；
- 对游戏逻辑友好——按钮直接调用游戏行为，不用复制不变量检查。

Cons：
- 每种 Component 都要手写 shadow 和 Editor，不自动；
- 只能在 Editor 里用，打包出去的版本没有这个调试能力。

作者在结尾提出一个更好的方向：把调试工具**做进游戏内的 UI**（Unity UI Toolkit），这样开发版和 QA 版都能用，不只限于 Editor。

## 和其他"数据查看器"的对比

这种做法本质上和 Entity Debugger 的差异是**白名单 + 可写**：只显示你挂了 `UnitComponent` 标签的 Entity，且允许改值/触发动作。对于调试驱动的开发循环，远比"把所有 Entity 全部可视化"有用。

## 相关

- [[ecs]]
- [[dots-ecs-programming-patterns]]
- [[runtime-editor-console-connection]] — 另一类"游戏内调试通道"的思路
- [[gemserk]]

## Sources

- [[sources/gemserk-custom-editor-ecs]]
