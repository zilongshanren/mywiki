---
tags: [game-development, 程序化生成, 地形, 模块化, marching-cubes, 球体网格]
date: 2026-04-27
sources: 1
---

# Planet 的瓦片组装系统（Planet Tile Assembly）

Oskar Stålberg 2016 年的设计玩具 *Planet* 在球形世界上实现了无缝程序化地形，其核心机制是一套基于**测地球面 + 类 Marching Cubes 模块选取**的瓦片组装系统。它是 Brick Block（Marching Cubes 原版）与后来基于 [[game-development/wave-function-collapse|WFC]] 的 Townscaper 之间的演进节点，证明了不依赖 WFC 同样能做出有机感强的程序化外观。

## 球面基础结构

底层网格是**测地球面**（geodesic sphere）：由近似等边三角形铺满的多面体。其对偶结构称为 Goldberg 球（Goldberg polyhedron），由六边形加上恰好 12 个五边形组成（类似足球）。

用户通过游标编辑**对偶网格的面**（即测地球面的顶点），每个顶点存储两个隐变量：高度（8 级）和地形类型。这是 Stålberg 自 Brick Block 以来贯穿所有作品的选取范式——用顶点数据驱动面上的模块选择。

## Marching Cubes 变体

问题：有 8 级高度 × 4 种地形 × 每三角形 3 顶点，组合爆炸，无法手工预制全部瓦片。

解决方案：先**忽略地形类型**，只处理高度差。将高度图转换为三维格点布尔阵列（格点是否在高度阈值之下），然后用类 Marching Cubes 方法在**三棱柱**（triangular prism，6 顶点）而非立方体（8 顶点）上选取模块，组合数大幅减少。高度差 ≥ 2 时使用专用悬崖变体模块，滨海处有海滩变体。

## 多地形叠加策略

多种地形类型（冰川、城墙建筑、树林）不扩展基础模块集，而是从原始高度图派生出各自的**专用高度图**（非该地形区域高度清零），再单独跑一遍 Marching Cubes 叠加模块。城市中心用固定预制建筑群叠加在顶点位置，以方形感打破三角格的几何痕迹。

## 后处理视觉润色

- 自定义环境光遮蔽（AO）
- 海洋瓦片内置小型流体模拟（波浪动画）
- 极地 shader：越靠近极点越积雪
- 体积云与动画月亮、大气辉光

这些效果彻底遮盖了模块边界，使瓦片本质几乎不可见。

## 与 WFC 的关系

*Planet* 的模块选取逻辑是人工规则（高度差→悬崖类型等），不具备 WFC 那种全局约束传播能力，因此模块数量与规则复杂度均远低于后续 Townscaper。但也正因如此，其可预测性与艺术可控性更强，体现了"刻意设计简单规则"而非"泛化约束求解"的不同策略。

## 相关

- [[rendering/marching-cubes]] — 底层格点布尔→模块选取算法
- [[game-development/triangle-grid]] — 三角网格基础结构
- [[game-development/wave-function-collapse]] — Stålberg 后续更复杂的系统
- [[game-development/driven-wfc]] — Boris 在 WFC 上的扩展工作

## Sources

- [[sources/boris-planet-generation]]
