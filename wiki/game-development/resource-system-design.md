---
tags: [游戏开发, unity, 深模块, aposd]
date: 2026-04-05
sources: 1
---

# 资源系统设计

游戏引擎的资源系统是 [[information-hiding|信息隐藏]] vs [[false-abstraction|虚假抽象]] 的战场。

## 典型浅模块问题

```csharp
// 调用者需要知道：
// 1. 引用计数的存在
// 2. 需要手动 Retain
// 3. 使用完要手动 Release
// 4. 不 Release 会内存泄漏
// 5. Release 过多会 crash

ResourceHandle handle = ResourceManager.Load("bullet");
handle.Retain();           // 必须手动 retain
// ... 使用 handle ...
handle.Release();          // 必须手动 release
```

这是 [[java-io|Java I/O]] 的同种病——把资源管理的复杂性推给调用者。

## 虚假抽象的版本

```csharp
// 看起来简单
GameObject obj = ResourceManager.Load("prefabs/bullet");
```

但调用者需要知道：生命周期谁管？引用计数还是 GC？场景切换会不会被卸载？如果这些信息在接口里看不到，就是 [[false-abstraction|虚假抽象]]——简单的外表下是一个定时炸弹。

## 深的资源系统

**RAII 风格**：

```csharp
using (var bullet = ResourceManager.Load<GameObject>("bullet"))
{
    // 用 bullet ...
} // 自动 Release
```

**或更彻底**：用 Unity 的 Addressables 系统。资源的加载、缓存、卸载全部由系统管理，调用者只需要一个 `AssetReference`。

## 核心原则

资源包格式（AssetBundle、ScriptableObject、JSON）这份知识应该只存在于加载器里。上层只管「我要一个 Prefab」。

参见 [[information-leakage]] 对资源系统高危区的讨论。

## 相关

- [[information-hiding]]
- [[information-leakage]]
- [[false-abstraction]]
- [[deep-modules]]

## Sources

- [[sources/aposd-day04]]
