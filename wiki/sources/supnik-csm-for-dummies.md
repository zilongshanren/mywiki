---
tags: [source, rendering, shadows, csm]
date: 2026-04-19
sources: 1
---

# CSM for Dummies（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 发表于 2011 年 3 月的短文，借 NVIDIA GPU Programming Guide 的一条建议自嘲 X-Plane 10 选择级联阴影贴图（CSM）的决定。

## 摘要

Supnik 引用 NVIDIA *GPU Programming Guide (G80)* 里对阴影技术的官方推荐：「**除非你知道自己在做什么，否则就做 multi-tap cascaded shadow maps**」。他调侃——换句话说就是「完全不知道自己在做什么的时候，就用 CSM，应该不会出大问题」——顺便承认 X-Plane 10 恰好也是 CSM 方案。文末反驳指南中「3 级对任何场景都够用」的说法：X-Plane 这种连续远景视距远超典型 3A 室内外场景，3 级根本吃不下。短文本身没有技术细节，但是 Supnik 对 CSM 作为 X-Plane 10 阴影基线的公开注脚，也为后续 [[gpu-sliced-volumetric-shadows-limits]] 等文章埋下伏笔。

## 关键要点

- NVIDIA 官方阴影技术建议：默认 multi-tap CSM
- 「3 级 CSM 对任何场景都够用」的经验在模拟飞行这种超大可视范围下不成立
- X-Plane 10 的阴影基线：CSM + multi-tap
- 大规模场景的 CSM 仍面临超视距、相机远离原点等特殊约束

## 链接到的概念

- [[cascaded-shadow-maps]]
- [[shadow-mapping-basics]]
- [[camera-relative-sun-shadows]]
- [[cached-shadowmaps]]
- [[gpu-sliced-volumetric-shadows-limits]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2011/03/csm-for-dummies.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2011-03-06_csm-for-dummies.md`
