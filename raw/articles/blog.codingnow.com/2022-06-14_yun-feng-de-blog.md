---
title: 云风的 BLOG
url: https://blog.codingnow.com/2022/06/
published: '2022-06-14'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### 给 ECS 增加分组功能

目前，我们用 ECS 管理游戏引擎中的对象。当游戏场景大到一定程度，就需要有一个机制来快速筛选出需要渲染的对象子集。换句话说，如果你创建了 100K 个 Entity ，但是只有 1K 个 Entity 需要同时渲染，虽然遍历所有可渲染对象的成本最小是 O(n) ，但这个 n 是 100K 这个数量级，还是 1K 这个数量级，区别还是很大的。

我们的 ECS 系统已经支持了 tag 这个特性，可以利用 visible tag 做主 key 快速筛选可见对象。但当镜头移动时，需要重置这些 tag 又可能有性能问题。重置这些 visible tags 怎样才能避免在 100K 这个数量级的 O(n) 复杂度下工作？

一个容易想到的方案是给 Entity 分组。比如在超大规模的场景下，我们可以按区块来分组。根据镜头所在的位置，可以快速的确定哪些 group 是关心的，哪些不必关心。

我首先想到的是用多个 world 来描述整个场景。每个 world 是一个 group ，按地理位置存放 Entity 。但这有明显的问题：渲染的有些环节是唯一的，比如 PreZ 阶段生成 Z Buffer 、后处理阶段处理屏幕空间的效果，这些需要多个分组一起处理。

所以，我还是倾向于给 Entity 加一个 group id 来区分它们。

如果把 ECS 看成是一个内存数据库，那么，我们的需求是 where 字句的查询功能。可以快速的筛选出 group id 属于某个集合的 Entity 。筛选合乎要求的所有 Entity 的成本应该是这类 Entity 的数量级，而不是 world 中所有 Entity 的数量级。

只有这样，才适合做大规模的场景，扩大场景对象数量的规模不影响渲染性能。

我希望这样一个分组功能相对已有的 ECS 特性是非侵入的，它最好不要修改已有的数据结构。在不使用分组功能时（小场景），不要影响基本功能。基于此，我设计了这样一个数据结构：

每个 Entity 可选一个（或多个） group 索引结构。group id 只能在创建 Entity 时赋予，并不可修改。我们在构建过程通过 group id 来维护这个索引结构。

该索引结构有四个字段：

uint64_t uid; uint64_t lastid; uint32_t groupid; uint32_t next;

其中，uid 是 64bit 自增 id ，每个 entity 在创建时被赋予唯一 id ；groupid 是它所属的分组号；lastid 用于索引同组的前一个对象的 uid ，next 则用于快速定位前一个同组对象。

这个索引结构就是一个普通的 component ，实际存放在一个连续的数组中。因为 Entity 只能在创建那一刻赋予唯一 uid ，而 uid 又是单调递增的。所以，这个索引结构的内容的 uid 字段是严格有序递增的。

在这个索引结构中，依靠 uid / lastid 便可以按 groupid 自然分成若干组。而 next 字段描述的是同组的前一个对象在这个索引结构数组中的相对偏移量。

当 Entity 没有删除时，next 形成了链表，可以快速的遍历所有同组对象，而 lastid 可以用于双重校验。

一旦 Entity 删除，我们不必立刻更新这个链表。在下次遍历时，next 会指向错误的位置，但通过 lastid 可以快速修复链表（因为正确的同组对象所在的位置就在附近）。

利用这个索引结构，我们可以快速的遍历出同组的 Entity ，并打上 tag 。之后，就可以利用 tag 来正常检索了。对于大世界场景，我们按地图区块分好 group ，再利用镜头所在位置，快速计算出附近有哪几个 group 需要渲染，就可以快速生成 visible tags 。

除了用于维护 visible tags ，这个分组功能还可以用于快速删除不必保存在内存中的 Entity 。只要根据 groupid 删选出来再批量删除即可。

以上的工作在 [这个 commit](https://github.com/cloudwu/luaecs/commit/c11e95df359644c8cee64084006014ffd070caa2) 中体现。