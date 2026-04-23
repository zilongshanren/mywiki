---
tags: [游戏引擎, 物理, 动画, 场景图, bitsquid]
date: 2026-04-19
sources: 1
---

# 布娃娃的速度继承

一个角色从动画切到 ragdoll 的瞬间，最直观的 bug 是**原地瘫倒**——动画里那股冲势没有传进物理系统。要让 ragdoll 带着动画已有的线速度和角速度一起"扑街"，就得在切换那一刻把动画对象的速度取出来、喂给物理体。

Niklas Frykholm 在 2012 年给出的这篇解法，有趣之处不在公式（线速度取位置差分、角速度由四元数差分和 axis-angle 分解），而在于**如何在一个 physics / scene graph / animation 三系统互不相识的架构里把这个数据跨出来**——这是 Bitsquid 「系统之间 coupling 越少越好」哲学的一次实战。

## 架构前提

Bitsquid 的物理、场景图、动画是**三个互不耦合的系统**。骨骼和刚体都只握住**场景图节点的整数索引**——这是它们的唯一共同语言。动画系统求完 curve 之后把 local transform 写进骨骼对应的节点；关键帧物理（被动画驱动的 hit body）从节点读世界变换；ragdoll 相反，物理算完把世界变换写回节点。这种 [[system-decoupling-patterns]] 下获取"一帧前的 transform"就变成了核心问题。

## 四条候选方案与取舍

**对动画曲线求导**。理论可行，工程上噩梦——不仅要对每条 curve 做微分，还要穿过 blend tree、local-to-world 链、IK、脚本驱动的位移等一切并非来自动画本身的运动来源。Niklas 直接放弃。

**倒退一帧再仿真一次**。多人 FPS 服务器做 hit 判定时确实会倒退时间，但为了拿个速度就重跑一遍仿真，工程复杂度远远大于收益。

**切换到 ragdoll 时延迟一帧**。看起来最便宜，但**违反 Bitsquid 的"不许延迟一帧"原则**——这是 Niklas 在文中顺便写下的一条重要设计戒律，见 [[no-frame-delays-principle]]。延迟一帧让对象处在"既是 A 又还不是 B"的灰色状态，会像癌细胞一样在代码里扩散出 `if (transition_to_ragdoll)` 这种补丁逻辑。

**在场景图里常驻 `last_world`**。每帧把上一次的世界变换 memcpy 一份保存下来，ragdoll 要用的时候直接差分。代价是场景图内存多 50%、加一次 memcpy。Niklas 选了这条——理由是**没有明显赢家时优先选最简单**，而且此方案事后还好优化：只给能变 ragdoll 的节点开 `last_world`、用 `(p,q)` 代替 4×4 矩阵、两个 buffer 做指针对换等等。

## 指针对换的陷阱

评论区有人提议"直接把 `world` 和 `last_world` 两个缓冲区指针交换"——这是经典 double-buffer 的思路。Niklas 的回复点破了陷阱：**场景图并不是每帧全量变换所有节点**，只变换"dirty"的那一小部分（本地矩阵或父节点变化过的）。指针对换之后，你必须变换**所有**节点才能保证 world 和 last_world 一致，总成本反而比"memcpy 一份 + 局部变换"更高。**增量计算的数据结构，没法无脑套 double buffer**——这是对任何脏标记系统都成立的一条隐形约束。

## 计算公式

拿到 `tm_0`、`tm_1` 两个世界矩阵后，线速度就是位置差分：`v = (p1 - p0) / dt`。角速度通过 `q = q1 * inverse(q0)` 得到增量旋转，再做 axis-angle 分解：`ω = axis * angle / dt`。评论区补充了两个重要订正：

- **位置应当取刚体质心**，不是节点原点——`v = (tm_1 * COM_local - tm_0 * COM_local) / dt`。
- **角速度有更便宜的近似**：`ω ≈ 2 * (q1 - q0) * conjugate(q0) / dt`，省掉 axis-angle 分解。

另一条网友提议——**向前仿真一帧**取代向后仿真，得到的速度落在同一邻域，工程上比向后走简单得多；但它忽略不了 IK 等非动画来源的位移。向前仿真也可以顺带喂给 per-object motion blur 的速度 buffer，一个数据两用。

## 相关

- [[system-decoupling-patterns]] — 场景图 / 动画 / 物理互不相识的代价就是跨系统数据获取要专门设计
- [[no-frame-delays-principle]] — 本文顺带立起的 Bitsquid 核心戒律
- [[per-entity-scene-graph]] — Bitsquid 的场景图实现
- [[scene-graph-matrix-stack-visitor]]
- [[game-physics-engine]]
- [[exponential-map-rotations]] — 角速度与四元数差分在指数映射下的等价视角
- [[niklas-frykholm]]

## Sources

- [[sources/bitsquid-inheriting-velocity-ragdolls]]
