---
tags: [source, 渲染, shader, 创意编程, code-golf]
date: 2026-04-19
sources: 1
---

# Modeling the World in 280 Characters（Xor）

[[xor-shader-artist|Xor]] 2025 年 6 月给 Codrops 写的文章开篇，解释他为什么写 280 字符以内的 tweet shader——这是一种融合 creative coding 与 code golf 的练习。

## 摘要

Xor 作为 graphics programmer 的日常是游戏里的后处理、光照、反射等视觉特效；业余写 tweet shader 则是一种以"字符预算"为约束的娱乐。本文是他创作过程的总览：动机（好奇 / 学习 / 挑战 / 社群四条）、shader 基础（GPU 并行 vs CPU、vertex/fragment/compute、fragment shader 的 FC/r/t/m/b uniform 规约）、以及 [Twigl.app](https://twigl.app) 工具平台——"geekest 300" 模式把 `gl_FragColor` 缩成 `o`、`gl_FragCoord` 缩成 `FC`、分辨率 `r`、时间 `t`，并自动包装 `main()` 外壳。给出两个代表作：**Galaxy** 197 字符动画螺旋星系、**Voxel DDA raytracer** 175 字符带边缘检测的 3D voxel 光线追踪。完整长文（创建过程、代码高尔夫技巧、Q&A、个人故事）在 Codrops。

## 关键要点

- **字符约束驱动创造力**：强迫思考最小可行 shader，很多时候压缩后反而更快。
- **Twigl geekest 300 模式**：预简命名 + 自动包装，280 字符塞下一个完整 fragment shader。
- **GPU 每秒几十亿像素** vs CPU 顺序，理解这点才能理解"shader 就是每像素独立跑"。
- **四项动机**：curiosity/passion、learning、challenge、community。

## 链接到的概念

- [[tweet-shader-280-char]]
- [[shader-code-golfing]]
- [[creative-coding-process]]
- [[xor-shader-artist]]

## 原文

- 链接：https://mini.gmshaders.com/p/modeling-the-world
- 本地：`raw/articles/mini.gmshaders.com/2025-06-23_modeling-the-world-in-280-characters.md`
