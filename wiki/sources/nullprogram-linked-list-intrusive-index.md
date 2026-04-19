---
tags: [source, programming-languages, data-structures, c]
date: 2026-04-19
sources: 1
---

# Linked lists, revisited（Chris Wellons / nullprogram）

[[chris-wellons]] 发表于 2025 年 12 月的文章，展示如何以简单的链表为基础，分阶段叠加哈希 trie 与 MSI 哈希表，而不破坏原始结构。

## 摘要

文章以环境变量的 key/value 列表为例，从最朴素的链表栈式构建开始（头插 LIFO），再用双指针技巧保持 FIFO 顺序。接着，作者将链表节点扩展为同时也是 [[hash-trie-intrusive|侵入式哈希 trie]] 节点，额外引入两个子指针，构造时即插入到 trie，实现 O(log n) 查询，并自然支持多映射迭代器。最后一步是外挂一个非侵入的 [[msi-hash-table|MSI 哈希表]]（power-of-two 数组），用于静态场景的常数时间查询。所有代码建立在 [[linear-allocator|arena 分配]] 之上，节点内存紧凑，无需资源管理开销，可直接用于嵌入式系统和微型 WebAssembly 程序。

## 关键要点

- 链表构建三种范式：LIFO 头插（3 行代码）、双指针 FIFO、侵入式 trie 混合
- 双指针技巧：`Env **tail = &head` 可在无分支、无哨兵节点的前提下维护尾指针
- 在链表节点里加两个 `child[2]` 指针即可把链表同时当哈希 trie 用
- MSI 哈希表非侵入、可在同一链表上建多张索引（例如按 value 长度）
- 迭代器/cursor 模式支持多映射遍历
- 所有结构都在 arena 上分配，符合 skeeto 一贯的分配哲学

## 链接到的概念

- [[linear-allocator]]
- [[hash-trie-intrusive]]
- [[msi-hash-table]]
- [[avoid-unsigned-types]]

## 原文

- 链接：https://nullprogram.com/blog/2025/12/31/
- 本地：`raw/articles/nullprogram.com/2025-12-31_null-program.md`
