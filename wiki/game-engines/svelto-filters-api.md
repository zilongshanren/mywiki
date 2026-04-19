---
tags: [ecs, svelto, 数据结构]
date: 2026-04-19
sources: 3
---

# Svelto.ECS Filters API

Svelto.ECS 的内存布局以**群组（Group / GroupCompound）**为核心：每个 entity 只能出现在一个 group 里，group 常被当成"状态机的状态"。GroupCompound 把最多 4 个 tag 组合出一个具体 group，用来表达多维状态。但当状态组合爆炸、或者只是想临时对某个子集做操作时，仅靠 group 会把内存切得过碎、代码也绕。[[sebastiano-mandala]] 在 Svelto 3.3（2022）把 filter API 重写了一版来填这个缺口。

## Filters 做什么

Filter 是**跨 group 的 entity 子集索引**。它不改变 entity 存放的位置，只在一个独立的数据结构里记录 "这些 entity 属于这个子集，分别在哪些 group 的哪些 index 上"。关键特点：

- **用户不再需要知道 entity 在哪些 group**——filter 自己保存 `(filterID, group) → indices`，iterate 的时候 filter 是"一等公民"，group 跟在它下面
- 可以和 GroupCompound 叠用，于是一个 entity 同时属于"某 group compound" + "某 filter 子集"
- 分两类：
  - **Transient filter** — 每次 entity submission 后自动清空，适合"本帧内临时打标"（例如"本帧受到伤害的实体"）
  - **Persistent filter** — 框架长期持有；entity 被删除时自动把它从相关 filter 里摘掉
- filter 的 ID 可自定义，还带一个 `context`，所以不同子系统可以用各自的语义复用 filter 命名空间

## 典型用法

新 Stride Doofuses demo 里，entity 的 group 代表游戏状态（饿 / 吃），不代表 mesh。为了知道每个 entity 用哪个 prefab 渲染，用 `stride entity ID` 当 filter ID 建 persistent filter：

```csharp
cachedFilter = ref sveltoFilters.GetOrCreatePersistentFilter<StrideComponent>(
    strideEntityId, StrideFilterContext.StrideInstanceContext);
cachedFilter.Add(entityIDs[index], groupID, index);
```

渲染时遍历 `StrideInstanceContext` 下的所有 filter，每个 filter 再遍历内部的 `(indices, group)` 对，把 matrix 拷出去给 Stride 实例化：

```csharp
foreach (ref var filter in filters) {
    foreach (var (indices, currentGroup) in filter) {
        var (matrices, _, _) = entitiesDB.QueryEntities<MatrixComponent, StrideComponent>(currentGroup);
        for (var i = 0; i < indices.count; ++i)
            outMatrices[k++] = matrices[indices[i]].matrix;
    }
}
```

注意必须用 `indices[i]` 做**二级索引**（先进 filter，再进 group 数组），直接用 `i` 会读错行——这是 filter 使用中最常见的坑。

## 用 Filter 替代 Event / Publisher-Consumer

Mandalà 在 Survival 示例（见 [[sources/sebaslab-survival-mini-example]]）里借机废掉了 publisher/consumer 模式。他的论点：**人们想要从 event 里拿到的东西，本质上是"处于某状态的一批 entity"**——这正好是 filter 能精确表达的。典型例子是伤害流水线里的两个 transient filter：

- `DamagedEntitiesFilter` — 本帧 `damageToApply > 0` 的 entity
- `DeadEntitiesFilter` — 从前者中筛出血量 ≤ 0 的

两者都是 transient，每帧自动清空；下游 engine 读取这些 filter 就能只处理"受伤"/"死亡"子集，而不需要事件、回调、或者单独的"Damaged" tag compound。Mandalà 认为这比 event-driven 更 ECS、也更容易测试。

## 与 DOTS ECS 的对照

DOTS ECS 1.0 引入的 [[dots-enableable-components|IEnableableComponents]] 在 Mandalà 看来是"filter 的弱化版"——它只能表达状态（启用/禁用），不能像 Svelto filter 那样建模 *ownership relationship*（例如把一组 entity 和一个外部资源绑定）。参见 [[svelto-on-dots]] 里他对 DOTS 1.0 的完整评价。

## Sources

- [[sources/sebaslab-svelto-filters-api]]
- [[sources/sebaslab-survival-mini-example]]
- [[sources/sebaslab-svelto-on-dots-update]]
