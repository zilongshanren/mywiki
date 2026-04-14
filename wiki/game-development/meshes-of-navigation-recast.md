---
tags: [游戏开发, ai, 寻路, 导航网格, 工具链]
date: 2026-04-14
sources: 1
---

# 导航网格与 Recast 的体素化生成

导航网格（navigation mesh，navmesh）是把"哪里能走"表达为一张可行走的多边形网面，是 3D 大场景下 [[a-star-pathfinding|A*]] 搜索最常用的底图。相比早年 FPS/RTS 里常见的手摆 waypoint 图或栅格寻路，navmesh 的优势在于**几何就是拓扑**——边就是可达性，面就是安全区，人物在面内任何位置都能路径平滑插值，不会出现绕着节点打转或者贴墙走的机械感。

## Recast 的核心流程

[[people/evan-todd|Evan Todd]] 在 2010 年为自己的 A3P 项目接入了开源的 [Recast](https://recastnav.com/) 导航网格生成器，并把它从"AI 最大的短板"直接拉到可用水平。Recast 的做法是**体素化**驱动的自动生成：

1. 把输入的多边形汤（polygon soup）栅格化为一个巨大的体素场（voxel / heightfield）。
2. 在体素层级识别地表，丢弃那些坡度过陡、头顶空间不够、离边缘太近等参数不满足的非可行走体素。
3. 用区域生长把剩余体素分成若干连通区。
4. 提取区域边界、三角化、简化，得到最终的 navmesh。

关键在于所有"能不能走"的判据都是**参数化**的：角色高度、允许坡度、爬高、Agent 半径等都以体素为单位喂进去。这让 navmesh 生成和运行时角色控制器的假设对齐——[[kinematic-character-controller]] 能过去的地方，navmesh 才标记为可达。

## Todd 的工具管线

Todd 的问题不是生成算法本身，而是**把 Recast 的结果送进自己的运行时**。他的 workaround 很原始但很 Indie：改 Recast demo 源码，让它导出 `.obj`，然后导入 Blender 修修补补，再走 Panda3D 的 `.egg` 导出链，最后在游戏里解析顶点数据跑 A\*。

这段吐槽折射出早期独立游戏引擎的一个通病：内容管线横跨三四个外部工具，每一步都要手动修 import 错误、剔退化三角形。Todd 后来自嘲这几乎比算法还痛苦，也是他后来转向自研引擎的原因之一。

## 和 A\* 的关系

Recast 负责**空间离散化**，A\* 负责**图上搜索**。两者的边界是干净的：navmesh 的每个多边形是 A\* 图的一个节点，邻接的公共边是连接。真正影响游戏性的还是 A\* 的 [[a-star-pathfinding|g(n) 代价函数]]——比如危险区、掩体偏好——和导航网格本身几何是否干净。

## 相关

- [[a-star-pathfinding]] — navmesh 上运行的搜索算法
- [[kinematic-character-controller]] — 角色控制器定义了 navmesh 参数
- [[people/evan-todd]]

## Sources

- [[sources/etodd-meshes-of-navigation]]
