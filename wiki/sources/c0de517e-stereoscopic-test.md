---
tags: [source, 渲染, 立体, reprojection, hlsl]
date: 2026-04-19
sources: 1
---

# Stereoscopic test（C0DE517E / Angelo Pesce 2010-11-02）

[[angelo-pesce]] 2010 年 11 月贴出的一份 FX Composer + HLSL 小实验，把立体 3D 的"单眼渲染 + 另一眼重投影"思路跑通了一个粗糙版本，主要意图是向同行说明**理论**而非给出可用解。

## 摘要

方法是典型的 screen-space reprojection：先把基准眼的 `(linearZ, pattern)` 烘到一张 A8B8G8R8 纹理（深度用经典 `(1,255,65025,160581375)` base-256 分解编到 RGB），再用全屏 pass 对每个目标像素沿 X 方向 brute-force 扫 127 个邻居，每个邻居 decode 回视空间、加一个硬编码 IPD 偏移 `(0.2, 0, 0)`、重投影回屏幕，判断是否落进 `2/width` 像素的容差带，取最近深度者作为答案。空洞用一个 `rowDist² / depth` 最小的"最邻近"启发式占位——作者自己承认不配叫做 solution。文章的核心价值是把**重投影 + 洞补**这一个在 stereo / motion blur / DoF 里反复出现的问题模式说清楚，并确认"整体两次渲染"是错的工业基线——应该 reproject + hi-Z/hi-stencil prime 做 partial redraw。正式的 inpainting 方法他承诺「可能」后续再写，但博客后来没有这篇跟进。

## 关键要点

- 立体视差几乎只沿屏幕 X，可把 reprojection 搜索降到一维
- 深度编码到 RGBA8 的 base-256 分解是当年常用 trick，用来在没有 float render target 的环境里精确传递 linear Z
- **disocclusion 洞补是 reprojection / motion blur / DoF 共享的核心难题**，方法论层面可相互借鉴
- brute-force 127 taps 是 proof-of-concept，不是产品实现；产品版应该先 reproject、再只在空洞处做 hi-Z / hi-stencil 加速的二次绘制
- 评论区点出：两眼各全渲染一遍在工业上绝对错误

## 链接到的概念

- [[stereo-reprojection-hole-fill]]
- [[temporal-supersampling]]
- [[reprojected-planar-reflection]]
- [[linear-z-trick]]
- [[angelo-pesce]]

## 原文

- 链接：https://c0de517e.blogspot.com/2010/11/stereoscopic-test.html
- 本地：`raw/articles/c0de517e.blogspot.com/2010-11-02_stereoscopic-test.md`
