---
tags: [unity, dots, ecs, 模式, cleanup-component]
date: 2026-04-19
sources: 1
---

# DOTS ECS 官方代码里学到的模式

Unity 的 DOTS 生态文档稀、教程乱，可信度最高的"权威写法"是 **Unity 自己引用 `Unity.Entities` 的包**——`Unity.Transforms`、Entities Graphics、`Unity.Scenes`、`Unity.Physics`。这些包和 `Unity.Entities` 一起编译，等同于官方用产品代码示范"这样写才不会随版本过期"。Sirawat 从里面扒出来的几个高频模式：

## 1. Cleanup component 监听 remove + destroy

`ICleanupComponentData` 的文档说"tag entities that require cleanup when destroyed"——实际用法是**配对追踪**：

- 业务组件 `Parent`（普通 `IComponentData`）
- 影子组件 `PreviousParent`（`ICleanupComponentData`）

当 `Parent` 被 remove **或** entity 被 destroy，`PreviousParent` 都会留下。`.WithNone<Parent>.WithAll<PreviousParent>` 这一个 query 能捕获两条路径，system 可以读到 `PreviousParent` 里存的"最后一刻"的值来做清理（比如通知这个 entity 的旧 parent 从 Children buffer 里移走它）。

单独用 `.WithNone<Parent>` 查不到"destroy 掉整个 entity"的情况——entity 没了就不会匹配任何 query。cleanup component 是这个盲区的解药。

## 2. Per-entity change checking pattern

见 [[dots-chunk-change-version]] 的末尾——`Parent` / `PreviousParent` 除了做 cleanup，也用来做**字段级变化检测**：`chunk.DidChange` 只能到 chunk 粒度，真要 per-entity 就比较当前 vs. 影子，值变了才做重活。

## 3. Helper 加一组相关组件（entry-point helper）

一个 GameObject `MeshRenderer` 被 DOTS 化以后需要一组组件协同——`RenderMeshUtility.AddComponents(entity, em, desc, array, info)` 是 Entities Graphics 的范式：

```csharp
var components = new FixedList128Bytes<ComponentType> {
    ComponentType.ReadWrite<WorldRenderBounds>(),
    ComponentType.ReadWrite<RenderFilterSettings>(),
    ComponentType.ReadWrite<MaterialMeshInfo>(),
    ComponentType.ChunkComponent<ChunkWorldRenderBounds>(),
    // ...
};
em.AddComponent(entity, new ComponentTypeSet(components));
```

`FixedList128Bytes<ComponentType>` 免去手动 dispose；`ComponentTypeSet` 配合 `AddComponent` 一次性添加一整套。API 使用者不用背所有 required component 的名字——helper 里装好。

## 4. System 自动补齐缺失组件

和 helper 互补的另一条路：让用户只 add 一个 entry 组件，**另写一个 system 用 `WithAll<That>.WithNone<RequiredX>` 自动补齐**。Entities Graphics 的 `UpdateHybridChunksStructure` 就在做这件事——用户忘了加（或手动 remove 了）`RootLODRange` 等组件，下一帧 system 直接把它们加回来。配合专门 recompute 数值的 system，结果是"supporting components 对外透明、被删了会自动回来"——这是一种用 ECS 惯用法实现的**隐式契约**。

## 5. NativeParallelMultiHashMap 当 tuple array

duplicate key 被允许，加上 `TryGetFirstValue` + `TryGetNextValue` 的迭代 API，可以当"每个 key 一串 value"的容器用：

```csharp
if (map.TryGetFirstValue(parent, out var child, out var it)) {
    do { children.Add(new Child { Value = child }); }
    while (map.TryGetNextValue(out child, ref it));
}
```

比 `NativeHashMap<K, NativeList<V>>` 省一层分配、Burst-friendly、跨 job 可以共享。

## 6. 可复用的 archetype 组

同一个 archetype 在多处要创建——写一个 `static` helper 返回 struct：

```csharp
internal struct ResolveSceneSectionArchetypes {
    public EntityArchetype SectionEntityRequestLoad;
    public EntityArchetype SectionEntityNoLoad;
}
internal static ResolveSceneSectionArchetypes Create(EntityManager em) =>
    new() {
        SectionEntityRequestLoad = em.CreateArchetype(typeof(...), typeof(...)),
        SectionEntityNoLoad      = em.CreateArchetype(typeof(...)),
    };
```

`Unity.Scenes` 里的写法。避免 archetype 定义散落在多个 system 里各自写一遍、某处加字段时漏改。

## 7. Disable tag component

需要暂时"冻结"一批 entity（不被任何 system 处理，但组件数据保留）——加一个 `DisableSceneResolveAndLoad` 这样的 tag，所有相关 query 都在 `WithNone<DisableSceneResolveAndLoad>` 里声明一次。相比移除业务组件，tag 方案：

- 移除 tag 就能"解冻"，业务组件不用重建。
- tag 名自文档化，一眼能看到 disabling 的意图。
- 查询侧的 WithNone 是集中式声明，避免散落的 `if` 判断。

`Unity.Scenes` 在编辑器加载场景时用这个模式防止 runtime system 动那些"还没走完导入流程"的 entity。

## 8. Request component（可逆触发）

`Unity.Scenes` 的 `RequestSceneLoaded`——加上组件 → section 开始加载，remove 组件 → 自动卸载。和"request entity + done tag"的 one-shot 模式不同：这里**组件的存在/不存在本身就是 state**，add/remove 对称地驱动 load/unload。

适合"可以来回切换"的操作（加载/卸载、启用/禁用）；不适合"做完就完"的一次性任务（发射子弹、播放特效）——后者用 request entity 更合适。

## 9. `using` 控制 Allocator 生命期

需要手动 Dispose 的 `Allocator.TempJob` 数组，最优雅的写法是 C# `using` 块：

```csharp
using (var entities = query.ToEntityArray(Allocator.TempJob))
using (var guids = query.ToComponentDataArray<TState>(Allocator.TempJob)) {
    for (...) { /* work */ }
} // 自动 Dispose 两个 array
```

这是 `Unity.Scenes` 的写法，防漏 dispose，配合早退 path 也安全。

## 相关
- [[ecs]]
- [[dots-enableable-components]]
- [[dots-chunk-change-version]]
- [[dots-ecs-cache-iteration]]
- [[data-driven-architecture]]
- [[sirawat-pitaksarit]]
- [[svelto-ecs]] — Sebastiano Mandalà 的对照路线：group 模型 + 显式 composition root + ECS-centric 而非 ECS-only
- [[svelto-on-dots]] — 把 DOTS ECS 当作引擎库接入 Svelto 的集成模式
- [[svelto-filters-api]] — filter 语义比 [[dots-enableable-components]] 更通用

## Sources

- [[sources/gametorrahod-ecs-patterns]]
