---
tags: [source, 引擎架构, 资源系统, 本地化, stingray, bitsquid]
date: 2026-04-19
sources: 1
---

# A New Localization System for Stingray（Niklas Frykholm / bitsquid 博客）

[[niklas-frykholm]] 发表于 2016-09-06 的博客，讲 Stingray 怎么把旧的"文件名点号 = property"方案换成 **resource override + suffix 规则**组合。

## 摘要

Stingray 原本用文件名点号片段（`trees/larch_03.fr.unit`、`trees/larch_03.ps4.unit`）作为平台/语言 property，platform property 编译期解析，其他 property 由脚本 preference order 在加载时解析。这套用了很多年，但有四个硬伤：文件名不能带 `.`、切语言要重载包、只分平台不够细、编辑器处理 property 极其复杂。

Niklas 做的重写分三层：第一层给字符串、声音等"天然本地化"资源做深度集成，`.strings` 直接变多语种 map，`Localizer.set_language("fr")` 即时切换；第二层用通用 `set_resource_override` 替换文件名魔法，运行时动态替换任意资源；第三层为了让 packaging 系统看见替换关系，加一张静态 `resource_overrides` 表，按 `suffix + platforms/flags` 匹配，flag 可以在编译期静态解析（`--resource-flag-true 4K`）或运行时动态解析（`--resource-flag-runtime noblood`）。

## 关键要点

- 旧 property 系统的四个痛点里"文件名不能带点"是改造的最大动因——外部工具生成带 `.` 的文件名频频造成崩溃。
- `set_resource_override` 不保证语义一致：override 的替身如果缺了脚本预期的节点，只能靠游戏层自己保证。
- packaging 看不见运行时 override，所以静态 override 表仍是必须的。
- 后缀规则能配置成 `.fr` / `.ps4`，向后兼容旧 property 命名。
- Niklas 自述："name matching 让我略有不适，但规则由用户显式控制，这个折中可接受。"——典型的工程取舍。

## 链接到的概念

- [[stingray-resource-override-suffix]]
- [[stingray-package-manager]]
- [[stingray-data-driven-render-config]]

## 原文

- 链接：https://bitsquid.blogspot.com/2016/09/a-new-localization-system-for-stingray.html
- 本地：`raw/articles/bitsquid.blogspot.com/2016-09-06_a-new-localization-system-for-stingray.md`
