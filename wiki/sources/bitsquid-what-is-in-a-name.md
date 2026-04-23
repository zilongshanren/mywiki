---
tags: [source, 软件设计, 资源系统, 标识符, bitsquid]
date: 2026-04-19
sources: 1
---

# What Is In a Name?（Niklas Frykholm / Bitsquid）

[[niklas-frykholm]] 2014 年 6 月的文章，系统讨论资源系统里"**资源 A 如何引用资源 B**"这件看似琐碎、实际每条路都暗藏坑的问题。

## 摘要

资源引用有三条基本路：**By Path**（`textures/flowers/rose`）、**By GUID**（`a54abf2e-…`）、**By Name**（人类可读 name 当 id）。Path 最直白但改名就断；补丁方案有两种：**redirect 占位符**（磁盘堆满遗迹、原路径永不回收、多级重定向难判重）和**rename tool**（工具复杂、扫全项目慢、分布式下可能出现改名和新建引用 race 导致 merge 后断引用）。**GUID** 解决改名，但换来一堆新问题：复制文件就冲突、`.png/.wav` 这类标准格式没地方塞 GUID 只能配 `.meta` 侧文件（同步 bug）、代码里写 GUID 完全不可读、断引用时连"原本指什么"都不知道、localization/platform override（Bitsquid 的 `rose.fr.dds`）得另建体系。**By Name** 没有相对 Path 的实质优势——改 name 一样断，还引入"文件名≠资源名"二重标识。**Path + GUID 双写**看着两全实际是复杂度叠加：仍要 rename tool 同步 path 字段、仍要处理 GUID 冲突、仍要设计 localization，**"更复杂但也不完美"最糟**。Bitsquid 最终选**纯 path + Dependency Checker 改名工具**：已有工具、边际成本最小。结论：资源引用没有银弹，**复杂度不在"如何存 id"而在"如何维护 id 关系图"**——rename tool、duplicate finder、reference cache、dependency checker 必须跟上。

## 关键要点

- 三条路：By Path / By GUID / By Name，每条都有暗角
- **Path 的补丁**：redirect 遗迹（磁盘污染、路径永占用）和 rename tool（工具复杂、慢、分布式 race）
- **GUID 的代价**：文件复制 = 冲突；`.png` 等标准格式需 `.meta` 侧文件；不可读调试；断引用无上下文
- **By Name 没有独立价值**：改 name 等同改 path 的问题，还引入二重标识
- **Path + GUID 双写**：复杂度叠加而不是两全——"更复杂但也不完美"最糟
- **Bitsquid 选 path-based**：因为已有 [[dependency-checker-tool|Dependency Checker]]，边际成本最小
- 嵌套资源（`Common/UI.strings#Cancel` 这种 URL 风格）对两种方案都是难题

## 链接到的概念

- [[resource-reference-path-vs-guid-vs-name]]
- [[strings-as-identifiers-antipattern]]
- [[identity-problem-naming]]
- [[dependency-checker-tool]]
- [[cheat-by-solving-less]]

## 原文

- 链接：https://bitsquid.blogspot.com/2014/06/what-is-in-name.html
- 本地：`raw/articles/bitsquid.blogspot.com/2014-06-18_what-is-in-a-name.md`
