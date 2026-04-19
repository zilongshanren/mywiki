---
tags: [source, unity, dots, ecs, 模式]
date: 2026-04-19
sources: 1
---

# ECS Programming Patterns from Official Packages（Sirawat Pitaksarit / Game Torrahod）

[[sirawat-pitaksarit]] 2024 年 5 月，从 Unity 自家的 `Unity.Transforms` / Entities Graphics / `Unity.Scenes` / `Unity.Physics` 等包里扒出 DOTS 的"官方推荐写法"——因为这些包和 `Unity.Entities` 一起迭代，能保证模式不过时。

## 摘要

作者归纳了 9 个模式：

1. **Cleanup component 对子**——业务组件 + 同字段 `ICleanupComponentData` 影子，`.WithNone<Real>.WithAll<Previous>` 一个 query 捕获组件 remove 和 entity destroy 两条路径。
2. **Per-entity change checking**——影子组件同时做"字段级 DidChange"；chunk 粒度 DidChange 太粗，比较 `Parent.Value != PreviousParent.Value` 才是真变。
3. **Entry-point helper 加一组组件**——`RenderMeshUtility.AddComponents` 用 `FixedList128Bytes<ComponentType>` + `ComponentTypeSet` 一次塞一批，免去用户背必需组件清单。
4. **系统自动补齐缺失组件**——另写一个 system 用 `WithAll<Entry>.WithNone<Required>` query 把缺的补回来；用户删了也会下一帧出现，形成"隐式契约"。
5. **`NativeParallelMultiHashMap` 当 tuple array**——duplicate key + `TryGetFirstValue`/`TryGetNextValue` 迭代，Burst-friendly，比 `HashMap<K, NativeList<V>>` 少一层 allocation。
6. **可复用 archetype 组**——`static` helper 返回存着多个 `EntityArchetype` 的 struct，避免定义散落 + 忘改漏改。
7. **Disable tag component**——`WithNone<DisableX>` 集中在 query 侧声明；add/remove tag 即"冻/解冻"，业务组件不用重建。
8. **Request component（可逆触发）**——`RequestSceneLoaded` add → load、remove → unload；组件存在与否本身就是 state，和"一次性 request entity"模式互补。
9. **`using` 控制 Allocator 生命期**——`Allocator.TempJob` 的 array 用 C# `using` 块，防漏 dispose、早退 path 也安全。

## 关键要点

- 官方包是 Unity DOTS 最可靠的"best practice"样本——保证与 Entities 版本同步不过时。
- Cleanup component 的"tag + 监听"本质：entity destroy 通过普通 query 捕获不到，影子组件留下"最后的值"。
- Chunk `DidChange` 是粗筛，per-entity 真变检测靠影子组件的"当前 vs 上次"比较。
- Tag-in-`WithNone` 模式让"临时禁用"是声明式的，避免分散的 `if`。
- `using` + `Allocator.TempJob` 是 NativeArray 生命期管理的默认写法。

## 链接到的概念

- [[dots-ecs-programming-patterns]]
- [[dots-chunk-change-version]]
- [[dots-enableable-components]]
- [[ecs]]
- [[data-driven-architecture]]

## 原文

- 链接：https://gametorrahod.com/ecs-patterns/
- 本地：`raw/articles/gametorrahod.com/2024-05-20_ecs-programming-patterns-from-official-packages.md`
