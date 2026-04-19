---
tags: [source, unity, prefab, gameobject, 数据驱动]
date: 2026-04-19
sources: 1
---

# Using Unity Prefabs and GameObjects only for data（Gemserk / Ariel）

[[gemserk]] 2020 年 5 月的主张：在 Unity 存纯数据时，社区默认用 ScriptableObject，但 GameObject + Prefab 其实能提供一套 SO 拿不到的结构能力——作者称这种用法为 Data GameObject。

## 摘要

文章系统列出 Data GameObject 相比 ScriptableObject 的增益：层级组合（子 GameObject = 子数据）、组件组合（多个无逻辑 MonoBehaviour = 行的多字段）、Scene 内逐实例覆写、Prefab Variants（类似"继承"的数据变体）、Nested Prefabs（子数据复用）、可独立打开的 Prefab 编辑器、免费 Transform 做位置数据、`GetComponent` + interface 查询。代价是 Inspector 选择字段时不能按类型过滤、以及运行时若不小心改了 Prefab 字段会写回磁盘。作者引用 GDC 《A Tale of Two Schemas》观点：数据通常需要"面向策划的编辑格式"和"面向引擎的运行时格式"两套 schema，Prefab 适合前者。配套 GitHub demo `DataGameObjectsExample`。

## 关键要点

- ScriptableObject 不能存在 Scene 里，这是 Data GameObject 的主要差异化。
- Prefab Variants（Unity 2018.3+）给数据带来"继承"关系。
- Nested Prefab 让数据片段能复用。
- 用 interface 返回只读视图（`WeaponData { int Damage { get; } }`）可以规避运行时误修改。
- Data GameObject 不一定要实例化——可以只用 `LoadPrefabContents` 读字段，避免空 GameObject 的 Update 开销。

## 链接到的概念

- [[unity-prefabs-as-data]]
- [[data-driven-architecture]]
- [[save-load-driven-data-design]]

## 原文

- 链接：<https://blog.gemserk.com/2020/05/26/using-unity-prefabs-and-gameobjects-only-for-data/>
- 本地：`raw/articles/blog.gemserk.com/2020-05-26_using-unity-prefabs-and-gameobjects-only-for-data.md`
