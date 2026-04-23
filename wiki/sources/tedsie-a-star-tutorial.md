---
tags: [source, unity, 寻路, a-star, 教学]
date: 2026-04-19
sources: 4
---

# A* 寻路演算法 Unity 实作系列（Ted Sie, 2016-07）

[[ted-sie]] 于 2016 年 7 月发表的 A\* 寻路四篇系列教学，以 Unity + C# 从零实作一个 grid-based A\* 寻路器。四篇对应"演算法简介 / 定义 Node / 生成 Node / Node 排序"四个步骤，是面向初学者的经典 tutorial，并非算法研究。

## 摘要

系列从 Dijkstra 对比引入 [[a-star-pathfinding]]，给出标准 Heuristic 公式 `F(n) = G(n) + H(n)` 和 Open/Close list 伪代码；随后用 C# 定义 `Node` 类记录 `G_Cost` / `H_Cost` / `isObstacle` / `parent` / `position`，并让其继承 `IComparable`、在 `CompareTo` 里按 `G+H` 从小到大排序。接着用 `NodeManager`（单例 MonoBehaviour）按 `numOfRows × numOfColumns` 生成二维 Node 数组，初始化时用 `Physics.Raycast` 从下向上打射线判定哪些 cell 落在 `Obstacle` tag 的物件下，并用 `OnDrawGizmos` + `Debug.DrawLine` 在 Scene 里画出 grid 可视化；`GetNeighbours` 返回 4 邻域（上下左右）。最后 `NodeSort` 基于 `ArrayList.Sort()` 封装 Open list 的 `Push/Remove/Contains/First`，利用 `Node.CompareTo` 自动按 F 值维持排序——作者注明这是 bubble-sort 级别的 O(n²) 实作，仅为教学清晰，不是效率最优，并提示可改用 heap sort。

## 关键要点

- 教学定位：代码全部直接贴出，以 Unity C# + MonoBehaviour 为前提，GameObject/Prefab/Inspector 工作流
- 数据结构：`Node` 以 position + G/H/parent/isObstacle 为核心，开放列表用朴素 `ArrayList` 包装
- 启发公式：`F = G + H`，`H` 未指定具体度量（后续 implement 篇才展开）
- 邻居拓扑：本批 4 邻域，后续 eight-ways 篇引入对角线
- 障碍判定：初始化阶段一次性 raycast，不支持运行时动态增删障碍
- `CompareTo` 原文有笔误（第二个比较写成 `this.H_Cost` 而非 `node.H_Cost`），读者在评论区指出
- 排序实作是 O(n log n) 的 `ArrayList.Sort` + 每次 Push/Remove 都重排——即 O(n² log n)，教学清楚但实际项目应换优先队列

## 链接到的概念

- [[a-star-pathfinding]]

## 原文

- Introduction：<https://tedsieblog.wordpress.com/2016/07/08/a-star-algorithm-introduction/>
- Node Definition：<https://tedsieblog.wordpress.com/2016/07/08/a-star-algorithm-node-definition/>
- Node Generate：<https://tedsieblog.wordpress.com/2016/07/08/a-star-algorithm-node-generate/>
- Node Sort：<https://tedsieblog.wordpress.com/2016/07/08/a-star-algorithm-node-sort/>
- 本地：`raw/articles/tedsieblog.wordpress.com/2016-07-08_a-algorithm-*.md`
