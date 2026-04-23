---
tags: [source, 渲染, 性能, profiling, opengl, gpu-counter]
date: 2026-04-19
sources: 1
---

# Moving the Needle - a Quick Audit of the 7970（Ben Supnik）

[[ben-supnik|Ben Supnik]] 2013-05-10 在 *The Hacks of Life* 上贴出一次 X-Plane 在 AMD 7970 + Sandy Bridge i5 + 1920×1200 + 4× SSAA 上的 GPU PerfStudio 审计小结。

## 摘要

Supnik 把 sim 扔进 AMD PerfStudio 2 看 GPU 做什么，结论熟悉："We're mostly CPU bound. Still."——跟每年 GDC 上 IHV 反复念叨的"多数游戏 CPU bound"对上了。唯一能吃满 GPU 的场景是大面积厚云团 + 4× SSAA，profile 按 GPU 时间排序时，一个**万顶点大云团 batch 在 1080p+4×SSAA 下吃掉 32 ms**，后面的云 batch 几 ms、其他 draw 是噪声。他由此回顾了 2012 年延迟管线里把 stenciling 砍掉的决定仍然正确（只有近距大灯值得补 stencil）。他点出 PerfStudio 2 的一个工程痛点——**不 sniff call stack**，无法数据挖掘到"哪个子系统烂"——并给出下一步计划：把 NV / AMD performance counter API 集成进 sim 自己，做 HUD 风格的逐子系统 GPU 耗时。

## 关键要点

- X-Plane 即便开 4× SSAA 也主要 CPU bound，只有大屏占云团能把 GPU 拉满。
- GPU profile 的分布强烈长尾——一个 draw call 吃掉几乎全部预算，其余是噪声。
- 外部 GPU profiler 只按 draw call 聚合，不跨 draw call 做子系统数据挖掘；工程师被迫自建 per-pass probe。
- 延迟光源的 stencil 剔除只在近距大光源下值得补，远距小光源跳过 stencil 更快（呼应 [[xplane-deferred-pipeline-hacks]]）。

## 链接到的概念

- [[engine-integrated-gpu-counter-probes]]
- [[bottleneck-analysis]]
- [[xplane-deferred-pipeline-hacks]]
- [[deferred-light-volume-stencil-depth-clamp-hack]]
- [[frame-profiler-overlay]]
- [[opengl-ext-vs-arb-fast-path-leak]]

## 原文

- 链接：<http://hacksoflife.blogspot.com/2013/05/moving-needle-quick-audit-of-7970.html>
- 本地：`raw/articles/hacksoflife.blogspot.com/2013-05-10_moving-the-needle-a-quick-audit-of-the-7970.md`
