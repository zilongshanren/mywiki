---
tags: [source, 渲染, 法线贴图, 切线空间]
date: 2026-04-14
sources: 1
---

# Normal Mapping Without Precomputed Tangents（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 2013 年 1 月的实验笔记，验证 Christian Schüler 发表在 *thetenthplanet.de* 的**不依赖预计算 tangent frame 的法线贴图**技术。

## 摘要

Anagnostou 读到 Schüler 的博客后在 FX Composer 里复现：用一张高分辨率 normal map（来自 Käy Vriend 博客）渲染 quad，一次用传统**预计算 TBN**、一次用**像素着色器内即时构造 TBN**（基于 `dFdx`/`dFdy` 的屏幕空间偏导数反解切线）。两张对比图视觉上非常接近——第二张整体略暗，但足以说明技术可用。他总结**这是带宽 / 显存紧于 pixel shader ALU 时的理想选择**，而且在 mesh 导出器生成错误 TBN 的情况下它也能兜底。评论区里 Käy Vriend 补充：FX Composer 跑 teapot 模型时，UV 畸变严重的壶嘴区域**预计算 TBN 反而丢对比度**，即时计算的版本更稳。另有评论质疑每像素做 mat3×vec3 的开销，作者澄清这个技术必须在 pixel shader 里算，因为 `dFdx`/`dFdy` 在 vertex shader 里没有等价物——所以「把 L / V 在 vertex shader 预变换到切线空间」那种快法这里不适用。

## 关键要点

- 技术来源：Christian Schüler（*ShaderX5* + thetenthplanet.de 后续优化）
- 核心机制：pixel shader 里用 `dFdx`/`dFdy` 对位置和 UV 求屏幕偏导，反解出 tangent / bitangent
- 收益：顶点不再存 T / B，省显存 / 带宽；对 mesh 导出器错误不敏感
- 代价：pixel shader 多几条算术指令；必须在 pixel shader 里，不能往 vertex shader 搬
- 视觉表现足够接近预计算版本；在 UV 畸变严重的区域反而更好
- 适合带宽约束 > ALU 约束的平台，以及顶点动画 / 过程式 UV 的情形

## 链接到的概念

- [[tangent-free-normal-mapping]]
- [[normal-map-blending]]
- [[fragment-shader]]
- [[compact-vertex-format]]
- [[kostas-anagnostou]]

## 原文

- 链接：<https://interplayoflight.wordpress.com/2013/01/21/normal-mapping-without-precomputed-tangents/>
- 本地：`raw/articles/interplayoflight.wordpress.com/2013-01-21_normal-mapping-without-precomputed-tangents.md`
