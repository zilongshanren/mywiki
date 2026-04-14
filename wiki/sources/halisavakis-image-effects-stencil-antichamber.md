---
tags: [source, 渲染, unity, shader, 模板缓冲, surface-shader]
date: 2026-04-14
sources: 1
---

# My take on shaders: Stencil shader (Antichamber effect) (Harry Alisavakis)

[[harry-alisavakis]] *My take on shaders* 系列第八篇（2017-06-28），跳出 image effect 线，第一次涉及 [[stencil-buffer|模板缓冲]]，目标是复刻《Antichamber》那种「魔方每一面看到不同物体」的视觉戏法。

## 摘要

文章的教学顺序很特别——先讲概念后讲代码。整套效果由两类物体组成：**stencil mask**（不可见的几何，唯一作用是往模板缓冲写入一个 reference number）和 **stencil object**（真实物体，但只在「当前像素的模板值等于自身 ref」时才输出颜色）。两者用同一个 `_RefNumber` 整型属性配对：编号 1 的 mask 让编号 1 的 object 可见，依此类推。Mask shader 用 `Tags { Queue = "Geometry-100" }` 强制提前绘制，`ColorMask 0` + `ZWrite off` 抹掉颜色和深度痕迹，`ForceNoShadowCasting=True` 避免投阴影，`Stencil { Ref [_RefNumber] Pass replace }` 在覆盖的像素上写入 ref。Object shader 是普通的 standard surface shader 加 `Stencil { Ref [_RefNumber] Comp equal }`，模板等于 ref 才输出。Alisavakis 承认这套朴素方案的缺点：stencil object 用 `ForceNoShadowCasting` 之后完全不会投阴影，要保留阴影需要更复杂的 multi-pass 处理，他没有深入。整支 shader 几乎完全套用 Unity Standard Surface 模板，只为模板缓冲加了几行配置——技术含量主要在「想到这个组合」而不是 shader 写法。

## 关键要点

- mask + object 配对模式：mask 写 ref、object `Comp equal`，是模板缓冲做「窗口可见」效果的最小套路。
- mask 必须用 `Queue = Geometry - 100` 抢在普通几何之前画，否则顺序错了 object 看不见。
- mask shader 的四件套：`ColorMask 0` + `ZWrite off` + `ForceNoShadowCasting` + `Pass replace`。
- 同一族技术能派生：传送门、X 光、橱窗物体、Doom 3 风格的可见性裁剪。
- 缺点：stencil object 默认不投阴影，否则会出现「人看不见物体但地上有阴影」的穿帮；要保留阴影需要更复杂的 pass。
- 比 [[render-textures-unity|RenderTexture]] 方案便宜一个数量级，因为模板缓冲是硬件专用通路。

## 链接到的概念

- [[stencil-portal-shader-antichamber]]
- [[stencil-buffer]]
- [[unity-surface-shaders]]
- [[render-textures-unity]]
- [[fragment-shader]]
- [[harry-alisavakis]]

## 原文

- 链接：<https://halisavakis.com/my-take-on-shaders-stencil-shader-antichamber-effect/>
- 本地：`raw/articles/halisavakis.com/2017-06-28_my-take-on-shaders-stencil-shader-antichamber-effect.md`
