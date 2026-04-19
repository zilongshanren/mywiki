---
tags: [渲染, 阴影, urp, unity, renderer-feature, post-processing]
date: 2026-04-19
sources: 1
---

# URP 的 Screen Space Shadow Map

URP 默认的主光阴影是**光源空间**的——那张 `_MainLightShadowmapTexture` 里每个像素是"从方向光望下去时最近物体的深度"，要在 shader 里采样它得先把世界坐标变换到光源 clip space。这套流程是 [[shadow-mapping-basics|经典 shadow mapping]] 的教科书写法，适合 forward lit shader 在着色时判断"这个像素是否在阴影里"。但当你想**在 post-process 里用阴影**——例如基于阴影 mask 画素描线、做 outline、或者把阴影延展一点——用光源空间的贴图非常笨，每个屏幕像素都要做一遍世界→光源的变换。

URP 有个现成的 Renderer Feature 叫 **Screen Space Shadows** 专门处理这件事。[[daniel-ilett|Daniel Ilett]] 在 2024 年的 Mystery Dungeon sketch shader 里用它作为整个 post-process 的切入口。

## 做了什么

加上 Screen Space Shadows feature 之后，Frame Debugger 里会出现一个新的 pass：它在 `MainLightShadow` pass（画 `_MainLightShadowmapTexture`）之后执行，输入那张光源空间的 shadowmap，输出到一张新的 **`_ScreenSpaceShadowmapTexture`**——**屏幕分辨率、单通道灰度、每个像素直接是"这个像素是否在主光阴影里"**（0 = 完全阴影，1 = 完全被光照亮，中间值代表半影）。

之后的 DrawOpaqueObjects pass 里 Lit shader 的 shadow sampling 从 `_MainLightShadowmapTexture` 自动切换到读 `_ScreenSpaceShadowmapTexture`——这步不用动自己的代码，URP 的内部 shader 变体开关会处理。

## 给 post-process 的好处

对做 post-process 的 renderer feature 作者来说，这张纹理是黄金：

- **已经在屏幕空间**——不用 projection 矩阵变换、直接用屏幕 UV 采样。
- **已经考虑了 cascade、bias、PCF**——URP 内部 shadow 采样的所有复杂性在这一步里解决完。
- **单通道 R8**——带宽友好，可以用作蒙版 / 阈值输入。

Ilett 的 Mystery Dungeon 效果就直接把它当作"哪些像素要画素描"的 mask——`Shader.GetGlobalTexture("_ScreenSpaceShadowmapTexture")` 拿到这张纹理，然后 Blit 到自己的 RTHandle 里做模糊（让素描能"溢出"阴影边界一点）、最后 `smoothstep` 出一个柔边作为 lerp factor 应用素描贴图。整个 post-process 的其它部分（triplanar 采样世界坐标纹理、cross-hatching）都建立在"屏幕空间阴影掩码已经免费拿到"的前提上。

## 启用方式

找到 URP 的 **Universal Renderer Data** asset（通常在 `Assets/Settings/`），底部 Renderer Features 列表 → Add Renderer Feature → **Screen Space Shadows**。没有可调参数，加就生效。

## 和 [[cached-shadowmaps|缓存 shadowmap]] 的关系

两件事正交：cached shadowmaps 是"对静态物体别每帧重画光源空间阴影贴图"的上游优化；Screen Space Shadows 是"把光源空间贴图转成屏幕空间贴图"的下游工具。两者可以组合——先用缓存生成光源空间阴影，再转成屏幕空间给 post-process 用。

## 黑盒到什么程度

Ilett 的原话："Dunno what this does under the hood - as far as I'm concerned, it's magic." 对大多数 shader 教程受众这就是正确态度——这个 feature 的价值在于"开启即用"。想深挖的话源码在 `Packages/com.unity.render-pipelines.universal/Runtime/Passes/ScreenSpaceShadowsPass.cs`，它实际上是一个全屏 quad shader，读光源空间 shadowmap、做 cascade 选择、写屏幕空间结果。

## 相关

- [[shadow-mapping-basics]]
- [[cached-shadowmaps]]
- [[blit-render-feature]] — Renderer Feature 模式的骨架
- [[scene-color-depth-nodes]] — 姐妹纹理 `_CameraDepthTexture` 的行为
- [[urp-volume-post-processing]]
- [[mystery-dungeon-sketch-shadows]]

## Sources

- [[sources/danielilett-mystery-dungeon-sketches]]
