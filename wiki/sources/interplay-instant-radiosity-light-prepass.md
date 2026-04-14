---
tags: [source, 渲染, 全局光照, 延迟渲染, 虚拟点光源]
date: 2026-04-14
sources: 1
---

# Instant Radiosity and light-prepass rendering（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 2013 年 3 月在 Interplay of Light 博客上的午休实验笔记：在 Hieroglyph 的 **light prepass** 引擎里快速实现 **Instant Radiosity** 以探索一次反弹 GI 的视觉效果。

## 摘要

Instant Radiosity 通过将间接光离散成大量 **虚拟点光源（VPL）** 来近似一次反弹的全局光照。Kostas 用 **Reflective Shadowmap**（32×32 双 render target）从光源视角快速采样，一张存世界位置、另一张存 albedo——直接作为光照 pass 的纹理输入，省去 CPU 回读。在 Hieroglyph light prepass 里得到了看起来不错的一次反弹照明：地面把方向光反射到周围物体，随着主光方向移动也不会出现显著闪烁（因为 VPL 天然稀疏）。文章同时明确指出方法的局限：VPL 没有遮挡、主光只能是方向或 spot（点光源要 cube shadow）、多主光或彩色光都要额外 pass、以及与真正的 RSM 存 radiant flux 做法的差异。整体定位是「十几行代码能加进 deferred / light prepass 的第一束 GI」。

## 关键要点

- Instant Radiosity = 从主光射线打到的表面点处放 VPL，用表面 albedo 作为 VPL 颜色
- [[tiled-light-prepass|Light prepass]] 和 [[deferred-rendering|deferred shading]] 天然适合消费大量小光源，而 forward 几乎不行
- 用 **RSM**（低分辨率）代替 CPU raycast 或 GPU 路径追踪，两张贴图双通道：位置 + albedo
- VPL 完全不带遮挡，是该技术的最大短板；粗略可用 screen-space depth buffer 补救
- 只存 albedo 而非 radiant flux → 彩色光源支持需要额外一次光照 pass
- 主光必须是方向或 spot；点光源需要 cube / dual-paraboloid shadowmap 才能做 RSM
- 多主光会线性增加 prepass 开销，所以场景里主光要极少（1 个最佳）
- 32×32 RSM 大约 1024 个 VPL，视觉上已经够用；主光移动时闪烁轻

## 链接到的概念

- [[instant-radiosity-vpl]]
- [[tiled-light-prepass]]
- [[deferred-rendering]]
- [[shadow-mapping-basics]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2013/03/21/instant-radiosity-and-light-prepass-rendering/
- 本地：`raw/articles/interplayoflight.wordpress.com/2013-03-21_instant-radiosity-and-light-prepass-rendering.md`
