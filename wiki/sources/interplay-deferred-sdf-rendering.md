---
tags: [source, 渲染, sdf, 延迟渲染]
date: 2026-04-14
sources: 1
---

# Deferred Signed Distance Field rendering（Kostas Anagnostou / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 2017 年 12 月的短文，记录了一次在 Unity 里让 SDF raymarching 与多边形几何共存于同一条 [[deferred-rendering|延迟渲染]]管线的实验。灵感来自 *Claybook* 与 *Dreams* 这类全 SDF 游戏，但方向相反——**保留传统管线，只把 SDF 作为几何源之一**。

## 摘要

作者魔改了 Unity 的 standard shader，在 g-prepass 里发一个 full-screen triangle：vertex shader pass-through；fragment shader 用远平面逆变换构造 world-space ray direction，sphere-trace 一遍 iq 风格的 SDF 场景，命中后把 albedo/normal/roughness 填入 G-Buffer，**并把命中点投回 NDC 写 `SV_Depth`**。写 depth 这一步让 SDF 和多边形几何在 z-buffer 上互相正确排序，也让 Unity 自带的屏幕空间后处理（SSR、SSAO、bloom）对 SDF 同样生效——这是整篇文章最有意思的副作用。代价是把光照从 SDF 剥离，失去了 SDF 原生廉价软阴影和反射；但换来了与既有引擎光照基础设施的零摩擦共存。

## 关键要点

- 混合几何在 deferred 下的最低摩擦接入：**写 G-Buffer + 写 depth**。
- Fragment shader 里 world-space ray 的构造：clip(x, y, 1, 1) → 逆 VP → 减 camera pos → 归一化。
- Unity material 系统只能对所有 SDF 统一配置（roughness、emissive），细粒度材质需要自写系统。
- shadow map pass 理论上可以同样魔改（让 SDF 参与光源深度 pass），但阴影成本会显著增加。
- 牺牲了 SDF native pipeline 里的 cheap soft shadow / cone AO，换来的是 Unity 现成的 PBR + 后处理链。

## 链接到的概念

- [[deferred-sdf-rendering]]
- [[deferred-rendering]]
- [[raymarching-intro]]
- [[sdf-ray-marched-shadows]]
- [[hybrid-raytracing-pipeline]]
- [[kostas-anagnostou]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2017/12/12/deferred-signed-distance-field-rendering/
- 本地：`raw/articles/interplayoflight.wordpress.com/2017-12-12_deferred-signed-distance-field-rendering.md`
