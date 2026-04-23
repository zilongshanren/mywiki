---
tags: [lightmap, baking, offline-lighting, global-illumination, area-light, dcc-tooling]
date: 2026-04-19
sources: 1
---

# Lightmap 烘焙工作流

「Baking（烘）」在渲染里指**把光照提前算好存成纹理**，运行时只是采样。不要跟「Cooking（炒）」混——后者是把数据直接序列化到磁盘以加速加载。

[[joost-van-dongen]] 在 *Proun* 里把整套静态关卡（lights 不动、几乎所有物体静止）全部用 lightmap 跑。代价是文件体积——lightmap 占整个游戏**三分之一**的磁盘——但换来的好处是**运行时承担不起**的那些效果可以白送：

- **Area light（面光源）**：阴影随距投射物体越远越糊，光源越大糊得越快。实时渲染要么退化成无限小光源的硬阴影、要么固定模糊量，Proun 直接离线算到正确的距离依赖软阴影。
- **Skylight（天空光）**：大气多向散射带来的来自全方向的弱光。让阴影不会「死黑」、细节更丰富。
- **Global illumination（间接光）**：红色物体会把一点红反射到相邻表面。在 Proun 的高饱和纯色几何上，这个效果尤其显眼——一块亮红面旁边的白墙会染上可见的红色晕。

**成本数据**：第二赛道烘一遍需要 van Dongen 的笔记本跑约 **30 小时**。但因为是离线、且 lights 不动，没人在乎速度。

**工具链**：Proun 的关卡编辑器本身就是 3ds Max 加一组自写插件——插件自动 unwrap 所有模型的 lightmap UV，再调用 **V-Ray** 渲出 lightmap。这套插件随游戏 beta 一起发布给玩家做关卡。值得学的点不在 V-Ray，而在「**把 DCC 工具 + 离线渲染器改造成引擎 pipeline 里的烘焙环节**」的 indie 式工具链——自己不写 baker，借一个成熟的影视渲染器。

**适用边界**：这一套的先决条件是静态——光源不动、大多数几何不动。关卡小到能存高分辨率 lightmap。动态 / 大世界 / 移动光需要走实时或混合方案（SH probe / SDF tracing / RTGI）。

## 相关

- [[screen-space-light-shafts]] —— 同作者、同作品的另一种「物理 vs 伪装」取舍
- [[colored-sky-sun-lighting]] —— 这套流程之上的艺术层
- [[joost-van-dongen]]

## Sources

- [[sources/joostdevblog-lighting-in-proun]]
