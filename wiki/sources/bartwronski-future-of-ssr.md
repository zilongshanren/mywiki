---
tags: [source, 渲染, ssr, reflection]
date: 2026-04-14
sources: 1
---

# The future of screenspace reflections（Bart Wronski）

[[bartosz-wronski|Bart Wronski]] 2014 年 1 月发表的复盘长文，总结他在 **Assassin's Creed 4: Black Flag** 上使用屏幕空间反射（SSR）的经验，以及与 Killzone: Shadow Fall、Battlefield 4 等同期作品的对照观察。一篇「The Good, The Bad, The Ugly」格式的工程反思，是早期 SSR 工业落地的一手记录。

## 摘要

文章先梳理 SSR 的优势：对任意朝向/曲率的反射面通用、与延迟管线零 CPU 成本集成、自动反射动画材质和粒子、给 cubemap 提供 SSAO 式的遮蔽、命中率被 Fresnel 天然偏向屏幕内信息。接着列出三类根本缺陷——离屏信息缺失、背面信息缺失（第三人称主角在镜面/窗户里反射不出）、深度缓冲的厚度假设失效（投射到层叠物体后阴影偏移）。真正「丑陋」的是这些缺陷在时空上不稳定：闪烁、空洞、角色留下幽灵拖影。作者坦陈 AC4 的可出货形态是大量 [[temporal-supersampling]]、双边滤波、保守测试、分离高斯基模糊、层级上采样、flood-fill 填洞，以及始终回退到 localized / parallax-corrected cubemap 叠加。最后展望：多帧累积 radiance/几何缓存、多层深度缓冲、低分辨率体素/球/盒加速结构引导光线——这些方向日后大多成真（SDF 追踪、probe 缓存、hybrid RT）。

## 关键要点

- **SSR 只能做「加料」**：单独用必崩；必须与 localized cubemap 或 parallax-corrected probe 叠加兜底。
- **半分辨率几乎是必选**：性能逼迫，代价是 [[aliasing]] 放大，temporal 必须上。
- **三类信息缺失**中最难处理的是厚度假设：可以在深度差太大时 reject，但在层叠物体下永远不准；用多层深度或 depth peeling 能缓解。
- **时间不稳定才是真正的杀手**：静态截图好看，运动里暴露无遗。作者明确点出 AC4、Killzone、BF4 都有肉眼可见的闪烁和幽灵。
- **预模糊源图 + 按粗糙度分开模糊反射图**：作者在 AC4 用了「半分辨率源图先做 gloss 无关的预模糊，再按 gloss 做宽半径分离模糊、按 confidence 加权」这一套。
- **未来方向**（2014 年视角）：体素 / voxel-list / 粗 BVH 引导主光线 + 屏幕空间精算命中；帧间 radiance/geometry 缓存；第二深度层用于校正厚度假设。

## 链接到的概念

- [[screenspace-reflections]]
- [[temporal-supersampling]]
- [[temporal-antialiasing]]
- [[aliasing]]
- [[motion-vectors]]
- [[deferred-rendering]]
- [[parallax-corrected-cubemap]]
- [[bartosz-wronski]]

## 原文

- 链接：https://bartwronski.com/2014/01/25/the-future-of-screenspace-reflections/
- 本地：`raw/articles/bartwronski.com/2014-01-25_the-future-of-screenspace-reflections.md`
