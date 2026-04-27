---
tags: [source, game-engines, unity, guid, asset-management, meta-file]
date: 2026-04-27
sources: 1
---

# Messing with Unity's GUIDs（Boris The Brave）

[[boris-the-brave]] 发表于 2020 年 2 月的文章，解析 Unity 内部资产引用系统（GUID + fileID），并介绍在 .dll → 源码升级时保持引用不断裂的技巧。

## 摘要

Boris 发布了 Tessera（功能裁剪版 .dll）和 Tessera Pro（含源码完整版）两款 Asset Store 插件，发现用户从 Tessera 升级到 Tessera Pro 后所有场景引用全部断裂。文章深入解释了 Unity 资产引用的内部结构：每个文件由 `.meta` 文件记录一个随机 GUID；场景/Prefab 中的引用用 `{guid, fileID}` 对表示，GUID 指向文件，fileID 指向文件内的具体对象。fileID 的计算规则在 MonoBehaviour 脚本和 .dll 之间不同：脚本中固定为 `11500000`，.dll 中则是类名的 32 位哈希值，因此无论如何修改 meta 文件都无法同时修复两者的 fileID。解决方案是创建一个"哑元"类 `Dummy_296730116`——名字经暴力碰撞搜索确定，使其哈希值与原 `TesseraTile` 类相同——从而让旧引用落到哑元类上，再通过自定义 Inspector 提示用户手动迁移。

## 关键要点

- Unity 资产引用 = `{guid（指向文件的 meta）, fileID（文件内对象标识）}`
- 90% 的引用断裂源于 meta 文件丢失或重新生成（导致 guid 变化）
- MonoBehaviour 在 .cs 文件中的 fileID 固定为 `11500000`；在 .dll 中 fileID = 类名哈希（32 位整数）
- .dll → .cs 升级时，guid 可通过编辑 meta 修复，但 fileID 不同步，无法完美兼容
- 暴力碰撞搜索 32 位 fileID 在个人 PC 上约需 9 分钟，可找到特定哈希值的类名
- 哑元类保留原属性可防止 Unity 清除数据，配合 Custom Editor 输出迁移警告

## 链接到的概念

- [[unity-asset-refactoring]]
- [[unity-complexity-patterns]]

## 原文

- 链接：https://www.boristhebrave.com/2020/02/05/messing-with-unitys-guids/
- 本地：`raw/articles/boristhebrave.com/2020-02-05_messing-with-unitys-guids.md`
