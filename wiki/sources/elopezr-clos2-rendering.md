---
tags: [source, 渲染, 帧分析, aaa, dx9]
date: 2026-04-14
sources: 1
---

# The Rendering of Castlevania: Lords of Shadow 2（Emilio López Ros）

[[emilio-lopez-ros|Emilio López Ros]] 2015 年 11 月发表的 AAA 帧拆解文章，用 Intel GPA（因为 DX9 后端无法用 RenderDoc 或 Nsight）抓取 **MercurySteam Mercury 引擎** 的一帧——游戏开场 Dracula 苏醒的场景——把这一帧从 depth pre-pass 到 sharpen 的每个 pass 逐个剖开。和作者 2018 年的 [[elopezr-rotr-rendering|Rise of the Tomb Raider 拆解]] 遥相呼应，一起构成了 elopezr.com 的两大「商业引擎解剖学」长文，且这篇覆盖了一个更老的**DX9 世代**引擎——很多今天看着「奇怪」的 trick 背后其实是平台限制与带宽预算的产物。

## 摘要

Mercury 引擎在这一帧里采用**延迟渲染管线**配合 4 张 G-Buffer（Normal+SSS、Albedo+AO、Specular+Fresnel、Ambient+AO）。它同时写一张「深度即颜色」的辅助缓冲，用来绕过 DX9 无法直接采样 depth 的限制。管线从 depth pre-pass 起步，填入 stencil 标签（Dracula=85、皮肤/头发=86、玻璃/血=133、蜡烛=21），接着是 GBuffer pass。最特别的一点是**光照阶段是一个「立方体 pass」**——渲染一个包围场景的大立方体作为全屏代理，读取 GBuffer + 一张 128×128 cubemap 计算主环境光，而不是惯常的全屏 quad。离散光源包括 point / spot 和不多见的 **"box light"**（用来给金属物件 fill），接着走 shadow caster、forward 透明、HDR→LDR（独立的亮度保存 trick：先把 HDR 归一化并把 luminance 存到 8bit alpha）、motion blur（重投影两帧摄像机矩阵）、dynamic exposure（金字塔 downsample 到 1 像素）、bloom + lens flare、tonemapping、vignette、镜头脏点 quad、AA + sharpen。

文章最重磅的解剖是 **GBuffer Ambient 通道**：一段 DX9 shader 汇编被逐行翻译，暴露出 MercurySteam 在动画几何上使用的是 **Valve 的 Ambient Cube**（[[valve-ambient-cube]]）——法线正负分量分别平方、分别和六个预计算颜色常数做内积，然后叠回 vertex color。López Ros 最初猜是球谐，读完汇编后修正为 Ambient Cube。另一个细节是 **Specular 通道含一个 Schlick 近似的 Fresnel 乘子**——游戏「不是 PBR」，但已经在用 PBR 的零件来打补丁。

## 关键要点

- **DX9 时代的延迟渲染**：4 张 G-Buffer + 一张独立的 depth-as-color（DX9 采样限制的 workaround）
- **Stencil 做材质分类**：pre-pass 时按角色/头发皮肤/玻璃/蜡烛分别写入不同 stencil ref，后续光照按材质分支
- **Cube 而非 Quad**：主环境光 pass 用包围场景的 3D cube 代理而不是 fullscreen quad——等价但选择奇特
- **Valve Ambient Cube 在 AAA 里的实例**：动画几何用六个方向的平均颜色做环境光，shader 汇编里 `saturate(n) * saturate(n) * cubePos + saturate(-n) * saturate(-n) * cubeNeg` 的模式被原样捕获
- **非 PBR 但偷 Fresnel**：Specular 的 w 通道存 Schlick 近似的 Fresnel 乘子，独立于实时光源
- **Box light**：点光/聚光之外的第三类离散光，盒形区域均匀发光，专门用来把金属物打亮/起 bloom
- **HDR→LDR 的亮度切割**：把 luminance 从 HDR 色里归一化掉、存到 8bit alpha，避免 full HDR 后续数学
- **Dynamic exposure**：一条 pyramid downsample 链，从半屏一路缩到 1 像素得到平均 log 亮度
- **Tonemapping 操作符**：`saturate(sqrt(Filmic · (1 - exp(-c))) - Exposure)`——作者不认识，显然是 MercurySteam 自制（某种 Reinhard 变体 + 嵌入式 gamma）
- **Lens dust specks**：几十个纹理 quad 乘在 bloom 目标上做镜头脏点，画面非常电影化
- **参考文献**：López Ros 明确说这一系列灵感来自 [Adrian Courrèges](https://www.adriancourreges.com/) 的 Graphics Study

## 链接到的概念

- [[valve-ambient-cube]]
- [[deferred-rendering]]
- [[early-z-late-z]]
- [[stencil-buffer]]
- [[spherical-harmonics]]
- [[physically-based-shading]]
- [[emilio-lopez-ros]]
- [[elopezr-rotr-rendering]]

## 原文

- 链接：https://www.elopezr.com/castlevania-lords-of-shadow-2-graphics-study/
- 本地：`raw/articles/elopezr.com/2015-11-28_the-rendering-of-castlevania-lords-of-shadow-2.md`
