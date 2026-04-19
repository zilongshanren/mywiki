---
tags: [source, 渲染, 全局光照, ReSTIR, 采样, NVIDIA]
date: 2026-04-19
sources: 1
---

# Understanding The Math Behind ReSTIR GI（A Graphics Guy's Note）

[[graphics-guy-notes|Jiayin Cao]] 发表于 2025 年 5 月的长文，配合 NVIDIA Zorah（RTX 50 旗舰 demo）的 GDC 演讲发布，专门讲 [[restir-gi-math|ReSTIR GI]] 论文里一笔带过的数学细节。

## 摘要

作者在 Zorah 项目中与 Daqi Lin 合作，把基于 ReSTIR PT 的全局光照方案实装进 NvRTX 版 Unreal Engine。本文不谈 Zorah 工程问题，专注 ReSTIR GI 理论：先把 emissive / 直接光 / 间接光三类贡献分开，定义 `L_k`（长度为 k 的路径贡献）；介绍 Primary Sample Space（PSS）——把 sampling 变量 `x` 写成 uniform `u` 的函数后，任意积分可以等价写在单位立方体上，这条性质为"把邻居像素的路径搬到当前像素"提供理论依据。中段推导 RIS 允许**每个初始候选使用不同 target function** 的性质（这条比论文原文更宽松，也顺便补救了 ReSTIR DI 里 visibility reuse 的 target function 不一致问题）。后半讨论 ReSTIR GI 里 initial candidate 的精确定义：把它当"整棵路径树"会导致 proposal PDF 定义困难（不同深度路径高度相关，不能当独立路径乘积），作者援引 GRIS 框架用 shift mapping + Jacobian 解决跨 domain resample；并讨论两种常见 target function 选择及其收敛差异。文章末尾点出 ReSTIR 的通用结构（initial sampling → temporal → spatial → final evaluation）可套用到任何具备时空相干性的采样问题。

## 关键要点

- PSS 是 ReSTIR GI / PT 能把路径 resample 的理论基础——允许把原域积分改写在单位超立方体上。
- RIS **不要求** target function 在所有候选上一致——这是 per-initial-candidate target function 性质，原论文没明说。
- 路径树 initial candidate 的坑：同一棵树里不同深度路径共享前缀，proposal PDF 不是各路径 PDF 的简单乘积；GRIS 用 shift mapping + Jacobian 统一处理。
- Zorah 的 Greenhouse 关卡展示了"实时纯路径追踪 + ReSTIR"在 AAA 级场景的可行性——所有 bounce 都在帧内动态求值。
- ReSTIR 本质是一种**通用的时空相干重要性采样**，图形只是其中一种落地；结构可抽象到任何有时空/样本间相干性的 MC 采样问题。

## 链接到的概念

- [[restir-gi-math]]
- [[restir-di-math]]
- [[path-tracing-basics]]
- [[monte-carlo-integration]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/understanding_the_math_behind_restir_gi/
- 本地：`raw/articles/agraphicsguynotes.com/2025-05-09_understanding-the-math-behind-restir-gi.md`
