---
tags: [source, 渲染, decal, 视差遮挡贴图, cyberpunk]
date: 2026-04-14
sources: 1
---

# Cyberpunk 2077: Phantom Liberty — Broken Edges（simonschreibt.de / Simon Trümpler）

[[simon-trumpler]] 于 2025 年 2 月发表的短篇 VFX 拆解，延续 [[sources/simonschreibt-fallout3-edges|Fallout 3 — Edges]] 的话题：比较不同世代的游戏如何用 decal 在低多边形墙体上伪造破碎感。这次的目标是 CDPR 的《Cyberpunk 2077: Phantom Liberty》里一面凿痕密布的混凝土墙。

## 摘要

Simon 第一眼以为这面墙是高多边形的独特 mesh，但通过分析发现结构其实非常简单：底层是一个 **倒角的方盒子**；一块 **overlap mesh** 被插入墙体充当破碎形状（因用了 3 种材质分 3 次 draw call）；接缝上先贴一张 **普通修补 decal** 盖住交线；最后再叠一张 **POM decal**——视差遮挡贴图的 decal，用灰度高度图在 pixel shader 里 ray-march 出深度，让整面墙看起来像一整块凿出来的石头。Simon 观察到 POM 的深度会随距离和角度被压平，Tech Art Aid 的 Oskar Świerad 在 Bluesky 确认：**步数与角度相关** 是 CDPR 的优化——掠射角时降低 ray-marching 步数以节约 ALU 并避免 POM swimming。整篇是一次「高级 PBR 版的 Fallout 3 边缘 decal」解读。

## 关键要点

- 复杂外观 = 简单盒子 + 分层 decal，而非独特 mesh
- overlap mesh 的多材质会拆成多次 draw call，可以从 wireframe fade-in 推断材质数
- 单纯 decal 遮不住 mesh 穿插的硬接缝，需要 POM decal 才能融合两层几何
- POM 的 ray-marching 步数可以随视角调整，极端角度下可能变成平贴
- 这条谱系能一路往前连到 [[normal-decal-edge-blending|Fallout 3 边缘 decal]] 和 CryEngine 的 destruction decal

## 链接到的概念

- [[pom-decal-broken-edges]]
- [[normal-decal-edge-blending]]
- [[parallax-corrected-cubemap]]
- [[simon-trumpler]]

## 原文

- 链接：https://simonschreibt.de/gat/cyberpunk-broken-edges/
- 本地：`raw/articles/simonschreibt.de/2025-02-10_simonschreibt.md`
