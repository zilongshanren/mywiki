---
tags: [unity, guid, fileid, asset-management, meta-file, serialization]
date: 2026-04-27
sources: 1
---

# Unity 的 GUID / fileID 资产引用系统

Unity 用一对标识符 `{guid, fileID}` 来表示场景和 Prefab 中的所有跨文件引用。理解这套系统是处理 Unity 资产迁移、重构插件包、以及排查"Missing Script"错误的前提。

## 基本结构

打开任何 Unity 场景文件，都能看到类似这样的引用：

```
{fileID: 11500000, guid: e3ad2bf01b7a6b7409eb683402aa8668, type: 3}
```

- **guid**：指向目标文件。Unity 为每个项目文件生成一个随机 UUID 写入配套的 `.meta` 文件（`MyFile.cs` → `MyFile.cs.meta`）。
- **fileID**：指向文件内的具体对象。

## fileID 的生成规则

fileID 的计算规则因引用类型不同而分叉，这是最容易踩坑的地方：

| 引用类型 | guid | fileID |
|---------|------|--------|
| 场景内本地引用 | 无 | 来自对象名称的哈希 |
| .dll 中的 MonoBehaviour | .dll 的 guid | 来自类名的哈希（32 位整数） |
| .cs 脚本中的 MonoBehaviour | .cs 的 guid | **固定为 11500000** |

这个不对称性是 .dll → 源码升级时引用不可能无缝兼容的根本原因：guid 可以通过修改 meta 文件来对齐，但 fileID 从 .dll 的哈希值（依类名）变成了固定常数 `11500000`，两者无法同时满足。

## 典型问题场景

Unity Asset Store 插件常见的发行模式是同一套代码发布"Lite 版（.dll）"和"Pro 版（源码）"。用户升级时，场景里所有对 .dll 中 MonoBehaviour 的引用都会因 fileID 变化而断裂，Inspector 显示"Missing Script"。

正确修复 guid 并不够，因为 fileID 的不兼容是结构性的，没有官方提供的迁移路径。

## 哑元类碰撞法

一种变通方案：创建一个"哑元"类，让它具有与旧引用完全相同的 guid 和 fileID，从而"接住"旧引用而不产生 Missing Script 错误。

- **guid**：在 .dll 的 meta 文件中直接设置，或在新 .dll/源码文件的 meta 中写相同值
- **fileID**：.dll 中的 fileID 是 32 位哈希，暴力搜索类名直到碰撞：9 分钟可在普通 PC 上找到目标哈希对应的类名

哑元类保留原类的全部属性字段（防止 Unity 清除序列化数据），并配合 Custom Editor 在 Inspector 中显示迁移提示。这是一种"优雅降级"而非真正兼容——用户仍需手动完成最终迁移，但不会丢失数据。

## 实践建议

- 用 Unity Project 标签页做文件操作（移动、重命名），让编辑器自动维护 meta 文件，避免 guid 失效
- 跨版本发行 .dll + 源码双轨插件时，提前规划好 guid 策略；fileID 不兼容是无解的结构限制
- [PlayMaker 迁移文档](https://hutonggames.fogbugz.com/default.asp?W1254) 是处理 Unity 引用更新的良好参考
- fileID 哈希算法细节见 Robin Ryf 的博文（robinryf.com/blog/2017/10/30/unity-behaviour-in-dlls.html）

## 相关

- [[unity-complexity-patterns]]
- [[unity-prefabs-as-data]]
- [[asset-exchange-format-strategy]]

## Sources

- [[sources/boris-unity-guids]]
