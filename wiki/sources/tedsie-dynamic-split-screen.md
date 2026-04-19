---
tags: [source, unity, camera, multiplayer]
date: 2026-04-19
sources: 1
---

# 动态分屏（Ted Sie / 阿祥的开发日常）

[[ted-sie|Ted Sie]] 发表于 2020 年 4 月的文章，讲解 Unity 中动态分屏（按玩家位置动态切分画面）的实现思路与平滑过渡处理。

## 摘要

多人本地游戏常用水平/垂直分屏，但固定分屏让玩家难以感知彼此相对位置。动态分屏按两位玩家的世界坐标动态切分画面——玩家接近时退化为共用视野，走远后沿连线方向切开。作者按"玩家中点 → 分割方向 → 相机偏差 → 剪裁平面"的流程拆解概念实现，并指出直接切换会产生顿感，解决方法是让相机偏差随距离平滑变化（退化为共视到完全分屏之间有个可调曲线）。文章定位为教学型案例，配 GIF 展示效果。

## 关键要点

- 动态分屏的价值是让玩家同时获得"自己视野"和"对方方位"的信息。
- 核心计算：两玩家中点 + 连线方向 → 两台相机各自的偏差与裁剪平面。
- 过渡优化靠 shaping 曲线把二态切换变成连续插值。
- 参考 Math for Game Programmers "Juicing Your Cameras With Math" 与 MattWoelk 的 Voronoi Split Screen 笔记。

## 链接到的概念

- [[dynamic-split-screen]]
- [[shaping-functions]]

## 原文

- 链接：https://tedsieblog.wordpress.com/2020/04/01/dynamic-split-screen/
- 本地：`raw/articles/tedsieblog.wordpress.com/2020-04-01_dynamic-split-screen-dong-tai-hua-mian-fen-ge.md`
