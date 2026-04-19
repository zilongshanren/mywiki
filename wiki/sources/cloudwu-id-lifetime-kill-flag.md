---
tags: [source, 生命期管理, 引用计数, actor, 并发, skynet, cloudwu]
date: 2026-04-19
sources: 1
---

# 对象生命期管理：ID + 销毁标记替代引用计数（云风的 BLOG）

[[cloudwu]] 发表于 2024 年 8 月的文章，记录他重写 skynet 2.0 时把多年零散使用的生命期管理手法固化成一个模式。核心是以 **id + 销毁标记** 替代 C++ 智能指针风格的引用计数。

## 摘要

文章先指出引用计数的两个问题：**销毁时机不可控**（由最后一个持有者决定，并发下很难预期），以及到处 +1/-1 的累积开销——后者正是为什么多数 GC 语言选 mark-sweep。云风的替代方案分两层：一是 **长期持有用 id 而非指针**，通过全局 hash 表换回指针；二是对象除了 refcount 还有一个**不可翻转的销毁标记**，set 之后所有新的"id → 指针"查询都会失败，refcount 只会单调递减，对象必然在可预期时间内销毁。语义由"所有人都不用了才销毁"变成"**我决定销毁，但等当前正在使用的短期流程结束**"。进一步约束"创建销毁都在同一线程完成"（actor 模型天然满足），hash 表写锁天生不并发，甚至可以用 copy-on-write 实现。

## 关键要点

- refcount 的致命问题：销毁时机不可控、到处 ±1 开销累积
- 用 id 替代长期持有的指针，传递 id 没有开销
- 销毁标记 + refcount 双字段：标记一次性设置，refcount 负责保护正在使用的短期流程
- 所有创建销毁放到同一线程 → hash 表可以用最简单的读写锁或 COW 实现
- Actor 模型天生契合这个约束
- 真正需要 refcount 的场景只剩"对象被多个处理流程同时使用"这一类

## 链接到的概念

- [[id-based-lifetime-with-kill-flag]]
- [[handle-based-resource-manager]]
- [[ltask-scheduler]]
- [[snapshot-diff-persistence]]
- [[simple-cpp-mark-sweep-gc]]

## 原文

- 链接：<https://blog.codingnow.com/cat2/cat15/> （2024-08-24）
- 本地：`raw/articles/blog.codingnow.com/2024-08-24_yun-feng-de-blog-2.md`
