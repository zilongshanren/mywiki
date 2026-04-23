---
tags: [source, 工具, 内存调试, sanitizer, asan, x-plane]
date: 2026-04-19
sources: 1
---

# This is Why ASAN Makes The Big Bucks（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2016 年 7 月的一张截图帖：Xcode 7 里 ASan（AddressSanitizer）抓住 X-Plane 一次内存踩踏的案发现场，顺带一段对 ASan 作为生产级调试工具的服气评价。

## 摘要

Supnik 对 Apple 的开发工具一向持保留态度——但 ASan 在 X-Plane 这种吃满 gamer-class PC 的大应用上**依然可用**：fully unoptimized debug 构建挂满 ASan 仍能跑到 7–10 fps，还能用真实用户级别的设置玩下去。对比 Valgrind 在 Linux 上跑 X-Plane 连 load 阶段都审计不完，这不在一个数量级。此案例的 bug：**几何累加器**类把多份几何打进一个 VBO，client 必须等 accumulation 结束才能删掉自己那段；但没人加 assert。当 client 提前删时，stale 指针在后续 VBO 组装里被使用，踩烂内存。ASan 给出的信息是「最好的结果」——not only 指出现在踩到哪儿，还打出**原分配点**和**释放点**的完整 backtrace。评论区有人提醒 ASan 是 Clang/LLVM 的跨平台工具、Linux 上支持更好，Supnik 澄清他是在说「集成到 Xcode 里的体验」。

## 关键要点

- ASan fully-instrumented 在 AAA 游戏规模下 7–10 fps 可用
- 报告信息：当前踩点 + 原分配栈 + 原释放栈三重 backtrace
- vs Valgrind：后者在 X-Plane 尺度下不可用
- bug 模式：多源累加共享 buffer 缺 lifetime assert → client 提前释放 → stale pointer 踩坑
- 教训：**写 assert 保护所有权语义**比事后靠工具便宜

## 链接到的概念

- [[undefined-behavior-c-cpp]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2016/07/this-is-why-asan-makes-big-bucks.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2016-07-06_this-is-why-asan-makes-the-big-bucks.md`
