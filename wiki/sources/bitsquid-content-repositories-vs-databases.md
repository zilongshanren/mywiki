---
tags: [source, bitsquid, 工具链, 内容管线, 版本控制]
date: 2026-04-19
sources: 1
---

# Content Repositories and Databases（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2010 年 1 月的一篇短文，对比"游戏内容放 VCS 还是放数据库"。

## 摘要

数据库对协作编辑和即时可见有天然优势，但放弃历史、分支、本地副本是 Frykholm 不接受的代价。他选择继续用 VCS，但准备写一个 **JSON-aware 3-way merger** 来消除 merge conflict——Bitsquid 的数据基本都是 JSON 结构，只要字段合并粒度够细，冲突极其少见。评论里 Criterion 的同行分享了 Burnout Paradise 在 SQL 上重写 Perforce 的经历，referential integrity 给得好，但 Frykholm 的反驳是"在数据库上重造 VCS，和在 VCS 上重造数据库一样糟糕"。

## 关键要点

- VCS 路线的不可替代点：**历史 / 分支 / 本地工作副本**；
- DB 路线的诱惑：**即时同步 / 无 merge conflict / 多人编辑同一关卡**；
- Bitsquid 的折中：JSON 存储 + 3-way merger + editor 触发 `svn update/commit` 模拟即时性；
- Referential integrity 可以通过 **GUID + 引用扫描 / mark-and-sweep GC** 在 VCS 里补；
- Frykholm 草拟了一个"VCS-数据库混合"的 schema：GUID + property map + 三种操作（create/destroy/change）。

## 链接到的概念

- [[vcs-vs-database-for-content]]
- [[decoupled-tool-engine-json-rpc]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2010/01/content-repositories-and-databases.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2010-01-19_content-repositories-and-databases.md`
