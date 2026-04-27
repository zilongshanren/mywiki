---
tags: [procedural-generation, wfc, csharp, open-source, game-development]
date: 2026-04-27
sources: 1
---

# DeBroglie（WFC C# 库）

DeBroglie 是 [[boris-the-brave]] 开发的开源 C# 库，实现 [[wave-function-collapse]] 算法，并在标准 WFC 之上提供**非局部约束（non-local constraints）**框架。2018 年以 v0.1 发布，此后持续迭代。

## 与标准 WFC 的区别

标准 WFC 只做局部约束传播：每格的候选瓦片集根据相邻格子的选择被逐步缩减。这已足够生成视觉上连续的纹理或随机关卡局部，但无法保证生成结果满足任何**全局性质**——最常见的问题是生成的地图不连通，或某类关键瓦片（入口、出口、宝箱房）出现次数不受控。

DeBroglie 通过引入非局部约束层解决这一问题。约束在每次传播后被调用，可以读写候选域、触发强制坍缩、甚至回溯。内置约束包括：

- **路径约束（Path Constraint）**：强制指定的一组瓦片类型在全图构成连通图，解决了 WFC 生成地图最常见的"孤立区域"问题。
- **计数约束（Count Constraint）**：控制某类瓦片在生成结果中出现的次数区间。
- **Border 约束**：强制边界格子使用指定瓦片集合，方便地图与相邻区域无缝拼接。

这套约束设计让 DeBroglie 成为关卡生成工具链里实用性较高的 WFC 实现，而不仅仅是演示算法的 demo。

## 接口设计

DeBroglie 同时提供 C# API（可嵌入 Unity、Godot 或任何 .NET 项目）和 Windows 命令行工具（接受 JSON 配置文件和 PNG 样本图）。API 层面，用户先构造 `TileModel`（邻接模式或重叠模式）、再配置约束列表，最后调用 `TilePropagator.Run()` 得到结果。结果中每格要么坍缩到单一瓦片，要么处于矛盾状态。

## 相关

- [[wave-function-collapse]]
- [[game-development/driven-wfc]]
- [[game-development/arc-consistency]]
- [[game-development/procedural-dungeon-generation]]

## Sources

- [[sources/boris-debroglie-v01]]
