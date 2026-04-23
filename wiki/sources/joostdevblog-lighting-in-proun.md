---
tags: [source, rendering, lightmap, baking, global-illumination, tooling, indie]
date: 2026-04-19
sources: 1
---

# Lighting in Proun（Joost van Dongen / Joost's Dev Blog）

[[joost-van-dongen]] 2010 年 11 月发表的文章，讲 *Proun* 视觉为什么好看——不是很多人猜的 DOF 景深，而是**精心的烘焙光照**。

## 摘要

*Proun* 场景静态（光不动、物体不动），van Dongen 用 lightmap 把所有光照离线算好存纹理——**lightmap 占整个游戏磁盘的 1/3**，但换来实时承担不起的效果。三样关键技术：**面光源 area light**（阴影随距离越远越糊）、**skylight**（来自全方向的弱光让阴影不死黑）、**global illumination**（亮红物体会把红色反射到邻近白面上——在 Proun 的纯色几何上尤其显眼）。代价是机器时间：第二赛道的 lightmap 在他笔记本上跑约 30 小时。工具链：**关卡编辑器本身就是 3ds Max + 自写插件**，插件自动 unwrap lightmap UV、再调 V-Ray 渲；这套插件随 beta 发给玩家自制关卡。评论里他承诺「Proun 完工后要做 Diablo 视角下的实时 area light shadow」。

## 关键要点

- 「baking」= 预烘光照到纹理；「cooking」= 数据直接序列化到磁盘（别混）
- Lightmap 占磁盘 1/3，换来：area light / skylight / GI
- 第二赛道烘一遍 ≈ 30 小时（笔记本）
- 工具链：3ds Max + 自写插件 + V-Ray，auto-unwrap lightmap UV
- 关卡编辑器 = 改造版 3ds Max，随游戏发给玩家
- 先决条件：光静止、几何静止、关卡小（能存高分辨率 lightmap）

## 链接到的概念

- [[lightmap-baking-workflow]]
- [[colored-sky-sun-lighting]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2010/11/lighting-in-proun.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2010-11-20_lighting-in-proun.md`
