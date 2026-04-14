---
tags: [source, shader-art, 创意编程, 工作流]
date: 2026-04-14
sources: 1
---

# Mini: Creative Code（Xor / GM Shaders）

[[xor-shader-artist|Xor]] 2022 年 9 月的 Mini，用一个"虫洞 shader"从头到尾的过程讲**创意编程的工作流**——灵感、原型、打磨、迭代。

## 摘要

文章把创作拆成四步。**灵感**：想一个自己没见过的东西或看参考图，但要确保目标在当前技能半径内——第一次写 shader 就别冲 3D。**原型**：不管细节先跑起来。虫洞的核心想法是把贴图往中心拉、绕中心拧一圈；实现成 `vec2 uv = vec2(length(p), atan(p.y,p.x)/PI - length(p));` 就出一个基础螺旋。**打磨**：修三个问题——`atan` 在 y=0 的间断线用 `p.x>0?atan(p.y,p.x)/PI : 1.-atan(p.y,-p.x)/PI` 弥合；中心和边缘扭曲不均用 **log-polar** 坐标 `log(length(p)) - seconds*0.5` 修正（扭曲变成尺度不变）；最后 `tex * vec4(0.5, 0.8, 1.3, 1.0)` 给冷蓝调。**迭代**：调参观察循环，本来想做虫洞，结果效果越调越像飓风——那就跟着它走，因为玩参数常常撞上比原计划更好的效果。最终成品 Shadertoy 链接：`7ldBzN`。

## 关键要点

- 创意编程的四步节奏：**灵感 → 原型 → 打磨 → 迭代**。
- **极坐标 + atan**是 shader art 常见工具，但 `atan` 的相位间断必须手动缝合。
- **log-polar 坐标**让径向扭曲尺度不变，也让径向动画天然好写。
- "调参中撞上新效果" 是 creative coding 的常态，接受它——别死守原计划。
- 借别人代码就动手改几个数——常比读懂学得快。

## 链接到的概念

- [[creative-coding-process]]
- [[shader-prototyping-tools]]
- [[fragment-shader]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/creative-code
- 代码：https://www.shadertoy.com/view/7ldBzN
- 本地：`raw/articles/mini.gmshaders.com/2022-09-10_mini-creative-code.md`
