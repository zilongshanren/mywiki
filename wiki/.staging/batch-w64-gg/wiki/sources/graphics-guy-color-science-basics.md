---
tags: [source, 渲染, 颜色, 色彩科学, hdr]
date: 2026-04-19
sources: 1
---

# Basic Color Science For Graphics Engineer（A Graphics Guy's Note）

[[graphics-guy-notes]] 2018 年 11 月的文章，在 Skull & Bones 接 HDR TV 支持时补的一轮色彩科学笔记。

## 摘要

游戏十多年都在 sRGB 小色域里做 HDR 渲染，到 HDR 显示普及后必须补齐底层色彩知识才能做对。文章从「SPD（光谱功率分布）是颜色的物理本体」开始，讲 color matching experiment（用 615/525/445 三单色光去匹配所有单色光，某些波长要负强度）、CIE XYZ 空间（用虚构原色避开负值，成为所有色彩空间的共同参考）、chromaticity diagram（投到 $x+y+z=1$ 平面降到 2D）。然后解释色彩空间三要素——primaries、white point、scaling factor——以及 white point 反解 $S_r, S_g, S_b$ 的线性方程。落地到三种色彩空间：Rec.709/sRGB（primaries 相同 transfer function 略异，只覆盖 CIE 1931 的 35.9%）、Rec.2020（UHDTV 标准，primaries 是单色光谱位点，覆盖 75.8%，用 PQ）、以及工程实践——在 sRGB linear 做光照、转 Rec.2020 做 color grading、PQ 编码送 HDR 显示。

## 关键要点

- SPD 是颜色的底层；RGB 是三通道视锥的投影。
- Color matching 实验中某些波长需负强度 → 催生虚构原色 XYZ。
- Chromaticity diagram 丢掉强度维只看 hue/saturation，蹄形外缘是单色光谱。
- 色彩空间 = primaries + white point + transfer function，三者齐全才能解释 $(R,G,B)$ 的含义。
- D65 白点 $(0.3127, 0.3290)$ 是 Rec.709/sRGB/Rec.2020 三者共用。
- Rec.2020 覆盖 75.8% CIE 1931，但转换不能凭空造 sRGB 色域外的颜色，除非做饱和 grading。

## 链接到的概念

- [[color-science-basics]]
- [[color-space]]
- [[spectral-rendering]]
- [[hdr-video-edr-metal]]

## 原文

- 链接：https://agraphicsguynotes.com/posts/basic_color_science_for_graphcis_engineer/
- 本地：`raw/articles/agraphicsguynotes.com/2018-11-29_basic-color-science-for-graphics-engineer.md`
