---
tags: [source, rendering, unreal, deferred-rendering, volumetric-fog, tiled-deferred]
date: 2026-04-14
sources: 1
---

# How Unreal Renders a Frame part 2（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] *How Unreal Renders a Frame* 系列第二篇，覆盖 UE4.17 默认管线中段：light assignment、volumetric fog、g-prepass、AO 与 direct lighting。

## 摘要

**ComputeLightGrid** 用 compute shader 把场景灯光分配到 view-space 3D 网格（屏幕 tile 64×64，32 个指数 z-slice，尺寸随分辨率 29×16×32），链表结构后用 **Compact** pass 转紧凑数组——但这套 cluster **只被 volumetric fog、environment reflection、translucency 使用**，opaque 主光照仍走 per-light deferred。**Volumetric fog** 分三个 compute pass：写 scattering/absorption → LightScattering（带 history volume 做时间滤波）→ FinalIntegration（沿 z raymarch 累加 transmittance），对应 [[volumetric-fog-froxels|froxel 体积雾]]。**G-prepass** 重绘所有 opaque（包括被 Z-prepass 保护的 skydome），depth 只 z-test、stencil 做 opaque 标记；静态道具还会采样三张预烘焙 atlas（irradiance / shadow / surface normal）。**AmbientOcclusion** 用 quarter-res + full-res 两段，加上每帧 jitter 实现 temporal supersampling。**直接光照**分 NonShadowedLights 和 ShadowedLights：非阴影灯数 > 80 时切到 tiled deferred compute pass；shadow 灯走三段式 *ShadowProjectionOnOpaque → InjectTranslucentVolume → StandardDeferredLighting*，所有 shadow 灯复用同一张屏幕 shadow buffer。文中也点出 UE4 维护 2 组 64³ RGBA16F translucency lighting volume（近 / 远 cascade，存 SH 系数 + 光方向近似）来服务后续透明物打光。

## 关键要点

- Light grid 是 **view-space 3D cluster**（64×64 tile × 32 exp z-slice）。
- Light cluster **只给 fog / reflection / translucency 用**——opaque 不用。
- Volumetric fog 是 froxel-aligned volume + 时间 TAA。
- **非阴影灯 > 80 时才切到 tiled deferred**；否则走 classic deferred。
- Shadow 灯三段式：screen-space shadow → translucent volume inject → deferred lighting。
- **Translucency 光照存 SH + 光方向**到 2 组 64³ volume，分近 / 远 cascade。
- Opaque 静态道具用三张预烘焙 atlas（irradiance / shadow / surface normal）共享光照信息。

## 链接到的概念

- [[unreal-frame-breakdown]]
- [[volumetric-fog-froxels]]
- [[tiled-deferred-shading]]
- [[deferred-rendering]]
- [[gbuffer-layouts]]
- [[spherical-harmonics]]

## 原文

- 链接：<https://interplayoflight.wordpress.com/2017/10/25/how-unreal-renders-a-frame-part-2/>
- 本地：`raw/articles/interplayoflight.wordpress.com/2017-10-25_how-unreal-renders-a-frame-part-2.md`
