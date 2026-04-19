---
tags: [source, graphics, planet-engine, dem, srtm]
date: 2026-04-19
sources: 1
---

# Evaluation of 30m elevation data in Outerra（Outerra Blog）

[[outerra-team]] 2015 年 5 月的文章，记录了 SRTM 1″（30m）全球数据集公开后在 Outerra 行星引擎里的真实测试结果——并不是「分辨率越高越好」的顺风文，而是一份「源数据有多烂、引擎侧要干多少脏活」的实测报告。

## 摘要

SRTM 30m 发布后 Outerra 做了两组对比：同样 fractal resample 下 `76/30`（76m 输出、30m 源）vs `76/90`（原 90m），以及 `38/30` vs `76/30`。结论是**数据源分辨率比输出分辨率更重要**——`76/30` 几乎不增加存储却拿到大部分视觉收益；而 `38/30` 把数据量翻 3 倍（12.5GB → 39GB），引擎侧 procedural refinement 反而会过响应产生虚假小凹坑。30m 源本身仍被空间滤波过，有效分辨率接近 90m；同时伴随大量 void、城市高程烘入、bathymetric 数据上采样伪影等系统性问题。

## 关键要点

- **`A/B` 记号**：输出分辨率 A，数据源分辨率 B；`76/30` 是甜点。
- 数据源的**空间低通**让山脊被提前削掉，procedural refinement 在此基础上会漂移（雪地伪凹坑）。
- **Void 与假值**：热带雨林、中亚山区、东北非在 30m 源里大量残留，90m 老数据集反而做过人工修补。
- **城市建筑烘进高程**（VAB in KSC 案例），需要 urban mask——但 mask 本身分辨率更粗，边界会产生新的伪影。
- **Bathymetric（海底）数据**：500m 上采来自 1km，引擎被迫标记 mandatory → 不能 fractal refine → 出现比原始 1km 更差的阶梯伪影；教训是**任何人为 upscale 都比保留原分辨率 + fractal refine 差**。

## 链接到的概念

- [[planet-terrain-dem-pipeline]]
- [[outerra-team]]
- [[fractal-texturing]]
- [[diamond-square-noise]]

## 原文

- 链接：https://outerra.blogspot.com/2015/05/evaluation-of-30m-elevation-data-in.html
- 本地：`raw/articles/outerra.blogspot.com/2015-05-27_evaluation-of-30m-elevation-data-in-outerra.md`
