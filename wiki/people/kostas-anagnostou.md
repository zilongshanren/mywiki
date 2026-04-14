---
tags: [人物, 作者]
date: 2026-04-14
sources: 5
---

# Kostas Anagnostou

英国图形程序员，博客 **Interplay of Light**（interplayoflight.wordpress.com）的作者。长期活跃在 D3D11 及之后的实时渲染实践线上，博客以简短、工程向的笔记为主——从 depth testing 的 API 细节、FX Composer / SharpDX 等原型工具对比，到 deferred shading、光照、GPU 调试等。他也是 Playground Games（Forza Horizon 系列）的高级图形工程师。

对这个 wiki 而言，Anagnostou 早期（2013）的几篇博客是**图形程序员日常原型与调试工具栈**的一个样本切片：那是 XNA 式微、SharpDX 兴起、FX Composer 停更、Unity 被当作 shader prototyping 工具使用的过渡时期。

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
