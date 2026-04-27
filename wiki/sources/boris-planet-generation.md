---
tags: [source, 程序化生成, 地形, 模块化, wfc, 球体网格]
date: 2026-04-27
sources: 1
---

# How Does Planet Work（Boris The Brave）

[[people/boris-the-brave]] 发表于 2022 年 12 月的文章，深度拆解 Oskar Stålberg 2016 年小游戏 *Planet* 的程序化地形系统。

## 摘要

*Planet* 的世界是一个测地球面（geodesic sphere），由近似等边三角形铺满。用户通过点击顶点修改"高度"与"地形类型"两个隐变量，游戏据此重新选取覆盖相关三角形的**模块**（预制网格片段）。为控制模块总数，游戏将高度图转换为三维格点布尔阵列，再用类 Marching Cubes 方法为三棱柱（triangular prism）选取模块，高度不连续处有专用"悬崖"变体模块。多种地形类型（冰川、城墙、树林）通过各自的派生高度图叠加渲染，无需扩大基础模块集。城市中心使用固定预制建筑覆盖顶点以打破三角网格感。文章指出，*Planet* 处于 Brick Block（Marching Cubes 原版）与后来基于 WFC 的 Townscaper 之间，证明了在 [[wave-function-collapse]] 之前也能做出自然感强的程序化外观。

## 关键要点

- 底层是测地球面（geodesic sphere），对偶结构为 Goldberg 球（六边形 + 12 个五边形）
- 用户编辑对偶网格的面，而非基础三角形——Brick Block 以来 Stålberg 作品的共有模式
- 高度图→3D 格点布尔→三棱柱 Marching Cubes，使同一模块在多种高度差下复用
- 多地形类型用"分层高度图叠加模块"解决，而非枚举所有组合
- 后期视觉润色（自定义 AO、波浪模拟、极地积雪 shader、体积云）彻底遮蔽了模块边界

## 链接到的概念

- [[game-development/planet-tile-assembly]]
- [[game-development/wave-function-collapse]]
- [[rendering/marching-cubes]]
- [[game-development/triangle-grid]]

## 原文

- 链接：https://www.boristhebrave.com/2022/12/18/how-does-planet-work/
- 本地：`raw/articles/boristhebrave.com/2022-12-18_how-does-planet-work.md`
