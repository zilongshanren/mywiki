---
tags: [source, bitsquid, ai, 寻路, 导航]
date: 2026-04-19
sources: 1
---

# A* is Overrated（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2010 年 10 月 Bitsquid Blog。对"把导航问题 = A\* 问题"这种流行误解的反击。核心论断：A\* 只是导航问题里**很小**的一部分，而且通常不是最难也不是最重要的那部分。

## 摘要

A\* 因为"算法正确性可证明 + 问题定义简洁"在教科书里无处不在，但游戏里三条现实削弱了它的重要性：

1. **多数敌人只在屏幕上出现几秒就被击杀**，玩家根本看不清它是否在沿路径走——更该把精力放在可见行为上。
2. **A\* 不一定是最佳寻路算法**——游戏通常只要"够短、看起来合理"；远距离搜索用 **hierarchical** 结构对性能的影响远大于每层的算法选择；寻路时间尺度是秒级的，可以用增量+并行搜索摊平。
3. **即使用 A\***，外围问题都比搜索本身更硬：open list 用堆还是链表、访问标记用哈希表还是节点 flag（flag 无法支持并发查询）、图怎么自动生成、动态阻挡怎么失效 in-flight 查询、路径跟随时怎么避让其它 agent、physics 与 navgraph 不一致怎么办。

Niklas 最在意的其实是 **local navigation**：玩家不会因为路径不是最短而抱怨，但会因为 agent 卡墙原地转圈马上注意到。评论区 [Detour/Recast 作者 Mikko Mononen](http://digestingduck.blogspot.com/) 补上工业级经验：agent 的 movement 必须严格约束在 navgraph 上；路径要存 **corridor**（一串多边形走廊）而不是 polyline；脱离 navmesh 时直接 kill agent（亚历山大式解法）比救回来更干净。作者顺手举了 Diablo 2 雇佣兵用纯 A\* 跟随玩家、一被怪挡住就绕到半张地图外再也回不来的典型反例，论证"follow 一个动态目标不该用纯 A\*"。

## 关键要点

- **寻路 ≠ 导航**：A\* 在整个导航系统里只是一块小拼图。
- 真正想要的算法是 **incremental、parallel、hierarchical、返回近似最短**——不是教科书的 textbook A\*。
- **分层结构**对远距离搜索性能的影响远超算法优化——把 50k 节点的大图硬算 A\* 基本是设计错误。
- **agent movement 严格约束在 navgraph 上**（Mikko）；脱网时就 kill，别救。
- **Corridor-based path**（多边形走廊）比直线 polyline 鲁棒得多——目标小幅移动可以修 corridor 而不必 replan。
- **local navigation** 才是玩家眼里 AI 是否靠谱的决定性因素，比 A\* 本身重要得多。
- Diablo 2 雇佣兵是**寻路工具错用**的经典反例；follow mode（回溯玩家步伐 + 局部小搜索）才是对的。
- 评论里也有支持 A\* 的声音（放大启发项退化为 local search、incremental A\*、单线程高吞吐更重要），Niklas 补充说他主要反对的是 **"有导航问题？套 A\* 就好了"的 cargo-cult 态度**，而不是 A\* 本身。

## 链接到的概念

- [[a-star-pathfinding]]
- [[local-navigation-over-pathfinding]]
- [[meshes-of-navigation-recast]]
- [[kinematic-character-controller]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2010/10/is-overrated.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2010-10-20_a-is-overrated.md`
