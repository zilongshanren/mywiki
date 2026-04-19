---
tags: [source, procedural-generation, tiling, sylves, townscaper]
date: 2026-04-19
sources: 1
---

# Infinite Random Rhombus Tilings（Boris The Brave）

[[boris-the-brave]] 发表于 2025 年 10 月的文章，提出一种与 Townscaper 类似、却避开其两个结构性问题的随机菱形网格算法，已在 Sylves 里实现。

## 摘要

文章先拆解 Townscaper 网格的两个毛病：(1) 三角形偶发，靠全局细分修补但锁死分辨率；(2) 每个六边形 chunk 边界固定成 8 tile，能看出来。Boris 的替代方案建立在一个干净的局部不变操作上——3 个菱形相交于一点时可原地旋转，不影响周围。把这个翻转作为 MCMC 步，在有限区域里能把菱形铺砖洗到均匀分布；推广到无限平面时，单一 chunk 切法会留下边界，于是用 [Infinite Modifying In Blocks](https://www.boristhebrave.com/2021/11/08/infinite-modifying-in-blocks/) 的做法：**三套错位 chunking 依次洗**，覆盖所有位置。最终得到一个纯函数 `f(coord) -> tile`，确定性、lazy、chunk 无关。文章也展示同一框架可改装为**随机矩形（herringbone 变体）**，思想同构。

## 关键要点

- 3 个菱形相交点的原地旋转是局部不变操作——翻不翻不影响其他位置
- 单层 chunking 留边界，三层错位 chunking 覆盖所有位置、不留印
- 给定 cell 的结果只依赖有限邻近 chunk 的 seed，是 `f(coord)` 纯函数
- 起点就是整齐菱形网，无三角形 ⇒ 不需要 Townscaper 那种全局细分
- 同一框架可扩展到 2 矩形互换 ⇒ 随机 herringbone

## 链接到的概念

- [[infinite-random-rhombus-tilings]]
- [[infinite-chunked-procedural-generation]]

## 原文

- 链接：https://www.boristhebrave.com/2025/10/17/infinite-random-rhombus-tilings/
- 本地：`raw/articles/boristhebrave.com/2025-10-17_infinite-random-rhombus-tilings.md`
