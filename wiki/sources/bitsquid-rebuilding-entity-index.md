---
tags: [source, game-engines, ecs, stingray, bitsquid, entity-system]
date: 2026-04-19
sources: 1
---

# Rebuilding the Entity Index（Bitsquid / Stingray）

Bitsquid 博客 2017-05-16 的匿名署名文章（根据风格与主题，来自 Stingray 的 entity system 维护者，疑似 [[niklas-frykholm|Niklas Frykholm]] 或其 gameplay 团队），讲述 Stingray 在引擎演进到 Flow / Property 系统后，如何把最初的 `Entity Index`（entity → array-of-components 的反查表）重写成可随 entity 数量线性扩展的结构。

## 摘要

Stingray 的 entity system 最初并不跟踪 "某个 entity 拥有哪些 component 实例" 这一层信息——每个 component manager 自己用 SoA 管。后来为了让 Flow visual scripting 通过 `(entity, component_name, property_name)` 读写属性，就在全局加了一张 Entity Index，把每个 entity 所拥有的 component 实例全部登记：`entity → [{ name_hash, component_manager*, instance_id }]`。这张表随 entity 数量线性膨胀，10 万以上 entity 时内存和 CPU 都快速下坡。

作者做了两步重构。第一步：把 `InstanceId` 的控制权从 component manager 收回给调用方，并规定 `InstanceId = hash(component_name_in_resource)`。这样 `instance_id` 就和 name 冗余，可以从索引中删除，只剩 `{ name_hash → component_manager* }`。第二步：观察到由同一份 entity resource 实例化出的所有 entity 其 lookup 表是相同的——只有 manager 指针相同，component 组合也相同。因此把 lookup list 提取成 resource 级共享的 "lookup prototype"，由 entity 持一个指针；当 entity 被程序化修改（加减 component）时再按需 fork。这把每个 entity 的固定开销从 O(n_components) 的表项降到一个指针，内存占用随 entity 数近乎常数增长。

## 关键要点

- 问题定位精确：Entity Index 之所以膨胀，是因为 *创建时无法预知 InstanceId*，只能一条条登记；把 `InstanceId = hash(name)` 这一约束前置，就把整张表变成可推导的。
- "按 resource 共享 lookup"是典型的 flyweight——entity system 层做 structural sharing，只有结构发生分叉时才复制。
- 给出了从 10k 到 10.24m entity 的基准：旧实现在 2.56m 处开始非线性劣化（约 2.4us/entity），新实现线性。
- API 对称性变好：`create(entity, hash("Transform"))` 与 `lookup(entity, hash("Transform"))` 形式一致，不再需要 `InstanceWithId` 这种外带返回值。
- 代价：component manager 失去了"自主分配 InstanceId"可能带来的优化空间，但作者判断这在现实中几乎没有用到。

## 链接到的概念

- [[entity-index-reconstruction]]
- [[ecs]]
- [[handle-based-resource-manager]]
- [[c-opaque-struct-modules]]

## 原文

- 链接：https://bitsquid.blogspot.com/2017/05/rebuilding-entity-index.html
- 本地：`raw/articles/bitsquid.blogspot.com/2017-05-16_rebuilding-the-entity-index.md`
