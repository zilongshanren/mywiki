---
tags: [source, 数据结构, 软件设计]
date: 2026-04-14
sources: 1
---

# Data structures and invariants（Fabian Giesen）

[[fabian-giesen|ryg]] 2010 年 9 月的教学长文，用单链表、带 tail 的链表、双向链表三个例子层层演进，把「不变量 = 当同一份数据通过多条路径被访问时必然诞生的同步约束」这一观点讲透了。这篇文章是后续 ryg 写数据结构系列的开篇引子。

## 摘要

教科书把 invariant 教在排序 / 搜索 / 图算法上，但实际工程里最常遇到的不变量是**数据结构层面**的：`head` 和 `tail` 必须一致；`prev` 与 `next` 必须互指；BST 左子树 < 当前节点 < 右子树。每多加一条指针（访问路径），写路径就多一条同步义务；special case 会在所有 mutator 里长出来。ryg 给了两种清理方法：一是用 pointer-to-pointer（`ListNode **tailNext` 代替 `ListNode *tail`），让空/非空的边界自然消失；二是给双向链表加**哨兵节点**（循环双向链表的 sentinel owner），让所有「第一个 / 最后一个元素」的特判全部蒸发，不变量只剩 `x->next->prev == x` 一条。这两个招数的共同本质是：**把数据结构的状态空间正则化，让状态空间里没有空洞，不变量就不会产生 special case**。文末顺手提了 AVL / 红黑树是同一种推理的最复杂形态——AVL 的不变量更强，所以 rebalance 的 local 修复规则也更复杂。

## 关键要点

- **裸单链表**：没有不变量，`head` 任意值都合法。这是单链表「干净」的根本原因。
- **带 tail 的单链表**：引入一条缓存路径，不变量变成 `head` 与 `tail` 必须指向同一个链表的首尾——所有 mutator 都要额外检查「是不是空」「是不是最后一个」。
- **tail-pointer-to-pointer 技巧**：存 `ListNode **tailNext`，空链表时指向 `&head`，彻底消除空/非空分叉；`AddAtBack` 变成两行。「保存前驱的 next 指针」idiom 还能泛化出 `insert after existing element` 这类接口。
- **双向链表 sentinel**：一个 dummy 节点作为 owner + 循环连接，把链表头尾都指向自己。空链表 = 只有 sentinel 的单元素循环。所有 `Insert / Remove` 都是 4 行无分支代码，只要维护 `x->next->prev == x`。
- **延迟维护（deferred maintenance）**：对复杂数据结构，可以在一批操作内部只维护部分不变量（比如只更新 `next`），最后扫一遍一次性修好 `prev`。这是 AVL / 红黑树 rebalance 的根部思想。
- **不变量 ≠ 等价**：评论区有人抱怨术语不严谨，ryg 明确反驳这就是标准 CS / 数学用法（knot invariants、loop invariants 等）。

## 链接到的概念

- [[data-structure-invariants]]
- [[fabian-giesen]]
- [[change-amplification]]
- [[information-hiding]]

## 原文

- 链接：https://fgiesen.wordpress.com/2010/09/27/data-structures-and-invariants/
- 本地：`raw/articles/fgiesen.wordpress.com/2010-09-27_data-structures-and-invariants.md`
