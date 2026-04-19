---
tags: [unity, prefab, refactoring, editor-tool, 数据演进]
date: 2026-04-19
sources: 1
---

# Unity 资产里的数据结构重构

Unity 项目里大量"数据"是序列化在 Prefab、Scene、ScriptableObject 里的 MonoBehaviour 字段。代码重构有 Rider 这种工具支撑（改类名能同步改 metadata），但**数据结构本身的重构**——字段重命名、类型改变、Component 位置调整——Unity 官方没有现成工具。

[[gemserk]] 把自研的 `unity-refactoring-tools` 的做法整理成了一套可以抄的模板。

## 四步工作法

在数据结构已经有大量内容（上百个 Prefab、几十个 Scene）时改结构，他们固定走这个顺序：

1. **新旧字段共存**：代码里保留老字段，同时加上新字段（新类型、新位置）。
2. **跑自动重构脚本**：脚本读旧字段、写新字段，遍历所有 Prefab 和 Scene，保存回磁盘。
3. **手动把代码切到新字段**：所有引用改走新字段。
4. **删掉旧字段并重新序列化**：移除代码里的旧字段，再跑一次 reserialize，让所有资产去掉残留。

文章聚焦第 2 步的实现。

## 扫 Prefab 的顺序问题

Prefab 的变体（Variant）会继承并覆写父 Prefab 字段，所以**必须先改完所有非 Variant，再改 Variant**，否则 Variant 里被覆写的值会被父级的新值顶掉：

```csharp
prefabs.Sort((a, b) => {
    var aIsVariant = PrefabUtility.IsPartOfVariantPrefab(a);
    var bIsVariant = PrefabUtility.IsPartOfVariantPrefab(b);
    if (!aIsVariant && bIsVariant) return -1;
    if (aIsVariant && !bIsVariant) return 1;
    return a.name.CompareTo(b.name);
});
```

然后用 `PrefabUtility.LoadPrefabContents` / `SaveAsPrefabAsset` / `UnloadPrefabContents` 三段式修改，不要直接操作 asset 实例（否则有引用被别的 Prefab 修改的风险）。

## 扫 Scene

Scene 里存在两种对象：Prefab 实例 和 独立 GameObject。独立的改了直接 dirty；**Prefab 实例只有在字段被 override 时才要改**——默认值靠上一步改 Prefab 时已经生效。作者的代码没显式区分这两种情况（都走 callback），因为大部分情况下 callback 只改 override 字段、不改默认值。跑完一遍 `MarkSceneDirty` + `SaveScene`。

遍历 Scene 时一定要限定 `"Assets"` 根目录，否则 `AssetDatabase.FindAssets("t:scene")` 会把 Packages 里别人家的 Scene 也卷进来。

## 几种典型重构模板

### 字段类型升级：散字段合进结构体

老：`public float speedBaseValue; public float speedIncrementValue;`
新：`public Speed speed { baseValue, incrementValue };`

脚本里读两个老字段组装成 `Speed` 写入 `speed`。跑完一遍之后所有 MonoBehaviour 都有正确的 `speed`，老字段保留一版供回退。

### Component 在层级里上移 / 下移

Unity 没有官方 API 把 Component 从一个 GameObject 搬到另一个。作者的技巧是 **JSON 序列化做搬迁**：

```csharp
var json = JsonUtility.ToJson(srcComponent);
var dstComponent = target.GetComponent<T>() ?? target.AddComponent<T>();
JsonUtility.FromJsonOverwrite(json, dstComponent);
Object.DestroyImmediate(srcComponent);
```

作者承认不确定 `JsonUtility` 能否覆盖所有字段类型，但对"可序列化"的字段（MonoBehaviour 本身的字段就必然是可序列化的）够用。另一个路子是 `SerializedObject`，没展开。

### 处理 Component 间的引用

`ComponentC` 持有对 `ComponentB` 的引用。`ComponentB` 被搬走后 `ComponentC.referenceToB` 会变成旧地址/悬空。作者的做法是**在同一个 callback 里手动修引用**：

```csharp
var componentC = gameObject.GetComponent<ComponentC>();
if (componentC.referenceToB == oldB) componentC.referenceToB = newB;
```

只覆盖"引用在同一 GameObject 内"的情况。跨 GameObject 引用没有自动方案——作者提到 `FindReference` 工具 + 反射可能是未来方向。

### 删 MonoBehaviour 前先清资产

如果直接从代码删掉 `MonoBehaviour` 类，所有用过它的 Prefab / Scene 就剩一个 "Missing Script" 占位符，连是谁都认不出来。良好实践是**先跑一遍 refactor 把 Component 从所有 asset 删掉、再删代码**。

### 纯 Asset（ScriptableObject 等）

比 Prefab 简单：`AssetDatabase.FindAssets("t:{T}")` → 对每个资产跑 callback → `EditorUtility.SetDirty` → 最后 `AssetDatabase.SaveAssets`。没有层级问题。

## 工程经验

- **一次只做一种重构**：多个结构改动搅在一起，出错了根本分不清哪步坏的。
- **准备"edge case"样本**：专门造一些包含复杂 Variant、嵌套 Prefab、跨引用的 Prefab/Scene，跑完用这些样本做人工验证。
- **版本控制兜底**：跑 refactor 前要干净工作区，出错可 `git checkout` 倒回去。
- **遇到"和我没关系的字段也改了"**：通常是之前代码改动没重新序列化，留着旧格式。标准处置是先 reserialize 全库 → commit → 再跑 refactor，这样 diff 只包含 refactor 自己产生的改动。

## 和理想状态的差距

作者指出：代码重构和数据重构还没有自动同步的工具链，**理想形态应该是一条 meta 脚本**：

```
CreateFieldWithNewType() → CopyDataFromOldToNew() → ChangeCodeToNewField() → RemoveOldField()
```

目前这几步都是人工穿插执行。另一个公认的盲区是 Mechanim Animation——动画曲线引用了 property path，MonoBehaviour 改字段名/层级后动画会静默失效，目前没有工具自动修。

## 相关

- [[unity-prefabs-as-data]] — 把 Prefab 当数据存时这个问题更频繁
- [[save-load-driven-data-design]] — 另一种"在数据结构演进时强制保持兼容"的思路
- [[data-driven-architecture]]
- [[gemserk]]

## Sources

- [[sources/gemserk-refactoring-prefab-data]]
