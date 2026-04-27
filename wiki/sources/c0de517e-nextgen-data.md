---
tags: [source, rendering, game-engines, data-driven-design]
date: 2026-04-27
sources: 1
---

# In the next-generation everything will be data (maybe)（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2014 年 1 月的文章，论述渲染领域早已天然"数据驱动"，并呼吁游戏开发的其他领域（动画、AI、gameplay）借鉴这种思路，从数据采集与仿真中挖掘更多计算价值。

## 摘要

Pesce 指出渲染之所以能高效利用 SIMD、多线程、GPU 等新硬件，正是因为渲染本质上是"少量 kernel 处理海量数据"。与之对比，游戏开发中的动画、AI 等子系统虽然拥有大量采集数据（motion capture、遥测等），却把它们手工切碎成状态机和脚本，而非让数据驱动运行时决策。文章分两类讨论数据：**采集数据**（需要压缩/降维）与**仿真数据**（需要预计算/存储），并举动画、机器学习 AI（Fight Night Round 4）、Hitman 人群等案例说明"用数据代替硬编码逻辑"的可行性与价值。结论是：游戏工业若想进入真正的"下一代"，需要更好地掌握数据过滤、表示、运行时并行算法等能力。

## 关键要点

- 渲染之所以可扩展：本质是少数 kernel 流式处理大量几何/像素数据，SIMD/GPU 恰好适合此模式
- "可视化编程"（蓝图/行为树/材质图）只是语法变换，并未真正改变语义，反而增加了 runtime 维护成本
- 数据两大维度：采集（motion capture、遥测、BRDF 测量）vs 仿真（预计算 lighting、物理）
- 动画领域的数据驱动先驱：kNN 运动搜索、运动合成树，可以减少手工状态机
- AI 案例：Fight Night Round 4 的完全 learning-based AI；Hitman Absolution 人群动画
- 后续能力缺口：感知/心理学度量、符号回归、统计分类、降维、并行 GPU 算法

## 链接到的概念

- [[game-engines/data-driven-architecture]]
- [[rendering/rendering-pipeline]]
- [[rendering/spherical-harmonics]]

## 原文

- 链接：https://c0de517e.blogspot.com/2014/01/in-next-generation-everything-will-be.html
- 本地：`raw/articles/c0de517e.blogspot.com/2014-01-18_in-the-next-generation-everything-will-be-data-maybe.md`
