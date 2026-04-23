---
tags: [source, bitsquid, 字体渲染, sdf]
date: 2026-04-19
sources: 1
---

# Distance Field Based Rendering of AngelCode Fonts（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2010 年 4 月开源一个小 C# 工具，把 **AngelCode BMFont** 输出的位图字体 + `.fnt` 转成 **SDF**（Valve 2007 SIGGRAPH 思路）的字体图集。

## 摘要

Valve 的"alpha-tested magnification"用 distance field 贴图做字体渲染：一张小图，任意放大都清晰；比起直接上采样 bitmap 好很多。Frykholm 没找到现成工具就写了一个：在 BMFont 里先以目标尺寸的 **8 倍**烘字体 + atlas（同时保证 `8 × spread` 像素 padding 避免字形互污），工具再缩小并估计每像素到轮廓的距离，输出新 `.tga` + 新 `.fnt`（所有度量都映射到缩小后的坐标）。`spread` 决定 distance field 在轮廓外延伸多远——外发光、外描边会用到这个 margin。评论里指出的两个坑：缩放会丢 TrueType **hinting**；中文这类大字集要么用超大 atlas（多张 1024×32 也扛不住大号字），要么降级到 runtime 生成 SDF / software rasterize。

## 关键要点

- 输入：AngelCode BMFont 的 `.tga` 位图 + XML 格式 `.fnt`；
- 参数：**scale factor**（8 倍源位图缩到 1 倍目标）、**spread**（distance field 外延的像素数）；
- 纯位图→SDF，**不用 vector 直接算距离**（工具更简单，代价是源位图必须够大才有好距离估计）；
- 丢 hinting 是这条路线的代价；小号字用位图 hinted 版本，大号 / 自由缩放用 SDF 版本；
- CJK / Unicode 全字集在大字号下贴图爆炸；单通道 SDF 的续作是 multi-channel SDF（文章没提）。

## 链接到的概念

- [[sdf-font-atlas-rendering]]
- [[slug-gpu-glyph-rendering]] — 更后期、更通用的 GPU 直接光栅字体路线

## 原文

- 链接：<https://bitsquid.blogspot.com/2010/04/distance-field-based-rendering-of.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2010-04-09_distance-field-based-rendering-of-angelcode-fonts.md`
