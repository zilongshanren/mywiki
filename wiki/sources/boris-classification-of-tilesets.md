---
tags: [source, game-development, tileset, autotile, procedural-generation]
date: 2026-04-27
sources: 1
---

# Classification of Tilesets（Boris The Brave）

[[people/boris-the-brave]] 发表于 2021 年 11 月的文章，提出一套对瓦片集（tileset）进行系统性分类的形式化框架。

## 摘要

文章尝试为各种瓦片集建立一套统一的「短代码」描述体系，以便在不同方案之间做横向比较。分类框架将一个瓦片集拆解为四个正交维度：**单元类型**（Cell type：方格 S、立方体 C、六边形 H、三角形 T）、**瓦片识别方式**（Tile identification：顶点/边/面存储的值及其取值数量，如 V2、E3）、**对称性**（Symmetry：旋转 R、镜像 M），以及**限制条件**（Restrictions：不合法组合的排除规则，如 -Blob）。四个维度组合产生一个紧凑代码，例如经典的 Marching Squares 是 S-V2，Blob 模式是 S-V2E2-Blob。文章通过对 CR31 stagecast 典型瓦片集的分类演示了框架的覆盖能力，并指出相同分类代码的瓦片集视觉风格可以截然不同，且分类本身并不唯一确定自动切片算法。该框架的价值在于系统性地探索瓦片集设计空间，例如对比方格与三角格子变体的瓦片数量差异，或将 Blob 扩展至六边形网格。

## 关键要点

- 四维分类：单元类型 × 瓦片识别 × 对称性 × 限制条件，形成 `S-V2`、`S-V2E2-Blob` 等短代码
- Marching Squares = S-V2（16 片），带旋转/镜像后 S-V2-RM 仅 6 片
- Blob = S-V2E2-Blob（47 片）；引入对称性可降至 16 片
- 三角格子变体（T-V2-RM = 4 片）比方格（S-V2-RM = 6 片）更省美术资源
- 同一分类代码可对应截然不同的视觉风格（blob gallery 示例）
- 分类不等于自动切片算法——相邻规则仍需单独定义

## 链接到的概念

- [[game-development/autotile-tileset-layouts]]
- [[game-development/tileset-classification]]

## 原文

- 链接：https://www.boristhebrave.com/2021/11/14/classification-of-tilesets/
- 本地：`raw/articles/boristhebrave.com/2021-11-14_classification-of-tilesets.md`
