---
tags: [source, bitsquid, 工具链, undo, copy-paste, 数据模型]
date: 2026-04-19
sources: 1
---

# Universal Undo, Copy and Paste（Niklas Frykholm / bitsquid blog）

[[niklas-frykholm|Niklas Frykholm]] 2011 年 4 月的延伸文：在前作（[[sources/bitsquid-collaboration-and-merging|Collaboration and Merging]]）的 objects-with-properties schema 之上，**Undo / Copy / Paste 几乎免费得到**。

## 摘要

继续接 [[guid-object-database-schema|GUID 对象数据库]] 的讨论：5 种原子操作（`create / destroy / set_property / add_to_set / remove_from_set`）足以表达该模型下的一切修改，而每个操作**都有显式的逆**——`create ↔ destroy`、`add_to_set ↔ remove_from_set`、`set_property` 的逆是把值改回旧值。Undo 就是每次变更把逆操作压栈；撤销时弹出执行；再把"它的逆"压入 redo 栈。用户级"一次撤销"通常对应多次底层 op，用**空闲时在栈里放 restore point** 的方式分段。Copy 的做法是把选中对象（与它们通过 GUID 引用的对象）一起导出到一个**临时 database**，序列化到 clipboard。Paste 反向：反序列化成临时 DB，**把所有 GUID 重命名一遍**（防止与现有对象撞 id），再把所有 property 里的 GUID 引用按 old→new 的 map 翻译，最后 merge 进主 database。因为这些都建在**底层数据模型**上，所有使用该 DB 的编辑器**自动获得** Undo / Copy / Paste / Save / Load 等功能——添加新 feature 不用每次各写一份。文章评论里还提到一个开放问题：**"owns" 还是 "uses"**——copy 一个压力板对象，它引用的门应不应该一起被复制？Frykholm 当时 DB 层不做区分，留给 semantic 层决定；但承认把这个区分下沉到 DB 层可能是更彻底的做法。

## 关键要点

- **Undo = 记录逆操作并压栈**：5 种原子操作每种都有显式的逆；
- **restore point**：空闲时在 undo 栈里放分段标记，让用户级的"一次 Ctrl+Z"对应多次底层 op；
- **Copy = 子图序列化**：把目标对象及其可达闭包导出成临时 DB，丢到 clipboard；
- **Paste = rename GUIDs + 翻译引用 + merge**：把所有 GUID 重映射，避免与主 DB 撞 id；
- **在底层数据模型上做这些**意味着**所有编辑器免费获得**这些功能，而不是每次 feature 单独实现一份；
- **owns vs uses 引用** 是未决的设计点：是否 copy 压力板时把门一起 copy——2011 年 Frykholm 留给 semantic 层；
- **实战反馈**：写作时 Bitsquid 的 sound editor 已经完整跑在这套 schema 上，Frykholm 评"每加一个 feature 都自动获得 Undo / Copy / Paste / Save / Load"。

## 链接到的概念

- [[guid-object-database-schema]]
- [[sources/bitsquid-collaboration-and-merging]]
- [[json-3-way-merge]]
- [[niklas-frykholm]]

## 原文

- 链接：https://bitsquid.blogspot.com/2011/04/universal-undo-copy-and-paste.html
- 本地：`raw/articles/bitsquid.blogspot.com/2011-04-26_universal-undo-copy-and-paste.md`
