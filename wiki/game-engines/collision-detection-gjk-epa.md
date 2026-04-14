---
tags: [游戏物理, 碰撞检测, gjk, epa, mpr]
date: 2026-04-14
sources: 1
---

# GJK / EPA / MPR：凸几何碰撞检测三件套

在 [[game-physics-engine|物理引擎的流水线]]里，broadphase 剔完之后，剩下的 collider 对要进入**精确碰撞检测**。对简单图元（sphere、box、capsule）可以写 special-case，但要支持任意凸多面体（polyhedron、cone、pyramid、convex hull），手写所有两两组合是不现实的——于是工业界转向**通用的凸形状算法**：GJK、EPA、MPR。

## GJK：只回答「相交 vs 不相交」

**Gilbert–Johnson–Keerthi** 是凸几何相交判定的经典算法。它基于 Minkowski 差：两个凸集 $A, B$ 相交当且仅当 Minkowski 差 $A \ominus B$ 包含原点。GJK 不显式构造这个差集，而是通过**支持函数（support function）**在需要的方向上采样极值点，然后在一个维持的最多 4 点单纯形（simplex）里迭代地「向原点逼近」。

GJK 的**致命限制**：它只告诉你「碰没碰」，不给你 contact 信息。物理解算需要知道 contact position、contact normal、penetration depth——GJK 不产出任何这些。于是它通常和 EPA 配对。

## EPA：补全 contact 信息

**Expanding Polytope Algorithm** 接着 GJK 的结尾单纯形跑。当 GJK 判定相交时，当前 simplex 已经包住原点；EPA 把这个 simplex 作为初始多面体，每次沿最靠近原点的面向外扩展，直到收敛出 Minkowski 差的边界点。这个边界点所在的法向就是 **penetration normal**，到原点的距离就是 **penetration depth**，由此反推出世界空间的 contact 点。

GJK + EPA 的组合是 Bullet 3D、Box2D 早期版本等工业引擎的主力路径。缺点是 EPA 的稳定性与精度比 GJK 更敏感——退化 simplex、平行面、数值抖动都会让它炸掉。

## MPR：单算法、直接出 contact

**Minkowski Portal Refinement**（又名 XenoCollide，Gary Snethen 提出）把 GJK 和 EPA 的两步合并成一步。MPR 从 Minkowski 差里挑一个内部点开始，构造一个「portal」三角形，然后反复细化 portal 直到它贴住边界。和 GJK+EPA 不同，MPR 的中间状态就直接包含生成 contact 所需的信息——不用二次扩展，数值上也更容易稳。代价是代码不如 GJK 那样教学清晰。

## 为什么都只吃凸形状

这三个算法都建立在凸几何的基本事实上：Minkowski 差仍是凸的、支持函数有唯一极值点、任意凸集与点的最近距离可以通过单纯形投影求。对凹几何，Minkowski 差不再是凸的，原点判定会给假阴性。因此 [[game-physics-engine|物理引擎]]统一把凹 collider 在建模阶段就**预拆成一组凸 collider**——哑铃拆成两个球加一根胶囊，而不是让检测算法去处理整体的凹形。

## 相关

- [[game-physics-engine]]
- [[rasterization]]（渲染端的可见性判定相比物理端的相交判定：只需 0/1 信息，不需要穿透深度）

## Sources

- [[sources/allenchou-game-physics-introduction]]
