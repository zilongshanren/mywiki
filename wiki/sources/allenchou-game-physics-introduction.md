---
tags: [source, 游戏物理, 物理引擎, 碰撞检测]
date: 2026-04-14
sources: 1
---

# Game Physics: Introduction & Acknowledgements（Allen Chou）

[[allen-chou|Allen Chou（周明倫）]] 2013 年 12 月发表的 **Game Physics Series** 开篇，写于他在 DigiPen 从图形程序员转岗为 junior project 的物理程序员之后半年。目标是把一个约束式刚体物理引擎（constraint-based rigid body physics engine）涉及的所有基本词汇和流水线结构**一次性摆清楚**，为后续按主题深入的系列文章做总索引。

## 摘要

文章先定义一组核心术语：**rigid body**（带 mass、inertia tensor、position、orientation、linear/angular velocity 的被模拟对象）、**collider**（刚体的几何部件，凸凹拆分的最小单位）、**collision**、**contact**、**contact manifold**（两个 collider 之间所有 contact 的几何摘要）。接着描述物理模拟的**三段流水线**：Broadphase（用网格 / AABB 树 / sweep-and-prune 粗剔除），Collision Detection（对可能相交的 collider 对精确判定并生成 contact 信息，一般方法是针对简单图元的 special-case 加通用的 **GJK / EPA / MPR**），Resolution（把所有 contact、spring、hinge、pin 统一建模为等式约束，用 Erin Catto 的 **Sequential Impulse** —— 一种 Gauss-Seidel LCP 的高效变体 —— 迭代求解）。文末列出作者学习物理引擎的参考来源：DigiPen 同学与教授、Box2D/Bullet 的作者 Erin Catto / Erwin Coumans、Christer Ericson 的 *Real-Time Collision Detection*、Ian Millington 的 *Game Physics Engine Development*、Gino van den Bergen 的 *Collision Detection*，强调这片领域至今仍是「tribal knowledge」——没有一本完整覆盖的书。

## 关键要点

- 刚体数据结构里必须同时缓存 mass 和 inertia tensor 的**倒数**，因为约束求解中反复需要。
- GJK 只回答「是否相交」，物理需要 contact 信息——所以要和 EPA 配对；MPR 则是把两步合并的单算法替代品。
- 把凹 collider 预拆成多个凸 collider 是常规策略，因为 GJK/MPR 只接受凸形状。
- Sequential Impulse 的几何直觉：多条约束的求解等价于在多个半空间上做一串点投影，是 Box2D、PhysX 等的工业标准。
- 评论区 Erwin Coumans（Bullet 作者本人）留言称赞，并提到 continuous collision detection、featherstone articulated bodies、dynamic AABB tree broadphase 是后续值得写的高阶主题。

## 链接到的概念

- [[game-physics-engine]]
- [[collision-detection-gjk-epa]]
- [[allen-chou]]
- [[engine-layering]]
- [[kinematic-character-controller]]

## 原文

- 链接：https://allenchou.net/2013/12/game-physics-introduction/
- 本地：`raw/articles/allenchou.net/2013-12-18_game-physics-introduction-acknowledgements-ming-lun-allen-ch.md`
