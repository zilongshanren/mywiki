---
tags: [character-controller, dots, unity, physics, ecs]
date: 2026-04-14
sources: 1
---

# Kinematic 角色控制器

角色控制器（character controller）在游戏里通常分两条路：rigidbody 控制器和 kinematic 控制器。两者的分水岭是「谁在对这个角色拥有最终解释权」。

**Rigidbody 控制器**把角色交给物理引擎：通过施加力和冲量来驱动位置，引擎自己处理碰撞、滑行、反弹。好处是与场景里其它物理物体天然耦合；坏处是手感「像踩在冰上」——惯性、摩擦、恢复系数都是物理参数而非玩家感觉，微操难度大。更麻烦的是遇到台阶时，刚体会被水平推力卡在竖直面前，无法自动上台阶。

**Kinematic 控制器**则放弃把角色当物理对象：每帧自己算速度、自己投射碰撞、自己决定「能走就走、不能走就贴着墙滑、遇到矮坎就抬腿上去」。代价是所有 corner case 都要你亲自处理——它出名地难写对。

## 一个最小 DOTS 实现的解剖

Steven Sell 在 Unity DOTS（Entities + Physics）上给出了一个典型骨架，涉及 [[ecs]] 范式里 component + system + job 的拆分：

- `CharacterControllerComponent` 装**纯数据**：输入（当前方向、速度量、跳跃请求）、控制参数（最大速度、跳跃力、最大台阶高度、拖拽）、内部状态（是否在地面、当前跳跃速度）。
- `CharacterControllerSystem` 是一个 `IJobChunk`，调度时声明在 physics world 更新之后、物理 group 结束之前，并通过 `JobHandle.CombineDependencies` 把 `ExportPhysicsWorld` 的输出织进依赖链，确保物理数据是最新的。
- 水平和竖直速度**分开存储**：总速度 = `gravityVelocity + jumpVelocity + horizontalVelocity`，三者各自独立推进，这样 gravity 为零时跳跃向量不会被误清零、地面上跳跃不会被重力抵消到看不见。

## HandleChunk 的 invariant 循环

控制器核心是每帧对每个角色实体跑一遍 `HandleChunk`：

1. **重力位移**。从当前位置出发加一个小 epsilon（向上 1e-3 之类），避免角色贴地时把自己和脚下平面误判为穿插。把 `gravity * dt` 作为试探速度，做 `ColliderCastAll`。如果没碰到，直接落入新位置；如果碰到，用 `ColliderDistance` 查询 penetration 深度，沿 surface normal 把自己推出表面，再做一次补 cast 防止被推进下一块几何。
2. **跳跃与 drag**。跳跃是「瞬时爆发速度」而不是持续加速：满足「grounded + 跳跃请求 + 前一次跳跃已结束」时，把 `jumpVelocity` 设为反重力方向一次性冲量，之后每帧靠 `Drag` 参数缓慢衰减。关键：要把 `jumpVelocity` 写回 component，让下一帧能看到衰减后的值。
3. **grounded 判定**。不能只做一条中心线 raycast——中心刚好悬空在小坑上时会误判为离地。这个实现打 5 条 raycast（中心 + 四周小偏移，偏移量从 collider bounds 比例取）。也不能改成一个 collider cast：那样贴墙下落也会被报成 grounded，允许了不想要的 wall jump。
4. **水平位移 = 先试 step，再退 slide**。把 `horizontalVelocity = direction * magnitude * dt` 作为 target。cast 若无碰撞直接走；若撞到东西，先做一次**自上而下** collider cast：从 `targetPos + (0, MaxStep, 0)` 垂直打到 `targetPos`，如果 `Fraction != 0`，说明 target 上方 MaxStep 之内有净空，把 target 抬起来 → 爬楼梯效果。如果抬不起来（撞到墙），改走 slide：对所有 penetration hit 累计 `SurfaceNormal * -Distance`，把水平速度投影掉冲入墙的分量，沿着墙面继续走。

## 设计取舍与 invariants 破坏

作者坦白了几个留给读者的 edge case，它们都是 kinematic 控制器反复被咬的典型位置：

- **不积分、只走单步**。每帧只做一次「试探 + 修正」，这意味着**高速移动会直接穿透薄墙**——试探终点已经在墙的另一侧，cast 不会命中。修正办法是对速度做 substep。
- **收窄的走廊**。两堵墙呈小角度相交时，slide 的累加投影会互相抵消，角色最终停住但表现难看。
- **不限制坡度**。能在任意陡度斜坡上不下滑，但这是重力在 grounded 时被人为置零的副作用——会出现垂直墙也能站稳的病态情形，生产系统里通常还要一个坡度上限。
- **移动平台 / 物理对象互动**缺席。

这些没解决的点恰好说明：kinematic 控制器的任何「基础版」都只是一个 invariant 维护器，每个新 invariant（坡度、平台、穿透预防）都会和既有的几条撞出新的 corner case。这也是 [[ecs]] 下数据/逻辑分离带来的好处——这些 invariant 都可以以新的 job/system 插进来，而不必重写核心结构。

## Sources

- [[sources/vertexfragment-dots-character-controller]]
- [[sources/allenchou-game-physics-introduction]]
