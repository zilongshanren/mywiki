---
tags: [ue, unreal, 蓝图, 验证, 资产, 工具]
date: 2026-04-19
sources: 1
---

# UE Blueprint Asset Validator：怎么验证蓝图的组件设置

Unreal 的 **Asset Validator** 系统允许项目写一组规则在 editor 里自动校验资产——贴图大小、三角形数、命名约定。它可以用 C++ 也可以直接在蓝图里写，贴合项目需求。[[thomas-poulet]] 在 [[sources/thomas-poulet-blueprint-validation|这篇文章]]里记下了一个被客户问到的案例：**怎么验证「一个蓝图派生类的组件上是否正确打了 tag」？** 过程有两处不直观的坑。

## 场景

有一个蓝图 `GizmoBase`。派生出 `GizmoFoo` / `GizmoBar`，每个派生类里手工加一个 component。规则：必须给这个 component 打上某个 tag。**从第二个派生类开始一定会有人忘**，然后 bug 到上线后都还在抓。

写个验证器自动检查不就行？思路对，但天真实现会踩坑。

## 坑 1：Blueprint 的输入不是你的 class

验证器的 `CanValidateAsset` 里拿到的 asset，**不是你的 `GizmoFoo` 实例，而是一个 `Blueprint` 类型的对象**—— 是那个蓝图资产本身。直接 `Cast<GizmoFoo>(asset)` 恒 fail。

正确做法：拿 `Blueprint` 的 **GeneratedClass**，和你期望的类型做比对（比较 class，不比较 instance）。

## 坑 2：蓝图不是「实例化的 actor」，是「生成配方」

过 validate 之后，要实际检查组件——但蓝图对象存的不是已经实例化的组件树，而是**生成配方**（一个描述「该这么实例化」的数据结构）。C++ 类可以直接读类的 component 属性；蓝图不行。

解法：用 **Subobject Data Subsystem**。这套子系统能遍历蓝图配方里的每一个 subobject handle，逐个 cast 到预期的 component 类型，然后检查属性（例如：tag 是否打上、render target 是否 assign 了）。

注意 Poulet 提到的一个细节：**这个遍历有时会多次回到同一个 component**。如果你的校验会有副作用（计数、push 到数组），要自己维护一个 *已见集合* 去重。

## 一个可复用的校验模板

```
CanValidateSetup(asset):
    BP = Cast<Blueprint>(asset)
    return BP.GeneratedClass->IsChildOf(ExpectedType)

ValidateLoadedAsset(asset):
    handles = SubobjectDataSubsystem::GatherSubobjectHandles(asset)
    seen = {}
    for handle in handles:
        if handle in seen: continue
        seen.add(handle)
        comp = Cast<ExpectedComponent>(handle)
        if not comp: continue
        if not comp.HasTag(requiredTag):
            ReportError("missing tag", comp)
        # 其他字段检查...
```

## 启示

- **蓝图资产的内部结构和 C++ 类型不一样**——它是一个「递归配方」。所有通用的 reflection/inspection 代码都必须走 Subobject Data Subsystem。
- **验证器最好写错误信息**：Poulet 的最后一条建议——给内容团队说清楚「哪个 component、缺了什么」，而不是只抛 bool。
- 相关：[[unreal-insights-counters-traces]] 做性能侧的检查，这篇做内容结构侧。一起构成项目「CI 级」的内容质量门。

## Sources

- [[sources/thomas-poulet-blueprint-validation]]
