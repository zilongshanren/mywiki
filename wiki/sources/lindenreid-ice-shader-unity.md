---
tags: [source, shader, 透明, fresnel, grabpass, unity]
date: 2026-04-14
sources: 1
---

# Ice Shader in Unity（Linden Reid）

[[linden-reid]] 2017 年 12 月 30 日的 Unity shader 教程，把 Fresnel 透明度、bump 光照和 GrabPass 扭曲三块叠成一块"冰/水晶"材质——她自己说这是当时写过最长的一篇。

## 摘要

Shader 分两个 pass。前置 pass 用 `GrabPass { "_BackgroundTexture" }` 抓取到目前为止的帧缓冲，再在 vertex shader 里把 `grabPos.xy` 按 `_BumpTex` 的 rg 通道偏移 `_DistortStrength`，fragment shader 用 `tex2Dproj` 采样得到屏幕空间扭曲的冰后背景。正式 pass 走 Transparent 队列 + `SrcAlpha OneMinusSrcAlpha` + `Cull Off`，fragment 同时做三件事：(1) `edgeFactor = abs(dot(viewDir, normal))`、`opacity = pow(min(1, _Color.a / edgeFactor), _EdgeThickness)` 算 Fresnel 边缘不透明度，再用 `1 - edgeFactor` 采样 ramp 纹理决定边缘颜色；(2) `bump = tex2D(_BumpTex, uv).rgb + input.normal`——直接把噪声 RGB 当法线加到顶点法线上（作者自嘲"lazy noise texture"），取 `dot(bump, lightDir)` 采样另一张 ramp 做 cel bump 光照；(3) 把边缘颜色/透明度与 bump 光照相乘输出。作者明确指出所有效果都可以拆出来复用到水面、玻璃等材质。

## 关键要点

- Fresnel 不透明度：`|dot(V, N)|` + `pow` 压缩，正面透明、边缘不透明
- "Lazy" bump：noise 纹理 RGB 直接加到 vertex normal 上做 iridescent 效果
- GrabPass + `ComputeGrabScreenPos` + `tex2Dproj` 实现屏幕空间扭曲背景
- 扭曲 pass 必须在主 color pass 之前
- ramp 纹理贯穿 cel 光照与边缘着色，复用了 cel-shader 系列的外化策略

## 链接到的概念

- [[ice-shader-unity]]
- [[unity-grabpass-blur]]
- [[stylized-water-shader]]
- [[cel-shader-outline]]
- [[texture-encoded-state]]
- [[alpha-blending]]
- [[linden-reid]]

## 原文

- 链接：https://lindenreidblog.com/2017/12/30/ice-shader-in-unity/
- 本地：`raw/articles/lindenreid.wordpress.com/2017-12-30_ice-shader-in-unity.md`
