---
tags: [source, 渲染, 阴影, csm, 优化]
date: 2026-04-19
sources: 1
---

# Stable Cascaded Shadow Maps - Ideas（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2011 年 3 月的一篇工程笔记，系统整理了在主机上实现 stable CSM 时绕不开的若干工程点，并顺带解剖了 Crysis 2 的阴影实现，最后提出了一个「远级联增量更新」的 sketch——这个 sketch 就是 2012 年 Mike Day 公开实现（见 [[cached-shadowmaps]]）的最上游出处。

## 摘要

Pesce 首先给 stable cascade 下了一个朴素定义：在世界空间把 shadow map 想成一张无限大的纹理，每帧截取固定尺寸窗口，**窗口必须整像素滑动**以避免阴影边缘爬行；窗口大小可用视锥外接球半径兜底。接着他把 CSM 实施过程中让他反复踩坑的要点列成一张清单：用 deferred shadow buffer 把可见性打到屏幕空间以一次只处理一级联；按「最优级联」而非 frustum 切分平面采样像素；用 pancake 压近平面时要在顶点着色器里 clamp 而非硬裁剪，并给近平面留缓冲；不要渲染光空间视锥后方的空白，用 scissor / stencil / hi-z 减少冗余。

然后他做了一段「rendering archeology」：观察 Crysis 2 的 deferred shadow、环形 PCF、无级联淡入、光空间 dither，以及**远级联每隔一帧才更新**的行为。他据此提出两条实现路径：粗暴加 padding 分帧重绘，或者在 shadowmap 原点做 wrap + 增量更新。后者需要解决每帧变化的 near/far 范围与动态物体两个副作用——而这正是一年多后 Mike Day 的论文要完整求解的问题。

评论区还引出 SDSM 作为一条正交优化路线（用 compute 扫 z-buffer 推紧致级联）。

## 关键要点

- **Stable cascade 的核心约束**：窗口整像素滑动，否则阴影边缘抖动。
- **Deferred shadow buffer** 的好处：每级联单独处理、天然支持淡入淡出与半分辨率上采样。
- **「最优级联」策略** vs frustum 切分：前者节省高分分辨率、但剔除时需要保留近级联物体向远级联的阴影投射。
- **Pancake 的权衡**：在 VS 里 clamp z 而非硬裁剪；近平面缓冲避免自阴影失真；hi-z 失效需额外 stencil 标记。
- **贴图打包**：不渲染光空间视锥后方、可把两张 shadowmap 塞进双通道 16-bit。
- **Crysis 2 观察**：远级联每隔一帧更新——这是 [[cached-shadowmaps]] 优化思路的观察起点。
- **增量缓存 sketch**：在 shadowmap UV 上 wrap、只渲染新边界——这就是 Mike Day 2012 论文的 2011 年 sketch 版本。
- **未解工程难点**：动态物体怎么处理、level z-range 每帧变化怎么 re-range。

## 链接到的概念

- [[stable-csm-implementation-tips]]
- [[cached-shadowmaps]]
- [[cascaded-shadow-maps]]
- [[shadow-mapping-basics]]
- [[angelo-pesce]]

## 原文

- 链接：https://c0de517e.blogspot.com/2011/03/stable-cascaded-shadow-maps-ideas.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-03-27_stable-cascaded-shadow-maps-ideas.md`
- 后续：Mike Day, *CSM Scrolling*, SIGGRAPH 2012（Insomniac Games）
