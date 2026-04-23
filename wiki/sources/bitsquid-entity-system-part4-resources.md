---
tags: [source, 游戏引擎, ecs, entity-system, bitsquid, blob, resource]
date: 2026-04-19
sources: 1
---

# Building a Data-Oriented Entity System, Part 4: Entity Resources（Niklas Frykholm / Bitsquid）

[[niklas-frykholm]] 2014 年 10 月 10 日连载的第四篇，把[[bitsquid-data-oriented-entity-system|Part 1–3 的 entity/component 机制]]和 [[offset-based-resource-blobs|blob 资源]] 两条线接在一起：一个 level 或 prefab 在磁盘上长成什么样、spawn 10 000 个 entity 的时候 CPU 走哪些 cache 才不浪费。

## 摘要

静态资源走 blob——指针换 offset、endian 出厂即交换，内存 `fread` 即用。但 entity 是**纯动态的**——所有 component 都可运行时增删改，所以 entity resource 里只有一套 **"怎么把 instance 构造出来"的指令**，不需要 instance 回头引用 resource。

最朴素的 layout 是每 entity 套一层 `struct { num_components; ComponentData[]; num_children; EntityResource[]; }`，spawn 时"创建 A、A 的 Transform、A 的 Mesh、A 的 Actor；创建 B、B 的 Transform……"。Niklas 指出这违反了 data-oriented 的第一原则 **"Do similar things together"**——交替创建不同 component 把 I-cache 和 D-cache 都打乱。改法是把 entity resource 按 **component 类型** 重排：先创建全部 entity，再按 type 一次性建 100 个 Transform、再一次性建 100 个 Mesh——**"Where there is one, there are many"**：让 EntityManager 一口气 `create_entities(n)`、让每个 ComponentManager 一口气建一批 instance。

对应的 resource 布局变成外层 `EntityResource { num_entities; num_component_types; parent_index[]; ComponentTypeData[]; }`，内层 `ComponentTypeData { component_identifier; num_instances; size; entity_index[]; instance_data[]; }`。**未知 component type 可以一次性 skip 整块**（原版要挨个 entity skip），数据导向重组带出的意外红利。父子关系摊进 `parent_index[]` 数组（`UINT_MAX` 表示根），不塞进 TransformComponent。

实现侧两个注册点：`register_component_compiler(name, fn, spawn_order)` 把 JSON 片段编成 binary blob——`spawn_order` 决定依赖顺序（Mesh 依赖 Transform 要后建）。`register_component_spawner(name, fn)` 拿 `(entity_lookup, num_instances, entity_index, data)` 批量建 instance，`entity_lookup[entity_index[i]]` 给出第 i 个 component instance 归属的 `Entity` 句柄。作者还讨论过把 `spawn_order` 换成显式依赖声明，更 clean。

## 关键要点

- 纯动态 entity system 里，resource 只存"指令"，instance 不反向引用 resource
- 朴素 per-entity 嵌套 layout 违反 "Do similar things together"：I-cache / D-cache 都乱
- 改法：外层按 component 类型分组——`EntityResource.ComponentTypeData[]` 每种 component 一整块
- **"Where there is one, there are many"**：EntityManager 一口气建 n 个、ComponentManager 一口气建一批
- 未知 component 类型可一次 skip 整块——数据导向重组的附加红利
- `parent_index[]` 在 EntityResource 根上平摊，不塞进 TransformComponent
- `ComponentData` wrapper：`{ identifier; size; data[] }`——size 让未知类型可跳
- 离线 `CompileFunction(JSON) → Buffer`；runtime `SpawnFunction(lookup, n, entity_idx, data)`
- `spawn_order` 数字排序决定依赖；作者考虑改成显式 depends-on 声明
- Level 常 10 000+ object，restart 时要 spawn 得快——值得优化

## 链接到的概念

- [[bitsquid-data-oriented-entity-system]]
- [[offset-based-resource-blobs]]
- [[ecs]]
- [[custom-allocator-interface]]
- [[handle-based-resource-manager]]

## 原文

- 链接：https://bitsquid.blogspot.com/2014/10/building-data-oriented-entity-system_10.html
- 本地：`raw/articles/bitsquid.blogspot.com/2014-10-10_building-a-data-oriented-entity-system-part-4-entity-resourc.md`
