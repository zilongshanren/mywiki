---
tags: [blender, 3d-modeling, hard-surface, subdivision, indie]
date: 2026-04-19
sources: 1
---

# Blender 硬表面建模：crease + bevel weight + harden normals

[[joost-van-dongen|Joost van Dongen]] 在做 *Robo Maestro* 机器人时总结的一套 Blender 硬表面（hard surface）建模路径。目标是**既要光滑曲面又要工业级硬棱**——这是 subdivision 建模的经典矛盾：加支撑边才能出硬棱，但顶点一多模型就僵，并且曲面会变糙。他的做法是尽量少放顶点，把"硬"的信息从几何搬到**每条边的标记属性**上。

## 核心组合

**1. Crease（折痕）** 是解决"硬边 vs 少顶点"冲突的关键。Subdivision modifier 默认把所有边都平滑化，一旦你在某条边上标记 crease=1，这条边就不再被 subdivision 平滑。于是基础网格可以保持极低多边形数（便于改形），曲面照样平滑，而需要硬棱的地方硬得利落。

**2. Bevel modifier + harden normals**：纯 100% 硬边看起来廉价、"假 3D"。高质量模型的棱角要**略微倒角**。Bevel modifier 自动给硬边加出一小段倒角；但 Blender 的 auto smooth 会因为倒角段的插值法线让棱再次软掉。勾上 **harden normals** 让倒角带不使用插值法线，就能既保留倒角的高光闪烁又不失去边缘紧致感。

**3. Bevel weight + limit method = weight**：Bevel 默认的"自动找硬边"有时误判。把 limit method 切到 weight 后，可以**逐条边**手动指定 bevel 权重（以及倒角宽度），决定哪些棱需要倒角、倒多大。

## 让 per-edge 元数据承担形状职责

这套流程的哲学是：**把形状决策从顶点数量转移到边/顶点上的命名属性**。Blender 提供的这类标记包括：

- **crease** —— 给 subdivision 用
- **bevel weight** —— 给 bevel modifier 用
- **seam** —— 给自动 UV unwrap 用
- **sharp** —— 给 smooth shading 用

每条属性都是"基础几何 + 模式化处理"的组合，好处是基础网格顶点少、易改。Joost 指出：他的协作者 Robin 后期还在调形时，他能**快速改曲率**正是因为基础网格顶点极少——改动只动几个点，subdivision / bevel / auto-smooth 自动把结果展开。

换个角度看，这是 [[deep-modules|深模块]]式的做法：基础网格是简单接口，subdivision + bevel + smooth 是厚重的实现层；修改接口（少数顶点 + 几个标记）就能驱动复杂几何输出。

## 相关

- [[joost-van-dongen]]
- [[procedural-mesh-primitives]] —— 参数化顶点公式的另一条路径（少顶点 + 程序化）

## Sources

- [[sources/joostdevblog-robo-maestro-modelling-tricks]]
