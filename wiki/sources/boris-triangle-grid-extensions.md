---
tags: [source, game-development, grid, geometry, math, procedural-generation]
date: 2026-04-27
sources: 1
---

# Some Triangle Grid Extensions（Boris The Brave）

[[people/boris-the-brave]] 发表于 2021 年 5 月的文章，是三角网格主文章的补充，涵盖三联六边形格（Trihex）、改进的距离函数，以及三角网格与等距（Isometric）网格的关系。

## 摘要

文章整理了 Boris 在发布三角网格教程后的三项延伸思考，由社区讨论直接触发。其一是 Trihex（三联六边形）格的构造方法；其二是将三角格的默认边距离函数替换为允许"踩顶点"的替代距离函数，使其行为接近六边形网格的六方向距离；其三是说明三角列式排列天然对应等距视图，为 Monument Valley 类型游戏提供了一种整洁的坐标处理方式。

## 关键要点

- **Trihex 格**：三角网格间距加倍即得到六边形+三角形交替铺砌的 Trihex 格，代码扩展量极小
- **替代距离函数**：允许经顶点中转（两步到达"3-邻居"），公式为 `(|da-db|+|db-dc|+|dc-da|)/2`，比原始三步函数更符合直觉
- **等距网格**：将三角格旋转为列排列后，直接复现等距坐标线；两个三角形组合成菱形可表示等距正方形；三对三角形可组合成立方体面
- **Settlers of Catan**：该棋盘游戏同时使用六边形格子和顶点，实质上是在 Trihex 格上操作

## 链接到的概念

- [[game-development/triangle-grid]]

## 原文

- 链接：https://www.boristhebrave.com/2021/05/27/some-triangle-grid-extensions/
- 本地：`raw/articles/boristhebrave.com/2021-05-27_some-triangle-grid-extensions.md`
