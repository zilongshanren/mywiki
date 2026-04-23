---
tags: [source, 渲染, shader, 纹理]
date: 2026-04-19
sources: 1
---

# A Tile Too Far（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2010 年 1 月的文章，介绍 X-Plane 场景渲染里在玩的「number puzzle」shader 瓦片随机化技巧，并讨论它和 texture atlas 结合时撞上 fixed function 壁垒的事。

## 摘要

Number puzzle 技巧：把一张重复纹理划分为 N×N 子瓦片，shader 里根据位置从噪声图里取随机瓦片编号，把 UV 高位替换掉——视觉上同一张纹理平铺不再看出接缝。成本几乎零（一次噪声采样 + 位运算），且关闭 shader 走 fixed function 时自动退化为原始重复 tiling——丑但合法，不需要双渲染路径。Supnik 在文章里临场想到的扩展：把瓦片选择范围约束在 atlas 的某段 UV 区间，允许一次 batch 绘制多种地表。问题是 atlas + UV wrap 在 fixed function 下根本不兼容（硬件 wrap 会越过子图边界），shader off 路径从「丑但合法」变成「花屏」。文章后半讨论 2010 年还要不要支持 fixed function——Supnik 的理由不是硬件占比，而是客户支持价值：让用户一键关掉 advanced path 是「等新驱动 vs 退货」的分水岭。

## 关键要点

- Number puzzle = 低位保留瓦片内部 UV + 高位用噪声置换 = shader 级纹理去重复。
- 优雅降级是免费的：shader off 仍有合法输出，不用写两套代码。
- atlas + wrap 的根本冲突：atlas 要求不越出子图，wrap 要求越出时 mod 回来——shader 里可以手动处理，fixed function 不行。
- Fixed function 保留的真实动机不是硬件，是客户支持——能关掉 advanced path 就能让用户留下来等新驱动。
- 与 [[stochastic-texture-sampling]] 互补：前者离散重组、mipmap 友好；后者连续混合、数学严格但成本高。

## 链接到的概念

- [[number-puzzle-tile-shader]]
- [[stochastic-texture-sampling]]
- [[sampler-filter-wrap-modes]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2010/01/tile-too-far.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-01-27_a-tile-too-far.md`
