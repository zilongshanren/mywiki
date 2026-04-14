---
tags: [source, 渲染, unity, shader, 后处理, displacement]
date: 2026-04-14
sources: 1
---

# My take on shaders: Simple Displacement (Harry Alisavakis)

[[harry-alisavakis]] 在 *My take on shaders* 系列的第六篇（2017-05-25）把前几篇的工具拼起来，做了一个由灰度遮罩控制的 UV 位移后处理。

## 摘要

shader 引入两个新属性：`_DisplacementMask`（灰度纹理）和 `_DisplacementAmount`（标量幅度）。fragment shader 里先 `tex2D(_DisplacementMask, i.uv)` 取一个灰度值，把它乘上 `_DisplacementAmount` 加到 `i.uv` 上得到新的采样坐标，再用新坐标采 `_MainTex`。结果是黑色区域不动、白色区域整体偏移最大、灰色区域按比例。Alisavakis 用一张「中心白圆 + 柔边」的甜甜圈遮罩演示了「冲击波」原型——把这个 mask 想象成从一个点开始扩散的圆环，就是几乎所有命中反馈的雏形。文章的篇幅不长，重点是把「[[image-effect-mask-blend|遮罩混合]]」这个上一篇教过的工具改写成「不是用来选哪些像素出特效，而是用来调制每个像素的位移强度」——同一张遮罩、不同的语义。文末他坦承这个 shader 没有暴露遮罩的位置和大小参数，要做真正可用的冲击波得用 in-shader 自定义遮罩或者从 C# 脚本传 uniform。

## 关键要点

- **核心算法**：`uv' = uv + maskValue * amount`，再 `tex2D(_MainTex, uv')`。
- 灰度遮罩当 displacement 强度场，黑色=不偏移，白色=最大偏移。
- 「中心白 + 柔边」的圆环遮罩 + 半径动画 = 冲击波。
- 与上一篇 [[image-effect-mask-blend|simple-masks]] 的区别：mask 不再控制「是否出特效」，而是「位移多少」——同一张图，两种语义。
- 局限：mask 是烘焙好的位图，纵横比绑定屏幕、参数无法运行时调；要做生产级冲击波得换 in-shader SDF。

## 链接到的概念

- [[uv-displacement-image-effect]]
- [[image-effect-mask-blend]]
- [[unity-image-effect-basics]]
- [[fragment-shader]]
- [[harry-alisavakis]]

## 原文

- 链接：<https://halisavakis.com/my-take-on-shaders-simple-displacement/>
- 本地：`raw/articles/halisavakis.com/2017-05-25_my-take-on-shaders-simple-displacement.md`
