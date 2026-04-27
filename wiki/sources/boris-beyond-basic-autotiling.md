---
tags: [source, game-development, tileset, autotile, procedural-generation]
date: 2026-04-27
sources: 1
---

# Beyond Basic Autotiling（Boris The Brave）

[[people/boris-the-brave]] 发表于 2021 年 9 月的文章，讨论超越 Marching Squares / Blob 标准自动切片方案的多种进阶思路。

## 摘要

标准自动切片（Marching Squares 16 片、Blob 47 片）在双材质过渡下尚可接受，但一旦引入第三种材质，所需瓦片数量会出现组合爆炸，实际上难以由美术师手工制作。文章系统介绍了几种应对策略：**分层组合**（将边框、底色等分开绘制后运行时合成，Tilesetter 工具即采用此思路）；**遮罩混合**（高分辨率图形直接用遮罩在两种纹理间插值，Factorio 的做法）；**程序生成瓦片**（在运行时动态生成瓦片内容）；**翼式瓦片**（Winged Tiles，瓦片图像主动超出格子边界以产生叠压效果，Truchet 图案即此类）；**波纹替换**（Ripple effect，Tiled 和 Townscaper 的做法：放置一格后自动级联修改周边格子直到全图一致）；以及最简的**无过渡风格**（Minecraft 式）。文章核心洞察是：组合爆炸问题既可从「减少需要绘制的瓦片数量」角度入手，也可从「允许系统级联调整」角度入手。

## 关键要点

- 双材质 Blob 需要 47 片；三材质开始组合爆炸，成为实际瓶颈
- **分层组合**：底色 + 边框分层绘制，运行时 composite，大幅减少美术量
- **遮罩混合**：适合高分辨率，遮罩可复用于多对材质过渡
- **翼式瓦片**：图像超出格子边界叠压，适合 Truchet 图案、草地溢出、等距物体
- **波纹效果**：Tiled / Townscaper 方案，修改局部后系统级联传播（基于约束求解）
- 约束驱动的波纹传播与 [[game-development/wave-function-collapse]] 属同一思路族

## 链接到的概念

- [[game-development/autotile-tileset-layouts]]
- [[game-development/wave-function-collapse]]
- [[game-development/tileset-classification]]

## 原文

- 链接：https://www.boristhebrave.com/2021/09/12/beyond-basic-autotiling/
- 本地：`raw/articles/boristhebrave.com/2021-09-12_beyond-basic-autotiling.md`
