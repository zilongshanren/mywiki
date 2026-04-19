---
tags: [数据结构, 软件设计, 不变量]
date: 2026-04-14
sources: 1
---

# 数据结构不变量

「不变量」（invariant）是一组必须在每一步前后都成立的条件。教科书把它教给算法——循环不变量、二分搜索不变量——但到了实际的数据结构代码里，大多数程序员早就忘光了。[[fabian-giesen|Fabian "ryg" Giesen]] 2010 年这篇写得非常清醒：**不变量是「一份数据通过多条路径被访问」时必然诞生的东西，而不是写算法时才用的形式主义**。一个数据结构有几条独立的「视图」通向同一份内容，就有几条必须同步维护的不变量。

## 从单链表看不变量的诞生

**例 1：裸单链表**。`head` 指针 + 每个节点的 `next`。没有不变量——任何一个 `head` 值都合法，空链表写成 `head = NULL`。`head = head->next` 就可以删头节点；`AddAtFront` 两行写完。很自然，因为「链表是什么」和「怎么遍历它」是同一条路径。

**例 2a：带 tail 指针的单链表**。为了让 `AddAtBack` 变成 O(1)，加上 `tail` 字段。这一加，就**凭空产生了一个不变量**——`head` 和 `tail` 必须相互一致：

```
(!head && !tail) ∨ (head && IsInList(tail) && !tail->next)
```

所有读 `tail` 的地方都在读缓存值（`tail` 在原则上可以从 `head` O(n) 重算）；所有写都必须同时更新两处。`RemoveFirst` 突然要判「是不是最后一个了」；`AddAtFront` 要判「之前是不是空的」；四个函数里每个都长出了 special-case。**增加一条读路径的代价是增加所有写路径的复杂度**——这就是 [[change-amplification|改动放大]] 的经典形态。

**例 2b：tail pointer-to-pointer**。ryg 给出的清理方案：不存 `tail` 指针，存 `ListNode **tailNext`——即「当前最后一个元素的 `next` 字段地址」。空链表时 `tailNext = &head` 本身就合法，空/非空的分叉消失了。新不变量变成：

```
IsValidNext(tailNext) && *tailNext == NULL
```

代码短了，special case 少了。这是一个很典型的设计直觉：**如果不变量里有大量 special case，往往说明数据结构的状态空间里有空洞**——改造数据表示把空洞填上，不变量和代码会一起变简洁。双重指针在 C 里的链表操作（删除、拼接、insert after）是一条根本技巧。

## 双向链表：sentinel 消除边界

**例 3a：裸双向链表**（`head`、`tail`、每节点 `prev`/`next`）的不变量大得多：空链表的特判、`head->prev == NULL`、`tail->next == NULL`、以及**每个节点的** `x->next->prev == x`。任何插入/删除都要在首尾和中间区分写法——写对过 doubly-linked list 的都知道那有多烦。

**例 3b：带 sentinel 的循环双向链表**。引入一个「哨兵」节点作为链表的 owner，初始时 `sentinel.next = sentinel.prev = &sentinel`。空链表在这个表示下**仍然有一个节点**（sentinel 本身），所以 `head == NULL` 的分支彻底消失。剩下的不变量干净到只有一条：

```
∀ x: x->next->prev == x
```

`InsertAfter`、`Remove` 都是 4 行无分支代码。和 tail pointer-to-pointer 一样，这是**让状态空间正则化后不变量变简单**的另一个例子。代价是需要给每个链表 own 一个 sentinel 的存储位置——ryg 在评论区里也顺手回答了这个代价：sentinel 不能被按值返回 / 移动，它的地址必须稳定。

## 更一般的教训

ryg 提出的设计直觉简单但深刻：

- **每多一条访问路径，就多一条不变量**。binary tree 有 left/right 没问题；加上 parent 就有 `x->left->parent == x`；加上 BST key 就有左子树 < x < 右子树；AVL 再加高度差不超过 1。每层都让写路径更重，到 AVL / 红黑树已经是 rotation 教科书地狱。
- **不变量可以延迟修复**。如果有一大段代码只用 next 不用 prev，你完全可以在这段代码内部把 prev 当作脏数据，最后一次遍历全部修好。比每次 `Insert` 都维护要便宜。对更复杂的数据结构，这个想法会放大成「一批操作 + 一次 rebalance」的 deferred maintenance 模式。
- **不变量 ≠ 等价关系**。评论区有人抱怨 ryg 滥用了「不变量」这个词，他反驳说这就是标准 CS 术语——loop invariants、data structure invariants 和数学里的 knot invariants 用法一致，都是「状态空间里的不动点条件」。

## 与 APoSD 的关系

这篇文章用的语言不是 [[john-ousterhout|Ousterhout]] 的，但讲的是同一件事。[[information-hiding|信息隐藏]] 的反面就是多个模块共享同一份数据但分别维护；[[information-leakage]] 与 [[change-amplification]] 在 ryg 这里有了数据结构层面的精确对应：**一条不变量就是一个可能泄漏的真相**。「不变量越简单代码越短」在 [[deep-modules|深模块]] 的语言里叫「接口的组合爆炸越少」。

## 相关
- [[fabian-giesen]]
- [[change-amplification]]
- [[information-hiding]]
- [[obscurity]]
- [[ring-buffer-virtual-stream]] —— 用单调计数器把「满 / 空」二义性压进无符号减法的不变量里
- [[negative-space-in-programming]] —— 好的不变量让一类 bug 根本写不出来，这是负空间的典型形态
- [[good-software-no-double-check]] — Boris The Brave：不要重复检查假设，一次建立即可

## Sources

- [[sources/ryg-data-structures-and-invariants]]
