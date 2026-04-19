---
tags: [source, procedural, fractal, l-system]
date: 2026-04-19
sources: 1
---

# L 系统分形图形学（Ted Sie / 阿祥的开发日常）

[[ted-sie|Ted Sie]] 发表于 2020 年 4 月的文章，系统介绍 Lindenmayer System 的五要素并演示 10 个经典分形案例。

## 摘要

L 系统是基于字符串重写的分形图形工具。文章先定义五要素：变量（每次迭代被替换的符号）、常数（控制符不变）、旋转角度、初始状态（axiom）、迭代规则（productions）。再规约一组绘图符号：`A/B` 画线段、`X/Y` 纯标记、`[ ]` 压出栈、`+/-` 方向旋转。随后以 Algae、Fractal Tree、Cantor Set、Koch Curve、Koch Snowflake、Sierpinski 家族（Triangle/Curve/Square Curve/Arrowhead）、Dragon Curve、Fractal Plant 十个例子逐一给出规则与渲染结果。L 系统的设计哲学是**规则与输出分离**——改几行产生式即得到新图形，非常适合做程序化美术工具内核。

## 关键要点

- L 系统 = 变量 + 常数 + 角度 + 初始状态 + 迭代规则。
- `[ ]` 作为栈是产生分支结构（如树、植物）的关键控制符。
- 从 Algae 的线性序列到 Fractal Plant 的复杂分支，规则复杂度有清晰谱系。
- 文章为后续 [[l-system-lightning-bolts|分形闪电]] 案例铺路。

## 链接到的概念

- [[l-system-fractals]]
- [[l-system-lightning-bolts]]
- [[fractal-texturing]]

## 原文

- 链接：https://tedsieblog.wordpress.com/2020/04/09/lindenmayer-system/
- 本地：`raw/articles/tedsieblog.wordpress.com/2020-04-09_lindenmayer-system-fen-xing-tu-xing-xue.md`
