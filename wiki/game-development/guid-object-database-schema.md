---
tags: [工具链, 内容管线, 版本控制, 数据库, bitsquid]
date: 2026-04-19
sources: 1
---

# GUID 对象数据库 schema

2010 年 Frykholm 给自己的内容管线草了一个 schema：不是传统关系数据库，也不是纯文件 JSON，而是一种**极简的对象-键值存储**，目标是让 diff / merge / 分支 / 离线工作全部天然落地。这篇设计稿在 Bitsquid 当时没有上线，但思路和后来 Our Machinery / The Machinery 的 Truth database、甚至 Unity ScriptableObject / Unreal Package 的引用模型都有同样味道。

这是 [[vcs-vs-database-for-content|"VCS vs 数据库"]] 与 [[json-3-way-merge|3-way JSON merge]] 这条线的收束。

## Schema 本身

数据库是一组对象：

- 每个对象用 **GUID** 唯一标识；
- 对象由**字符串键 → 值**的集合组成；
- 值可以是：`null`（等同于 key 不存在）/ `bool` / 数字 / 字符串 / **数据 blob**（贴图、顶点数据）/ **另一个对象的 GUID 引用** / **一组 GUID 引用（set）**；
- 特殊的根对象 GUID 为全零，作为 database 的入口点。

就这么点东西。没有类型系统、没有 schema 校验、没有数组——**只有 set**。

## 为什么砍掉数组

数组重排序的 merge 是出了名的难（对应 [[json-3-way-merge]] 里那段讨论）。Frykholm 直接一刀砍掉：数据库里只有 set，没有 array。如果某个场景里对象顺序确实重要（比如 GUI 层级），就在每个对象里放一个 `sort_order` 字段，查询时按它排——用**显式可合并字段**代替了"顺序这个隐式语义"。

## 5 种原子操作

所有对数据库的修改被压缩到 5 种操作：

```
create(guid)
destroy(guid)
change_key(guid, key, value)
add_to_set(guid, key, object_guid)
remove_from_set(guid, key, object_guid)
```

这套操作集**同时是 diff 的表示**——两个版本之间的差异就是一串这样的操作。由此 VCS、online/offline 协作、branch 都直接成立：

- 本地 change list：用户积累一串 op，想提交时批量 apply 到中央库；
- 在线协作：op 作为 message 广播，相当于多人在同一份数据上做 CRDT 风格的编辑；
- 冲突定义被压缩到**同一 key 同时被改成不同值**——其他所有"修改"都可以自动合并。最后这一处真冲突 Frykholm 用 "later wins" 解决。

## 和引擎的关系：generic vs runtime 分层

评论区追问"这样的数据库怎么给 C++ 引擎跑"——Frykholm 答得很明白：这套 schema 是给**生产侧**用的（编辑器、导出器），**不是给 runtime 的**。

- runtime 吃 [[offset-based-resource-blobs|紧凑二进制 blob]]，从 data compiler 生成出来，直接 mmap 上 struct；
- generic 侧是这套 GUID 数据库——键是字符串，方便加字段、向后兼容、被工具批处理（比如"扫所有 texture，找出非 POT 尺寸的"一句脚本搞定）；
- 编辑器用反射友好的语言写（C#），类定义在编辑器里，存取数据时从数据库 load/save 各自的字段。runtime 不需要生成 struct。

这个分层和 [[decoupled-tool-engine-json-rpc|Bitsquid 工具架构]] 里 generic/runtime 的切分完全一致，是整个管线的同一根骨头。

## 和 NoSQL 的关系

评论里有人指出这就是 NoSQL。Frykholm 同意术语，但反过来强调：**关键不是"用 NoSQL"**，关键是**这些限制**（只有 set、key 是 string、只有 5 种操作）让数据库**可以被无冲突地 diff 和 merge**——这是一个普通 NoSQL 引擎给不了的属性。可以用 Tokyo Cabinet 之类的做后端存储，但 schema 本身比后端更重要。

## 相关

- [[vcs-vs-database-for-content]]
- [[json-3-way-merge]]
- [[decoupled-tool-engine-json-rpc]]
- [[offset-based-resource-blobs]]
- [[c-serialization-metadata]]
- [[niklas-frykholm]]

## Sources

- [[sources/bitsquid-new-data-storage-model]]
