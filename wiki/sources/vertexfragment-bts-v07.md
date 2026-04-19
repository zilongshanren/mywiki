---
tags: [source, indie-game, devlog, unity, urp]
date: 2026-04-19
sources: 1
---

# Beyond the Storm - v0.7（Steven Sell / Vertex Fragment）

[[steven-sell]] 2025 年 7 月的独立游戏 devlog，宣告 *Beyond the Storm* 第一次**公开发布**（GitHub 上 `BTS-Public` 仓库），也承认原初"大而全开放世界"的野心在单人开发规模下不可行，v0.8 之后会把范围砍成 2-3 小时的"短篇"体验。

## 摘要

中断一年（其间做了 [Ponder](https://pondertcg.com/)）后回归，v0.7 做的渲染侧改动主要三件：

1. **草地从 quad-based 切到 bladed**（单片 blade mesh），解决了原先 quad 方案在高视角、低密度、边界过渡时的 artifact；好处是 wind 和 flower tips 都能做，森林区 vs 草原区可以用不同 blade 变体和 flower mesh。相关系统（草地、地形层）同时更新成按坡度和区域配置做更好的 blend，森林里能出现土路、不再是均匀绿地。
2. **体积雾完全重写**（未进 demo 构建），跟着他同期那篇 [[urp-volumetric-fog-raymarch]] ramble 走的实现。
3. **云渲染从"0.25 秒一次 + 插值"切换到实时**——这一条是 [[volumetric-cloud-quarter-res-upsample|quarter-res + temporal upsample]] ramble 的实际落地。之前"每帧 FPS 毛刺"一直是作者不满意的点，这版终于压住了。

另加一个小效果：实体踩水/游泳时的 water trail。和之前做船的 wake 一样，显示在起伏水面上比平面上复杂得多。

文末附项目规模数据：2096 commits、112k 行 C# 活跃代码、975 个 C# 文件；110 个 shader、18352 行 HLSL；最大 `Common.hlsl` 1069 行、`TerrainImpl.hlsl` 943 行。单人长期项目的真实量级样本。

## 关键要点

- 独立开发的"scope 坍缩"时刻：大世界 → 2-3 小时短篇；保留了地形/建筑/水体，可能砍建造和地形变形等重功能。
- 三个技术改动都对应同期 ramble，是理论 → 实践闭环的真实案例。
- "草地从 quad 到 blade"：quad 的优势是换贴图切风格，blade 的优势是 wind + flower tip + 坡度混合。
- 规模参考：单人多年项目约 10 万行 C# + 1.8 万行 shader；最大的 shader header 也就 1000 行量级。

## 链接到的概念

- [[deferred-grass-shader]] — v0.7 之前的 quad-based 方案
- [[urp-volumetric-fog-raymarch]] — v0.7 的体积雾实现
- [[volumetric-cloud-quarter-res-upsample]] — v0.7 的云优化落地
- [[indie-game-dev-rhythm]]

## 原文

- 链接：https://www.vertexfragment.com/ramblings/bts-v07/
- 本地：`raw/articles/vertexfragment.com/2025-07-10_beyond-the-storm-v0-7.md`
