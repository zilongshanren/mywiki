---
tags: [source, 渲染, 引擎架构, 延迟渲染, 前向渲染, stingray, bitsquid, vr]
date: 2026-04-19
sources: 1
---

# Stingray Renderer Walkthrough #8: stingray-renderer & mini-renderer（Tobias Persson / bitsquid 博客）

[[tobias-persson]] 2017-03-14 发表的 Stingray 渲染器 Walkthrough 第 8 篇——把 [[sources/bitsquid-renderer-walkthrough-7-data-driven|#7]] 讲过的 data-driven 机制，在**两套 shipping 模板** `renderer.render_config`（stingray renderer，~1500 行）与 `mini_renderer.render_config`（mini renderer，~400 行）上演示实际一帧的全流程。

## 摘要

**Stingray renderer** 是默认高端延迟管线，支持 PBR metallic 材质、cascaded shadow maps、atlased local light shadows、clustered shading（simple 灯）+ custom 材质灯走 traditional deferred、SSR、localized parallax-corrected reflection probes、TAA、DoF、motion blur、lens distortion、bloom、auto exposure、LUT color grading、以及五条 stereo 路径（Mono / Stereo / Instanced Stereo / NV SPS / NV VRSLI）。一帧的 `layer_configs/default` 数组按顺序是：shadow_mapping → clustered_shading → clears + vr_mask → gbuffer + linearize_depth + decals + motion_vectors → reflections + ssr + lighting → emissive + fog + skydome + hdr_transparent + stream_capture + selection → post_processing → transparent (LDR) + debug_shadows + vr_present。G-buffer 是"浮动"语义，PC 上 color targets 合计 192 bpp（不含 depth/stencil）。`lighting` resource_generator 内部还有四步：sun shadow screen-space mask（多次 fullscreen_pass + stencil culling per cascade）、SSAO、"global lighting" 全屏 pass（SSR + SSAO + clustered simple lights + sun 合成）、custom 材质灯的 deferred proxy。

每个阶段边界插 `extension_insertion_point` 空 layer 给 [[render-config-extension-points]] 当命名 hook。`static_branch` 在启动时消除整段分支（如 `vr_supported=false` 时 `vr_mask` 完全被剔除），`dynamic_branch` 在每次 `render_world` 时重算（如 `auto_exposure_enabled`）。

**Mini renderer** 的设计目标正相反——"**砍掉一切不必要**"：纯 forward、无 post、不留 HDR target（直接曝光 + tonemap + sRGB 到 LDR backbuffer）。主战场是 mobile VR，fill rate 严重受限时全屏 pass 几乎全禁。作者把它作为 data-driven 价值的示范——**400 行 json 完整描述一条管线**，读者不看引擎源码也能搞懂。

Walkthrough 系列计划下一篇讲 shader 和材质系统，但实际没再更。

## 关键要点

- **shadow 必须先画**——Stingray 为支持半透明接收阴影，shadow_mapping 与 lighting 无法交错。
- **方向光走 cascaded atlas、local 光走 atlased shadow map**——两张 shadow target 统一管理。
- **simple light 走 clustered shading、custom 材质灯走 traditional deferred proxy**——默认管线里两种 lighting 路径并存。
- **反射三段 fallback**：SSR → localized parallax-corrected probes → global cubemap。
- **`stabilize_and_linearize_depth` 双任务**：输出 R32F linear depth 并用 hacky TAA resolve 给 `stable_depth` 去闪烁。
- **`generate_motion_vectors`** 给 skydome 这类没写 gbuffer 的像素补算 velocity。
- **post_processing 打包成一个 resource_generator**——步骤可独立关闭，但最后的 scene combine（tonemap + sRGB + LUT 到 backbuffer）不可省。
- **Mini renderer 不存 HDR**——mobile VR 上省一次 hdr → ldr 的全屏 copy 比任何 post 技巧都重要。
- **extension_insertion_point 是跨项目复用渲染特性的工业手段**——插件在命名锚点 `insert_at`。
- **未解的架构债**：太多 static_branch、`global_resources` 缺 transient aliasing、resource barrier 追踪隐式——Tobias 点名 [Frostbite FrameGraph](http://www.frostbite.com/2017/03/framegraph-extensible-rendering-architecture-in-frostbite/) 与 [Unity SRP](http://aras-p.info/texts/files/2017_GDC_UnityScriptableRenderPipeline.pdf) 是下一代方向。

## 链接到的概念

- [[stingray-default-frame-flow]]
- [[stingray-data-driven-render-config]]
- [[render-config-extension-points]]
- [[stingray-sort-key-bit-layout]]
- [[stingray-renderer-three-stage-pipeline]]
- [[cascaded-shadow-maps]]
- [[clustered-shading]]
- [[deferred-shading]]
- [[temporal-antialiasing]]
- [[render-graph]]

## 原文

- 链接：https://bitsquid.blogspot.com/2017/03/stingray-renderer-walkthrough-8.html
- 本地：`raw/articles/bitsquid.blogspot.com/2017-03-14_stingray-renderer-walkthrough-8-stingray-renderer-mini-rende.md`
