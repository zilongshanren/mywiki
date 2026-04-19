---
tags: [unity, prefab, gameobject, scriptable-object, 数据驱动]
date: 2026-04-19
sources: 1
---

# Unity 把 Prefab 当纯数据容器用

[[gemserk]] 写过一篇观点明确的短文：在 Unity 里存**纯数据**（无逻辑）时，社区的默认选择是 `ScriptableObject`，但他主张大量场景应该改用**GameObject + Prefab**——叫做 Data GameObject。理由是 GameObject 免费带来了一堆 ScriptableObject 没有的结构能力。

## 额外拿到的能力

把 Prefab 视作一条数据记录、把 GameObject 视作一行带字段的值，能同时得到以下几样东西：

1. **层级组合**：GameObject 可以嵌套成树，子对象即子数据。`GetComponentInChildren<HealthData>()` 直接取到子节点里的数据分支。ScriptableObject 没有天然树形。
2. **组件组合**：GameObject 上挂多个 MonoBehaviour（全部是 `[SerializeField]`、无逻辑）就等于"一行多列"。`GetComponent<HealthData>()`。
3. **Scene 内覆写**：Prefab 在 Scene 里的实例可以逐字段修改，形成"全局模板 + 场景定制"；ScriptableObject 没法塞进 Scene。
4. **Prefab Variants**：Unity 2018.3 之后支持的变体机制给数据带来继承关系——"精英怪"是"普通怪"的 variant，只改了血量和贴图。
5. **Nested Prefabs**：数据片段可以作为子 Prefab 被多个母 Prefab 复用。
6. **Prefab 编辑器**：Prefab 可以在不实例化的情况下编辑，内部树结构一目了然。
7. **自带 Transform**：做"刷怪点偏移"这类带位置语义的数据时，Transform 就是天然字段，不用自己定义 `Vector3`。
8. **GetComponent / interface 查询**：数据行为可以走 interface（`WeaponData` 有基础版和进阶版两种实现），`GetComponent<WeaponData>()` 是一次统一访问。

代价仅是 Prefab 运行时会实例化一个空壳 GameObject——作者指出**这些数据 Prefab 其实不会被实例化**，只是被 `LoadPrefabContents` 读出字段，所以成本是额外的序列化开销、而不是额外的 Update 循环。

## 两个踩坑点

1. **编辑器字段选择**：`ScriptableObject` 字段在 Inspector 里会按类型过滤候选；而 `GameObject` 字段会列出场景里所有 GameObject，对 Component 类型字段则直接显示空（只能拖）——可用性略差。
2. **运行时误修改**：Prefab 在运行时若被代码改了字段，改动会悄悄写回磁盘（editor 内）。作者的做法是**把数据 Prefab 当只读**，要么只在加载时读取，要么通过 interface/struct 返回不可变视图。

## 背后的哲学

作者引用 GDC 《A Tale of Two Schemas》的观点：游戏数据常需要两套 schema，一套面向策划（可读、结构化、能加注释），一套面向引擎（扁平、易索引、快序列化）。Prefab 天然适合前者——美术/策划能用 Unity 自带的 Inspector 直接编辑；后者仍然可以在 build 期由代码把 Prefab 转成自定义的运行时结构。

## 和 ScriptableObject 的分工

作者没有全盘否定 ScriptableObject：简单的配置（音量曲线、一个随机表）仍然适合 SO；**数据有层级 / 有组合 / 有继承关系**时才应该切到 Prefab。两者差的也就是"树 vs 表"的抽象能力。

## 相关

- [[unity-asset-refactoring]] — 把这种 Prefab 数据批量演进的工程问题
- [[data-driven-architecture]]
- [[save-load-driven-data-design]] — 同样强调"数据/运行时"的两套表示
- [[gemserk]]

## Sources

- [[sources/gemserk-prefabs-as-data]]
