---
tags: [source, bitsquid, particle, collision, hash-cache]
date: 2026-04-19
sources: 1
---

# Hack Day Report — bitsquid: development blog

[[niklas-frykholm|Niklas Frykholm]] 2012 年 6 月的 hack day 复盘，主要干货是**粒子碰撞系统的重写**——用"每粒子自带一张平面 + 空间哈希缓存"替换了之前的世界 slice 方案。

## 摘要

文章前半段介绍 Bitsquid 的 hack day 模式（一天完成 proof-of-concept、鼓励失败、事先公开主题、无会议无 Skype）；后半段聚焦 Niklas 自己那一天的产出。粒子碰撞传统做法是切一块世界 slice 做简化表示——slice 多大、精度多高、如何处理动态物体，全是参数地狱且换场景就崩。受 Naughty Dog GDC talk 启发，新方案让**每个粒子内嵌一张碰撞平面**（4 float，不增 flag，不存在时放原点下方足够远），测试退化为一次 dot + compare，完全 cache-local 可并行。为了让少量 raycast 预算在大量粒子间共享，他在 `(量化位置, 量化方向) → plane` 上建了一张 HashMap：cell 大小 xy/z 分别给，MurmurHash 前三轮作为 key；超限就丢旧。本质是一个**两层有损缓存**（粒子内 + 空间 hash + PhysX raycast）。代价：V 形凹槽粒子静不住、多面角落行为差——Niklas 选择保持简单而不存多个平面。同一天其他项目包括改进选择高亮（wireframe pass）、屏幕截图/视频跨平台捕获、Lua 热打 profiler。

## 关键要点

- per-particle plane：4 float，"没碰撞" = 平面放到原点远处，不要 flag。
- 问题拆成两部分：plane test（trivial）+ 找 plane。
- 找 plane 用 raycast 预算参数控制（每帧允许的 raycast 数）。
- raycast 结果共享：`HashMap<uint64, plane>`，key 是量化位置 xor 6 方向 id。
- 设计哲学：**有损 + 分层 cache** 替代统一共享碰撞表示。
- 预 hash 成 uint64 再塞 HashMap——比用复合 struct key 省内存、取模更快。

## 链接到的概念

- [[particle-collision-plane-cache]]
- [[murmur-hash-inverse]]

## 原文

- 链接：https://bitsquid.blogspot.com/2012/06/hack-day-report.html
- 本地：`raw/articles/bitsquid.blogspot.com/2012-06-19_hack-day-report.md`
