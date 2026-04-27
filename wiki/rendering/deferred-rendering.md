---
tags: [渲染, 延迟渲染]
date: 2026-04-05
sources: 2
---

# 延迟渲染（Deferred Rendering）

**先把几何信息写到 G-Buffer，然后做统一光照 pass**。解决 forward rendering 的光源数限制。

## Forward vs Deferred

| | Forward | Deferred |
|---|---|---|
| 光源数 | 4-8 典型 | 10-100+ |
| G-Buffer 带宽 | 无 | 高 |
| MSAA | 易 | 难 |
| 透明处理 | 易 | 必须另开 forward pass |
| 移动端友好 | 更好 | 差（带宽） |

## G-Buffer 典型布局

- RT0: Albedo + AO (RGBA8)
- RT1: Normal (RG16F 或压缩)
- RT2: Roughness + Metallic + Specular (RGBA8)
- Depth buffer 单独

## 优势

- 光源数量与几何解耦——O(N+M) 而非 O(N×M)。
- 每个光源只和**影响像素**交互（light volume / tile）。

## 劣势

- G-Buffer 带宽成本高——**移动端 killer**。
- MSAA 昂贵（每个 sample 要 resolve G-Buffer）。
- 无法处理半透明——必须加一个 forward pass。

## 在 Unreal 历史中的意义

UE3 推广 deferred rendering 成为主流。UE5 的 Lumen 在 deferred 基础上添加动态 GI。详见 [[engine-evolution]]。

## 相关
- [[rendering-pipeline]]
- [[fragment-shader]]
- [[engine-evolution]]
- [[cached-shadowmaps]] —— 利用帧间相干性缓存远级联阴影
- [[tbdr-vs-imr]] —— TBDR 的 tile memory 让 deferred 的带宽成本几乎为零
- [[tiled-light-prepass]] —— ROTR Foundation 引擎的 thin G-Buffer + 二次几何提交方案
- [[fizzle-lod-fading]] —— deferred 管线下用 discard 噪声替代 alpha blending 做 LOD fade
- [[deferred-grass-shader]] — 延迟管线下用 alpha cutout + tessellation + geometry shader 做草地
- [[visibility-buffer]] —— thin-gbuffer + 后续 compute shading 的现代替代方案
- [[tiled-light-culling]] —— per-tile 光源剔除机制，Karis 加入 specular cone 剔除
- [[sparse-shadows-cone-tracing]] —— Karis 2012：shadow map 只管 diffuse，远处 specular 走 cone trace
- [[instant-radiosity-vpl]] —— 大量 VPL 的间接光，天然适合 deferred / light prepass 消费
- [[deferred-alpha-lighting]] —— deferred 下给透明物打光的四条方案综述
- [[skysaga-rendering-tech]] —— Meandros 引擎：token command stream + 4-RT G-Buffer + G-Buffer modification 天气系统
- [[unreal-frame-breakdown]] —— UE4.17 默认 deferred 管线的 RenderDoc 逐 pass 拆解
- [[hybrid-hair-rendering]] —— Wronski 的混合 deferred/forward 头发 trick，规避 fat G-Buffer 分支与 alpha-test 锯齿
- [[valve-ambient-cube]] —— DX9 世代 deferred 管线里给动画几何填 ambient 的穷人 SH
- [[deferred-sdf-rendering]] —— 把 SDF raymarch 的 albedo/normal/depth 写进 G-Buffer，让 SDF 与多边形共存于同一条 deferred 管线
- [[dynamic-resolution-scaling]] —— gameknife 2013 年在 gkEngine 上把 deferred lighting 与半分辨率 SSAO/shadow mask、0.75× 全局缩放 + 锐化 pass 组合成一套像素省量方案
- [[multiple-render-targets]] —— G-Buffer 的硬件前提：一次 draw 写多附件
- [[xplane-gbuffer-format]] —— Supnik 2010 年 X-Plane 10 延迟管线的 16 字节 G-Buffer 布局：`256×shadow + shine` 浮点打包、16F 眼空间深度 + 行星几何求交后备
- [[deferred-light-volume-stencil-depth-clamp-hack]] —— 光源包围体 stencil 剔除 + 远剪裁面切穿问题的三档处理
- [[deferred-depth-reuse-tradeoffs]] —— 光照 pass 复用深度 buffer 的三条路线：拷贝 / NV_texture_barrier / 往 G-Buffer 写眼空间 Z
- [[xplane-deferred-pipeline-hacks]] —— Supnik 2012-11 四连篇合编：X-Plane 10.10 延迟管线重写四条教训（stencil 优化关掉 / 双 depth domain 合并为一 pass / sRGB + linear blend 共存 / 工程复杂度来自硬边角叠加）
- [[deferred-rendering-mythbusting]] —— Pesce 2011 拆解六条常见误解，提出「deferred 是通用 pattern 不是单一结构」的判断框架
- [[rendering-perception-psychology]] —— Pesce 2011 质疑 deferred 是否损失了预计算光照对材质微妙性的表现
- [[realtime-quality-vs-quantity]] —— Pesce 2012：数量 vs 质量的结构性取舍，延迟渲染的功能堆砌是典型案例
- [[rendering-pipeline-taxonomy]] — Pesce 2016 的统一管线分类框架，把 deferred 放入更大的连续体中定位
- [[msaa-deferred-edge-detection]] —— MSAA 延迟管线下 POINT/LINEAR 法线差值边缘检测，stencil 复用模式
- [[screen-space-filter-kernel]] —— 屏幕空间滤波核的距离缩放/各向异性/深度剔除设计规则

## Sources

- [[sources/gea-day02]]
- [[sources/c0de517e-cached-shadowmaps]]
- [[sources/elopezr-rotr-rendering]]
- [[sources/vertexfragment-deferred-grass]]
- [[sources/elopezr-clos2-rendering]]
- [[sources/interplay-deferred-sdf-rendering]]
- [[sources/gameknife-gkengine-rendering-optimization]] —— gkEngine 从 deferred lighting 演进到可切换 deferred shading 的一次实战：DP 减半但 G-Buffer 带宽涨 50 %，Hybrid Deferred Shading 的国产实验
- [[sources/c0de517e-deferred-optimizer-notes]] —— Pesce 2012：Space Marine 延迟渲染器优化 post-mortem，出货前六个月性能翻倍
- [[sources/c0de517e-realtime-renderer-notes]] —— 2014 年 Forward/Forward+/Deferred 四管线横向对比
- [[sources/c0de517e-rendering-continuum]] — Pesce 2016：渲染管线连续体分类学，Forward/Deferred/VB/Texture-Space 统一框架
- [[sources/adrian-gta-v-graphics-1]]
- [[sources/adrian-gta-v-graphics-2]]
- [[sources/adrian-doom-2016-graphics]]
- [[sources/humus-tile-based-deferred-forward]] —— Engel 2012：分块延迟/前向的带宽收益及阴影代价抵消分析
- [[sources/humus-edge-detection-trick]] —— Engel 2010：MSAA 边缘检测，延迟管线应用
