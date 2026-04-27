---
tags: [source, procedural-generation, algorithms, mathematics, game-development]
date: 2026-04-27
sources: 1
---

# Exploring Rectangle Subdivisions（Boris The Brave）

[[people/boris-the-brave]] 发表于 2025 年 5 月的文章，探讨矩形递归细分的不可约细分枚举问题。

## 摘要

文章由 Vuntra City 开发者 Larissa Davidova 关于程序化城市生成的演讲引发：她使用"旋转（whirl）"模式将矩形划分为 5 块以避免横贯整张地图的长街道。Boris 以此为起点，从数学角度形式化"不可约矩形细分"——即一个细分不存在能被单个矩形替换的子集。不可约细分是构造所有矩形细分的原子单元，视觉上也最有趣因为没有可被眼睛识别的规律结构。作者随后写脚本枚举了所有在整数网格上 5×5 范围内的不可约矩形细分，并将结果发布为 JSON 文件供程序化生成使用。

## 关键要点

- **可约性定义**：若细分中存在至少两个矩形组成的子集恰好构成矩形边界，则为可约——可以"向上合并"为更简单的细分
- 所有矩形细分均可通过递归细分构造，每步选择一个不可约子划分
- 不可约细分在视觉上最自然，没有明显重复结构
- 整数网格足够通用——非整数版本都可以通过"滑动"切割线得到
- 5×5 范围内的完整不可约细分集合已枚举并发布为 JSON，可直接用于生成

## 链接到的概念

- [[game-development/rectangle-subdivisions]]
- [[recursive-subdivision]]

## 原文

- 链接：https://www.boristhebrave.com/2025/05/03/exploring-rectangle-subdivisions/
- 本地：`raw/articles/boristhebrave.com/2025-05-03_exploring-rectangle-subdivisions.md`
