---
tags: [source, bitsquid, 版本控制, 内容管线, 工具链]
date: 2026-04-19
sources: 1
---

# Avoiding Content Locks and Conflicts — 3-way JSON Merge（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2010 年 6 月的 post，兑现他在 [[sources/bitsquid-content-repositories-vs-databases|"Content Repositories and Databases"]] 里开的 todo：写一个理解 JSON 结构的三路合并器，让 Bitsquid 的内容继续留在 VCS 里也不吃 merge 冲突的苦。

## 摘要

关卡设计师不该在 WinMerge 里读 XML/JSON；大部分所谓 "content conflict" 其实是行级合并器不懂层级结构搞出来的假冲突。Frykholm 写了一个**结构化**三路合并器：把 JSON object 的 diff 表达成 `object[key] = value` 操作序列（新增 = null→value，删除 = value→null），三路合并就是把两边的 op 集合合并；真冲突（同 key 两边改成不同值）用 `always pick right` 处理，关卡设计师在**关卡编辑器**里再修。数组用 `id`（GUID）字段来消歧——有 id 的数组能精确区分 update/delete+insert，无 id 的走启发式。代码最初放在 bitsquid.se 公共域下载，后来迁到 bitbucket。

## 关键要点

- **问题本质**：行级合并器不懂 JSON 层级，制造假冲突；
- **真冲突极少**：两个人很少真的同时修改同一字段到不同值；
- object 合并：diff = key-value 操作序列，union 即 merge；
- 真冲突策略：**picks right**，不弹对话框，交由专业工具（关卡编辑器）善后；
- **数组靠 `id` 字段消歧**，推荐所有 authored 数组都带 GUID id；
- 公共域代码，鼓励任何人拿去改。

## 链接到的概念

- [[json-3-way-merge]]
- [[vcs-vs-database-for-content]]
- [[guid-object-database-schema]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2010/06/avoiding-content-locks-and-conflicts-3.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2010-06-03_avoiding-content-locks-and-conflicts-3-way-json-merge.md`
