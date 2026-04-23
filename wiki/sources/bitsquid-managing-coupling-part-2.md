---
tags: [source, bitsquid, 系统设计, 事件, 回调, 轮询]
date: 2026-04-19
sources: 1
---

# Managing Coupling Part 2 — Polling, Callbacks and Events（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2011 年 2 月 Bitsquid Blog。系列第二篇。聚焦一个具体子问题：**低层系统需要告诉高层系统"某件事发生了"，三种常见做法怎么选、怎么实现**。

## 摘要

先厘清方向：高层叫低层是无问题的，低层 → 高层的通知才是本文话题。三种方式各自的工程判断：

**Polling** —— 桌面编程里 polling 被视为不礼貌（busy-wait、100% CPU），但在游戏循环里这个前提不成立。只要对象数不爆炸，poll 对帧时间无感；而且 **poll 的代码常比 callback 清晰得多**（character controller 直接 `input.A_is_pressed()` 比注册回调 + 转发给 controller 简单）。**作者主张默认 poll**。不适合 poll 的是物理碰撞这种 N² 关系——真那样做已经变回 event 系统。

**Callbacks** —— 关键设计问题是**立即执行还是延迟执行**。作者坚定推延迟：避免 I/D-cache 抖动、免去全局锁、避免"callback 删了当前正在遍历的对象"这种自杀 bug、可并行生成最后合并。延迟后回调形态和 polling 类似——"何时执行由高层说了算"。C++ 实现他直接用 C 风格函数指针 + user data；member function pointer 不堪用、observer pattern 样板太多堆分配太多、FastDelegate 平台 trick 太多。用自定义的 `struct Callback16 { void (*f)(void); char data[12]; }` 存函数指针 + 内联数据，调用时整体 cast——raw memory 的自由度在引擎里极值钱。对象在回调执行时已销毁？用上一篇的 **ID 引用**，回调里查 ID 是否仍有效。

**Events** —— 等价于 callback 换成 enum；单点监听用 callback、批量处理用 event。存储方式极朴素：一块 raw buffer，`[enum1][data1][enum2][data2]...` 连续拼接，高层线性扫分发；可自由 move/copy/merge/跨核传递。**红线**：每个低层系统的 event 流只能有一个高层消费者，**绝不做全局 switchboard / pub-sub**——那样 coupling 会以隐形方式被种回代码库。

## 关键要点

- 游戏里 polling 被严重低估——只要规模不爆就优先 poll。
- 不适合 poll：物理碰撞（N²）、事件数太多、对象多到单帧扫不完。
- Callback **必须延迟**：I/D-cache、多线程、避免 iterate-while-delete bug、跨核合并——四大好处。
- Member function pointer、observer pattern、FastDelegate 全部不要；用**C 风格函数指针 + 内联 data struct**。
- 函数指针/数据块 cast 来回是可接受的——错 cast 99% 立刻大崩溃，当场改。
- Callback 引用的对象可能已销毁 → **ID 引用**兜底，查 ID 有效性再 deref。
- Event 的存储 = raw byte buffer；**不要**做成通用序列化框架。
- **绝对不**做 global event switchboard / pub-sub——这是经验教训也是个人 pet peeve。
- 消费节奏：一帧消费一次、生产者溢出时按子系统语义决定扩容/丢旧/冻结生产。
- 小金句："每次你想设计一个干净灵活的 C++ API，它最后都趋同到纯 C。"

## 链接到的概念

- [[polling-callbacks-events]]
- [[system-decoupling-patterns]] — 本系列第一篇，提供 ID 引用机制
- [[id-based-lifetime-with-kill-flag]]
- [[handle-based-resource-manager]]
- [[intent-vs-state]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2011/02/managing-decoupling-part-2-polling.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2011-02-11_managing-coupling-part-2-polling-callbacks-and-events.md`
