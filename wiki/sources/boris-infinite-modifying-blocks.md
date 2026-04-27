---
tags: [source, game-development, procedural-generation, wfc, infinite-generation]
date: 2026-04-27
sources: 1
---

# Infinite Modifying in Blocks（Boris The Brave）

[[boris-the-brave]] 发表于 2021 年 11 月的文章，在 [[modifying-in-blocks]] 的基础上提出支持**惰性、确定性、常数时间**无限生成的分层块求值方案。

## 摘要

朴素的"惰性分块 WFC"（如 Marian42 的城市生成器）虽然能在玩家移动时动态加载新区块，但由于求值顺序依赖玩家轨迹，即使使用相同随机种子也会产生不同结果，不具备确定性。本文的核心贡献是将 Modifying in Blocks 扩展为**分层结构**，让任意位置的块只依赖固定数量（12 个）的前驱块，从而在无限平面上实现确定性惰性生成。

分层方案使用 4 层：Layer 1 块彼此独立，Layer 2 每块依赖 2 个 Layer 1 块（沿 x 偏移半块宽），Layer 3 依赖 Layer 2（沿 y 偏移半块高），Layer 4 为最终输出层。经过 4 层覆盖，几乎所有原始背景瓦片均被替换，块边界的痕迹极难察觉。

## 关键要点

- 传统懒加载 WFC 依赖求值顺序，无法保证确定性
- 分层块依赖树深度固定（4 层，共 12 块），实现常数时间 per-block 代价
- Layer 1 块之间完全独立，之后每层块与上层的依赖数量均为 2（而非全部先驱）
- 代价：整体约 4 倍于朴素方案；无法表达大于块尺寸的空间模式
- 初始背景填充是可选项，但缺少它会削弱鲁棒性

## 链接到的概念

- [[modifying-in-blocks]]
- [[wave-function-collapse]]
- [[model-synthesis]]

## 原文

- 链接：https://www.boristhebrave.com/2021/11/08/infinite-modifying-in-blocks/
- 本地：`raw/articles/boristhebrave.com/2021-11-08_infinite-modifying-in-blocks.md`
