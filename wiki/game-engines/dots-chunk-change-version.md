---
tags: [unity, dots, ecs, 变化追踪, 版本号]
date: 2026-04-19
sources: 1
---

# DOTS Chunk Change Version：按写权限粒度的变化追踪

DOTS 给每个 **archetype chunk** 维护一个 **change version**（uint），配合 `System.LastSystemVersion` 可以实现"这个 chunk 自我上次 update 以来变过没有"——变过就 re-process，没变过就跳过。大规模 ECS 系统几乎必依赖这个机制来做增量工作，但行为有几个非直觉点，写错很容易出难追的 bug。

## 三个版本号的舞蹈

- **🌍 Global system version**：每个 system（包括 system group）update 完都 +1。
- **↩️ Last system version**（per-system）：每个 system update **完之后**把 global 值 cache 进来。进入下一次 update 时，`LastSystemVersion` 反映的是**上次 update 时**的 global。
- **✏️ Chunk change version**（per-chunk）：当 query 以 **write 权限**命中某 chunk 时，立即将 chunk 的 change version 更新为**当前**全局值。

"chunk 变了吗"的判定：**chunk.changeVersion > system.lastSystemVersion**。

## 关键陷阱 1：write 意图即 change，不管有没有真写

change version 的更新是**按 query 的写权限**判定，**不看 C# 代码是否真的修改了组件**。`RefRW<T>` 在 query 里出现一次，就算 foreach 内没动它，所有匹配到的 chunk 都会被标记为"这一帧变过"。

推论：**change filter 只能当优化，不能当 branch logic**。假设把 filter 拿掉，整套逻辑必须仍然正确；filter 在的时候只是"少做一些冗余工作"。不能依赖它做业务判定。

## 关键陷阱 2：filter 最多只能挂 2 个组件

- `SystemAPI.Query<...>.WithChangeFilter<T1>()` / `<T1, T2>` 只有这两个重载。
- `EntityQueryBuilder.AddChangedVersionFilter` 虽然"看起来可 additive"，源码里硬编码了上限 2——第三次调用抛错。

需要 3+ 组件的变更检测必须降到 `IJobChunk`，自己在 Execute 里调 `chunk.DidChange(ref typeHandle, lastSystemVersion)` 组合 if/else。

## 关键陷阱 3：相邻 system 并不相邻

`[UpdateAfter(A)]` 的 B 并不是紧接 A 的下一次 update——system group 里还有许多内置 system（Transform hierarchy、physics、animation...）穿插。作者测下来两个相邻自定义 system 之间夹着**3 个内置 system**。这意味着：

- 从 system A 到 system B，global version 可能 +4、+5。
- 但 B 的 `LastSystemVersion` 记录的是**上一帧** B 自己 update 后的值，不是 A 的值——所以 A 本帧刚写的 chunk，**B 本帧 did-change 成立**，下一帧 did-change 不再成立（因为 B 自己也 update 过一次）。

## 关键陷阱 4：first frame 一切都是 "changed"

第一次 update 时 `LastSystemVersion = 0`——任何 chunk change version（即便从未被写过）都满足 `> 0` 于是被视为 changed。这符合"filter 是优化，无 filter 也正确"的原则：初次 update 把所有 chunk 过一遍是对的。

## 关键陷阱 5：RequireForUpdate 不考虑 filter

`RequireForUpdate<T>()` / `[RequireMatchingQueriesForUpdate]` 可以让 system 在无匹配 entity 时跳过 update——但**忽略所有 filter**。即使 change filter 不 match 任何 chunk，`RequireForUpdate` 还是让 system 每帧跑。真要"只在某些组件变了才跑 update"得自己在 `OnUpdate` 里 `query.IsEmpty` 早退（`IsEmpty` 算 filter）。

## 关键陷阱 6：Enableable 不做 chunk 级优化

把一个组件对 16 个 entity disable 后，它们仍然留在原 chunk 里（只是 mask 标记 off）。chunk 的 change version 更新按 chunk 粒度——哪怕所有 active entity 都不在这个 chunk 里，只要 query 以 RW 命中过这个 chunk，change version 就更新。Enableable 更多是 per-entity 优化，不对 chunk change tracking 省事。

## Per-entity change checking 的官方模式

Unity `Unity.Transforms` 里 `Parent` 的处理给出了模式范例——chunk 级 DidChange 太粗，需要 per-entity 时：

- 创建一个"影子"组件 `PreviousParent`（字段和 `Parent` 一模一样，类型改为 `ICleanupComponentData`）。
- 一个 system 负责：新 Parent 出现时 add `PreviousParent` 并复制值。
- 另一 system 在 `chunk.DidChange(ref ParentHandle) || chunk.DidChange(ref PreviousParentHandle)` 里，逐 entity 比较 `Parent.Value != PreviousParent.Value`——真变了才做重活，结束后 `PreviousParent = Parent`。

`ICleanupComponentData` 还顺带解决组件 remove / entity destroy 的通知——`WithAll<PreviousParent>.WithNone<Parent>` 可以捕捉 Parent 消失的两种路径。

## IJobChunk 的 RW 决定看 ComponentTypeHandle

`IJobChunk` 里拿 `NativeArray<T>` 要靠 `SystemAPI.GetComponentTypeHandle<T>(isReadOnly)`。**`isReadOnly` 的值决定了这个 query 对系统是 RW 还是 RO**，从而决定 chunk change version 是否被更新。`[ReadOnly]` 属性可以贴在 job 字段上做编译期检查，但作者觉得它不一定参与 system 的读写依赖计算——更稳的是 handle 参数本身是对的。

## 相关

- [[ecs]]
- [[dots-enableable-components]]
- [[dots-ecs-cache-iteration]]
- [[dots-ecs-programming-patterns]]
- [[aos-vs-soa]]
- [[sirawat-pitaksarit]]

## Sources

- [[sources/gametorrahod-chunk-change-version]]
