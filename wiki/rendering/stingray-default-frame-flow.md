---
tags: [渲染, 引擎架构, 数据驱动, stingray, bitsquid, frame-graph, 延迟渲染]
date: 2026-04-19
sources: 1
---

# Stingray 默认 render_config 的一帧走向

Stingray 随引擎附送两套 `render_config` 模板：**stingray renderer**（约 1500 行 sjson 的"高端"延迟管线，默认启用）与 **mini renderer**（约 400 行的前向轻量管线，面向移动 VR）。Tobias Persson 在 Walkthrough #8 里逐条拆解了前者的 `layer_configs/default` 数组——这是一份把一帧的 GPU 调度**整条**写在配置里的样板，所有"加一个 pass"的实验都只需要改 json、热重载、看画面。

## 一帧的八个阶段

把默认 layer array 合并同类项，大致是八段，**严格自上而下**，每条对应一个 [[stingray-sort-key-bit-layout|sort_key 的 Layer 位]]：

1. **Shadow maps + 光源簇化**——`shadow_mapping` resource_generator 先跑，原因是 Stingray 要让半透明几何也能接收阴影，不能把 shadow 画和灯光 pass 交错。方向光走 cascaded shadow map atlas，点/聚光灯走 local atlas。`clustered_shading` 把 simple spot / point 灯塞进 [Humus 的 clustered shading 结构](http://www.humus.name/Articles/PracticalClusteredShading.pdf)。自带材质图的 custom 灯不进簇，后面走 traditional deferred proxy。
2. **Clear + VR mask**——一条特殊 layer 清 `hdr0 / gbuffer2 / depth_stencil`；VR 模式下 `vr_mask` resource_generator 在 stencil 上标出镜头外像素。`vr_supported` 为 false 时整段被 `static_branch` 完全剔除。
3. **G-buffer + decals + motion vectors**——`gbuffer` layer 绑 `gbuffer0..3` + `depth_stencil`，FRONT_BACK 排序。PC 默认色彩 target 合计 **192 bpp**（不含 depth / stencil），用"浮动"语义——同一个通道的字段含义随材质不同而变。紧接 `stabilize_and_linearize_depth` 把深度线性化成 R32F 并做一个粗糙的深度 TAA resolve（输出 `stable_depth` 给后续 DoF / gizmo 用）。`decals` layer 在 gbuffer0/1 上 splat 延迟贴花。之后 `generate_motion_vectors` 给 gbuffer 里**没写过**的像素（skydome）补算 velocity。
4. **反射 + 主光照**——`reflections` layer 把反射探头当作"带材质的光源"画入 `hdr1`（三段 fallback：SSR → 视差校正的 localized 探头 → 全局探头）。`ssr_reflections` 半分辨率跑 screen-space reflections。`lighting` resource_generator 负责最重的一步：sun-shadow screen-space mask（多次全屏 pass + stencil culling 针对各 cascade）、SSAO、"global lighting" 全屏 pass（混合 SSR/SSAO、clustered simple lights、sun）、以及 custom 光源的 traditional deferred proxy volume。
5. **Emissive + fog + skydome + HDR 透明**——`emissive` 把自发光材质叠进 hdr0；`fog` resource_generator 给 hdr0 加雾；`skydome` 层单独画天穹（BACK_FRONT）；`hdr_transparent` 层走 forward + clustered shading 画透明材质和 VFX。
6. **抓帧 + 选择框**——`stream_capture_buffers` 把指定 target 读回 CPU（多缓冲）；`cubemap_capture` 在编辑器里供 reflection probe 烘焙用；`selection` layer 画编辑器里的对象选择轮廓。
7. **Post processing**——整个 post 管线封装成一个 resource generator：TAA resolve → DoF → motion blur → 镜头畸变/色散 → bloom → auto exposure → scene combine（曝光/tonemap/sRGB/LUT）→ debug。每一步都能被 render_setting 单独关，但 step 7（scene combine 到 backbuffer）不可省。
8. **LDR transparent + VR present**——`transparent` layer 在 output_target 上画 HUD / debug lines；`debug_shadows` 叠 shadow map 可视化；VR 下 `vr_present` 合成左右眼。

## extension_insertion_point：config 级的 hook

每个阶段边界插了若干 `extension_insertion_point="gbuffer"` / `"lighting"` / `"post_processing"` / `"first"` / `"last"` 空 layer。它们不做事，只是给 [[render-config-extension-points|render_config_extension]] 提供命名锚点——插件可以 `insert_at` 把新的 resource_generator / layer 挂进来。对内部团队来说这是功能模块化、跨项目复用特效的工业手段。

## Mini renderer：减法哲学

`mini_renderer.render_config` 砍到约 1/3 行数，设计目标是"**除了必须，一切都砍**"：

- **纯前向**。理论上支持 clustered shading per-pixel 灯，但实际项目大多只保留一个方向光 + 光照烘焙。
- **零 post processing**。移动 VR 受 fill rate 严重限制，全屏 pass 几乎全禁。
- **不留 HDR target**。光照在线性空间算完直接曝光 + tonemap + sRGB 写进 LDR backbuffer，省一次 hdr0 → ldr 的全屏 copy。

作者把它作为**"data-driven 相对于硬编码管线的价值证明"**放在 shipping 产品里——用户就算读不到引擎源码，也能通过读 400 行 json 把一条"完整"的前向管线搞懂。

## 未来方向：FrameGraph / SRP 风向

Tobias 在 #7 末尾承认 render_config 的三条债：

1. **分支太密**——跨平台 + 多种 stereo 路径（Mono / Stereo / Instanced Stereo / NV SPS / NV VRSLI，光 PC 就五条）让一份 config 里到处是 static_branch，难读。
2. **资源生命周期太静态**——`global_resources` 一启动就分配、直到引擎关才释放；DX12 / Vulkan 时代需要 transient aliasing，他点名想借鉴 Yuriy O'Donnell 2017 GDC 的 [FrameGraph: Extensible Rendering Architecture in Frostbite](http://www.frostbite.com/2017/03/framegraph-extensible-rendering-architecture-in-frostbite/)，以及 Aras 同期的 [Scriptable Render Pipeline](http://aras-p.info/texts/files/2017_GDC_UnityScriptableRenderPipeline.pdf)。
3. **resource barrier 依赖隐式追踪**——shader 按名字绑资源，dispatch 阶段才能发现依赖、补 D3D12/Vulkan barrier。他想转成"每个 layer / resource_generator 显式声明输入输出"，让 barrier 可以静态推导。

这三条正好是 2017 年之后业界共识的 frame graph 三件套。Stingray 2015 年就做了"声明式渲染管线"这件事，但用的是 **sjson 解释器**而非 **C++ builder**——Walkthrough #7/#8 里的反思，是对声明式粒度提得不够细、运行期绑定太晚的工程自省。

## 相关

- [[stingray-data-driven-render-config]] —— 机制层（render_settings / global_resources / layer_config / resource_generator 四件套）
- [[render-config-extension-points]] —— extension_insertion_point 的设计
- [[render-pass-orchestration]]
- [[stingray-renderer-three-stage-pipeline]]
- [[stingray-sort-key-bit-layout]]
- [[cascaded-shadow-maps]]
- [[clustered-shading]]
- [[deferred-shading]]
- [[render-graph]] —— Frostbite FrameGraph 与 Stingray 的对照
- [[tobias-persson]]

## Sources

- [[sources/bitsquid-renderer-walkthrough-8-default-pipes]]
