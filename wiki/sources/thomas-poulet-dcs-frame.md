---
tags: [source, 渲染, frame-analysis, dcs, 体积云, MSAA, 2021]
date: 2026-04-19
sources: 1
---

# Digital Combat Simulator: Frame Analysis（Thomas Poulet / 2021）

[[thomas-poulet]] 2021 年 9 月写的 DCS 2.7 帧分析。标的是 Eagle Dynamics 的 DCS World——面向发烧友的真实飞行/战斗模拟器，2008 年就发布，但 2.7 版本给渲染做了大改造。Poulet 对自研引擎特别感兴趣，于是抓了两个场景：外视 Mirage 2000 白天 + A-10C 夜间座舱视角。

## 摘要

DCS 是一个 **clustered deferred** 引擎，GBuffer 用了一种罕见的**多层 R8G8_UNORM texture array + YUV 编码 albedo** 布局（5 层、开 MSAA），stencil 被当 material ID 用得很重（terrain / runway / plane / building / vegetation / cockpit 各有值）。shadow map 是 4 slice 4K CSM，远 slice 因为没做 LOD、没有 proxy caster，一架飞机要 100 万顶点只覆盖 100 像素——一个有趣的未优化。地形和静态环境走 **compute scatter → indirect draw** 的 GPU-driven 路线，但因为没用 bindless，导致大量 empty indirect draw。云是重头——**两张 SDF（水平 + 垂直）驱动 cloudscape**，再用 3D Perlin-Worley 128³ 噪声做 raymarch 细节，路数和 Guerrilla 的 Horizon Nubis 一致。HDR 用 ACES filmic，bloom 六级 blur，最后用 MSAA resolve + heat 效果统一解多重采样。整体给人的感觉：**自研 + 非 AAA 资源规模下，非常老练的「把路子走窄」的选择**。

## 关键要点

- **GBuffer 布局**：5 层 R8G8_UNORM array + MSAA，YUV 跨层存 albedo；详见 [[yuv-gbuffer-layered]]。
- **Stencil = material ID**：terrain 0x04、plane 0x08、vegetation 0x25、cockpit 0x28。
- **CSM 未做 LOD**：远 slice 的 triangle-to-pixel 比约 10,000:1，模拟器能容忍但不漂亮。
- **Compute scatter + indirect draw**：地形/静态物的 GPU culling + lod 选择；shadow map 和 GBuffer pass 共用。
- **Cockpit envmap**：256³ 实时合成 cubemap（prebaked cockpit + env + cloud + shadow + scattering），给 IBL 和透明座舱玻璃用。
- **Reflection 双轨**：环境反射 map ~70% 分辨率 + SSLR（SSR）1/2 分辨率 + blur 到 1/8。
- **Volumetric clouds**：SDF 驱动的 cloudscape，[[cloudscape-sdf-volumetric]] 单列一页。
- **ACES tone mapping + 六级 bloom**。
- **Heat distortion**：用 exhaust 几何生成 mask，同 pass 里 resolve MSAA。
- **UI 是 3D 几何**：MFD 等 cockpit 显示屏按 3D geometry 处理，和世界里的 HUD 混在一起。

## 链接到的概念

- [[thomas-poulet]]
- [[yuv-gbuffer-layered]]
- [[cloudscape-sdf-volumetric]]
- [[deferred-rendering]] / [[tiled-light-prepass]]
- [[msaa-ssaa]]
- [[shadow-mapping-basics]] / [[camera-relative-sun-shadows]]
- [[multidraw-indirect-occlusion-culling]]
- [[screenspace-reflections]]
- [[bindless-rendering]]

## 原文

- 链接：<https://blog.thomaspoulet.fr/posts/dcs-frame-analysis/>
- 本地：`raw/articles/blog.thomaspoulet.fr/2021-09-19_digital-combat-simulator-frame-analysis-thomas-poulet.md`
