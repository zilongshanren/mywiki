---
tags: [source, 渲染, 反走样, ssaa, fxaa, x-plane]
date: 2026-04-19
sources: 1
---

# Non-Square OGSSAA+FXAA（Ben Supnik / The Hacks of Life）

[[ben-supnik|Ben Supnik]] 发表于 2012 年 10 月的 AA 方案笔记，记录 X-Plane 10 从旧版 FXAA 升级到 FXAA 3.11 过程中探索的一个非标组合。

## 摘要

X-Plane 的锯齿瓶颈在**时序稳定性**而非单帧画质——背景里长而细的水平线（屋顶、道路）在相机平移时"爬"。Supnik 试了两项改动：(1) 把 OGSSAA 的采样网格从方形改成**非方形**（1×2、2×2、2×4），把额外采样都花在竖直方向；8× = 2×4 时细屋顶的时序抖动显著改善。(2) 按 FXAA 作者 Timothy Lottes 的建议，**让 FXAA 在 SSAA 空间里跑，再把结果 mix 下采样**——而不是先 downsample 再 FXAA。管线已经支持这种拓扑。放弃的另一选项是 1.4×1.4 scaling：总填充只翻倍，但**box filter 破坏 FXAA 需要的"像素位置"信息**，FXAA 无法干活。结论：非方形 OGSSAA 给 FXAA 做方向偏置——把 shader 内走样和几何锯齿拆给两套方案处理，而非暴力 4× fill rate。

## 关键要点

- 非方形 OGSSAA：2× = 1×2，4× = 2×2，8× = 2×4；竖向额外采样解决 X-Plane 的水平线时序抖动。
- FXAA 必须在**SSAA 空间**运行再合并下采，而非先 downsample——Lottes 亲自澄清。
- 1.4×1.4 scaling 被否：box filter 破坏 FXAA 的像素位置假设。
- 静态单帧改善不明显，**时序稳定性**才是这套组合的真正卖点。
- FXAA 3.11 接入；SSAA 处理 shader 内走样，FXAA 处理残余几何锯齿。

## 链接到的概念

- [[ogssaa-fxaa-non-square]]
- [[aa-techniques-survey-2011]]
- [[msaa-ssaa]]
- [[temporal-antialiasing]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2012/10/non-square-ogssaafxaa.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2012-10-31_non-square-ogssaa-fxaa.md`
