---
tags: [计算几何, cgal, arrangement, 多边形, 拓扑]
date: 2026-04-19
sources: 1
---

# CGAL Arrangement 导入多边形的三种策略与 antenna 陷阱

CGAL 的 `Arrangement_2` 是平面曲线排列的数据结构，把一堆可能自相交、互相重叠、甚至退化的曲线扫成一个有拓扑一致性的平面图（顶点 / 半边 / 面）。[[ben-supnik|Supnik]] 在 X-Plane 的地图生成里要把大量外部来的多边形（来源不可信、边可能自交、相邻多边形可能碰撞）灌进一个统一的 arrangement，然后回头问：**哪些面是「多边形内部」？**

问题之所以难，在于外部几何和 arrangement 之间不是 1:1 的关系：一个输入多边形可能被其它多边形切成多段，一个输出面可能来自多个输入的联合，而且输入本身可能有 antenna（从多边形内部伸出去又折回来的零宽尖刺）——这类退化结构会让朴素的「跨边翻转 inside/outside」策略失效。

## 三条导入路径

Supnik 总结 CGAL 里把多边形塞进 arrangement 的三种方法：

1. **general-polygon-set**：直接把多边形集合当代数对象做并 / 交。底层一次性 N 路分治合并 N 个面，比用户手写任何两两合并都快。适合「很多面做布尔运算」。
2. **overlay 自定义合并**：用 CGAL 的 `overlay` 自由函数，自己指定「两张 arrangement 的 face × face 该怎么组合」。适合需要携带数据、自定义语义的场合。
3. **curves 批量 insert**：把多边形拆成曲线一次性 `insert`，让 CGAL 的 sweep line 帮你把相交、拓扑、退化一锅煮熟。这是 Supnik 处理「来源不明的脏多边形」的首选。

## 批量 sweep 之后：怎么找内部？

选了方法 3 后要回答「哪些 face 是多边形内部」。Supnik 给了三种判定：

### 1. Bounded 测试（最简单）

一个多边形单独 sweep 进空 arrangement 后，所有 bounded 的 face 就是其内部。这只在「一次一个多边形」场景可用——多个多边形混进同一个 arrangement 时失效。解决办法是：每个多边形各自 sweep，再用 general-polygon-set 合并。

### 2. 外→内 toggle 策略

从无穷远开始往里走，每跨一条 halfedge 翻转一次「inside/outside」状态。halfedge 上挂的数据（来源曲线属性）可以在 toggle 时一并检查。

**antenna 陷阱**：多边形里的 antenna（零宽尖刺）是一条边，但它在同一个面里出入两次——遍历算法只 toggle 一次，结果错乱。更糟的是，*toggling 数据存在 edge 上而不是 halfedge 上*，所以即使你想用拓扑识别 antenna 也不行：「face()==twin()->face()」在原始多边形里是真的，但如果 antenna 的顶点恰好碰到另一个多边形变成真正的拓扑分割，这个等式就不再成立，antenna 就藏不住了。

两种绕法都需要「提前知道哪条是 antenna」：要么插入前就剔除，要么插入时不给 antenna 贴数据。

### 3. Winding rule（绕数规则）

用在 offset / Minkowski sum 一类几何运算里——只要**左转闭合轮廓**围起来的区域算内部。做法：插入曲线时记曲线方向，sweep 后比较 halfedge 与底层曲线的方向，在 halfedge 上打 inside/outside 标签，遍历时累加绕数。

这里 antenna 也会出问题——antenna 只有一个方向的曲线，但产生两条 halfedge，总有一条会被错标。但 Supnik 指出：做 offset buffer 的真实场景里几乎不会出现 antenna，这个限制可以忽略。

## 工程教训

这篇短文把一个看上去纯理论的几何问题拍回了工程层面：**拓扑数据结构的「干净抽象」在脏输入面前会漏**。antenna 问题的本质是「edge 粒度的数据标签对 halfedge 粒度的查询不够」——和 [[cgal-exact-arithmetic-mantissa-growth|CGAL 精确算术里 mantissa 增长]] 一样，都是 CGAL 为了给你「一致拓扑」承诺而必须付出的代价。在工业管线里，Supnik 的折中是：**预处理阶段检测并剔除 antenna**，再进 CGAL，比事后在 arrangement 上修拓扑便宜得多。

## 相关

- [[cgal-exact-arithmetic-mantissa-growth]]
- [[ben-supnik]]

## Sources

- [[sources/supnik-cgal-arrangements-import]]
