---
tags: [source, bitsquid, 内容管线, 数据库, 版本控制]
date: 2026-04-19
sources: 1
---

# A New Data Storage Model（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2010 年 8 月的 post，把前面两篇（[[sources/bitsquid-content-repositories-vs-databases]] 与 [[sources/bitsquid-3-way-json-merge]]）的思路推到极致：设计一个**schema 极简的对象数据库**，让 diff / merge / 分支 / offline 全都天然落地。当时没实装（Bitsquid runtime 还是走 JSON 文件），是一份结构化的设计稿。

## 摘要

数据库是一组对象，每个对象有 GUID、由 key-value 组成。值可以是 bool / number / string / data blob / GUID 引用 / GUID set。没有数组，只有 set（若顺序重要，放个 `sort_order` 字段）。所有修改被压缩到 5 种操作：`create / destroy / change_key / add_to_set / remove_from_set`——这套操作**同时是 diff 的表示**，可以本地累积 change list 再批量提交。合并时真冲突只剩"同 key 改成不同值"这一种，用 later-wins 解决。引擎不直接读这套数据；runtime 吃 data compiler 生成的 [[offset-based-resource-blobs|二进制 blob]]；generic 侧这套 schema 只服务编辑器和批处理工具。评论区追问"这不就是 NoSQL"，Frykholm 回答：术语没错，但关键是这些**限制**使冲突可合并——这是普通 NoSQL 后端给不了的属性。

## 关键要点

- 5 种操作：`create / destroy / change_key / add_to_set / remove_from_set`；
- **没有数组**（数组重排的 merge 问题从 schema 层面消掉）；
- GUID 作为唯一身份；根对象 GUID 全零；
- 操作序列即 diff，diff 天然可合并、可 branch、可离线；
- **generic vs runtime 分层**：editor 吃 schema，runtime 吃 compiled blob；
- 编辑器用 C#（反射友好）写，类定义驻编辑器，类自己负责 load/save；
- 真冲突 later-wins。

## 链接到的概念

- [[guid-object-database-schema]]
- [[vcs-vs-database-for-content]]
- [[json-3-way-merge]]
- [[decoupled-tool-engine-json-rpc]]
- [[offset-based-resource-blobs]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2010/08/new-data-storage-model.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2010-08-18_a-new-data-storage-model.md`
