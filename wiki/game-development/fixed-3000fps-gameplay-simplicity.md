---
tags: [gameplay, simulation, collision-detection, simplicity, fixed-timestep]
date: 2026-04-19
sources: 1
---

# 3000fps 固定步长：用「暴力高频」换来碰撞简单性

Proun 里 Joost van Dongen 把所有 gameplay 逻辑（包括碰撞检测、障碍物动画）锁在 **3000 帧每秒** 的固定步长上跑，图形仍然按显卡能力的 60fps 渲染。乍看离经叛道——实际上这是一个清晰的 **simplicity-over-performance** 决策。

## 要解决的问题：tunneling

常规游戏以 60fps 做碰撞，每帧间隔约 16ms；快速物体（子弹、加速后的赛车）可能一帧在障碍一侧、下一帧在另一侧，完全穿过。两种常规解法：

1. **Raycast between frames**：把上一帧位置和当前帧位置之间打一条射线。
2. **Sub-step**：仅对碰撞检测在必要时加倍步进。

两种都要么引入「前后两帧插值」的数学，要么让碰撞以与 gameplay 不同的帧率跑，代码就得处理「某些状态变化频率不同」的细节。

## Joost 的选择

直接把整套 gameplay tick 频率拉到 **3000fps**：

- 玩家小球是已知半径的球体，最高速度也是已知上限；球心 1/3000 秒能走的距离比任何多边形厚度（Proun 里所有碰撞体本就是无限薄的三角形）小得多，tunneling 在可达速度内**被物理不可能化**。
- 碰撞代码仍然是最朴素的「当前位置 vs 当前几何」，**没有**任何「介于两帧之间」的插值或 swept volume 数学。
- 实现时间极短，bug 面极窄。

## 为什么这在 Proun 里能工作

- Gameplay 计算量极小：就是小球 + 少量移动轨道段 + 简单物理，CPU 基本闲置。
- 图形才是 CPU/GPU 大头，尤其是动态模糊之类的后处理。Joost 实测：这种「50 倍物理步长」只在「CPU 极弱 + 显卡极强」这一不现实配置下才影响帧率。
- Proun 的轨道本身也会移动，高频 tick 顺便让运动障碍的碰撞精度提升——同一套机制解决两个问题。

评论区有人指出这并没**真正**消除 tunneling（只是把阈值推得足够高），也有人建议改用 swept volume 或 ray test。Joost 的回应道破本质：他不是在追求最优解，而是在追求**实现最短、出 bug 概率最低、不需要改写原有碰撞响应代码**的解。对他这类需要亲力亲为的独立开发者，代码简洁性比 CPU 占用更值钱。

## 适用边界

Joost 自己承认：换成 FPS 游戏这招就不行——子弹尺寸小、速度高，3000fps 依然漏穿，必须用 ray cast。这条经验的真正抽象是：

> 当 gameplay 的计算密度远小于图形预算时，与其用算法复杂度换 CPU，不如用多余的 CPU 换代码简单性。

类似思路散见于 [[continuous-design]] 的讨论里：**性能是有余量的，余量可以花在降低复杂性上**。

## Sources

- [[sources/joostdevblog-proun-3000fps-collision]]
