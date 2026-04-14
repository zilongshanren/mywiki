---
tags: [source, 游戏开发, 寻路, 导航网格]
date: 2026-04-14
sources: 1
---

# Meshes of navigation（Evan Todd / etodd.io）

[[people/evan-todd|Evan Todd]] 2010 年 5 月发表的一篇短文，记录他把开源项目 [Recast](https://recastnav.com/) 接入自己的第三人称对战游戏 A3P 的过程。

## 摘要

Todd 此前的 AI 是基于手放 waypoint 的，导致 bot 经常撞墙或在两个点之间来回跳。他发现 Recast 这个 C++ 开源导航网格生成器：输入多边形汤，输出基于体素栅格化的可行走 navmesh，参数化控制坡度、高度、agent 半径等。由于 Recast 开源，Todd 直接 fork 了 demo 源码，让它导出 `.obj`，再经过 Blender 中转到 Panda3D 的 `.egg`，最后在游戏中提取顶点数据作为 A\* 寻路图。整篇文章既是对 Recast 的推荐，也是早期独立开发者跨工具内容管线痛苦的缩影。

## 关键要点

- Recast 用体素化 + 区域生长自动生成 navmesh，参数化可控
- navmesh 从根本上解决了 waypoint AI 的"机械感"问题
- Todd 的工具链横跨 Recast → .obj → Blender → .egg → 游戏，靠人工修 import bug 粘合
- 文末还提了要专门写一篇讲 A\* 在 navmesh 上实现的后续（是否写了待查）

## 链接到的概念

- [[meshes-of-navigation-recast]]
- [[a-star-pathfinding]]
- [[kinematic-character-controller]]

## 原文

- 链接：https://etodd.io/2010/05/08/meshes-of-navigation/
- 本地：`raw/articles/etodd.io/2010-05-08_meshes-of-navigation.md`
