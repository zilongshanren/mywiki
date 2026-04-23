---
tags: [source, 渲染, 延迟渲染, x-plane, 2012]
date: 2026-04-19
sources: 4
---

# Deferred Weirdness 系列四篇（Ben Supnik / The Hacks of Life）

[[ben-supnik|Supnik]] 2012-11-16 到 11-19 连着写了四篇复盘 X-Plane 10.10 延迟渲染管线重写，合编为本条源摘要：

- 2012-11-16 *Deferred Lighting: Stenciling is not a Win*
- 2012-11-17 *Deferred Weirdness: Collapsing Two Passes*
- 2012-11-18 *Deferred Weirdness: When Not to be Linear*
- 2012-11-19 *Deferred Weirdness: What Have We Learned?*

## 摘要

X-Plane 10.10 把初代 deferred 管线全面改造。本系列拆出四个主题：(1) 光源体积的 **stencil 剔除优化**在 X-Plane 的负载画像（顶点带宽紧、shader 浅、光源多但小）下**反而是净亏损**，关掉后顶点吞吐减半；(2) **双 depth domain**（外部世界 + 近距座舱）不能走双 deferred pass——带宽会炸——必须合成一套多 buffer 多 stencil 的缝合状态机，用 stencil 标记 + depth clear 两步把两张 depth 上的测试拼起来；(3) 延迟光累加必须 **linear**，但 X-Plane 旧 alpha 内容（玻璃/淡出 3D 物体/emissive-albedo G-Buffer 层间合成）**必须 sRGB**——同一帧维护两套 blend 方程；(4) 三条困难单独都好办，**juggling 三条同时出现**才是真正的复杂度来源，根源是 X-Plane 作为**平台**无法单方面改美术工作流。

## 关键要点

- **Stencil 光源体积优化不是普适胜利**——workload 画像决定——X-Plane 的街灯场景里顶点流比 fill rate 更瓶颈，stencil 两 pass 得不偿失。下一步考虑把光源体积换成屏幕空间 quad。
- **两次 deferred pass 不可行**。log-depth 在 VS 里跨相机平面 NaN、FS 里改 depth 杀早期 Z。解法：G-Buffer / HDR / LDR 共用 depth，但用 [[deferred-depth-reuse-tradeoffs|路线 C]]（G-Buffer 写 16F 眼空间 Z）承担位置重建，depth 可 clear 重用。
- **多 buffer 缝合怪流程 11 步**：一次 depth clear + stencil 多位（heat blur、in-cockpit）+ MRT 频繁切换。不做 surface 二次 pass，但 state 切换很多。
- **sRGB 与 linear blend 必须共存**：累加光 linear；G-Buffer 层间 alpha blend 必须 sRGB 才能保证 `blend(A,B,α) + blend(C,D,α) = blend(A+C,B+D,α)`——这等式只在"blend 和 addition 在同一 color space"时成立。
- **alpha 过 G-Buffer 的取舍**：所有通道按 src-alpha 加权平均，eye-space Z **不 blend**（阴影 aliasing 禁区）。normal 能 blend 依赖 [[compact-normal-encoding|Lambert azimuthal 编码]]。
- **不能把 linear additive 效果画进延迟**——必须留 HDR forward post-gbuffer pass。
- **教训**：工程复杂度是 "硬边角叠加" 的结果，单条都能治，多条 juggling 才炸；尽可能只留一个硬边角。
- Supnik 自评：复杂管线是 **success** 而非失败——成功同时交付延迟管线收益 + 兼容旧内容。

## 链接到的概念

- [[xplane-deferred-pipeline-hacks]] — 本系列的合编概念页
- [[deferred-rendering]]
- [[xplane-gbuffer-format]]
- [[deferred-depth-reuse-tradeoffs]]
- [[deferred-light-volume-stencil-depth-clamp-hack]]
- [[deferred-alpha-lighting]]
- [[linear-lighting-pipeline]]
- [[srgb-premultiplied-alpha-compression]]
- [[compact-normal-encoding]]
- [[agp-vs-vram-streaming]]
- [[cheat-by-solving-less]]

## 原文

- 链接：
  - http://hacksoflife.blogspot.com/2012/11/deferred-lighting-stenciling-is-not-win.html
  - http://hacksoflife.blogspot.com/2012/11/deferred-weirdness-collapsing-two-passes.html
  - http://hacksoflife.blogspot.com/2012/11/deferred-weirdness-when-not-to-be-linear.html
  - http://hacksoflife.blogspot.com/2012/11/deferred-weirdness-what-have-we-learned.html
- 本地：
  - `raw/articles/hacksoflife.blogspot.com/2012-11-16_deferred-lighting-stenciling-is-not-a-win.md`
  - `raw/articles/hacksoflife.blogspot.com/2012-11-17_deferred-weirdness-collapsing-two-passes.md`
  - `raw/articles/hacksoflife.blogspot.com/2012-11-18_deferred-weirdness-when-not-to-be-linear.md`
  - `raw/articles/hacksoflife.blogspot.com/2012-11-19_deferred-weirdness-what-have-we-learned.md`
