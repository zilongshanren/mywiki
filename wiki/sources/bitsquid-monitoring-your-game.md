---
tags: [source, bitsquid, 性能监控, 数据导向, 调试工具]
date: 2026-04-19
sources: 1
---

# Monitoring your game（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2011 年 5 月的文章，讲为什么"可视化监控 + 数据流回放"比 debugger 更适合抓帧率毛刺、动画抖动、相机突跳这类**时间维度**的 bug。

## 摘要

传统 debugger 对"只在帧间 diff 才存在"的 glitch 无力——在 glitch 处下断点，call stack 也看不出什么。作者提出的做法是把游戏当未知生物：**戳它、看曲线**。画 `delta_time(t)`、每个 profiler scope 的耗时占比、bone 旋转、相机位置、内存碎片、带宽曲线，掉帧和抖动一目了然。

实现底座很简洁：一个 **event buffer** 装满 POD struct，每条 event 以 type id 打头跟变长负载（`ENTER_PROFILER_SCOPE` / `ALLOCATE_MEMORY` / `RECORD_GLOBAL_FLOAT` …）。避免多线程锁热点的做法是**每个线程一个 64 KB TLS 小 cache**，满了或帧末才 flush 到全局 buffer。同一份 buffer 既给在线 visualizer 画实时曲线，又推到 TCP 给 PC 上的离线 visualizer（内存近乎无限、可回放完整会话）。record 接口 expose 给 Lua，几行 Lua 就能在游戏控制台动态挂探针画图。

## 关键要点

- **monitoring = 事件流 + visualizer**：一份 event buffer 驱动一切可视化，不为每种图各做一套；
- Event buffer 是**连续 POD struct**（"file format for memory"），事件不删，reader 各挑各的；
- **TLS 64 KB cache + 帧末批量 flush** 把多线程锁热点降到 O(1/帧)；
- **字符串指针即 intern ID**：event 里只存 `const char *`，依赖字面量地址唯一且永久；动态字符串要手动 intern；
- 跨网络传输时首见字符串指针就专门发一条"字典消息"(`ptr, value`)，离线端建翻译表；
- 两类消费者：**在线 visualizer**（游戏内画）+ **TCP 离线 visualizer**（PC 全量回放）；
- debug heap 与游戏主 heap 分开，shipping 配置可整块 strip；
- 接口 expose 给 Lua——游戏控制台里几行 Lua 就能挂探针 + 画图，30 秒验证假设。

## 链接到的概念

- [[game-monitoring-event-buffer]]
- [[string-handling-game-runtime]]
- [[offset-based-resource-blobs]]
- [[a-metric-for-memory-fragmentation]]
- [[linear-allocator]]
- [[niklas-frykholm]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2011/05/monitoring-your-game.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2011-05-26_monitoring-your-game.md`
