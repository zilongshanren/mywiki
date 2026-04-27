---
tags: [source, rendering, ibl, cubemap, 视差修正, 误差分析]
date: 2026-04-27
sources: 1
---

# Being More Wrong: Parallax Corrected Environment Maps（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2015 年 3 月的跟进文章，承接其 2014 年 6 月《Oh, Envmap Lighting, How Do We Get You Wrong》，专门分析视差修正（parallax-corrected / localized / proxy geometry）cubemap probe 引入的额外误差层。

## 摘要

作者系统枚举三类主要误差来源。第一是预过滤形状（pre-filter shape）的错误：cubemap 不在无穷远时，BRDF 波瓣的"落点"取决于视向量、法线、表面位置和参数等多个维度，而不只是角度；以 proxy 中心角度为基础的预过滤只优化了单一观察点，且对于非垂直入射墙面会产生各向异性 footprint，导致粗糙表面的反射看起来比实际更清晰。第二是可见性（visibility）问题：box proxy 无法捕获室内物体，导致反射穿透遮挡物；更精细的 proxy 又会破坏预过滤的连续性假设，形成尖锐不连续。第三是一些次要误差：probe 间的插值误差、非漫反射散射的烘焙误差、大气散射影响等。结论是：如果你认为自己的 PBR 管线没有重大误差，那只是你还没找到它们；PBR 的价值在于把 hack 变成"有物理依据的 hack"，需要参考真值（path tracer）来量化和优化。

## 关键要点

- parallax correction 最适用于**粗糙表面**（filter footprint 错误最不显著），但反讽地，**遮挡 / 可见性修复最困难**的也恰恰是粗糙表面
- renormalization（Lazarov / Black Ops 2）trick：用 diffuse irradiance 比值修正 cubemap 强度——只在粗糙材质上有效，sharp 反射上反而会出错
- screen-space reflections 与 cubemap fallback 混用时的过渡噪声往往比单独用其中一种更糟糕
- 用 importance sampling 做多 tap 实时参考渲染是验证预过滤误差的可靠方法；可以通过 free-parameter 数值优化拟合更准确的近似

## 链接到的概念

- [[parallax-corrected-cubemap]]
- [[envmap-ibl-approximation-errors]]
- [[screenspace-reflections]]
- [[split-sum-approximation]]

## 原文

- 链接：https://c0de517e.blogspot.com/2015/03/being-more-wrong-parallax-corrected.html
- 本地：`raw/articles/c0de517e.blogspot.com/2015-03-28_being-more-wrong-parallax-corrected-environment-maps.md`
