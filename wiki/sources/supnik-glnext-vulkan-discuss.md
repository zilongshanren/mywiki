---
tags: [source, vulkan, opengl, 图形api, x-plane]
date: 2026-04-19
sources: 1
---

# glNext is Neither OpenGL nor Next, Discuss（Ben Supnik）

[[ben-supnik]] 2015-03-14 发表，Khronos 刚公布 glNext（当时尚未定名为 Vulkan）+ SPIR-V 讲座后的立场帖。

## 摘要

作者承认自己惯常"不爱大重写、不爱新玩具"的保守立场在这里被翻转了——他更愿意要 Vulkan 而非继续加 OpenGL 扩展，即使迁移要自己多做事。两条已知事实：glNext 不是 OpenGL 的增量扩展，是**替换**；位于图形栈更底层，把内存分配、barrier、descriptor、命令录制全部暴露给应用。三条他最看重的卖点：**线程友好**——OpenGL 把队列 / 命令缓冲 / 线程锁成 1:1，加扩展救不了，X-Plane 的 scenery 后台加载本该无锁，却被驱动的"我不知道有没有人在用"强制同步；**显式性能**——Vulkan 明确告诉你哪些调用贵哪些便宜，直接解决 OpenGL 组合爆炸导致 fast path 无法文档化的困境；**Shim 策略**——因为 Vulkan 不是 GL，反而可以写一个基于 Vulkan 的 OpenGL 实现，让 legacy 代码在 shim 上跑，关键路径再钻洞到原生。反面：Vulkan 不适合 3D 入门教学、轻量手游、一亿行 OpenGL CAD。最大未知是**资源管理**——Metal 因为 iOS 共享内存可以很简单，但 PC GPU 上写 AMD/NVIDIA 级别的资源管理器对小团队是真正挑战。

## 关键要点

- glNext ≠ OpenGL 的升级，是替换
- OpenGL 的线程不友好写在核里——X-Plane 的 scenery 后台加载被迫陪驱动走锁
- "显式性能"直接解 [[supnik-iphone-4-perf-gap|OpenGL 规范不谈速度]]的痛
- Shim 路径：Vulkan 上实现 OpenGL → 旧代码仍跑 → 钻洞原生化关键路径
- Vulkan 不是人人适用；资源管理是小团队最大风险

## 链接到的概念

- [[vulkan-explicit-performance]]
- [[iphone-4-opengl-es-perf-gap]]
- [[graphics-api-history]]
- [[metal-api-overview]]
- [[api-fast-path-design]]
- [[opengl-ext-vs-arb-fast-path-leak]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2015/03/glnext-is-neither-opengl-nor-next.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2015-03-14_glnext-is-neither-opengl-nor-next-discuss.md`
