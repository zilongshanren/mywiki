---
tags: [source, bitsquid, 物理, 动画, 场景图]
date: 2026-04-19
sources: 1
---

# Inheriting Velocity in Ragdolls（Niklas / Bitsquid）

[[niklas-frykholm]] 2012 年 4 月 20 日的博客——如何在角色从动画切到 ragdoll 的一瞬把动画已有的线速度、角速度带进物理系统，让倒下的动作自然。

## 摘要

Bitsquid 的物理、场景图、动画三系统**互不耦合**，靠场景图节点的整数索引通信。要算切换瞬间的速度，必须同时拿到"前一帧"和"这一帧"两个世界变换。Niklas 列举四条候选：对动画曲线求导（被 blend tree / IK / 脚本污染，放弃）；倒退一帧仿真（FPS 服务器做过，但工程过重）；延迟一帧切换（违反 Bitsquid 的 "不许延迟一帧" 戒律）；**在场景图里每帧保存 `last_world`**（内存多 50%、memcpy 一份，但最简单）。

Niklas 选了第四条，理由是"没有明显赢家时先选最简单的，需要时再优化"。评论区对这套方案做了三处重要补充：**指针 double-buffer 不适用**（场景图只增量变换 dirty 节点）；**速度应当取刚体质心位置差分**；**角速度有更便宜的四元数公式** `2(q1-q0)*conj(q0)/dt`，省掉 axis-angle 分解。还有一条有趣建议：**向前仿真一帧**比向后仿真简单、速度也足够好，顺带可供 per-object motion blur 使用。

## 关键要点

- 三系统解耦的代价：跨系统数据获取需要专门设计。
- **"不许延迟一帧"**在这篇文章里被顺手立为 Bitsquid 戒律，理由是延迟会让对象进入自相矛盾的过渡态并扩散出 `if` 补丁。
- 没有明显赢家 → 先选最简单 → 保留优化空间。
- 增量计算的数据结构不能无脑做 double buffer。
- 质心位置差分和四元数角速度近似都是评论区给出的关键订正。

## 链接到的概念

- [[ragdoll-velocity-inheritance]]
- [[no-frame-delays-principle]]
- [[system-decoupling-patterns]]
- [[per-entity-scene-graph]]
- [[niklas-frykholm]]

## 原文

- 链接：https://bitsquid.blogspot.com/2012/04/inheriting-velocity-in-ragdolls.html
- 本地：`raw/articles/bitsquid.blogspot.com/2012-04-20_inheriting-velocity-in-ragdolls.md`
