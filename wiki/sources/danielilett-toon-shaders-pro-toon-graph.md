---
tags: [source, shader, toon, shader-graph, urp, unity]
date: 2026-04-19
sources: 1
---

# Toon Shaders Pro for URP — Toon (Shader Graph)（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 的 *Toon Shaders Pro for URP* 资产包提供的 **Shader Graph 变体**。结构与 [[sources/danielilett-toon-shaders-pro-toon|HLSL 版 Toon shader]] 基本一致，主要差异：只支持 Specular workflow、暴露一个 `CalculateToonLighting` 子图供再利用。

## 摘要

这个 Shader Graph 版本的存在理由不是做更多事，而是**给新手和 Shader Graph 用户一个可改的模板**——把 toon 光照封装成 `CalculateToonLighting` subgraph，让用户在任意 graph 里接入同一套 diffuse/specular/rim 阈值系统。参数面板几乎和 HLSL 版一致，缺失项：Metallic workflow、Use Vertex Colors、Convert From Roughness、Global Illumination Strength 滑杆（对应 Shader Graph 在自定义 lighting 上的局限性）。新增 `Specular Strength` 全局乘子（相当于 HLSL 版的 Specular Boost 反向），`Glossiness` 直接控制高光尺寸。

## 关键要点

- **与 HLSL 版对应关系**：Surface Options / Diffuse / Specular / Rim / Normal 五组 —— Metallic workflow 不暴露。
- **`CalculateToonLighting` subgraph**：暴露给用户在别处接入的完整 toon 光照黑盒；默认值合理，输入繁多。
- **Shader Graph 限制的选择**：作者明言"SG 做不了某些细节"——复杂 lighting 数学留给 HLSL 版。
- **扩展路径**：文档建议 duplicate graph 然后改，而不是改原 graph，避免升级覆盖。

## 链接到的概念

- [[cel-shading-pipeline]]
- [[shader-graph-lighting-primer]]
- [[shader-graph-custom-function-hlsl]]
- [[fresnel-edge-highlight]]

## 原文

- 链接：<https://danielilett.com/toon-shaders-pro/toon-graph/>
- 本地：`raw/articles/danielilett.com/2026-01-01_toon-shaders-pro-for-urp-toon-shader-graph.md`
