---
tags: [source, shader, toon, 光照, stencil, unity]
date: 2026-04-14
sources: 1
---

# Cel Shader with Outline in Unity（Linden Reid）

[[linden-reid]] 2017 年 12 月的 Unity shader 教程，两 pass 的 cel shading + 描边——她所有 shader 系列里被最多人引用的一篇。

## 摘要

Pass 1 做 cel 光照：`dot(N, L)` 得到标量光强，用它作为 u 坐标采样一张两段硬色阶的 ramp 纹理，最后 `albedo * lighting * _Color`。ramp 纹理必须是 clamp+point 采样，水平方向两段（左深右亮），才能保留硬边。作者自述第一版把 ramp 采样放在 vertex shader 里，结果三角形内部被线性插值成渐变——**必须在 fragment 做**。Pass 2 做描边：在 vertex shader 里把顶点沿法线方向外推 `_OutlineExtrusion`，然后借 stencil buffer 实现「只在原模型边缘画」——Pass 1 写 stencil = 4，Pass 2 用 `Comp notequal` 读 stencil，只有不在原模型区域的像素才写入。同时 `Cull OFF` 避免 backface 被丢、断裂描边。作者列了四个踩坑：(1) 光照放 vertex shader 的 blended 边缘；(2) 缩放 vertex 而不是沿法线 extrude 导致的不均匀描边；(3) 非 manifold mesh 让描边裂开；(4) 忘记 `Cull OFF` 漏描边。

## 关键要点

- 用 1D ramp 纹理 + fragment shader 采样实现硬色阶 cel 光照
- 描边 = 沿法线外推后的第二次绘制 + stencil masking
- `Ref 4 Comp always Pass replace` 写 stencil；`Comp notequal` 读 stencil 实现内部 mask
- `Cull OFF` 保证描边完整
- 非 manifold mesh 会让 extrude 出现裂缝

## 链接到的概念

- [[cel-shader-outline]]
- [[stencil-buffer]]
- [[stylized-water-shader]]
- [[texture-encoded-state]]
- [[linden-reid]]

## 原文

- 链接：https://lindenreidblog.com/2017/12/19/cel-shader-with-outline-in-unity/
- 本地：`raw/articles/lindenreid.wordpress.com/2017-12-19_cel-shader-with-outline-in-unity.md`
