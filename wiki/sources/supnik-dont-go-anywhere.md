---
tags: [source, debugging, threading, gdb]
date: 2026-04-19
sources: 1
---

# Don't Go Anywhere!（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 发表于 2011 年 3 月的短札记，讲一个多线程 C++ 程序里命中断点后被调试器「跑飞」的典型坑，以及 gdb 的 `scheduler-locking` 指令。

## 摘要

场景是经典的 NaN 排查：命中断点后想打印一个 vector 的某元素值。问题在于 `operator[]` 在 debug build 下是一次带越界检查的函数调用，gdb 要执行它必须短暂放跑进程，这一瞬间 X-Plane 的其他 worker 线程也会被放开，结果下次停下时已经是另一个线程里的另一个断点，backtrace 毫无价值。硬办法是用命令行把模拟器伪装成单核机器，但载入变得很慢。Supnik 给出的精确武器是 `set scheduler-locking on/off`：开启后 gdb 只会让当前线程跑，其他线程被冻结，可以安心在断点里逐行检查 STL 容器。还存在 `step` 档位实现「step 时锁定、continue 时放开」的混合策略。

## 关键要点

- debug 模式下 `std::vector::operator[]` 是函数调用，被 gdb 求值需要线程「活」起来
- 线程在求值间隙被调度器调度，会让下一个断点落在另一个线程
- 关线程池（X-Plane 支持伪造 CPU 核数）是粗暴但有效的 workaround，代价是慢启动
- `set scheduler-locking on` 锁住调度器，只有当前线程可运行
- `set scheduler-locking off` 恢复正常多线程执行
- 还有 `step` 档位专供「步进时锁、continue 时放」

## 链接到的概念

- [[gdb-scheduler-locking]]
- [[message-queue-thread-ownership]]
- [[supnik-race-condition-debug]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/03/dont-go-anywhere.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-03-07_don-t-go-anywhere.md`
