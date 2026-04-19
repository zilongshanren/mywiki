---
tags: [人物, 作者]
date: 2026-04-14
sources: 15
---

# Kostas Anagnostou

英国图形程序员，博客 **Interplay of Light**（interplayoflight.wordpress.com）的作者。长期活跃在 D3D11 及之后的实时渲染实践线上，博客以简短、工程向的笔记为主——从 depth testing 的 API 细节、FX Composer / SharpDX 等原型工具对比，到 deferred shading、光照、GPU 调试等。他也是 Playground Games（Forza Horizon 系列）的高级图形工程师。

对这个 wiki 而言，Anagnostou 早期（2013）的几篇博客是**图形程序员日常原型与调试工具栈**的一个样本切片：那是 XNA 式微、SharpDX 兴起、FX Composer 停更、Unity 被当作 shader prototyping 工具使用的过渡时期。

他 2024–2025 年的博客集中在**现代 GPU 前沿**——D3D12 work graphs 的实操教程与性能调查、mesh shaders + meshlet 遮挡剔除、async compute 的 pairing 方法论、以及 shader 指令隐藏成本的 ISA 级别分析。这些文章把他从「工具链与原型」的早期身份推进到「现代 GPU-driven 管线观察者」的新阶段。

## 相关
- [[early-z-late-z]] —— Conservative Depth 与 UAV + `[earlydepthstencil]` 的补充
- [[tangent-free-normal-mapping]] —— 他试验并验证的免 tangent 技术
- [[shader-prototyping-tools]] —— 他对 FX Composer / Unity / SharpDX 的对比
- [[sharpdx-assimp-pipeline]] —— 他的 SharpDX + Assimp 模型加载实验
- [[instant-radiosity-vpl]] —— 他在 Hieroglyph light prepass 上的一次反弹 GI 原型
- [[parallax-corrected-cubemap]] —— 非专烘焙 cubemap 的 BoxScale hack
- [[vertex-vector-interpolation-artifact]] —— FX Composer 归一化导致的 Blinn 高光撕裂
- [[dual-depth-buffer-thickness]] —— ShaderX6 thickness 技巧的 front/back 分流改进
- [[deferred-alpha-lighting]] —— deferred 下透明物打光的四条路径综述
- [[gpu-driven-grass-tiles]] —— Marco Giordano 的 GPU driven culling 直接参考了 Kostas 的 multi-draw indirect / occlusion culling 实验
- [[normalised-blinn-phong-shader]] —— 2013 年给美术同事做的 PBR 教学 FX Composer 工程
- [[divergent-gradient-in-branches]] —— 分支内 shader-computed uv 的 tex2D 隐形性能坑
- [[tessellation-fur-rendering]] —— D3D11 isoline domain 生成 fur 的 64×64 方案
- [[skysaga-rendering-tech]] —— Meandros 引擎（SkySaga: Infinite Isles）完整管线总览
- [[unity-postprocessing-adventures]] —— 2015 年在 Unity 里搭体积光束后处理 pipeline 的实验
- [[unreal-frame-breakdown]] —— 2017 年用 RenderDoc 逐 pass 拆解 UE4.17 默认 deferred 管线（三篇合一）
- [[gpu-based-occlusion-culling]] —— 2017 年 DX11 上的 GPU-driven HZB + stream compaction + indirect draw retrofit
- [[deferred-sdf-rendering]] —— 2017 年把 SDF raymarch 结果写进 Unity G-Buffer + SV_Depth 的 hybrid 实验
- [[multidraw-indirect-occlusion-culling]] —— 2018 年 GPU-driven 剔除 Part 2：NVAPI MultiDraw + mesh LOD + programmable vertex fetch
- [[hybrid-raytraced-shadows-reflections]] —— 2018 年用 compute shader 手写 BVH hybrid raytracer 做硬阴影与镜面反射
- [[d3d12-work-graphs]] —— 2024 年两篇 workgraph 教程 + 性能对比（SSSR 改造，发现比 compute+indirect 慢 3×，但结构上消除了 compaction/drain）
- [[meshlets-and-mesh-shaders]] —— 2025 年在 St Miguel/Bistro 上做的 mesh shader + AS hi-z 遮挡剔除实测（gbuffer -44%、z-prepass -48%）
- [[async-compute]] —— 2025 年关于 pairing 策略与 pass 重排的实操笔记
- [[shader-instruction-cost]] —— 2025 年 ISA 级别分析 atan2/waterfall/LDS bank conflict 等隐藏成本
- [[gpu-utilisation-holistic-tuning]] —— 2025 年的整帧调优方法论（瓶颈分析 + shader 类型选择 + async compute 配对）
- [[vertex-shader-export-bottleneck]] —— 2025 年受控实验：N 卡 ISBE/PE/TRAM，1→10 float4 export 让 drawcall 成本近 3 倍，AMD GCN 几乎无影响
- [[spatial-hash-rtao-cache]] —— 2025 年 11 月的 RTAO 加速 + 去噪方案（pcg + xxhash32 双哈希、age eviction、自适应 cell size）
- [[mlp-signal-encoding-rendering]] —— 2026 年 2 月的小 MLP 在渲染里实测：辐亮度 MLP 赢 SH、辐照度 SH 赢 MLP、BRDF 要 Rusinkiewicz 参数化
- [[hlsl-cooperative-vectors-tensor-cores]] —— 2026 年 2 月 Agility SDK preview 把大 MLP 加速 173× 的实测

## Sources
- [[sources/interplay-tools-of-the-trade]]
- [[sources/interplay-depth-testing]]
- [[sources/interplay-tangent-free-normal-mapping]]
- [[sources/interplay-unity-as-fxcomposer]]
- [[sources/interplay-sharpdx-model-loading]]
- [[sources/interplay-instant-radiosity-light-prepass]]
- [[sources/interplay-parallax-corrected-cubemap]]
- [[sources/interplay-interpolate-view-light-vectors]]
- [[sources/interplay-dual-depth-thickness]]
- [[sources/interplay-lighting-alpha-deferred]]
- [[sources/interplay-normalised-blinn-phong]]
- [[sources/interplay-branches-texture-sampling]]
- [[sources/interplay-fur-tessellation]]
- [[sources/interplay-skysaga-rendering]]
- [[sources/interplay-unity-postprocessing]]
- [[sources/interplay-unreal-frame-part1]]
- [[sources/interplay-unreal-frame-part2]]
- [[sources/interplay-unreal-frame-part3]]
- [[sources/interplay-gpu-occlusion-culling]]
- [[sources/interplay-deferred-sdf-rendering]]
- [[sources/interplay-multidraw-indirect-occlusion]]
- [[sources/interplay-bgfx-gpu-driven-port]]
- [[sources/interplay-digital-dragons-gpu-driven]]
- [[sources/interplay-hybrid-raytraced-shadows-reflections]]
- [[sources/interplay-workgraphs-intro]]
- [[sources/interplay-workgraphs-performance]]
- [[sources/interplay-hidden-shader-cost]]
- [[sources/interplay-meshlets-mesh-shaders]]
- [[sources/interplay-async-compute]]
- [[sources/interplay-gpu-utilisation-holistic]]
- [[sources/interplay-vertex-shader-exports]]
- [[sources/interplay-spatial-hash-rtao]]
- [[sources/interplay-neural-rendering-1-mlp]]
- [[sources/interplay-neural-rendering-2-coopvec]]
