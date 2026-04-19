---
tags: [引擎架构, ecs, entity-system, 数据导向, stingray, 哈希表, 原型链]
date: 2026-04-19
sources: 1
---

# Entity Index 的原型链式重构

Stingray 的 [[ecs|Entity / Component]] 系统里，Entity 本身只是一个 id，不直接持有它的组件列表——所有组件由各自的 Component Manager 按 SoA 存储。但要让 Flow（可视化脚本）通过 **组件名** 读写属性，引擎又必须维护一张 "Entity × 组件名 → (Component Manager, Instance)" 的查找表。这张表叫 **Entity Index**。

最直白的实现：每个 Entity 单独挂一张小数组，里面是该实体的所有组件条目。听起来很简单，但 Stingray 的合成测试给出一张让人不想接手的曲线——10 万实体 26 MB、1000 万实体 130 MB，每实体平均耗时从 0.5 μs 滑到 2.5 μs。**memory 和 time 都超线性**。问题出在哪里？每个 entity 的 entry 列表之间毫无复用，哪怕一万个实体共享同一套组件组合，这张表也乖乖存一万份拷贝。

## 重构前提：一个隐式的约束变显式

解决起点是一个被忽视的新约束：**Flow 要能按组件名找到组件，那组件名就是 InstanceId**。

原 API 里 Component Manager 自己决定 InstanceId，调用方拿到一个 opaque 的 handle；重构后倒过来——**调用方把 InstanceId 传进去**，让它等于组件名的 32 位哈希：

```cpp
// 重构前
InstanceWithId r = mgr.create(entity);       // mgr 决定 id
Instance i = mgr.lookup(entity, r.id);

// 重构后
mgr.create(entity, hash("Transform"));       // 调用方决定 id
Instance i = mgr.lookup(entity, hash("Transform"));
```

InstanceId 冗余了（它就是组件名的哈希），Entity Index 里那一列直接省掉。剩下的是 `(Entity, ComponentName) → ComponentManager*` 的查表。

## 关键洞察：entity 的组件集合构成"原型链"

多数 entity 由资源（prefab）生成，组件组合天然在少数形状里重复。如果把 "追加一个组件" 看作一次"继承"，那每个 entity 的组件集合就是一条 **prototype chain**：

```
P0 = []
P1 = P0 + [&transform_manager,     "Transform"]
P2 = P1 + [&render_data_manager_1, "Fog"]
P3 = P2 + [&render_data_manager_1, "Vignette"]
P4 = P1 + [&render_data_manager_2, "Fog"]      // 换了个 manager 就分叉
P5 = P4 + [&render_data_manager_2, "Vignette"]
```

- 所有从同一 prefab 生成的 entity 共享同一个尾节点 prototype。
- 运行时动态 add/remove 组件会让 entity 迁移到不同原型——但只要顺序一致，大量共享仍然成立。

每个 prototype 节点只存 **(base_prototype, component_manager, component_name)** 三元组，约 16 字节。Entity 本身只存 `Prototype` 一个值。查找组件时沿链往回走，直到 name 命中或抵达根。

## 伪代码

```cpp
struct PrototypeDescription {
    Prototype base;
    ComponentManager* mgr;
    IdString32 name;
};
Map<Entity, Prototype>              entity_prototype;
Map<Prototype, PrototypeDescription> prototypes;

void register_component(Entity e, ComponentManager* m, IdString32 n) {
    Prototype p  = entity_prototype[e];
    Prototype np = mix(p, mix(hash(m), hash(n)));   // content-addressed
    if (!prototypes.has(np))
        prototypes.insert(np, {p, m, n});
    entity_prototype[e] = np;
}

ComponentManager* find(Entity e, IdString32 n) {
    Prototype p = entity_prototype[e];
    while (p) {
        auto& d = prototypes[p];
        if (d.name == n) return d.mgr;
        p = d.base;
    }
    return nullptr;
}
```

Prototype 名字用内容哈希（mix base 和该层 content），天然去重——两条独立构造的链只要最终内容相同就落到同一个 prototype id 上。

## 效果

合成测试重测：内存从"随实体数线性增长到 130 MB"塌到**稳定 < 1 MB**；时间从"每实体 2.5 μs 且增长"变成**恒定 0.7 μs**。内存赢在 prototype 之间的结构共享，时间赢在 prototype map 非常紧凑所以 lookup 的 cache miss 极少。

代价是查找变成链式遍历；但因为 prototype 节点 16 字节、chain 深度 ~ 组件数（个位数），实测比原始数组查表还快——热点都在 L1 里。

## 这个模式不止是 ECS 的把戏

结构共享 + 内容哈希 的原型链，是 JavaScript V8 的 **hidden class / map transitions** 一模一样的路子：对象按属性添加顺序共享一条 shape transition，shape 只存一份，单个对象只存 shape id + 值数组。Ethereum 的 **trie**、Git 的 **tree object**、Clojure 的 **persistent data structure** 也都是"不可变前缀 + 哈希 consing"的变体。Stingray 不过是把这个经典技巧挪到 ECS 的 Entity Index 上——当你在设计时发现某个集合"加一个元素"的模式压倒性地占多数，就该想想原型链而不是散列数组。

## 为什么"后重构"比"一开始就设计成这样"更现实

Niklas 的博客特别提到：原始 Entity Index 设计时，Flow / Property 的"按组件名访问"还不存在，InstanceId 是 opaque 的。新需求到位之后，一个之前合理的设计决策（让 Manager 自由分配 InstanceId）变成了瓶颈。这是 [[continuous-design|持续设计]] 的又一个例子——**新约束揭示了旧抽象的冗余**，适时重构比一开始猜未来更健康。

## 相关

- [[ecs]] — Stingray 的 Entity/Component system 背景
- [[id-based-lifetime-with-kill-flag]] — 同样是"Entity id + side table"的配套设计
- [[handle-based-resource-manager]] — Stingray 风格的句柄管理
- [[c-opaque-struct-modules]] — Component Manager 的 API 封装哲学
- [[aos-vs-soa]] — Component Manager 内部用 SoA
- [[continuous-design]]
- [[niklas-frykholm]]

## Sources

- [[sources/bitsquid-rebuilding-entity-index]]
