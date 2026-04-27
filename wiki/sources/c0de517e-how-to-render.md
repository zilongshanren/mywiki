---
tags: [source, rendering, innovation, methodology, research, meta, problem-solving]
date: 2026-04-27
sources: 1
---

# How to Render It: Ten Ideas to Solve Computer Graphics Problems（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2023 年 2 月的文章，总结其职业生涯中反复有效的十余种渲染创新元技法（metatechniques）。

## 摘要

文章原本是 Pesce 十年前想写的一本书的骨架，最终以博客形式呈现。他列举了十三条"思维工具"，不是具体算法，而是探索解决方案空间的方法论：选择正确的工作空间（屏幕/世界/物体/纹理空间）、系统列举数据结构选项及其特性、将计算分解为"场景编码—求解—实时查询"三阶段并允许各阶段用不同表示、考虑对偶问题、跨帧增量计算（TAA 只是其中之一）、用暴力近似估计数据上界、建立真值层级（现实 → 渲染方程 → 具体简化 → 可用数据）、以数值优化和数据可视化辅助探索、优先度量感知误差而非 MSE、向艺术家学习、建立先验假设、刨根问底追问"为什么"、以及用廉价代理快速原型。文章特别强调感知误差和艺术家视角往往比数学精确度更重要，许多"精确"方案因模型假设错误而输给"粗糙"方案。

## 关键要点

- "使用正确空间"：屏幕空间、世界空间、物体空间各有取舍，SSAO 是屏幕空间思路的标志性案例
- 三阶段计算框架：场景编码 / 求解 / 实时查询可独立选择最优数据结构
- 跨帧增量计算是通用策略，不只是 TAA——shadowmap tile 缓存、探针异步更新均属此列
- "真值层级"：在批评近似之前先确认所在的层级（是模型假设错？还是数据不够？）
- ML 可作为可行性上界来验证数据充分性，而非必须是最终部署方案
- 感知误差与艺术家反馈优先于 L2/MSE；粗糙度修改符号作为面光源近似的故事是经典反例
- "刨根问底"作为研究工具：随机选一项 pipeline 步骤深挖，几乎必然发现未被修正的假设错误

## 链接到的概念

- [[rendering/rendering-roi-philosophy]]
- [[rendering/realtime-quality-vs-quantity]]
- [[rendering/temporal-antialiasing]]
- [[rendering/stable-csm-implementation-tips]]
- [[rendering/screenspace-reflections]]
- [[rendering/ground-truth-ambient-occlusion]]
- [[rendering/monte-carlo-integration]]
- [[rendering/importance-sampling-pdf-cancellation]]

## 原文

- 链接：https://c0de517e.blogspot.com/2023/02/how-to-render-it-ten-ideas-to-solve.html
- 本地：`raw/articles/c0de517e.blogspot.com/2023-02-20_how-to-render-it-ten-ideas-to-solve-computer-graphics-proble.md`
