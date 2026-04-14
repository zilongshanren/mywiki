---
tags: [人物, 作者, 渲染, 游戏引擎]
date: 2026-04-14
sources: 2
---

# Emilio López Ros（Redorav）

**Emilio López Ros** 是一位西班牙图形程序员，个人博客为 [The Code Corsair](https://www.elopezr.com)（elopezr.com），署名 **Redorav**。早年在 Gameloft 马德里工作室参与了若干手游原型开发，后来转向 AAA 渲染方向。他的博客以两类内容见长：

## 风格

- **逐帧拆解 AAA 游戏的渲染管线**——沿袭 Adrian Courrèges 的「Graphics Study」传统，用 RenderDoc 把商业游戏的一帧从 depth pre-pass 一路跟到最终 tonemapping。ROTR、Castlevania: Lords of Shadow 2、Shadow of Mordor 都被他扒过。这类文章是「读源码」之外为数不多能让外人窥见商业引擎内部的途径。
- **技术 deep-dive**：对自己熟悉的某个主题写 tutorial 风格的长文。[[temporal-antialiasing|TAA]] 那篇是社区公认最好的 TAA 入门之一，从 jitter 一路讲到 reconstruction filter 的每一个坑。

## 对本 wiki 的贡献

| 文章 | 贡献的概念 |
|---|---|
| The Rendering of Rise of the Tomb Raider | [[tiled-light-prepass]]、[[hbao-interleaved-sampling]]、[[depth-aware-upsampling]]、[[fizzle-lod-fading]]、[[volumetric-fog-froxels]] |
| Temporal AA and the Quest for the Holy Trail | [[temporal-antialiasing]]、[[motion-vectors]]、[[taa-history-rectification]] |

## 相关

- [[temporal-antialiasing]]
- [[tiled-light-prepass]]
- [[rendering-pipeline]]

## Sources

- [[sources/elopezr-rotr-rendering]]
- [[sources/elopezr-taa-holy-trail]]
