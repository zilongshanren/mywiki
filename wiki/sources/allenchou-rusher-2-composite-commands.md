---
tags: [source, 设计模式, 命令模式, ecs, as3]
date: 2026-04-14
sources: 1
---

# Rusher 2 – Composite Commands（Allen Chou）

[[allen-chou|Allen Chou（周明倫）]] 2011 年 10 月发表的 **Rusher 2** 系列教程之一，讲解 ActionScript 3 下他自己维护的一个轻量 ECS + 命令模式游戏框架里，**复合命令（composite command）**的基本用法。技术栈虽已过时，但命令模式的架构思路至今通用。

## 摘要

作者假设读者已经看过前一篇介绍 `Command` 基类的文章，本文聚焦于 `SerialCommand` 的用法：一串子命令**顺序执行**，前一个通过 `Command.onComplete` 信号广播完成之后，下一个才启动。子命令可以通过构造函数一次传入，也可以用继承自 `CompositeCommand` 的 `append()` 方法动态添加。文章用一个具体例子演示：场上有 5 个小球，玩家点击鼠标时，5 个小球依次（带 0.025s 间隔）tween 到鼠标位置。作者通过 `SerialCommand` 包装 5 个 `TweenNanoTo` 子命令实现这个效果，强调**每个 Command 实现者必须在工作完成时主动调用 `complete()`**，否则整个链条会卡死。同时提到还有一个对偶的 `ParallelCommand`，语义是所有子命令同时启动，全部完成之后父命令才触发 `onComplete`。教程最后预告下一篇将讲状态机。

## 关键要点

- 命令模式的隐藏假设是**跨帧执行**：Tween 类命令一跑就是几百毫秒，普通函数调用的「瞬时完成」语义不适用，必须通过 `onComplete` 信号显式表达「做完了」。
- `CompositeCommand` 支持递归——子命令自己也可以是复合命令，自然形成命令树；这和行为树（Behavior Tree）的 Sequence / Parallel 节点在结构上完全同构。
- Rusher 2 框架结合了依赖注入（用 `[Inject]` 标注 `entityManager` / `commandManager` / `clock` / `mouse`），system 通过这种方式拿到其它系统的引用——是一种典型的 ECS 架构实现。
- `Mouse.isPressed()` 与 `Mouse.isDown()` 的语义区别：前者只在按下那一帧为 true，适合「一次性动作」；后者在按住期间持续为 true，适合持续输入。这个区别是多数游戏输入系统都要处理的基本约定。

## 链接到的概念

- [[composite-command-pattern]]
- [[ecs]]
- [[allen-chou]]

## 原文

- 链接：https://allenchou.net/2011/10/rusher-2-composite-commands/
- 本地：`raw/articles/allenchou.net/2011-10-24_rusher-2-composite-commands-ming-lun-allen-chou-zhou-ming-lu.md`
