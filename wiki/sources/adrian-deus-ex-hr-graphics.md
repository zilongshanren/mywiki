---
tags: [source, 渲染, frame-analysis, light-prepass, deferred, adriancourreges]
date: 2026-04-27
sources: 1
---

# Deus Ex: Human Revolution – Graphics Study（Adrian Courrèges）

[[people/adrian-courreges]] 发表于 2015 年 3 月的帧分析文章，深入解剖《Deus Ex: Human Revolution》（2011，Eidos Montréal，Crystal Engine，DX11）的完整渲染管线。

## 摘要

文章以 RenderDoc 为工具，逐 pass 拆解一帧的生成过程。游戏使用 **Light Pre-Pass** 渲染架构（非完整 G-Buffer 的延迟渲染，也非前向渲染）：先渲染法线+深度，再生成阴影遮罩（PSSM 技术，支持最多 4 个光源），接着执行 SSAO，然后逐点光源积累 irradiance 到 light map，最终在正向 pass 中结合 light map 和材质贴图完成着色。关键性能技巧是将深度函数设为 `COMPARISON_EQUAL` 而非 `LESS`，实现零 overdraw。UI 渲染共 317 次 draw call，整帧约 253 次用于不透明+透明对象。文章还附有深度散焦（双层高斯模糊 DoF）和交互对象轮廓（Sobel 边缘检测 + alpha 通道标记）的实现细节。

## 关键要点

- [[light-prepass-pipeline]]：先渲染法线/深度，再单独计算 irradiance，最后正向着色——"零 overdraw"的关键
- 阴影遮罩：PSSM 技术将 4 个光源的 PCF 软阴影存入单张 RGBA8 纹理各通道，每通道存储 0–1 浮点 PCF 值
- SSAO 结果存入法线贴图的 alpha 通道，节省一张渲染目标
- 不透明 pass 后关闭深度写入、depth test 改 EQUAL，避免重复着色同一像素
- 轮廓效果（Silhouette）复用 light map alpha 通道标记可交互对象，配合 Sobel 算子产生发光轮廓
- LDR 工作流下 bloom 通过 alpha 通道携带 emissive 强度，不依赖 HDR bright-pass

## 链接到的概念

- [[light-prepass-pipeline]]
- [[shadow-mapping-basics]]
- [[deferred-rendering]]

## 原文

- 链接：http://www.adriancourreges.com/blog/2015/03/10/deus-ex-human-revolution-graphics-study/
- 本地：`raw/articles/adriancourreges.com/2015-03-10_deus-ex-human-revolution-graphics-study-adrian-courreges.md`
