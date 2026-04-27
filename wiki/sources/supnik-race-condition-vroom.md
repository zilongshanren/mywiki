---
tags: [source, concurrency, tsan, threading, race-condition, clang, x-plane]
date: 2026-04-27
sources: 1
---

# Vroom, Vroom! I'm Going to Win This Race Condition!（Ben Supnik / The Hacks of Life）

[[people/ben-supnik]] 发表于 2017 年 2 月的文章，记录为 X-Plane 引入 ThreadSanitizer（tsan）后发现的一系列竞态条件，并深入讨论竞态条件何时"真正良性"以及为何这个问题越来越难回答。

## 摘要

tsan 通过影子内存动态追踪线程访问，能在竞态发生时立即报告（而不必等到运行崩溃），将"偶发性现场崩溃"变成"每次启动稳定复现"。文章依次展示三个案例：（1）主线程初始化 texture preference 时后台线程已开始加载纹理（良性竞态，重构消除）；（2）多个机场挤出任务通过"bounce between threads"惯用法共享 shader-layer vector，违反了惯用法的独占前提，导致偶发 vector 扩容崩溃（真实 bug）；（3）天气双缓冲设计缺陷，worker 较快时 tsan 看不到竞态，需要跑 30 分钟才捕捉到。结论：Clang 的优化已复杂到连有经验的程序员也无法静态推理"这个竞态安全"，唯一正确的做法是消除所有竞态。

## 关键要点

- tsan 基于同步点检测竞态，不依赖实际执行顺序，大幅降低复现难度
- "bounce between threads"惯用法只在各任务对数据结构拥有独占访问时成立，共享则失效
- 双缓冲不能保证竞态安全，除非 worker 在每帧都与主线程同步完毕
- tsan 有跟踪饱和问题（>4 线程时可能漏报），部分竞态需长时间运行才能捕捉
- 现代 Clang 的重排能力已超越人类静态推理上限，"良性竞态"在实践中不存在

## 链接到的概念

- [[computer-systems/tsan-race-condition-detection]]
- [[computer-systems/undefined-behavior-c-cpp]]
- [[software-design/app-space-lock-free-simplification]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2017/02/vroom-vroom-im-going-to-win-this-race.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2017-02-17_vroom-vroom-i-m-going-to-win-this-race-condition.md`
