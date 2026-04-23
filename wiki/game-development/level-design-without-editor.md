---
tags: [level-design, tools, indie, 2d, procedural]
date: 2026-04-19
sources: 1
---

# 没有关卡编辑器时怎么做关卡（Swords & Soldiers 实践）

Ronimo Games 做 Swords & Soldiers（一个程序员的主机项目）时没来得及写正式的 2D 关卡编辑器，靠几条朴素的数据约定完成了一整张 Wii 评分 9 分的美术关卡设计。Joost van Dongen 把这套做法拆成三层。

**核心 gameplay 数据直接用 Notepad**：因为游戏本质在一条线上展开，每一行文本对应一类信息——金矿位置、塔位置、地形高度、地形类型（岩石/雪/草地）。设计师直接编辑行文本即可，没有图形工具也不妨碍理解和迭代。美术想摆装饰物（props），就多开几行，每个 prop 给一个字符代号，对着 prop 表在 Notepad 里敲字符摆位置。「有一种硬核 hacking 感」，但够用。

**关卡曲线自然化用两层模糊**：设计师给的高度值不直接当顶点高度用，先做邻域平均（blur）得到平滑曲线；再加一层地表贴花（tiling texture 里画了小起伏），把剩余的 triangle strip 数学味藏掉。看起来像手绘的地形，其实数据极稀疏。

**背景/前景走程序化放置**：多层视差 + 每层一组背景元素（近处摇曳的树、中景山丘、远景山脉、云），引擎随机放置。美术通过「这层多密 / 这层完全移除」+ 「每关一张背景渐变 + 大气雾渐变」两个旋钮来做沙漠、山地、森林的差异。**代价**：做不出「这一关背景里有座城」这种独一无二的地标；重复感会积累，只能靠两条渐变遮掩。

教训：有时把工具成本换成一点美术自由度受限是划算的，但设计师必须对「地标级独特性」的缺失做心理准备。RoniTech 2 后来补上了正式的 in-game 关卡与美术编辑器。

## 相关
- [[tools-first-iteration-loop]] —— 工具优先 vs 工具延后的权衡
- [[game-settings-hot-reload]] —— 同样是最小成本拿到设计师可迭代性

## Sources
- [[sources/joostdevblog-designing-levels-without-tools]]
