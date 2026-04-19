---
tags: [source, unity, prefab, refactoring, editor-tool]
date: 2026-04-19
sources: 1
---

# Refactoring Data stored in Unity Prefabs, Scenes and other Assets（Gemserk / Ariel）

[[gemserk]] 2022 年 4 月的长文：如何在项目已有大量内容时安全地修改 Unity 中 MonoBehaviour 的字段结构。配套仓库 `unity-refactoring-tools`。

## 摘要

作者提出四步法：1) 新旧字段并存；2) 跑批量脚本把老字段值写到新字段，遍历所有 Prefab 和 Scene；3) 代码改到新字段；4) 删老字段 + reserialize。文章主要讲第 2 步的实现模板 `RefactorTools.RefactorMonoBehaviour<T>`：先 `AssetDatabase.FindAssets("t:prefab")` 找出包含 T 的 Prefab，**按"非 Variant 在前、Variant 在后"排序**后用 `LoadPrefabContents` / callback / `SaveAsPrefabAsset` 三段式改写；再按 `"Assets"` 目录限定找 Scene，`OpenScene` → 遍历 root GameObject 的所有 T 组件跑 callback → `MarkSceneDirty` + `SaveScene`。给了四种重构模板：字段类型升级（散字段合进结构体）、Component 上移/下移父子（用 `JsonUtility.ToJson` + `FromJsonOverwrite` 搬迁）、处理 Component 间引用的手工修复、删 MonoBehaviour 前先清资产。最后提到两个空白：代码重构和数据重构没有自动联动工具、Mechanim Animation 的 property path 引用无法自动修。

## 关键要点

- 改 Variant 前必须先改完所有非 Variant Prefab，否则 override 会被覆盖。
- `PrefabUtility.LoadPrefabContents` 的三段式是唯一稳妥的 Prefab 改写方式。
- `JsonUtility.ToJson` + `FromJsonOverwrite` 可以当作"搬 Component"的兜底办法。
- `AssetDatabase.FindAssets("t:scene")` 要限定 `"Assets"` 目录，避免卷进 Packages 下的 Scene。
- 删 MonoBehaviour 类前先跑 refactor 把组件从 asset 里删掉，否则会留 Missing Script。
- 一次只跑一种重构，保持 git 工作区干净便于回退。
- 跨 GameObject 的 Component 引用没有自动方案，作者提到 `FindReference` 工具 + 反射是可能方向。

## 链接到的概念

- [[unity-asset-refactoring]]
- [[unity-prefabs-as-data]]

## 原文

- 链接：<https://blog.gemserk.com/2022/04/24/refactoring-prefabs-and-unity-objects/>
- 本地：`raw/articles/blog.gemserk.com/2022-04-24_refactoring-data-stored-in-unity-prefabs-scenes-and-other-as.md`
