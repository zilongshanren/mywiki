---
tags: [source, game-development, tileset, autotile, procedural-generation]
date: 2026-04-27
sources: 1
---

# Quarter-Tile Autotiling（Boris The Brave）

[[people/boris-the-brave]] 发表于 2023 年 5 月的文章，介绍四分之一格 autotile 方案——将每个格子拆成四个象限分别选切片，作为 Marching Squares 双网格方案的替代。

## 摘要

Quarter-tile（也叫 sub-tile、meta-tile、RPG Maker autotile）将基础格拆成四个半尺寸象限，每个象限的切片选择依赖当前格及相邻的三个格的地形类型，共 6 条规则（覆盖所有象限组合）。优势是切片数量少（有旋转仅需 5 张半尺寸切片，无旋转 14-20 张），不需要理解双网格，实现简单；代价是表达力弱于 Marching Squares——无法做大曲率弧线，也不能直接支持多地形过渡。实践中常将象限预组合成完整切片（48 张 blob pattern），交给引擎正常处理。文章还比较了两种方案的切片数、地形数据存储位置、曲线能力，并提到 3D 扩展（八分之一格）和 ortho-tile 变体。

## 关键要点

- 每象限切片仅依赖 4 个相邻格，规则总数仅 6 条，旋转共用后 5 张半尺寸切片足够
- 相比 Marching Squares：切片数更少、不需要双网格，但曲线半径受限、多地形支持弱
- RPG Maker 的 autotile 系统即此方案的标准实现
- 预组合成 48 张 blob 切片后可直接复用现有引擎 autotile 管线
- 多地形处理：叠加多层独立 autotiling（带透明度）或为每对地形专门设计切片

## 链接到的概念

- [[game-development/quarter-tile-autotiling]]
- [[game-development/autotile-tileset-layouts]]
- [[game-development/tileset-classification]]
- [[rendering/marching-squares-ambiguities]]

## 原文

- 链接：https://www.boristhebrave.com/2023/05/31/quarter-tile-autotiling/
- 本地：`raw/articles/boristhebrave.com/2023-05-31_quarter-tile-autotiling.md`
