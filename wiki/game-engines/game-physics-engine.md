---
tags: [游戏物理, 刚体, 物理引擎, 引擎架构]
date: 2026-04-14
sources: 1
---

# 游戏物理引擎（约束式刚体模拟）

游戏物理引擎是一个**每帧跑一次的三段流水线**，它把场景中的刚体（rigid body）往前推进一个时间步，然后修正各种「违规」：两个 collider 穿插了、一根弹簧被拉得太长、一个铰链被拉开了。Bullet、PhysX、Box2D、Havok 都是这条流水线的工业级实现；结构大同小异。

## 核心词汇

- **刚体（rigid body）**：一个被模拟的整体对象，其内部所有部分之间不发生相对位移与旋转。典型数据结构包含 mass、inertia tensor（2D 下退化为标量 moment of inertia）、position、orientation、linear / angular velocity。质量和惯性张量的**倒数**通常也预先算好缓存，因为求解约束时反复要用。
- **Collider / Fixture**：刚体的一个几何「部件」。一个哑铃是一个刚体，但通常拆成「左砝码 + 右砝码 + 连杆」三个凸 collider——把凹几何拆成多个凸 collider 是常规策略，原因是后面介绍的 GJK/MPR 只接受凸形状。Unity 叫 collider，Box2D 叫 fixture。
- **Contact**：两个 collider 相交时，物理引擎把它们的交集区域简化成一组 **contact point**，每个点带位置、法向和穿透深度。
- **Contact manifold**：一对 collider 之间所有 contact 的集合，是两者几何相交体的一种简化几何摘要。

## 三段流水线

**1. Broadphase**：粗略剔除不可能碰撞的 collider 对。最 naive 的做法是 $N^2$ 两两比对——有人仍把它叫「N-squared broadphase」。工业级实现包括显式网格、隐式网格、sweep-and-prune、以及动态 AABB 树（Bullet 的主力）。broadphase 允许假阳性——反正后面碰撞检测会把它们再打回去——但不允许漏报。这一步存在的理由与 [[culling]] 在渲染里的地位完全一致：早剔除、早止损。

**2. Collision detection**：对 broadphase 吐出的每一对 collider，精确判定它们是否真的相交，并且在相交时**生成 contact 信息**（法向、穿透深度、接触点位置）。注意这一点和渲染里的可见性判断很不一样：渲染只关心「可见 / 不可见」，物理却需要知道「穿了多深、应该往哪里推回去」。对简单几何（sphere-sphere、sphere-box、box-box）通常写 special-case 实现；对任意凸多面体，则走 [[collision-detection-gjk-epa|GJK / EPA / MPR]] 这一族算法。

**3. Resolution**：修正违规。所有 contact、弹簧、铰链、销点都被统一建模为**等式约束（equality constraint）**，物理引擎通过向刚体施加**冲量（impulse）**把它们的速度和位置调整回合法区间。Erin Catto（Box2D 作者）推广的 **Sequential Impulse** 是工业标准解法，本质是 Gauss-Seidel LCP 的一个高效变体——反复地一条一条约束迭代松弛，几何直觉是「多个半空间求交等价于一串点投影」。

## 与引擎层的关系

物理子系统在 [[engine-layering|引擎分层]] 里通常夹在 collision / scene 查询层和 gameplay 层之间；它对渲染几何无感，但它要求 [[ecs|ECS]] 或 component 系统把变换（transform）以 canonical 形式暴露出来。典型的 [[kinematic-character-controller|kinematic 角色控制器]]正是绕开这套完整流水线、直接手写 collider cast + penetration 查询的一个折中——因为完整的约束求解虽然物理正确，但手感飘，不适合玩家输入。

## 为什么这片领域难学

Allen Chou 把游戏物理称为 **tribal knowledge**：没有一本完整的书从 broadphase 讲到 sequential impulse，入门资料散落在 GDC 讲座、论坛帖、Box2D / Bullet / ODE 源码、以及少数个人博客（Box2D 的 Catto、Bullet 的 Erwin Coumans、Dirk Gregorius、Christer Ericson 的 *Real-Time Collision Detection*、Ian Millington 的 *Game Physics Engine Development*）里。要做一个能跑的物理引擎，约束求解、数值稳定性、continuous collision detection（CCD）、featherstone articulated bodies 这些子题目要一个个啃。

## Sources

- [[sources/allenchou-game-physics-introduction]]
