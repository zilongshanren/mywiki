---
tags: [source, 渲染, mipmap, moire, 屏幕, deus-ex]
date: 2026-04-14
sources: 1
---

# Deus Ex: Scanlines（Simon Trümpler）

[[simon-trumpler|Simon Trümpler]] 写于 2013 年 1 月的 Game Art Tricks 短文，讨论《Deus Ex: Human Revolution》总部里电子公告牌近距离出现的**扫描线式故障艺术**，并顺带把它归到「纹理采样 moiré」这条老现象上。

## 摘要

Deus Ex 总部的屏幕在玩家走近时会闪出一层会随距离变化的扫描线和 RGB 裂变，像《黑客帝国》或《午夜凶铃》的视觉语言。Simon 没有直接给出最终机制——他更像是在把一组可能的解释列出来：评论里有人指出这本质是 **moiré**，当纹理的规则像素网格和显示器的规则像素网格以非整数比 + 非对齐叠加时，会出现低频干涉纹；平时我们用 mipmap 和三线性/各向异性过滤避免这种现象，但 Deus Ex 的屏幕资产大概率**故意不生成 mipmap 或用 negative lod bias**，让 aliasing 出现作为故障感的一部分。评论里还提到两个有趣的衍生：Team Fortress 2 里有玩家利用 mipmap 在不同距离切换不同层级的内容（近看高 mip 时图像完全变成「How could this happen?」的文字）做「反向彩蛋」；另一位开发者提议把 scanline UV scale 做成相机距离的函数，以更可控的方式逼近同样的视觉。

## 关键要点

- 近看屏幕的扫描线很可能是 mipmap 缺失或 lod bias 负值导致的 **moiré**——而非专门的 post-process
- Moiré 是同类频域采样冲突的通用现象，摄影、电视播报中也常见
- 由于显示器 RGB subpixel 有水平偏移，高对比规则纹理的 moiré 会伴随**彩色裂变**
- TF2 的玩家喷漆利用同一机制在不同 mip level 藏不同内容
- 更可控的替代是**按相机距离动态调 scanline UV scale**

## 链接到的概念

- [[mipmap-moire-scanline]]
- [[crt-shader-effects]]
- [[aliasing]]
- [[simon-trumpler]]

## 原文

- 链接：https://simonschreibt.de/gat/deus-ex-scanlines/
- 本地：`raw/articles/simonschreibt.de/2013-01-23_simonschreibt.md`
