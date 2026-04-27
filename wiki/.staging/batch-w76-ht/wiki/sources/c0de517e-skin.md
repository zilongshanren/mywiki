---
tags: [source, rendering, subsurface-scattering, skin]
date: 2026-04-19
sources: 1
---

# Skin（c0de517e.blogspot.com / Angelo Pesce）

[[angelo-pesce]] 2010 年 3 月的一则短评，列举当年自己心目中皮肤渲染做得最出色的几款游戏：*Bad Company 2*（户外光照整体最自然）、*Mass Effect 2*（过场动画光照漂亮但皮肤略「平」），以及 *Fight Night*（综合最复杂，同时是唯一没有 shadowmap 瑕疵的）。Pesce 把「今年的个人目标」定为超越这几款作品的皮肤效果。

## 摘要

博文本身只有三四句话，真正的技术信息密度集中在评论区。当时在 EA（后转 AMD）的 Jim Hejl 确认 *Fight Night 4* 的皮肤方案借鉴了 *ShaderX7* 里他自己撰写的那一章——即早期的**屏幕空间扩散（screen-space diffusion）**思路，为了在 60Hz 下 ship 做了大量近似。Pesce 本人在回帖里补充：FN4 实际并**没有**把 SSS 用到 gameplay 中，他自己曾把 UV-space blur 技术大幅优化，但最终得出的结论是——在严格预算下，用数学上不严谨但视觉过关、而且超级快的 hack 反而更合算，并推荐 d'Artiste 上 Stahlberg 写的皮肤着色一文作为参考。

这一条小评注折射了 2010 年前后皮肤渲染的工业现实：学界已经有 [[sss-practical-implementation|d'Eon & Luebke 的十高斯可分 SSS]] 等较完整的方案，但在 60Hz AAA 实时管线里，团队往往只 ship 得起近似版甚至纯 hack。

## 关键要点

- 2010 年 Pesce 视角的皮肤渲染 benchmark：Bad Company 2 / Mass Effect 2 / Fight Night 4。
- FN4 的皮肤路线基于 Jim Hejl 在 *ShaderX7* 中的屏幕空间扩散方案，但最终版本做了大量简化。
- UV-space blur（纹理空间模糊）是当时主流 SSS 近似之一，优化后仍不足以进 FN4 gameplay 路径。
- 经验性结论：在严格性能预算下，视觉合格的 hack 有时比「数学更正确」的完整 SSS 更实用。
- 相关技术脉络见 [[sss-practical-implementation]]（Jimenez / d'Eon 风格的可分高斯 SSS 实现）。

## 链接到的概念

- [[sss-practical-implementation]]
- [[angelo-pesce]]

## 原文

- 链接：https://c0de517e.blogspot.com/2010/03/skin.html
- 本地：`raw/articles/c0de517e.blogspot.com/2010-03-07_skin.md`
