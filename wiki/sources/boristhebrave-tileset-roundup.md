---
tags: [source, game-development, procedural-generation, tileset, autotile]
date: 2026-04-19
sources: 1
---

# Tileset Roundup（Boris The Brave / 2013）

[[boris-the-brave]] 2013 年 7 月发表的 autotile 方案综述，系统梳理了 2D 游戏中以「方形、不可旋转」为限制条件下的几种主流 autotile 贴图布局，按所需切片数量由少到多依次比较。

## 摘要

Autotile 指玩家用刷子只刷「实 / 空」语义，程序自动挑选正确贴图。作者从**Marching Squares（16 片）**讲起：以每个格点的四角作为 0/1，二进制拼成索引查表。痛点在于艺术家其实想标记格子本身而非角，且 16 片的视觉多样性很快露馅。升级版是 **Blob（48 片）**，直接枚举 8 邻域的 256 种情况，合并掉角邻居无效的冗余，留下 47 个实心 + 1 个空。为压缩 Blob 的手绘成本，作者介绍 **Sub-blob（20 子片 + 空）**——把每片切成 4 个象限，观察单象限只有内弧/外弧/横分/竖分/实心 5 种可能，拼装生成任意 Blob 片；RPG Maker VX 的 TileA2 用的就是这套。最后作者给出自己命名的 **Micro-blob（13 子片 + 空）**：如果不在意子象限之间的图案连贯，可以进一步去重，切片比 Marching Squares 还少，但灵活度仍高于 Marching Squares。整篇核心论点是：切片数量、表达力、艺术成本三者之间存在可量化的权衡曲线，不同项目应在曲线上挑合适的点。

## 关键要点

- Marching Squares 的索引公式 `topLeft + 2*topRight + 4*bottomLeft + 8*bottomRight`，本质是二进制计数
- Blob 的关键洞察：角邻居只有在两条相邻边都实心时才有意义，否则压进同一类；故 256 种表象只剩 47 种有效
- Sub-blob 的象限独立性是近似成立的：允许不同象限独立选子片，可能产生子片之间微小的花纹错位，但通常可接受
- Micro-blob 的代价是艺术控制力下降，不能针对特定邻域定制花纹
- 文章显式排除了旋转、多材质过渡、随机替代片等扩展；这些会让切片基数再上一个数量级

## 链接到的概念

- [[autotile-tileset-layouts]]
- [[boris-the-brave]]

## 原文

- 链接：https://www.boristhebrave.com/2013/07/14/tileset-roundup/
- 本地：`raw/articles/boristhebrave.com/2013-07-14_tileset-roundup.md`
