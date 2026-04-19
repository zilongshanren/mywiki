---
tags: [source, blender, 3d-modeling, hard-surface]
date: 2026-04-19
sources: 1
---

# Neat tricks for modelling the Robo Maestro robot（Joost's Dev Blog）

[[joost-van-dongen]] 发表于 2021 年 11 月的 Blender 硬表面建模笔记——他为自己的程序化音乐玩具 *Robo Maestro* 做主角机器人时用到的几个技巧。

## 摘要

做 Robo Maestro 机器人时 Joost 想要"既光滑又硬挺"的工业风。传统 subdivision 建模要加支撑边才能做硬棱，但支撑边一多基础网格就僵、曲线就糙。他的解法是把形状信息从顶点转到 per-edge 标记属性上：**crease** 告诉 subdivision 哪里别平滑、**bevel weight** 告诉 bevel modifier 哪条边要倒角以及倒多大、**harden normals** 让倒角边不走法线插值避免"auto smooth 又软回去"、**limit method = weight** 手动控制哪里要倒角。这套流程让他保持极少顶点，后期仍能快速改曲面——合作者 Robin 提完反馈后他能立刻调完。结尾提了 Robo Maestro 本体。

## 关键要点

- Hard surface 建模的核心矛盾：硬棱需要支撑边，但支撑边多了基础网格僵、曲面糙
- **Crease** 标记 subdivision 不平滑的边，让基础网格超低多边形仍出硬棱
- **Bevel modifier** 给硬棱加小倒角避免"廉价 3D"感；配合 **harden normals** 不失锋利
- **Bevel weight + limit method = weight** 改为手动逐边控制倒角与宽度
- Blender 的"给边/顶点打标"家族：crease、bevel weight、seam（UV）、sharp（shading）
- 低顶点 + 模式化处理让**改形低成本**——后期 art direction 反馈能快速吸收

## 链接到的概念

- [[blender-hard-surface-modeling]]
- [[joost-van-dongen]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2021/11/neat-tricks-for-modelling-robo-maestro.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2021-11-24_neat-tricks-for-modelling-the-robo-maestro-robot.md`
