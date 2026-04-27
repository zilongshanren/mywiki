---
tags: [source, procedural-generation, wfc, constraint-solving, game-development]
date: 2026-04-27
sources: 1
---

# Wave Function Collapse Explained（Boris The Brave / BorisTheBrave.Com）

[[people/boris-the-brave]] 发表于 2020 年 4 月的教程，系统讲解 WFC 算法的约束求解本质。

## 摘要

文章以迷你数独为切入点，将 WFC 还原为约束编程（Constraint Programming）的一个特例。核心三要素：**变量**（每个格子的候选集）、**域**（可能的瓦片值）、**约束**（相邻瓦片必须匹配）。求解流程是约束传播（Constraint Propagation）加回溯（Backtracking）的组合——先传播消除候选，若卡住就随机猜测，矛盾时回溯。WFC 只是在"有多解"的场景下把随机猜测保留下来，用最小熵启发式（Least Entropy）选格子、加权随机选瓦片，从而把"约束求解器"变成"约束生成器"。文章还介绍了 Overlapped WFC：用 3×3 重叠模式代替相邻约束，更忠实地复现样本局部纹理。

## 关键要点

- 约束传播：每次域缩减都沿约束边传播，直到无变化或发现矛盾
- 回溯：矛盾时恢复保存状态，排除错误猜测
- 最小熵启发：优先选候选最少（但多于 1）的格子，减少回溯
- 支持计数优化：每格每边每瓦片维护"支持计数"，降为 0 即可立即淘汰
- Overlapped WFC：约束从 2 格邻接扩展到 NxN 重叠补丁，捕捉更远距离相关性
- WFC 的弱点：仅约束局部，大尺度缺乏整体结构，需结合其他手段

## 链接到的概念

- [[wave-function-collapse]]
- [[autotile-tileset-layouts]]
- [[infinite-random-rhombus-tilings]]

## 原文

- 链接：https://www.boristhebrave.com/2020/04/13/wave-function-collapse-explained/
- 本地：`raw/articles/boristhebrave.com/2020-04-13_wave-function-collapse-explained.md`
