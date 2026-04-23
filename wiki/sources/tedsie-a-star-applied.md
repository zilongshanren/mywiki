---
tags: [source, unity, 寻路, a-star, 教学]
date: 2026-04-19
sources: 4
---

# A* 寻路 Unity 实作系列 · 应用篇（Ted Sie, 2016-07-10）

[[ted-sie]] 于 2016 年 7 月 10 日连发的 A\* 教学续作四篇，承接前作 [[sources/tedsie-a-star-tutorial]]（Node 定义 / 生成 / 排序四篇基础），给出完整的 `AStar.FindPath` 实作、8 邻域（对角线）扩展、Line-of-sight 后处理以及基于 raycast 的运行时障碍判定。整组相当于把伪代码落地到 Unity Scene，并做两次最明显的优化。

## 摘要

`AStar.cs` 以静态方法 `FindPath(start, goal)` 封装核心循环：初始化 `openList`/`closedList`（都是前作的 `NodeSort`），`start.G_Cost = 0`、`H_Cost = (goal.pos - cur.pos).magnitude`（欧氏距离启发式）；每轮从 `openList` 取排序后第一个节点，若等于 goal 则回溯 `parent` 链反转为路径；否则用 `NodeManager.GetNeighbours` 取邻居，未在 closed 且未在 open 的加入 open 并记录 G/H/parent，已在 open 的则用当前 G+cost 与旧 G 比较择小更新——这是标准 A\* 伪代码的直译。

**8 邻域扩展**：在原 4 邻域（上下左右）基础上，`GetNeighbours` 追加 4 个对角邻居，路径更接近欧几里得直线，移动距离更短。作者没处理对角穿墙与 `sqrt(2)` 代价修正，属于教学级省略。

**Line-of-sight 优化**：在 `CalculatePath` 返回前套一层 `LineOfSight(path)`：用 `Physics.Linecast(startNode, nextNode)` 遍历折线，若两点间无碰撞就跳过中间节点，保留视线被挡时的最后一个可见点作为新 waypoint。相当于在 grid 约束下做路径平滑（path smoothing），把锯齿状 grid 路径压缩成对角直线段。

**障碍判定**：在 `NodeManager.CreateNodes` 生成每个节点时，从 cell 下方发向上的 `Physics.Raycast`，命中 tag 为 `Obstacle` 的物件就调 `node.MarkAsObstacle()`。判定一次性完成，不支持运行时动态更新。

`TestAStar.cs` 是结果展示脚本：把起点 / 终点两个 Cube 拖入 Inspector，每 `intervalTime` 秒调一次 `FindPath`，用 `OnDrawGizmos` + `Debug.DrawLine` 在 Scene 中把路径画成绿线。无新算法内容，仅为 wiring。

## 关键要点

- **启发函数**：欧氏距离 `(goal.pos - cur.pos).magnitude`——与 8 邻域搭配天然 admissible
- **open/closed 操作**：全部走前作 `NodeSort`（朴素 `ArrayList.Sort`），保持教学一致性，效率次要
- **8 邻域**：简单加 4 个 diag 分支，**未做对角代价修正**也**未做 corner-cutting 禁止**——工程上应该处理
- **LOS 平滑**：`Physics.Linecast` 做 post-process，把 grid path 折线段按可见性合并；是 [[a-star-pathfinding]] 的常见后处理技巧
- **障碍烘焙**：启动时向上 raycast 打 Obstacle tag，设计上等同静态 navmesh 烘焙
- **运行模式**：`TestAStar` 每秒重算一次，说明整条路径被当作 full replanning 而非增量更新，适合教学但大场景不可行
- **作者对 goal 不可达情况**：`openList` 空但 goal 未命中时仅 `Debug.LogError("Goal Not Found")` 后返回当前 node 的 `CalculatePath`——其实应当返回 null，属于教学代码小瑕疵

## 链接到的概念

- [[a-star-pathfinding]]

## 原文

- Implement（虚拟代码实例化）：<https://tedsieblog.wordpress.com/2016/07/10/a-star-algorithm-implement/>
- Eight Ways（斜向优化）：<https://tedsieblog.wordpress.com/2016/07/10/a-star-algorithm-eight-ways/>
- Line of Sight（可视点优化）：<https://tedsieblog.wordpress.com/2016/07/10/a-start-algorithm-line-of-sight/>
- Obstacle Detection（障碍物判定）：<https://tedsieblog.wordpress.com/2016/07/10/a-star-algorithm-obstacle-detection/>
- Achievement（实作成果，已合并进摘要的 wiring 段）：<https://tedsieblog.wordpress.com/2016/07/10/a-star-algorithm-achievement/>
- 本地：`raw/articles/tedsieblog.wordpress.com/2016-07-10_a-algorithm-*.md`
