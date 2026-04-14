---
tags: [source, lua, 垃圾回收, 增量-GC, 源码阅读]
date: 2026-04-14
sources: 1
---

# Lua 5.1 增量式 GC 剖析（云风 / blog.codingnow.com）

[[cloudwu]] 发表于 2011 年 3 月的源码阅读笔记，对 Lua 5.1.4 从 stop-the-world 切换为增量式 GC 的实现做了一次细致的内部解剖。文章本身标注"待续"，是系列的第一篇。

## 摘要

文章从动机讲起：Lua 5.0 的 stop-the-world GC 在游戏服务器这种数据量大、实时性要求高的场景停顿明显；Lua 5.1 把 GC 切成增量式——仍然是 stop-the-world 但分步执行，每一步只做一点再把控制权还给用户代码。接着按 `global_State.gcstate` 的五态机 (`GCSpause / GCSpropagate / GCSsweepstring / GCSsweep / GCSfinalize`) 展开每个阶段的关键操作，指出 propagate 阶段在 gray 链清空后必须进入一个不可被打断的 `atomic(L)` 来封顶 mark。然后重点解释三色标记中"为什么需要两种白色"：答案是 mark 结束到 sweep 结束之间新建的对象既不能涂黑（会在本轮结束后无法重置回白）也不能涂成当前被清的白色（会被错杀），解法是两种白做乒乓开关。最后讲另外几个标记位：`FINALIZEDBIT` 避免 `__gc` 重复触发，`KEYWEAKBIT / VALUEWEAKBIT` 处理 weak table，`FIXEDBIT` 保护保留字和元方法名字符串使其永不回收——并顺手解释了为什么这让 Lua 的元方法比较能退化到指针比较、比 `strcmp` 和 `lua_pushlstring` 快得多；`SFIXEDBIT` 只给主 mainthread 用，`luaC_freeall` 时依然保护它，真正的释放是 `close_state` 最后一句显式 free。

## 关键要点

- Lua 5.1 的 GC 是增量式不是并发：只是把 stop-the-world 切成小步
- 状态机五阶段：pause → propagate → sweepstring → sweep → finalize
- propagate 阶段最后必须 `atomic(L)` 封顶
- 三色标记中"灰"是 derived 的：非白非黑 = 灰
- 两种白色做乒乓，解决 mark 结束至 sweep 结束之间新建对象的着色问题
- `FIXEDBIT` 的副作用：被钉住的字符串地址不变，元方法比较可退化为指针比较
- `SFIXEDBIT` 只标记 mainthread，`lua_close` 时也受保护，最后由 `close_state` 显式释放
- `GCSWEEPCOST` 等"神秘数字"用于换算 GC 步长预算（待续）

## 链接到的概念

- [[lua-incremental-gc]]
- [[garbage-collector]]
- [[simple-cpp-mark-sweep-gc]]
- [[lua-design-philosophy]]
- [[cloudwu]]

## 原文

- 链接：https://blog.codingnow.com/2011/03/
- 本地：`raw/articles/blog.codingnow.com/2011-03-31_yun-feng-de-blog.md`
