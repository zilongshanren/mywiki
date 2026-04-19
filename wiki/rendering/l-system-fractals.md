---
tags: [procedural, fractal, l-system, graphics]
date: 2026-04-19
sources: 1
---

# L 系统与分形图形

Lindenmayer System（L 系统）是一种基于字符串重写规则的分形图形学工具。给定一个初始状态、一组迭代规则，反复替换变量即可生成具有自相似结构的图形，广泛用于植物形态、雪花、曲线等分形对象的建模。

## 系统五元素

- **变量（variables）**：每次迭代按规则被替换的符号。
- **常数（constants）**：不参与替换的符号，常为控制符（如旋转、压栈）。
- **旋转角度**：方向旋转符号 `+` / `-` 对应的角度值。
- **初始状态（axiom）**：第 0 次迭代的起始字符串。
- **迭代规则（productions）**：每次迭代对变量的替换规则。

常见控制符：`A`/`B`（沿当前方向画线段）、`X`/`Y`（纯标记，不作画）、`[`/`]`（压栈/出栈当前位置与方向，用于分支）、`+`/`-`（顺/逆时针旋转）。

## 经典案例

[[Ted Sie]] 在文中以 10 个案例贯通 L 系统：

- **Algae**：`A → AB, B → A`，斐波那契生长序列的字符串形式。
- **Fractal Tree**：`A → A[-B]+B, B → AA`，角度 45 度，借 `[ ]` 产生二叉树。
- **Cantor Set**：`A → AXA, X → XXX`，经典的分形点集。
- **Koch Curve / Snowflake**：产生锯齿自相似的边界。
- **Sierpinski Triangle / Curve / Square Curve / Arrowhead Curve**：不同规则下的 Sierpinski 家族。
- **Dragon Curve**：`X → X-YA-, Y → +AX+Y`，龙形曲线。
- **Fractal Plant**：`X → A-[[X]+X]+A[+AX]-X, A → AA`，角度 25 度，植物形态。

## 工程价值

L 系统的核心价值在于**规则与输出分离**——修改几行产生式即可得到结构完全不同的图形，非常适合做程序化美术工具的内核。它也是后续工程化改造（如 [[l-system-lightning-bolts|分形闪电]]）的基础。

## 相关

- [[l-system-lightning-bolts]]
- [[fractal-texturing]]
- [[procedural-mesh-primitives]]
- [[turbulence-domain-warping]]

## Sources

- [[sources/tedsie-l-system-fractals]]
