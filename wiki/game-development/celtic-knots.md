---
tags: [procedural-generation, graphics, blender, pattern-generation, game-development]
date: 2026-04-27
sources: 2
---

# 凯尔特编结图案生成

凯尔特编结（Celtic Knot）是源自凯尔特文化的精细装饰纹样，核心特征是多条线条相互穿越形成连续的 over-under 交替图案。Boris The Brave 为 Blender 开发了一个插件，通过算法将任意框架网格自动转换成三维贝塞尔曲线的凯尔特编结形态。

## 基本生成原理

生成算法以一个框架网格（framework mesh）为输入，将网格的每条边替换为一条编结线段。关键在于处理线段在节点处的穿越关系（crossing resolution）：每个交叉点必须决定哪条线在上、哪条线在下，以维持 over-under 的交替规律。Boris 的实现能自动计算这一关系，保证生成结果满足凯尔特编结的拓扑约束（每条线的上下关系必须严格交替）。

输出为 3D 贝塞尔曲线路径，可在 Blender 中进一步调整。对于历史文物中那些特殊角度和精细变体，插件不做自动处理，需要手动修饰。

## 斜纹（Twill）扩展

2018 年的 1.0 版本新增了**斜纹（Twill）**生成能力。斜纹是一种比平纹（plain weave）更复杂的编织结构：交叉点并非每隔一个就反转，而是按照某种规律偏移，从而在宏观上产生对角线纹路（如斜纹布料、人字纹等）。实现参考了 Akleman 等人 2010/2011 年关于拓扑编织物的研究，将连续 over-under 计数参数化。

## 与程序化生成的关联

凯尔特编结生成是一类特殊的**图形模式程序化生成**问题：输入是一个拓扑结构（网格），输出是满足全局拓扑约束（交替穿越）的几何曲线集合。与 [[game-development/constraint-based-tile-generators]] 中的约束满足思路有相通之处——只是约束的载体是曲线的上下关系而非瓦片的兼容规则。

## Sources

- [[sources/boris-celtic-knots]]
- [[sources/boris-celtic-knots-twills]]
