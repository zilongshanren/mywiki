---
tags: [source, debugging, 并发, race-condition]
date: 2026-04-19
sources: 1
---

# I Just Saw a Race Condition（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2010 年 9 月的极短随笔，记录一次**调试器观察副作用释放线程导致看见 race condition**的小事故。

## 摘要

Supnik 在 debugger 里 print 一个变量的值，然后 print 一个 STL 容器的片段。这次 print STL 容器的操作需要**在被调试进程里执行代码**（STL iterator / accessor 是函数，不是 inline 可直接读的内存布局）。调试器为此**临时释放了所有线程**——其他线程中有一个正在往这个变量里 race 写。等 print 返回、程序重新挂起时，变量值已经被另一个线程改过。他于是看见了一个只有在「继续执行—再暂停」之间才会被观察到的 race condition：**调试动作本身成了扰动源**。

## 关键要点

- 调试器的"打印值"并非纯粹读内存——涉及容器 / 智能指针 / 计算表达式时会在目标进程里执行函数。
- 要执行函数，必须**临时解锁所有线程**（否则 stop-the-world 下函数可能死锁在 mutex 上）。
- 这个短暂的 resume-all 创造了 race 窗口——**观察行为改变了被观察量**，调试版的海森堡效应。
- 提示：遇到"debugger 里看到离谱数值但复现不了"，先怀疑是不是 print 一个非 POD 对象导致的 thread release。

## 链接到的概念

- [[ben-supnik]]
- [[message-queue-thread-ownership]] —— 线程间共享可变状态的 Supnik 式解法
- [[vfx-multithreading-patterns]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/09/i-just-saw-race-condition.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-09-01_i-just-saw-a-race-condition.md`
