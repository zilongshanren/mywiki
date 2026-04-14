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

此外他在 2014 年前后还写过一组**早期 Android / Java 手游开发时期**的短文（Gameloft《Dragon Mania》性能抢救、独立项目《Will of Flame》的自研引擎、Floyd–Steinberg dither、Java 向量数学的吐槽），虽然不如后来的 AAA 拆解重磅，但能看到一个图形程序员从 MIDP 时代的低端机优化走到 RenderDoc 拆解 ROTR 的完整轨迹。

## 对本 wiki 的贡献

| 文章 | 贡献的概念 |
|---|---|
| The Rendering of Rise of the Tomb Raider | [[tiled-light-prepass]]、[[hbao-interleaved-sampling]]、[[depth-aware-upsampling]]、[[fizzle-lod-fading]]、[[volumetric-fog-froxels]] |
| The Rendering of Castlevania: Lords of Shadow 2 | [[valve-ambient-cube]]、[[deferred-rendering]] 的 DX9 世代实例 |
| Temporal AA and the Quest for the Holy Trail | [[temporal-antialiasing]]、[[motion-vectors]]、[[taa-history-rectification]] |

## 相关

- [[temporal-antialiasing]]
- [[tiled-light-prepass]]
- [[rendering-pipeline]]

## Sources

- [[sources/elopezr-rotr-rendering]]
- [[sources/elopezr-taa-holy-trail]]
- [[sources/elopezr-floyd-steinberg-dithering]]
- [[sources/elopezr-dragon-mania]]
- [[sources/elopezr-will-of-flame]]
- [[sources/elopezr-wof-editors]]
- [[sources/elopezr-java-vector-math]]
- [[sources/elopezr-clos2-rendering]]
