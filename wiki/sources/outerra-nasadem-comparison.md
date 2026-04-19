---
tags: [source, graphics, planet-engine, dem, nasadem, srtm]
date: 2026-04-19
sources: 1
---

# Preliminary comparison of NasaDEM dataset（Outerra Blog）

[[outerra-team]] 2018 年 1 月的短文，测试了 NASA 即将发布的 NasaDEM preliminary build（宣称重新处理 SRTM 原始数据、用新源 fill void）。

## 摘要

在 SRTM1 原本出 bug 的 s50w075（南美安第斯）tile 做 A/B：原始 SRTM1 满是人工细峰、空洞、被 clamp 到海平面的区域，甚至负高程；SRTM3（90m）稍好但含有线性伪影、高程偶发错值、void 用超粗数据回填；**NasaDEM preliminary 在这块 tile 上依旧有大量 void、线性伪影与错误高程**。对照下独立维护的 Viewfinder Panoramas（全球 3″，用各地本地地图修补 SRTM 空洞）几乎没有伪影。Amazon delta（n00w051）这种原本 OK 的区域 NasaDEM 也未见改进。Outerra 的结论是：不要指望 NasaDEM 自动解决 SRTM 历史包袱；更靠谱的 void fill 来源仍是 Viewfinder Panoramas 等本地地图融合的数据集。

## 关键要点

- **NasaDEM = 重处理 SRTM 原始数据 + 新 void-fill 源**，但 preliminary 的 void 和伪影未消失。
- **Viewfinder Panoramas** 是无（显著）伪影的 3″ 全球备选，适合做补洞参考。
- **单一数据源不够**：planet 引擎需要维护多源合并管线。
- 该文 caveats 多次强调属 preliminary + 非官方结果。

## 链接到的概念

- [[planet-terrain-dem-pipeline]]
- [[outerra-team]]

## 原文

- 链接：https://outerra.blogspot.com/2018/01/preliminary-comparison-of-nasadem.html
- 本地：`raw/articles/outerra.blogspot.com/2018-01-28_preliminary-comparison-of-nasadem.md`
