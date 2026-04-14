---
tags: [source, rendering, shader, unity, 2d]
date: 2026-04-14
sources: 1
---

# How I'd do it: BLUK visuals（Harry Alisavakis / Technically Art）

[[harry-alisavakis]] 于 2017 年 4 月发表的技术美术小品文，拆解手机游戏 BLUK 那种「彩色 2D 雾 + 伪 3D 精灵 + 视差滚动」的视觉风格并给出一套 Unity 自制方案。

## 摘要

作者把 BLUK 的远景氛围归纳为两条线索：一是距离相关的「天空色覆盖」，二是精灵底部向天空色渐变的柔化过渡。他不想靠半透明平面或脚本手动调值这种笨办法，于是写了一支 2D 精灵着色器 `Custom/2DFogSpriteShader`，在 [[fragment-shader]] 里直接算当前像素世界坐标到相机的距离，归一化为 `distFactor` 后：先用 `lerp(texcol, _SkyColor, distFactor)` 做距离相关的整体染色，模拟「越远越淡入地平线」；再用第二次 lerp 对精灵下沿做竖向渐变，`gradientFactor = distFactor / 3` 决定渐变起始高度，复杂图案若出现透明通道被污染就回填原图 alpha。配套两个极简 C# 脚本：一个把天空色同步到相机 `backgroundColor` 和材质 `_SkyColor`，一个把背景物体挂到相机下按 `(farClip - z) / farClip` 的权重做视差。整篇文章是技术美术「把观感拆成可参数化的着色项」的范例。

## 关键要点

- BLUK 视觉的核心是距相关的单色覆盖，本质是 HLSL `distance(worldPos, _WorldSpaceCameraPos)` 的一个 saturate 重映射
- 精灵着色器在顶点阶段算世界坐标传给片元，片元里做两次 lerp 完成「远处淡化」和「下沿柔化」
- alpha 处理是个坑：作者最初让渐变污染了透明区域，后来显式把 `texcol.a` 赋回 `finalCol.a`，再加一个 `if (IN.texcoord.y < gradientFactor) finalCol = _SkyColor` 遮住下沿的黑边
- 视差脚本不用改相机、而是让背景物体按各自 z 距离反向平移，越深的物体移动越少，避免跟物理系统冲突
- 这是 Alisavakis 博客的第一篇「技术拆解」文章，后续 ShaderQuest 系列的雏形

## 链接到的概念

- [[bluk-2d-fog-sprite-shader]]
- [[fragment-shader]]
- [[shaderlab-hlsl-basics]]

## 原文

- 链接：<https://halisavakis.com/how-id-do-it-bluk-visuals/>
- 本地：`raw/articles/halisavakis.com/2017-04-05_how-id-do-it-bluk-visuals.md`
