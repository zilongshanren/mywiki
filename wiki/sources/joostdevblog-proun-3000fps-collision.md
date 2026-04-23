---
tags: [source, gameplay, collision-detection, fixed-timestep, simplicity, proun]
date: 2026-04-19
sources: 1
---

# Dirty collision detection trickery in Proun（Joost van Dongen / Joost's Dev Blog，2010-10-20）

[[joost-van-dongen]] 在 Proun 里用一个「暴力高频」的技巧绕过碰撞 tunneling 问题，并借此阐述他在 Ronimo 团队里推行的代码风格：能用简单手段就不用复杂手段。

## 摘要

常规游戏以 60fps 做碰撞，快速物体一帧内可能跨越薄障碍物造成 tunneling。常见解法是在前后两帧之间打射线，或让碰撞跑 sub-step。两种都要引入额外数学或让碰撞与主循环异频，代码复杂度上升。Joost 的做法是把 Proun 所有 gameplay（含障碍动画）锁在 **3000fps** 固定步长，图形仍跑 60fps。小球直径已知、最高速度已知，1/3000 秒能走的距离远小于任何多边形厚度，tunneling 在可达速度内被物理不可能化；碰撞代码仍是最朴素的「当前位置 vs 当前几何」，无需任何插值或 swept volume。实测只在「极弱 CPU + 极强 GPU」这种不现实组合下才影响帧率；Proun 图形（特别是动态模糊）才是 CPU/GPU 大头，gameplay 基本闲着。评论区有人质疑这并没真正消除 tunneling，只是把阈值推高，也有人建议 swept volume 或 ray test；Joost 的回应是：他要的不是最优解，而是**实现最短、bug 面最小、不需要改写碰撞响应代码**的解。该方案**不适用**于 FPS（子弹小速度高，3000fps 还是会漏）。

## 关键要点

- Fixed timestep 的频率不是信仰数字，而是根据**已知最小尺寸 / 最大速度**倒推出来的安全阈值。
- 「gameplay 计算密度 ≪ 图形预算」时，用空闲 CPU 换代码简单性是合理交易。
- 同一套机制顺便解决了「轨道本身在动，动态障碍的碰撞精度」问题。
- Joost 强调代码整洁比性能优先：10w 行代码量的 Ronimo 项目里，可读性是 bug 压制的前提。

## 链接到的概念

- [[fixed-3000fps-gameplay-simplicity]]
- [[continuous-design]]
- [[joost-van-dongen]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2010/10/dirty-collision-detection-trickery-in.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2010-10-20_dirty-collision-detection-trickery-in-proun.md`
