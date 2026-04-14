---
tags: [source, unity, urp, shader, 透明度, dither]
date: 2026-04-14
sources: 1
---

# Shader Toolbox for URP - Dither Transparency（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] *Shader Toolbox* 资产包中的 **Dither Transparency** shader 文档页。表面是一份资产包 shader 的参数说明，但拆开来正好是 **dither alpha clipping 技术**在 URP Lit shader 上的完整参数集，包括 Bayer 矩阵的运行时生成和可替换的外部 dither 贴图。

## 摘要

文档按三段组织：**Surface Options**（workflow Metallic / Specular 切换、opaque / transparent、front/back/both、alpha clip 阈值、receive shadows——标准的 URP Lit 面板）、**Lit Properties**（Base Color、Base Texture、Metallic/Specular、Smoothness、从 roughness 贴图转换、Normal Map、Heightmap、AO、Emission——也是标准 URP Lit 的物理渲染输入）、**Dithering Properties**（是否使用外部 dither 贴图，否则运行时生成 Bayer 矩阵；dither 贴图的红通道存阈值；dither scale 控制一个 dither 单元覆盖几个像素，整数值最干净；Opacity 作为最终 alpha 的倍数乘）。真正新加进来的只有最后一组 dither 参数，前两组是 URP 内建 Lit shader 的标配。

## 关键要点

- Dither transparency 的核心是 `clip(col.a * opacity - threshold)`，`threshold` 来自屏幕坐标对应的 Bayer 矩阵值——等效于"按图案丢像素"。
- Bayer 矩阵可以 shader 内部生成，也可以外挂——外挂贴图只用红通道，意味着可以用任意 stipple pattern（不只是标准 Bayer）。
- Dither Scale 非整数会和像素格产生 beating 伪影，这是所有"基于屏幕坐标的周期图案"的通病。
- 这个 shader 没有走 URP 的 transparent 队列，依然是 opaque + `AlphaTest`——因此它的优势是能写深度、被 SSAO / depth-based 后处理正确处理，代价是视觉上看到点阵而非连续半透。

## 链接到的概念

- [[dither-alpha-clipping]]
- [[fizzle-lod-fading]] —— LOD 切换最常见的 dither 用途
- [[physically-based-shading]]
- [[alpha-blending]]

## 原文

- 链接：https://danielilett.com/shader-toolbox/dither-transparency/
- 本地：`raw/articles/danielilett.com/2026-01-01_shader-toolbox-for-urp-dither-transparency.md`
