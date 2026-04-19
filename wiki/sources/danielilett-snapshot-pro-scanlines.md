---
tags: [source, 渲染, unity, urp, 后处理, scanlines, crt]
date: 2026-04-19
sources: 1
---

# Snapshot Shaders Pro - Scanlines（Daniel Ilett）

[[daniel-ilett]] 发布的 *Snapshot Shaders Pro* 产品内参考文档，介绍 Scanlines 扫描线后处理的四个参数。

## 摘要

Scanlines 用一张**外部贴图** (`Scanline Texture`) 驱动扫描线图案，而不是像 [[crt-shader-effects|CRT Shader Graph]] 那样用 `Fraction`/`Modulo` 节点程序化生成。贴图通常很小、横向或竖向重复平铺满屏。产品自带两张示例纹理：`Resources/Textures/ScanlineBasic.png` 给黑白硬边扫描线，`ScanlineColor.png` 给带 RGB 子像素条纹的版本——正好对应 [[crt-shader-effects|Cyan CRT]] 里用 `Modulo 3 + Step` 自造的 RGB 条纹效果，但 Pro 版换成了查表。参数：`Strength`（叠加强度）、`Size`（平铺尺寸）、`Scroll Speed`（随时间滚动，设 0 停住）。查表法的优势是**随便换风格**：Game Boy 3×3 点阵、街机孔栅、CRT 子像素都只是换一张贴图。

## 关键要点

- 贴图驱动而非程序化——换 `Scanline Texture` 就换风格
- 两张示例纹理：Basic（纯黑白线）、Color（RGB 子像素条纹）
- 参数：`Strength`、`Size`、`Scroll Speed`——调强度、周期、运动
- 和 [[crt-shader-effects|Cyan CRT breakdown]] 的程序化扫描线做同一件事，选了"更灵活、像素不完美时靠贴图插值"的工程权衡
- `Scroll Speed=0` 常和像素化管线搭，滚动时常和 [[crt-shader-effects|CRT]] 整体效果搭

## 链接到的概念

- [[crt-shader-effects]]
- [[retro-rendering-techniques]]
- [[urp-volume-post-processing]]

## 原文

- 链接：<https://danielilett.com/snapshot-shaders-pro/scanlines/>
- 本地：`raw/articles/danielilett.com/2026-01-01_snapshot-shaders-pro-scanlines.md`
