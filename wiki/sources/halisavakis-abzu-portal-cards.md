---
tags: [source, 渲染, unity, shader, 游戏设计, 引导, 透明]
date: 2026-04-14
sources: 1
---

# How I'd do it: ABZÛ portal cards (Harry Alisavakis)

[[harry-alisavakis]] *How I'd do it* 系列 2017-09-25 的开篇，Alisavakis 看完 Matt Nava 在 GDC 上讲 [ABZÛ](https://en.wikipedia.org/wiki/Abz%C3%BB) 的技术美术 talk 后立刻写下的复刻。

## 摘要

文章以 GDC 视频 18 分钟处提到的 "portal cards" 为原型：ABZÛ 在远方的通道口、洞穴入口、大群鱼群背后铺一张正对玩家的透明贴片，贴片透明度随相机距离变化——远则显、近则隐——既美化远景又隐式引导玩家前往目标位置。Alisavakis 用 10 分钟写了一支 Unity vertex/fragment shader 复刻这个思路，不是为了像素级还原，而是想强调"15 行代码能做到的近似"。核心是三部分：`mul(unity_ObjectToWorld, v.vertex)` 拿 worldPos，`distance(worldPos, _WorldSpaceCameraPos)` 算相机距离，`lerp(_MinAlpha, _MaxAlpha, saturate(camDist / _MaxCamDist))` 把它映射到 alpha；再用 `pow((sin(uv.x * π) + 1) / 2, _FallOffU)` 和同样的 V 方向做 UV 内部软化 falloff，避免 card 看起来像硬边方块。他特别指出**要关掉 fog**（`UNITY_APPLY_FOG` 去掉），因为 portal card 常用于穿透远景雾气，不能被 fog 洗掉颜色。

## 关键要点

- ABZÛ portal card 是 Matt Nava 在 GDC 上讲的一个**兼具美学和导航功能**的小 trick：远处放一张距离驱动 alpha 的透明贴片，走近自动淡出。
- 它同时解决了"远景空荡"和"玩家不知道去哪"两个问题，不需要手工脚本。
- shader 核心：`col.a = lerp(_MinAlpha, _MaxAlpha, saturate(camDist / _MaxCamDist))`。
- UV 内部 falloff 用 `pow((sin(uv * π) + 1) / 2, _FallOff)` 得到从四边向中心渐变的软遮罩，指数 `_FallOff` 调"宽窄"。
- **必须跳过 fog** —— portal card 的用途就是穿透雾，fog 会洗掉它的颜色。
- 透明管线：`Queue=Transparent` + `Blend SrcAlpha OneMinusSrcAlpha` + `ZWrite Off`。
- 同是 [[harry-alisavakis|Alisavakis]] 两天后写的 *Shader bits: World and screen space position*（见 [[world-screen-space-position-shader]]）把这里用到的 worldPos 套路独立成 bit。
- Bonus 给了一个 UE4 material 实现截图，证明这个思路跨引擎可移植。

## 链接到的概念

- [[abzu-portal-cards-shader]]
- [[coordinate-spaces]]
- [[world-screen-space-position-shader]]
- [[alpha-blending]]
- [[fragment-shader]]
- [[volumetric-fog-froxels]]
- [[harry-alisavakis]]

## 原文

- 链接：<https://halisavakis.com/how-id-do-it-abzu-portal-cards/>
- 本地：`raw/articles/halisavakis.com/2017-09-25_how-id-do-it-abzu-portal-cards.md`
