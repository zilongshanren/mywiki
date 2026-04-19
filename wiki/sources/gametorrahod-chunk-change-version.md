---
tags: [source, unity, dots, ecs, 变化追踪]
date: 2026-04-19
sources: 1
---

# Chunk's Change Version（Sirawat Pitaksarit / Game Torrahod）

[[sirawat-pitaksarit]] 2024 年 5 月的博客，从 API 面到底层机制讲清 DOTS 的 **chunk change version** 是怎么工作的、有哪些反直觉点。

## 摘要

DOTS 给每个 archetype chunk 维护一个 `uint` **change version**，系统侧维护 `LastSystemVersion` 和一个全局递增的 `GlobalSystemVersion`。判断规则：**chunk.changeVersion > system.LastSystemVersion** ⇒ "chunk 自上次该 system update 以来变过"。更新规则是**按 query 的 write 权限**：`RefRW<T>` 出现在 query 里，哪怕 foreach 体没真的写，所有 match 的 chunk 都会被打上本帧 change version。

API 面：`SystemAPI.Query<>.WithChangeFilter<T>/<T1,T2>` 有硬编码的**最多 2 个组件**上限；`EntityQueryBuilder.AddChangedVersionFilter` 调用第三次会抛错。3+ 组件的变更检测只能降到 `IJobChunk`，在 Execute 里自己 `chunk.DidChange(ref handle, lastSystemVersion)` 组合。

作者用 90 个 entity + "胖 buffer" 把 archetype 压成每 chunk 15 entity 做实验，验证了几个陷阱：(1) 第一次 update `LastSystemVersion = 0`，任何 chunk 都满足 `> 0` → 全被视为 changed（这符合"filter 是优化不是 branch logic"的原则）；(2) `[UpdateAfter(A)]` 的 B 并不是紧接 A 的下一次——system group 内置 system 会穿插，作者测下来两个自定义 system 之间夹 3 个内置；(3) `RequireForUpdate<T>` 忽略 filter；(4) Enableable 不做 chunk 级优化——只要 RW query 匹配到 chunk，即便 active entity 一个都没有也会更新 change version。

末尾给出 `Unity.Transforms` 的 `Parent` / `PreviousParent` 模式做 **per-entity change checking**：影子组件 + `ICleanupComponentData` 一石二鸟——既能比 chunk 粒度更细地判断"真变了"，又能在组件 remove / entity destroy 时捕获现场做清理。

## 关键要点

- Write **意图**即更新 change version，不看实际是否修改。
- Filter 最多 2 个组件（源码硬编码），3+ 要降到 `IJobChunk`。
- First-frame `LastSystemVersion = 0` 导致全 "changed"——设计上是对的。
- `[UpdateAfter]` 并不真的紧邻，内置 system 穿插会让 `LastSystemVersion` 跳多档。
- Enableable 是 per-entity，**不**省 chunk 级 change tracking 的工作。
- `IJobChunk` 里 RW/RO 由 `SystemAPI.GetComponentTypeHandle<T>(isReadOnly)` 的参数决定，`[ReadOnly]` 属性作用未必传达。
- Per-entity change checking：影子组件 `PreviousT` as `ICleanupComponentData`，`chunk.DidChange(A) || chunk.DidChange(PreviousA)` → per-entity 比较。

## 链接到的概念

- [[dots-chunk-change-version]]
- [[dots-enableable-components]]
- [[dots-ecs-programming-patterns]]
- [[ecs]]

## 原文

- 链接：https://gametorrahod.com/change-version/
- 本地：`raw/articles/gametorrahod.com/2024-05-13_chunk-s-change-version.md`
