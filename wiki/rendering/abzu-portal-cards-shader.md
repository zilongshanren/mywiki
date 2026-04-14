---
tags: [渲染, unity, shader, 透明, 游戏设计, 引导, vfx]
date: 2026-04-14
sources: 1
---

# ABZÛ「portal card」shader

**Portal cards** 是 Matt Nava 在 GDC 上讲 [ABZÛ](https://www.youtube.com/watch?v=l9NX06mvp2E) 美术技巧时提到的一个小手法：在远方的通道口、洞穴入口或大群鱼群后面放一张**正对玩家的透明贴片**（广告牌式的 card），贴片的不透明度随相机距离变化——远则显、近则隐。视觉结果是远景中有"模糊的光团/色斑"引导玩家前往，走近后卡片自然淡出、让真正的几何接管。这是一个既**美化远景**又**隐式引导玩家**的双功能工具，[[harry-alisavakis|Harry Alisavakis]] 在 *How I'd do it* 系列里用一支十几行的 vertex/fragment shader 复刻了它的核心思想。

## 核心公式：按相机距离 lerp alpha

整个效果本质上是**一个由相机距离驱动的 alpha 曲线**加上**一个平面内的 falloff 形状**。fragment 里只有几行：

```hlsl
fixed4 col = tex2D(_MainTex, i.uv) * _BaseColor;
float camDist = distance(i.worldPos, _WorldSpaceCameraPos);
col.a = lerp(_MinAlphaValue, _MaxAlphaValue, saturate(camDist / _MaxCamDist));

float falloffU = pow((sin(i.uv.x * PI) + 1) / 2, _FallOffU);
float falloffV = pow((sin(i.uv.y * PI) + 1) / 2, _FallOffV);
col.a *= falloffU * falloffV;
```

三部分分别讲：

1. **相机距离 → alpha 曲线**：vertex shader 把 `worldPos` 用 `mul(unity_ObjectToWorld, v.vertex)` 算出并 interpolate 到 fragment，再用 `distance(worldPos, _WorldSpaceCameraPos)` 得到这个像素到相机的距离。`saturate(camDist / _MaxCamDist)` 把距离归一化到 `[0, 1]`，于是近处得 0、远处得 1，再用 `lerp(_MinAlphaValue, _MaxAlphaValue, t)` 把这段线性值映射到美术指定的"最不透明 / 最透明"两端。默认是 0 → 1，即近处完全透明、远处完全可见——和直觉相反，但"近处让几何接管"才是 portal card 的要义。
2. **UV 内部 falloff**：如果卡片是硬边矩形，远看会像一个发光的方块，违和。用 `pow((sin(uv.x * π) + 1) / 2, _FallOffU)` 做**水平方向的软化 falloff**——`sin(πx)` 在 `x ∈ [0, 1]` 上是一个从 0 到 1 再到 0 的拱形，用它当权重可以让 alpha 从卡片两侧向中心渐变到 1；`pow(_, _FallOffU)` 的指数调整拱形的"宽窄"。垂直方向同理。两者相乘就得到一个从四边向中心收敛的椭球形软遮罩，远看就像一团自然的光晕而不是一张方卡片。
3. **关闭 fog**：portal card 的常见用法是指引远方的洞口，**刻意穿透雾**。Unity 的默认 surface shader 会自动把 fog 混进 color，于是即便 alpha 正确，颜色也会被 fog 拉灰——Alisavakis 特别指出要**跳过 `UNITY_APPLY_FOG`**，或者直接写 unlit 版本。

## 为什么这是一个"用技术解决设计问题"的样本

ABZÛ 这个 trick 的漂亮之处在于它一次性解决了三个问题：

- **美化远景**：远处的洞穴、光柱、鱼群即便几何 LOD 被裁掉，也有一张贴片顶替，画面不空。
- **引导玩家**：玩家的眼睛天生会被"亮 / 饱和 / 运动"吸引，把 portal card 贴在你希望他前往的位置，就是一次隐式的 UX 导航。这是 [ABZÛ](https://en.wikipedia.org/wiki/Abz%C3%BB) 游戏设计里"开放但不迷路"的核心机制之一。
- **自动淡出**：玩家一旦走近，卡片自己消失，避免了"近看发现是贴片"的穿帮。相比传统的 billboard / imposter 做法，它不需要美术手工摆 trigger、不需要脚本管理淡出逻辑，全部由 shader 里一行距离判断完成。

这是[[harry-alisavakis|Alisavakis]] *How I'd do it* 系列的第一期，他在系列里专门复刻 GDC / 粉丝关心的技术美术片段——强调**能在 10 分钟内用 15 行 shader 做出来的版本**，为的是把思路说清楚，而不是追求还原到像素级。

## 工程细节与坑

- **透明排序**：portal card 走 `Queue=Transparent` + `Blend SrcAlpha OneMinusSrcAlpha` + `ZWrite Off`。多张 portal card 之间的互相遮挡会因为不写深度而乱序，需要美术保证它们不重叠或用 [[alpha-blending|alpha blending 的深度排序]] 手法处理。
- **worldPos 取整方式**：原文写 `mul(unity_ObjectToWorld, v.vertex)`——这给出顶点的世界位置，不是相机空间位置。用这个算距离需要 `_WorldSpaceCameraPos` 是世界空间（Unity 的约定确实如此）。如果要更精确的"到屏幕中心"的距离，应该算 view space 或直接比 `ComputeScreenPos` 的深度分量。
- **falloff 的对称假设**：`sin(uv * π)` 形状假设 UV 是 [0, 1] 的规整方块。如果贴图有 padding / 非方形 aspect，需要先 `TRANSFORM_TEX` 或手工映射。
- **性能**：每 portal card 只是一个几何平面 + 一支极便宜的 shader，几十上百张堆起来几乎零成本，这也是 ABZÛ 敢大量铺的原因。

## 相关

- [[coordinate-spaces]] —— worldPos 的计算与 shader 内坐标空间切换
- [[world-screen-space-position-shader]] —— Alisavakis 后续在 *Shader bits* 系列里把这套取 worldPos 的套路单独拎出来写了
- [[alpha-blending]] —— 透明管线与深度排序
- [[unity-surface-shaders]]
- [[fragment-shader]]
- [[volumetric-fog-froxels]] —— 真正的体积雾背景下让 portal card 能透雾的原因
- [[harry-alisavakis]]

## Sources

- [[sources/halisavakis-abzu-portal-cards]]
